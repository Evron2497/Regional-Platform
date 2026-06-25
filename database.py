# import sqlite3

# def get_db():
#     # Unified fresh platform_v2 database
#     conn = sqlite3.connect("platform_v2.db", timeout=10.0)
#     conn.row_factory = sqlite3.Row
#     conn.execute("PRAGMA journal_mode=WAL;")
#     return conn

# def init_db():
#     conn = get_db()
    
#     # 1. Profiles Table (Base table execution setup)
#     conn.execute('''CREATE TABLE IF NOT EXISTS profiles 
#                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
#                      name TEXT, 
#                      continent TEXT, 
#                      country TEXT, 
#                      bio TEXT, 
#                      photo_url TEXT, 
#                      status TEXT DEFAULT 'browsing')''')
    
#     # AUTOMATED MIGRATION: Safely inject new rate columns if database file already exists
#     try:
#         conn.execute("ALTER TABLE profiles ADD COLUMN chat_rate REAL DEFAULT 0.0;")
#     except sqlite3.OperationalError:
#         pass  # Column already exists, safe to ignore
        
#     try:
#         conn.execute("ALTER TABLE profiles ADD COLUMN meetup_rate REAL DEFAULT 0.0;")
#     except sqlite3.OperationalError:
#         pass  # Column already exists, safe to ignore
    
#     # 2. Transactions Table 
#     conn.execute('''CREATE TABLE IF NOT EXISTS transactions 
#                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
#                      transaction_id TEXT UNIQUE, 
#                      merchant_request_id TEXT UNIQUE,
#                      profile_id INTEGER, 
#                      account_ref TEXT, 
#                      amount REAL, 
#                      type TEXT, 
#                      status TEXT DEFAULT 'pending')''')
#     conn.commit()
#     conn.close()

# # --- PROFILE CRUD MANAGEMENT ---

# def add_single_profile(name, continent, country, bio, chat_rate, meetup_rate, photo_url, status='browsing'):
#     """
#     Inserts a user profile record. 
#     Defaults to 'browsing' for direct Admin entries, override with 'pending_approval' for client forms.
#     """
#     conn = get_db()
#     conn.execute("""
#         INSERT INTO profiles (name, continent, country, bio, chat_rate, meetup_rate, photo_url, status) 
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#     """, (name, continent, country, bio, chat_rate, meetup_rate, photo_url, status))
#     conn.commit()
#     conn.close()

# def get_profiles():
#     """Returns all profiles safely transformed into explicit dicts to avoid indexing crashes"""
#     conn = get_db()
#     rows = conn.execute("SELECT * FROM profiles").fetchall()
#     conn.close()
    
#     profiles = []
#     for row in rows:
#         profiles.append({
#             'id': row['id'],
#             'name': row['name'],
#             'continent': row['continent'],
#             'country': row['country'],
#             'bio': row['bio'],
#             'chat_rate': row['chat_rate'] if row['chat_rate'] is not None else 0.0,
#             'meetup_rate': row['meetup_rate'] if row['meetup_rate'] is not None else 0.0,
#             'photo_url': row['photo_url'],
#             'status': row['status']
#         })
#     return profiles

# def get_single_profile_rates(profile_id: int):
#     """Helper used by the FastAPI STK Push endpoint to determine price dynamically"""
#     conn = get_db()
#     row = conn.execute("SELECT chat_rate, meetup_rate FROM profiles WHERE id = ?", (profile_id,)).fetchone()
#     conn.close()
#     return row

# def get_available_profiles():
#     """Returns ONLY profiles currently available for browsing (hides booked or pending approvals)"""
#     conn = get_db()
#     rows = conn.execute("""
#         SELECT id, name, continent, country, bio, chat_rate, meetup_rate, photo_url, status 
#         FROM profiles 
#         WHERE status = 'browsing'
#     """).fetchall()
#     conn.close()
    
