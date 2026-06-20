from fastapi import FastAPI, Request
import sqlite3

app = FastAPI()

def get_webhook_db():
    # Use the unified fresh platform_v2 database
    conn = sqlite3.connect("platform_v2.db", timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

@app.post("/mpesa/confirmation")
async def mpesa_confirmation(request: Request):
    """Safaricom hits this URL instantly when a customer pays your Paybill"""
    data = await request.json()
    
    # 1. Parse standard Safaricom Daraja API production JSON keys
    # Safaricom payloads look slightly different inside a validation/confirmation callback.
    # It usually arrives nested inside 'Body' -> 'stkCallback' OR as flat parameters depending on your API type.
    # Here, we process standard C2B (Customer to Business) format mapping:
    account_number = str(data.get("BillRefNumber", "")).strip()  # E.g., 0165367846721 or MEET0165361
    amount = float(data.get("TransAmount", 0))
    transaction_id = str(data.get("TransID", "")).strip().upper()  # E.g., SFT712XYZ0
    
    if not account_number or not transaction_id:
        return {"ResultCode": 1, "ResultDesc": "Rejected: Missing crucial parameters"}

    # 2. Dynamically determine payment type & extract Profile ID
    payment_type = None
    profile_id = None

    if account_number.startswith("016536784672"):
        payment_type = "chat"
        profile_id = account_number.replace("016536784672", "")
    elif account_number.startswith("MEET016536"):
        payment_type = "meetup"
        profile_id = account_number.replace("MEET016536", "")

    # 3. Log into Database if parsed successfully
    if profile_id and payment_type:
        try:
            profile_id = int(profile_id)
            conn = get_webhook_db()
            
            # Insert the transaction entry into the tracking table
            # 'OR IGNORE' avoids duplicating if Safaricom double-sends a notification retry
            conn.execute("""
                INSERT OR IGNORE INTO transactions (transaction_id, profile_id, account_ref, amount, type, status)
                VALUES (?, ?, ?, ?, ?, 'completed')
            """, (transaction_id, profile_id, account_number, amount, payment_type))
            
            conn.commit()
            conn.close()
            print(f"💰 [M-PESA SUCCESS] Logged {payment_type} payment of KES {amount} via {transaction_id} for profile {profile_id}")
            return {"ResultCode": 0, "ResultDesc": "Confirmation received successfully"}
            
        except Exception as e:
            print(f"❌ [DATABASE ERROR] Failed logging incoming payment payload: {e}")
            return {"ResultCode": 1, "ResultDesc": "Internal Database Log Error"}
            
    print(f"⚠️ [M-PESA IGNORED] Account reference parsing format failed for ref: {account_number}")
    return {"ResultCode": 1, "ResultDesc": "Rejected: Invalid Account Structure Reference Format"}