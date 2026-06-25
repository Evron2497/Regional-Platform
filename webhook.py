# import base64
# import sqlite3
# from datetime import datetime
# from fastapi import FastAPI, Request, HTTPException
# from pydantic import BaseModel
# import httpx

# app = FastAPI()

# # --- CONFIGURATION (Populate with your Daraja Details) ---
# MPESA_CONSUMER_KEY = "p8Fhi6QWduA2P7opsijEWJA7Uy55WbPmotMMVvnLC5Dw4W9e"
# MPESA_CONSUMER_SECRET = "gAyVOCGwrCfBoQxA23968I4gpAQ0R4Q44p5rDrGEmC9orGlFKtVK0o7uc6wZRpGx"
# MPESA_PASSKEY = "N/A"

# # For Tills (Buy Goods), your Shortcode is usually the Till Number. 
# # For Paybills, it's the Paybill Number.
# MPESA_SHORTCODE = "727691" 
# CALLBACK_URL = "https://yourdomain.com/mpesa/callback" 

# def get_webhook_db():
#     conn = sqlite3.connect("platform_v2.db", timeout=10.0)
#     conn.row_factory = sqlite3.Row
#     conn.execute("PRAGMA journal_mode=WAL;")
#     return conn

# # --- NEW: Helper to fetch rate from your database ---
# def get_profile_amount(profile_id: int, payment_type: str) -> int:
#     """
#     Queries your database to get the cost set for this specific profile.
#     Adjust the table name ('profiles') and column names ('chat_rate', 'meetup_rate') 
#     to match your actual database design.
#     """
#     conn = get_webhook_db()
#     cursor = conn.cursor()
    
#     try:
#         # Example query: Adjust column and table names based on your DB schema
#         cursor.execute("SELECT chat_rate, meetup_rate FROM profiles WHERE id = ?", (profile_id,))
#         row = cursor.fetchone()
#         conn.close()
        
#         if not row:
#             raise HTTPException(status_code=404, detail="Profile not found")
        
#         if payment_type == "chat":
#             return int(row["chat_rate"])
#         elif payment_type == "meetup":
#             return int(row["meetup_rate"])
#         else:
#             raise HTTPException(status_code=400, detail="Invalid payment type")
            
#     except sqlite3.Error as e:
#         if conn: conn.close()
#         raise HTTPException(status_code=500, detail=f"Database lookup failed: {str(e)}")

# # --- DARAJA API AUTH HELPERS ---
# async def get_mpesa_access_token():
#     url = "https://sandbox.safaricom.co.uk/oauth/v1/generate?grant_type=client_credentials" # Use api.safaricom.co.ke for production
#     auth_string = f"{MPESA_CONSUMER_KEY}:{MPESA_CONSUMER_SECRET}"
#     encoded_auth = base64.b64encode(auth_string.encode()).decode()
    
#     headers = {"Authorization": f"Basic {encoded_auth}"}
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, headers=headers)
#         if response.status_code == 200:
#             return response.json().get("access_token")
#         raise HTTPException(status_code=500, detail="Failed to fetch M-Pesa token")

# def generate_stk_password(shortcode, passkey, timestamp):
#     return base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()


# # --- CONNECT & PUSH ENDPOINT ---
# @app.post("/mpesa/connect")
# async def connect_user_profile(payload: ConnectRequest):
#     """
#     Triggered when a user clicks 'Connect'. 
#     Fetches the profile amount from DB and requests an M-Pesa STK prompt.
#     """
#     # 1. Look up how much this specific profile charges
#     amount = get_profile_amount(payload.profile_id, payload.payment_type)
#     if amount <= 0:
#         raise HTTPException(status_code=400, detail="Invalid payment amount configured for this profile")

#     # 2. Format Phone Number safely (e.g., 0712345678 -> 254712345678)
#     phone = payload.phone_number.strip()
#     if phone.startswith("0"):
#         phone = "254" + phone[1:]
#     elif phone.startswith("+254"):
#         phone = phone.replace("+", "")

#     # 3. Generate credentials
#     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#     password = generate_stk_password(MPESA_SHORTCODE, MPESA_PASSKEY, timestamp)
#     access_token = await get_mpesa_access_token()

#     # 4. Generate the exact account structure format your confirmation route expects
#     if payload.payment_type == "chat":
#         account_ref = f"016536784672{payload.profile_id}"
#     else:
#         account_ref = f"MEET016536{payload.profile_id}"

#     # 5. Determine Transaction Type based on your shortcode type
#     # For a Buy Goods Till: Use "CustomerBuyGoodsOnline"
#     # For a Paybill: Use "CustomerPayBillOnline"
#     transaction_type = "CustomerBuyGoodsOnline" 

