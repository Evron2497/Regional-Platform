# import sqlite3

# def get_db():
#     # 🔥 CHANGED DATABASE FILE TO FORCE AN IMMEDIATE STRUCTURE REFRESH
#     conn = sqlite3.connect("platform_v2.db", timeout=10.0)
#     conn.row_factory = sqlite3.Row
#     conn.execute("PRAGMA journal_mode=WAL;")
#     return conn

# def init_db():
#     conn = get_db()
    
#     # 1. Profiles Table
#     conn.execute('''CREATE TABLE IF NOT EXISTS profiles 
#                     (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, continent TEXT, 
#                      country TEXT, bio TEXT, rate REAL, photo_url TEXT, status TEXT DEFAULT 'browsing')''')
    
#     # 2. Transactions Table - Built fresh with transaction_id explicitly defined
#     conn.execute('''CREATE TABLE IF NOT EXISTS transactions 
#                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
#                      transaction_id TEXT UNIQUE, 
#                      profile_id INTEGER, 
#                      account_ref TEXT, 
#                      amount REAL, 
#                      type TEXT, 
#                      status TEXT DEFAULT 'completed')''')
#     conn.commit()
#     conn.close()

# # --- PROFILE CRUD MANAGEMENT ---

# def add_single_profile(name, continent, country, bio, rate, photo_url):
#     conn = get_db()
#     conn.execute("INSERT INTO profiles (name, continent, country, bio, rate, photo_url) VALUES (?, ?, ?, ?, ?, ?)", 
#                  (name, continent, country, bio, rate, photo_url))
#     conn.commit()
#     conn.close()

# def get_profiles():
#     conn = get_db()
#     data = conn.execute("SELECT * FROM profiles").fetchall()
#     conn.close()
#     return data

# def get_available_profiles():
#     conn = get_db()
#     query = """
#         SELECT p.* FROM profiles p 
#         WHERE NOT EXISTS (
#             SELECT 1 FROM transactions t 
#             WHERE t.account_ref = '016536784672' || p.id 
#             AND t.type = 'chat' 
#             AND t.status = 'completed'
#         )
#     """
#     data = conn.execute(query).fetchall()
#     conn.close()
#     return data

# def update_profile(id, name, continent, country, bio, rate, photo_url):
#     conn = get_db()
#     conn.execute("UPDATE profiles SET name=?, continent=?, country=?, bio=?, rate=?, photo_url=? WHERE id=?", 
#                  (name, continent, country, bio, rate, photo_url, id))
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
#     if row and row['status'] == 'approved':
#         return True
#     return False

# def claim_and_verify_transaction(tx_id, profile_id, search_type="chat"):
#     conn = get_db()
#     tx_id = tx_id.strip().upper()
    
#     if search_type == "chat":
#         expected_ref = f"016536784672{profile_id}"
#     else:
#         expected_ref = f"MEET016536{profile_id}"
        
#     row = conn.execute(
#         "SELECT 1 FROM transactions WHERE transaction_id = ? AND account_ref = ? AND type = ?", 
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
    
    # 1. Profiles Table (Updated with chat_rate and meetup_rate)
    conn.execute('''CREATE TABLE IF NOT EXISTS profiles 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     name TEXT, 
                     continent TEXT, 
                     country TEXT, 
                     bio TEXT, 
                     chat_rate REAL DEFAULT 0.0, 
                     meetup_rate REAL DEFAULT 0.0, 
                     photo_url TEXT, 
                     status TEXT DEFAULT 'browsing')''')
    
    # 2. Transactions Table (Updated with merchant_request_id and a 'pending' default status)
    conn.execute('''CREATE TABLE IF NOT EXISTS transactions 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     transaction_id TEXT UNIQUE, 
                     merchant_request_id TEXT UNIQUE,
                     profile_id INTEGER, 
                     account_ref TEXT, 
                     amount REAL, 
                     type TEXT, 
                     status TEXT DEFAULT 'pending')''')
    conn.commit()
    conn.close()

# --- PROFILE CRUD MANAGEMENT ---

def add_single_profile(name, continent, country, bio, chat_rate, meetup_rate, photo_url):
    conn = get_db()
    conn.execute("""
        INSERT INTO profiles (name, continent, country, bio, chat_rate, meetup_rate, photo_url) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, continent, country, bio, chat_rate, meetup_rate, photo_url))
    conn.commit()
    conn.close()

def get_profiles():
    conn = get_db()
    data = conn.execute("SELECT * FROM profiles").fetchall()
    conn.close()
    return data

def get_single_profile_rates(profile_id: int):
    """Helper used by the FastAPI STK Push endpoint to determine price dynamically"""
    conn = get_db()
    row = conn.execute("SELECT chat_rate, meetup_rate FROM profiles WHERE id = ?", (profile_id,)).fetchone()
    conn.close()
    return row

def get_available_profiles():
    conn = get_db()
    query = """
        SELECT p.* FROM profiles p 
        WHERE NOT EXISTS (
            SELECT 1 FROM transactions t 
            WHERE t.account_ref = '016536784672' || p.id 
            AND t.type = 'chat' 
            AND t.status = 'completed'
        )
    """
    data = conn.execute(query).fetchall()
    conn.close()
    return data

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
    if row and row['status'] == 'approved':
        return True
    return False

# --- STK PUSH FLOW RECONCILIATION HELPERS ---

def create_pending_transaction(merchant_request_id, profile_id, account_ref, amount, payment_type):
    """Logs the checkout initiation right when the prompt fires onto the phone handset"""
    conn = get_db()
    conn.execute("""
        INSERT INTO transactions (merchant_request_id, profile_id, account_ref, amount, type, status)
        VALUES (?, ?, ?, ?, ?, 'pending')
    """, (merchant_request_id, profile_id, account_ref, amount, payment_type))
    conn.commit()
    conn.close()

def complete_stk_transaction(merchant_request_id, transaction_id):
    """Updates status to completed when Safaricom sends a success webhook callback response"""
    conn = get_db()
    conn.execute("""
        UPDATE transactions 
        SET transaction_id = ?, status = 'completed' 
        WHERE merchant_request_id = ?
    """, (transaction_id, merchant_request_id))
    conn.commit()
    conn.close()

def claim_and_verify_transaction(tx_id, profile_id, search_type="chat"):
    conn = get_db()
    tx_id = tx_id.strip().upper()
    
    if search_type == "chat":
        expected_ref = f"016536784672{profile_id}"
    else:
        expected_ref = f"MEET016536{profile_id}"
        
    row = conn.execute(
        "SELECT 1 FROM transactions WHERE transaction_id = ? AND account_ref = ? AND type = ? AND status = 'completed'", 
        (tx_id, expected_ref, search_type)
    ).fetchone()
    
    conn.close()
    return row is not None
