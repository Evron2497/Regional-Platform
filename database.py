import sqlite3

def get_db():
    conn = sqlite3.connect("platform_v2.db", timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    conn = get_db()
    
    # 1. Profiles Table with added created_at tracker
    conn.execute('''CREATE TABLE IF NOT EXISTS profiles 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     name TEXT, 
                     continent TEXT, 
                     country TEXT, 
                     bio TEXT, 
                     photo_url TEXT, 
                     status TEXT DEFAULT 'browsing',
                     created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # AUTOMATED MIGRATIONS
    try:
        conn.execute("ALTER TABLE profiles ADD COLUMN chat_rate REAL DEFAULT 0.0;")
    except sqlite3.OperationalError:
        pass
        
    try:
        conn.execute("ALTER TABLE profiles ADD COLUMN meetup_rate REAL DEFAULT 0.0;")
    except sqlite3.OperationalError:
        pass

    try:
        conn.execute("ALTER TABLE profiles ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP;")
    except sqlite3.OperationalError:
        pass
    
    # 2. Transactions Table 
    conn.execute('''CREATE TABLE IF NOT EXISTS transactions 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     transaction_id TEXT UNIQUE, 
                     merchant_request_id TEXT UNIQUE,
                     profile_id INTEGER, 
                     account_ref TEXT, 
                     amount REAL, 
                     type TEXT, 
                     status TEXT DEFAULT 'pending')''')

    # 3. Persistent Messages Table Schema
    conn.execute('''CREATE TABLE IF NOT EXISTS messages 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     profile_id INTEGER, 
                     sender TEXT, 
                     message TEXT, 
                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    conn.commit()
    conn.close()

# --- PROFILE CRUD MANAGEMENT ---

def add_single_profile(name, continent, country, bio, chat_rate, meetup_rate, photo_url, status='browsing'):
    conn = get_db()
    conn.execute("""
        INSERT INTO profiles (name, continent, country, bio, chat_rate, meetup_rate, photo_url, status, created_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (name, continent, country, bio, chat_rate, meetup_rate, photo_url, status))
    conn.commit()
    conn.close()

def get_profiles():
    conn = get_db()
    rows = conn.execute("SELECT * FROM profiles").fetchall()
    conn.close()
    
    profiles = []
    for row in rows:
        profiles.append({
            'id': row['id'],
            'name': row['name'],
            'continent': row['continent'],
            'country': row['country'],
            'bio': row['bio'],
            'chat_rate': row['chat_rate'] if row['chat_rate'] is not None else 0.0,
            'meetup_rate': row['meetup_rate'] if row['meetup_rate'] is not None else 0.0,
            'photo_url': row['photo_url'],
            'status': row['status']
        })
    return profiles

def get_single_profile_rates(profile_id: int):
    conn = get_db()
    row = conn.execute("SELECT chat_rate, meetup_rate FROM profiles WHERE id = ?", (profile_id,)).fetchone()
    conn.close()
    return row

def get_available_profiles():
    """
    MODIFIED: Returns profiles currently status='browsing' ONLY IF they are less than 30 days old.
    If 1 month passes without a connection update, they automatically vanish.
    """
    conn = get_db()
    rows = conn.execute("""
        SELECT id, name, continent, country, bio, chat_rate, photo_url, status 
        FROM profiles 
        WHERE status = 'browsing' AND created_at >= datetime('now', '-30 days')
    """).fetchall()
    conn.close()
    
    profiles = []
    for row in rows:
        profiles.append({
            'id': row['id'],
            'name': row['name'],
            'continent': row['continent'],
            'country': row['country'],
            'bio': row['bio'],
            'chat_rate': row['chat_rate'] if row['chat_rate'] is not None else 0.0,
            'photo_url': row['photo_url'],
            'status': row['status']
        })
    return profiles

def update_profile(id, name, continent, country, bio, chat_rate, meetup_rate, photo_url):
    conn = get_db()
    conn.execute("""
        UPDATE profiles 
        SET name=?, continent=?, country=?, bio=?, chat_rate=?, meetup_rate=?, photo_url=? 
        WHERE id=?
    """, (name, continent, country, bio, chat_rate, meetup_rate, photo_url, id))
    conn.commit()
    conn.close()

def delete_profile(profile_id):
    conn = get_db()
    conn.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
    conn.commit()
    conn.close()

def approve_meetup(profile_id):
    conn = get_db()
    conn.execute("UPDATE profiles SET status = 'approved' WHERE id = ?", (profile_id,))
    conn.commit()
    conn.close()

def check_meetup_status(profile_id):
    conn = get_db()
    row = conn.execute("SELECT status FROM profiles WHERE id = ?", (profile_id,)).fetchone()
    conn.close()
    if row and row['status'] in ('approved', 'booked'):
        return True
    return False

# --- MANUAL & ADMIN TRANSACTION VERIFICATION HELPERS ---

def submit_manual_transaction(tx_id, profile_id, account_ref, amount, payment_type):
    conn = get_db()
    tx_id = tx_id.strip().upper()
    try:
        conn.execute("""
            INSERT INTO transactions (transaction_id, profile_id, account_ref, amount, type, status)
            VALUES (?, ?, ?, ?, ?, 'pending')
        """, (tx_id, profile_id, account_ref, amount, payment_type))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_pending_verifications():
    conn = get_db()
    # Aliased account_ref AS account_number to prevent runtime crashes in main app rendering script
    rows = conn.execute("""
        SELECT t.id, t.transaction_id, t.merchant_request_id, t.profile_id, 
               t.account_ref AS account_number, t.amount, t.type, t.status, 
               p.name as profile_name 
        FROM transactions t
        LEFT JOIN profiles p ON t.profile_id = p.id
        WHERE t.status = 'pending'
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def admin_approve_transaction(tx_id):
    conn = get_db()
    tx_id = tx_id.strip().upper()
    conn.execute("""
        UPDATE transactions 
        SET status = 'completed' 
        WHERE transaction_id = ?
    """, (tx_id,))
    conn.commit()
    conn.close()

def claim_and_verify_transaction(tx_id, profile_id, search_type="chat"):
    conn = get_db()
    tx_id = tx_id.strip().upper()
    
    if search_type == "chat":
        expected_ref = f"446040-CHA{profile_id}"
    elif search_type == "meetup":
        expected_ref = f"446040-MEE{profile_id}"
    else:
        expected_ref = "446040-SUB"
        
    row = conn.execute(
        "SELECT 1 FROM transactions WHERE transaction_id = ? AND account_ref LIKE ? AND type = ? AND status = 'completed'", 
        (tx_id, f"{expected_ref}%", search_type)
    ).fetchone()
    
    conn.close()
    return row is not None

def get_transaction_session_lookup(tx_id):
    conn = get_db()
    tx_id = tx_id.strip().upper()
    row = conn.execute("""
        SELECT profile_id, type 
        FROM transactions 
        WHERE transaction_id = ?
    """, (tx_id,)).fetchone()
    conn.close()
    if row:
        return {'profile_id': row['profile_id'], 'type': row['type']}
    return None

# --- PERSISTENT SECURE CHAT OPERATIONS ---

def save_chat_message(profile_id: int, sender: str, message: str):
    conn = get_db()
    conn.execute("""
        INSERT INTO messages (profile_id, sender, message) 
        VALUES (?, ?, ?)
    """, (profile_id, sender, message))
    conn.commit()
    conn.close()

def get_chat_history(profile_id: int):
    conn = get_db()
    rows = conn.execute("""
        SELECT sender, message, timestamp 
        FROM messages 
        WHERE profile_id = ? 
        ORDER BY timestamp ASC
    """, (profile_id,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]