#     stk_body = {
#         "BusinessShortCode": MPESA_SHORTCODE,
#         "Password": password,
#         "Timestamp": timestamp,
#         "TransactionType": transaction_type, 
#         "Amount": amount,
#         "PartyA": phone,
#         "PartyB": MPESA_SHORTCODE, # For Till, this is usually your Store Number
#         "PhoneNumber": phone,
#         "CallBackURL": CALLBACK_URL,
#         "AccountReference": account_ref,
#         "TransactionDesc": f"Connect {payload.payment_type} with Profile {payload.profile_id}"
#     }

#     stk_url = "https://sandbox.safaricom.co.uk/mpesa/stkpush/v1/processrequest" # Use production URL for live apps
    
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }

#     async with httpx.AsyncClient() as client:
#         response = await client.post(stk_url, json=stk_body, headers=headers)
#         res_data = response.json()
        
#         if response.status_code == 200 and res_data.get("ResponseCode") == "0":
#             # Save the request transaction state if necessary
#             return {
#                 "status": "initiated",
#                 "message": f"STK Prompt of KES {amount} successfully sent to {phone}.",
#                 "merchant_request_id": res_data.get("MerchantRequestID")
#             }
#         else:
#             return {"status": "failed", "error": res_data}





import base64
import sqlite3
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()

# --- CONFIGURATION ---
MPESA_CONSUMER_KEY = "p8Fhi6QWduA2P7opsijEWJA7Uy55WbPmotMMVvnLC5Dw4W9e"
MPESA_CONSUMER_SECRET = "gAyVOCGwrCfBoQxA23968I4gpAQ0R4Q44p5rDrGEmC9orGlFKtVK0o7uc6wZRpGx"
MPESA_PASSKEY = "N/A"

# Updated to reflect your active Lipa Na M-Pesa Paybill configurations
MPESA_SHORTCODE = "542542" 
CALLBACK_URL = "https://yourdomain.com/mpesa/callback" 

# --- INBOUND DARAJA PAYLOAD OBJECT DEFINITION ---
class ConnectRequest(BaseModel):
    phone_number: str
    amount: float
    profile_id: int
    payment_type: str

def get_webhook_db():
    conn = sqlite3.connect("platform_v2.db", timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def get_profile_amount(profile_id: int, payment_type: str) -> int:
    """Queries your database to get the exact operational pricing configuration set for this specific profile action."""
    if payment_type == "profile_submission":
        return 100  # Enforce base standard fixed flat rate cost rule
        
    conn = get_webhook_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT chat_rate, meetup_rate FROM profiles WHERE id = ?", (profile_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="Target client profile record entry not found")
        
        if payment_type == "chat":
            return int(row["chat_rate"])
        elif payment_type == "meetup":
            return int(row["meetup_rate"])
        else:
            raise HTTPException(status_code=400, detail="Invalid target platform payment destination parameter type")
            
    except sqlite3.Error as e:
        if conn: conn.close()
        raise HTTPException(status_code=500, detail=f"Internal system database routing engine exception: {str(e)}")

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
        raise HTTPException(status_code=500, detail="Authentication verification error parsing Daraja server tokens")

def generate_stk_password(shortcode, passkey, timestamp):
    return base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()


# --- CONNECT & PUSH ENDPOINT ---
@app.post("/mpesa/stk-push")
async def connect_user_profile(payload: ConnectRequest):
    """
    Triggered when a user clicks 'Connect'. 
    Fetches the profile amount from DB and requests an M-Pesa STK prompt.
    """
    # 1. Look up how much this specific profile charges
    amount = get_profile_amount(payload.profile_id, payload.payment_type)
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid execution fee profile context configuration")

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

    # 4. Generate the explicit Account Reference structure matching Streamlit & DB expectations
    if payload.payment_type == "chat":
        account_ref = f"446040-CHA{payload.profile_id}"
    elif payload.payment_type == "meetup":
        account_ref = f"446040-MEE{payload.profile_id}"
    else:
        account_ref = f"446040-SUB{payload.profile_id}"

    # 5. Enforce standard M-Pesa Paybill Online operation parameters
    transaction_type = "CustomerPayBillOnline" 

    stk_body = {
        "BusinessShortCode": MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": transaction_type, 
        "Amount": amount,
        "PartyA": phone,
        "PartyB": MPESA_SHORTCODE, # For Paybills, PartyB is matching your BusinessShortCode
        "PhoneNumber": phone,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": account_ref,
        "TransactionDesc": f"Paybill Gateway operational reference targeting: {account_ref}"
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
            return {
                "status": "initiated",
                "message": f"STK Paybill transactional reference window successfully activated targeting: {phone}.",
                "merchant_request_id": res_data.get("MerchantRequestID")
            }
        else:
            return {"status": "failed", "error": res_data}