#     profiles = []
#     for row in rows:
#         profiles.append({
#             'id': row['id'],
#             'name': row['name'],
#             'continent': row['continent'],
#             'country': row['country'],
#             'bio': row['bio'],
#             'chat_rate': row['chat_rate'] if row['chat_rate'] is not None else 0.0,
#             'meetup_rate': row['meetup_rate'] if row['meetup_rate'] is not None else 0.0,
#             'photo_url': row['photo_url'],
#             'status': row['status']
#         })
#     return profiles

# def update_profile(id, name, continent, country, bio, chat_rate, meetup_rate, photo_url):
#     conn = get_db()
#     conn.execute("""
#         UPDATE profiles 
#         SET name=?, continent=?, country=?, bio=?, chat_rate=?, meetup_rate=?, photo_url=? 
#         WHERE id=?
#     """, (name, continent, country, bio, chat_rate, meetup_rate, photo_url, id))
#     conn.commit()
#     conn.close()

# def delete_profile(profile_id):
#     conn = get_db()
#     conn.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
#     conn.commit()
#     conn.close()

# def approve_meetup(profile_id):
#     conn = get_db()
#     conn.execute("UPDATE profiles SET status = 'approved' WHERE id = ?", (profile_id,))
#     conn.commit()
#     conn.close()

# def check_meetup_status(profile_id):
#     conn = get_db()
#     row = conn.execute("SELECT status FROM profiles WHERE id = ?", (profile_id,)).fetchone()
#     conn.close()
#     # Returns True if approved or booked to keep private session flows open
#     if row and row['status'] in ('approved', 'booked'):
#         return True
#     return False

# # --- MANUAL & ADMIN TRANSACTION VERIFICATION HELPERS ---

# def submit_manual_transaction(tx_id, profile_id, account_ref, amount, payment_type):
#     """Inserts a transaction entry directly from the manual code submitted by client"""
#     conn = get_db()
#     tx_id = tx_id.strip().upper()
#     try:
#         conn.execute("""
#             INSERT INTO transactions (transaction_id, profile_id, account_ref, amount, type, status)
#             VALUES (?, ?, ?, ?, ?, 'pending')
#         """, (tx_id, profile_id, account_ref, amount, payment_type))
#         conn.commit()
#         return True
#     except sqlite3.IntegrityError:
#         return False  # Code was already posted before
#     finally:
#         conn.close()

# def get_pending_verifications():
#     """Fetches all raw client transactions awaiting administrative approval"""
#     conn = get_db()
#     rows = conn.execute("""
#         SELECT t.*, p.name as profile_name 
#         FROM transactions t
#         LEFT JOIN profiles p ON t.profile_id = p.id
#         WHERE t.status = 'pending'
#     """).fetchall()
#     conn.close()
#     return [dict(row) for row in rows]

# def admin_approve_transaction(tx_id):
#     """Called when an admin hits approve in their workspace notifications dashboard"""
#     conn = get_db()
#     tx_id = tx_id.strip().upper()
#     conn.execute("""
#         UPDATE transactions 
#         SET status = 'completed' 
#         WHERE transaction_id = ?
#     """, (tx_id,))
#     conn.commit()
#     conn.close()

# def claim_and_verify_transaction(tx_id, profile_id, search_type="chat"):
#     """Checks the database to see if the transaction has been approved/completed by the Admin"""
#     conn = get_db()
#     tx_id = tx_id.strip().upper()
    
#     if search_type == "chat":
#         expected_ref = f"446040-CHA{profile_id}"
#     elif search_type == "meetup":
#         expected_ref = f"446040-MEE{profile_id}"
#     else:
#         expected_ref = "446040-SUB"
        
#     row = conn.execute(
#         "SELECT 1 FROM transactions WHERE transaction_id = ? AND account_ref = ? AND type = ? AND status = 'completed'", 
#         (tx_id, expected_ref, search_type)
#     ).fetchone()
    
#     conn.close()
#     return row is not None
import sqlite3

