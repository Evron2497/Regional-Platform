# from fastapi import FastAPI, Request
# import sqlite3

# app = FastAPI()

# def get_webhook_db():
#     # Use the unified fresh platform_v2 database
#     conn = sqlite3.connect("platform_v2.db", timeout=10.0)
#     conn.row_factory = sqlite3.Row
#     conn.execute("PRAGMA journal_mode=WAL;")
#     return conn

# @app.post("/mpesa/confirmation")
# async def mpesa_confirmation(request: Request):
#     """Safaricom hits this URL instantly when a customer pays your Paybill"""
#     data = await request.json()
    
#     # 1. Parse standard Safaricom Daraja API production JSON keys
#     # Safaricom payloads look slightly different inside a validation/confirmation callback.
#     # It usually arrives nested inside 'Body' -> 'stkCallback' OR as flat parameters depending on your API type.
#     # Here, we process standard C2B (Customer to Business) format mapping:
#     account_number = str(data.get("BillRefNumber", "")).strip()  # E.g., 0165367846721 or MEET0165361
#     amount = float(data.get("TransAmount", 0))
#     transaction_id = str(data.get("TransID", "")).strip().upper()  # E.g., SFT712XYZ0
    
#     if not account_number or not transaction_id:
#         return {"ResultCode": 1, "ResultDesc": "Rejected: Missing crucial parameters"}

#     # 2. Dynamically determine payment type & extract Profile ID
#     payment_type = None
#     profile_id = None

#     if account_number.startswith("016536784672"):
#         payment_type = "chat"
#         profile_id = account_number.replace("016536784672", "")
#     elif account_number.startswith("MEET016536"):
#         payment_type = "meetup"
#         profile_id = account_number.replace("MEET016536", "")

#     # 3. Log into Database if parsed successfully
#     if profile_id and payment_type:
#         try:
#             profile_id = int(profile_id)
#             conn = get_webhook_db()
            
#             # Insert the transaction entry into the tracking table
#             # 'OR IGNORE' avoids duplicating if Safaricom double-sends a notification retry
#             conn.execute("""
#                 INSERT OR IGNORE INTO transactions (transaction_id, profile_id, account_ref, amount, type, status)
#                 VALUES (?, ?, ?, ?, ?, 'completed')
#             """, (transaction_id, profile_id, account_number, amount, payment_type))
            
#             conn.commit()
#             conn.close()
#             print(f"💰 [M-PESA SUCCESS] Logged {payment_type} payment of KES {amount} via {transaction_id} for profile {profile_id}")
#             return {"ResultCode": 0, "ResultDesc": "Confirmation received successfully"}
            
#         except Exception as e:
#             print(f"❌ [DATABASE ERROR] Failed logging incoming payment payload: {e}")
#             return {"ResultCode": 1, "ResultDesc": "Internal Database Log Error"}
            
#     print(f"⚠️ [M-PESA IGNORED] Account reference parsing format failed for ref: {account_number}")
#     return {"ResultCode": 1, "ResultDesc": "Rejected: Invalid Account Structure Reference Format"}



import base64
import sqlite3
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()

# --- CONFIGURATION (Populate with your Daraja Details) ---
MPESA_CONSUMER_KEY = "YOUR_CONSUMER_KEY"
MPESA_CONSUMER_SECRET = "YOUR_CONSUMER_SECRET"
MPESA_PASSKEY = "YOUR_LIPA_NA_MPESA_ONLINE_PASSKEY"

# For Tills (Buy Goods), your Shortcode is usually the Till Number. 
# For Paybills, it's the Paybill Number.
MPESA_SHORTCODE = "YOUR_TILL_OR_PAYBILL_NUMBER" 
CALLBACK_URL = "https://yourdomain.com/mpesa/callback" 

def get_webhook_db():
    conn = sqlite3.connect("platform_v2.db", timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

# --- NEW: Helper to fetch rate from your database ---
def get_profile_amount(profile_id: int, payment_type: str) -> int:
    """
    Queries your database to get the cost set for this specific profile.
    Adjust the table name ('profiles') and column names ('chat_rate', 'meetup_rate') 
    to match your actual database design.
    """
    conn = get_webhook_db()
    cursor = conn.cursor()
    
    try:
        # Example query: Adjust column and table names based on your DB schema
        cursor.execute("SELECT chat_rate, meetup_rate FROM profiles WHERE id = ?", (profile_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        if payment_type == "chat":
            return int(row["chat_rate"])
        elif payment_type == "meetup":
            return int(row["meetup_rate"])
        else:
            raise HTTPException(status_code=400, detail="Invalid payment type")
            
    except sqlite3.Error as e:
        if conn: conn.close()
        raise HTTPException(status_code=500, detail=f"Database lookup failed: {str(e)}")

# --- DARAJA API AUTH HELPERS ---
async def get_mpesa_access_token():
    url = "https://sandbox.safaricom.co.uk/oauth/v1/generate?grant_type=client_credentials" # Use api.safaricom.co.ke for production
    auth_string = f"{MPESA_CONSUMER_KEY}:{MPESA_CONSUMER_SECRET}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()
    
    headers = {"Authorization": f"Basic {encoded_auth}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("access_token")
        raise HTTPException(status_code=500, detail="Failed to fetch M-Pesa token")

def generate_stk_password(shortcode, passkey, timestamp):
    return base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()


# --- CONNECT & PUSH ENDPOINT ---
@app.post("/mpesa/connect")
async def connect_user_profile(payload: ConnectRequest):
    """
    Triggered when a user clicks 'Connect'. 
    Fetches the profile amount from DB and requests an M-Pesa STK prompt.
    """
    # 1. Look up how much this specific profile charges
    amount = get_profile_amount(payload.profile_id, payload.payment_type)
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid payment amount configured for this profile")

    # 2. Format Phone Number safely (e.g., 0712345678 -> 254712345678)
    phone = payload.phone_number.strip()
    if phone.startswith("0"):
        phone = "254" + phone[1:]
    elif phone.startswith("+254"):
        phone = phone.replace("+", "")

    # 3. Generate credentials
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = generate_stk_password(MPESA_SHORTCODE, MPESA_PASSKEY, timestamp)
    access_token = await get_mpesa_access_token()

    # 4. Generate the exact account structure format your confirmation route expects
    if payload.payment_type == "chat":
        account_ref = f"016536784672{payload.profile_id}"
    else:
        account_ref = f"MEET016536{payload.profile_id}"

    # 5. Determine Transaction Type based on your shortcode type
    # For a Buy Goods Till: Use "CustomerBuyGoodsOnline"
    # For a Paybill: Use "CustomerPayBillOnline"
    transaction_type = "CustomerBuyGoodsOnline" 

    stk_body = {
        "BusinessShortCode": MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": transaction_type, 
        "Amount": amount,
        "PartyA": phone,
        "PartyB": MPESA_SHORTCODE, # For Till, this is usually your Store Number
        "PhoneNumber": phone,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": account_ref,
        "TransactionDesc": f"Connect {payload.payment_type} with Profile {payload.profile_id}"
    }

    stk_url = "https://sandbox.safaricom.co.uk/mpesa/stkpush/v1/processrequest" # Use production URL for live apps
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(stk_url, json=stk_body, headers=headers)
        res_data = response.json()
        
        if response.status_code == 200 and res_data.get("ResponseCode") == "0":
            # Save the request transaction state if necessary
            return {
                "status": "initiated",
                "message": f"STK Prompt of KES {amount} successfully sent to {phone}.",
                "merchant_request_id": res_data.get("MerchantRequestID")
            }
        else:
            return {"status": "failed", "error": res_data}
