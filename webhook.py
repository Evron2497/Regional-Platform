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

# Configured to mirror your Lipa Na M-Pesa manual payment setup
MPESA_SHORTCODE = "542542" 
CALLBACK_URL = "https://yourdomain.com/mpesa/callback" 

# --- INBOUND OBJECT DEFINITIONS ---
class ConnectRequest(BaseModel):
    phone_number: str
    amount: float
    profile_id: int
    payment_type: str

class ManualTransactionRequest(BaseModel):
    transaction_id: str
    profile_id: int
    payment_type: str
    amount: float

def get_webhook_db():
    conn = sqlite3.connect("platform_v2.db", timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def get_profile_amount(profile_id: int, payment_type: str) -> int:
    """Queries the database for exact operational pricing configured for this specific profile action."""
    if payment_type == "profile_submission":
        return 100  # Base flat rate calculation
        
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
        raise HTTPException(status_code=500, detail=f"Internal system database engine exception: {str(e)}")

# --- DARAJA API AUTH HELPERS ---
async def get_mpesa_access_token():
    url = "https://sandbox.safaricom.co.uk/oauth/v1/generate?grant_type=client_credentials"
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


# --- COEXISTING MANUAL TRANSACTION LOGGER ---
@app.post("/mpesa/log-manual")
async def log_manual_transaction(payload: ManualTransactionRequest):
    """
    Optional API endpoint to programmatically ingest a manual code claim
    into the database structure for Admin tracking.
    """
    conn = get_webhook_db()
    tx_id = payload.transaction_id.strip().upper()
    
    if payload.payment_type == "chat":
        account_ref = f"446040-CHA{payload.profile_id}"
    elif payload.payment_type == "meetup":
        account_ref = f"446040-MEE{payload.profile_id}"
    else:
        account_ref = f"446040-SUB{payload.profile_id}"

    try:
        conn.execute("""
            INSERT INTO transactions (transaction_id, profile_id, account_ref, amount, type, status)
            VALUES (?, ?, ?, ?, ?, 'pending')
        """, (tx_id, payload.profile_id, account_ref, payload.amount, payload.payment_type))
        conn.commit()
        return {"status": "success", "message": "Transaction submitted successfully to admin approval queue."}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="This transaction reference ID has already been claimed.")
    finally:
        conn.close()


# --- CONNECT & PUSH ENDPOINT ---
@app.post("/mpesa/stk-push")
async def connect_user_profile(payload: ConnectRequest):
    """
    Triggered if an automated STK prompt is initialized. 
    Inserts a 'pending' placeholder tracking metric into our transactional ledger.
    """
    amount = get_profile_amount(payload.profile_id, payload.payment_type)
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid execution fee profile context configuration")

    phone = payload.phone_number.strip()
    if phone.startswith("0"):
        phone = "254" + phone[1:]
    elif phone.startswith("+254"):
        phone = phone.replace("+", "")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = generate_stk_password(MPESA_SHORTCODE, MPESA_PASSKEY, timestamp)
    access_token = await get_mpesa_access_token()

    if payload.payment_type == "chat":
        account_ref = f"446040-CHA{payload.profile_id}"
    elif payload.payment_type == "meetup":
        account_ref = f"446040-MEE{payload.profile_id}"
    else:
        account_ref = f"446040-SUB{payload.profile_id}"

    stk_body = {
        "BusinessShortCode": MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline", 
        "Amount": amount,
        "PartyA": phone,
        "PartyB": MPESA_SHORTCODE, 
        "PhoneNumber": phone,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": account_ref,
        "TransactionDesc": f"Paybill manual confirmation reference targeting: {account_ref}"
    }

    stk_url = "https://sandbox.safaricom.co.uk/mpesa/stkpush/v1/processrequest"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(stk_url, json=stk_body, headers=headers)
        res_data = response.json()
        
        if response.status_code == 200 and res_data.get("ResponseCode") == "0":
            # Record structural tracking item down within database
            conn = get_webhook_db()
            conn.execute("""
                INSERT INTO transactions (merchant_request_id, profile_id, account_ref, amount, type, status)
                VALUES (?, ?, ?, ?, ?, 'pending')
            """, (res_data.get("MerchantRequestID"), payload.profile_id, account_ref, amount, payload.payment_type))
            conn.commit()
            conn.close()

            return {
                "status": "initiated",
                "message": f"STK verification route setup successfully activated targeting: {phone}.",
                "merchant_request_id": res_data.get("MerchantRequestID")
            }
        else:
            return {"status": "failed", "error": res_data}