def get_db():
    # Unified fresh platform_v2 database
    conn = sqlite3.connect("platform_v2.db", timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    conn = get_db()
    
    # 1. Profiles Table (Base table execution setup)
    conn.execute('''CREATE TABLE IF NOT EXISTS profiles 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     name TEXT, 
                     continent TEXT, 
                     country TEXT, 
                     bio TEXT, 
                     photo_url TEXT, 
                     status TEXT DEFAULT 'browsing')''')
    
    # AUTOMATED MIGRATION: Safely inject new rate columns if database file already exists
    try:
        conn.execute("ALTER TABLE profiles ADD COLUMN chat_rate REAL DEFAULT 0.0;")
    except sqlite3.OperationalError:
        pass  # Column already exists, safe to ignore
        
    try:
        conn.execute("ALTER TABLE profiles ADD COLUMN meetup_rate REAL DEFAULT 0.0;")
    except sqlite3.OperationalError:
        pass  # Column already exists, safe to ignore
    
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
    """
    Inserts a user profile record. 
    Defaults to 'browsing' for direct Admin entries, override with 'pending_approval' for client forms.
    """
    conn = get_db()
    conn.execute("""
        INSERT INTO profiles (name, continent, country, bio, chat_rate, meetup_rate, photo_url, status) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, continent, country, bio, chat_rate, meetup_rate, photo_url, status))
    conn.commit()
    conn.close()

def get_profiles():
    """Returns all profiles safely transformed into explicit dicts to avoid indexing crashes"""
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
    """Helper used by the FastAPI STK Push endpoint to determine price dynamically"""
    conn = get_db()
    row = conn.execute("SELECT chat_rate, meetup_rate FROM profiles WHERE id = ?", (profile_id,)).fetchone()
    conn.close()
    return row

def get_available_profiles():
    """Returns ONLY profiles currently available for browsing (hides booked or pending approvals)"""
    conn = get_db()
    rows = conn.execute("""
        SELECT id, name, continent, country, bio, chat_rate, meetup_rate, photo_url, status 
        FROM profiles 
        WHERE status = 'browsing'
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
            'meetup_rate': row['meetup_rate'] if row['meetup_rate'] is not None else 0.0,
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
    # Returns True if approved or booked to keep private session flows open
    if row and row['status'] in ('approved', 'booked'):
        return True
    return False

# --- MANUAL & ADMIN TRANSACTION VERIFICATION HELPERS ---

def submit_manual_transaction(tx_id, profile_id, account_ref, amount, payment_type):
    """Inserts a transaction entry directly from the manual code submitted by client"""
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
        return False  # Code was already posted before
    finally:
        conn.close()

def get_pending_verifications():
    """Fetifications all raw client transactions awaiting administrative approval"""
    conn = get_db()
    rows = conn.execute("""
        SELECT t.*, p.name as profile_name 
        FROM transactions t
        LEFT JOIN profiles p ON t.profile_id = p.id
        WHERE t.status = 'pending'
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def admin_approve_transaction(tx_id):
    """Called when an admin hits approve in their workspace notifications dashboard"""
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
    """Checks the database to see if the transaction has been approved/completed by the Admin"""
    conn = get_db()
    tx_id = tx_id.strip().upper()
    
    if search_type == "chat":
        expected_ref = f"446040-CHA{profile_id}"
    elif search_type == "meetup":
        expected_ref = f"446040-MEE{profile_id}"
    else:
        expected_ref = "446040-SUB"
        
    row = conn.execute(
        "SELECT 1 FROM transactions WHERE transaction_id = ? AND account_ref = ? AND type = ? AND status = 'completed'", 
        (tx_id, expected_ref, search_type)
    ).fetchone()
    
    conn.close()
    return row is not None

# --- PERSISTENT SECURE CHAT OPERATIONS ---

def save_chat_message(profile_id: int, sender: str, message: str):
    """Saves a single message into a profile's custom private room mapping"""
    conn = get_db()
    conn.execute("""
        INSERT INTO messages (profile_id, sender, message) 
        VALUES (?, ?, ?)
    """, (profile_id, sender, message))
    conn.commit()
    conn.close()

def get_chat_history(profile_id: int):
    """Fetches complete chronological database log message details for a room"""
    conn = get_db()
    rows = conn.execute("""
        SELECT sender, message, timestamp 
        FROM messages 
        WHERE profile_id = ? 
        ORDER BY timestamp ASC
    """, (profile_id,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]
