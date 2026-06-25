# import streamlit as st
# import database as db
# import os
# import uuid
# import base64
# import requests  # Added to make requests to your FastAPI M-Pesa backend
# import subprocess
# import time

# # --- EMBEDDED BACKEND BOOTSTRAPPER ---
# # This forces FastAPI to run as a quiet background process on port 8000 inside the same container
# if "backend_started" not in st.session_state:
#     try:
#         # Replace 'main:app' with the filename:variable of your FastAPI server
#         # (e.g., if your FastAPI app code is in main.py, keep it as main:app)
#         subprocess.Popen([
#             "uvicorn", "main:app", 
#             "--host", "127.0.0.1", 
#             "--port", "8000"
#         ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#         st.session_state.backend_started = True
#         time.sleep(2) # Give the background process 2 seconds to bind to port 8000 safely
#     except Exception as e:
#         st.error(f"Internal wrapper failed to spin up background API gateway: {e}")

# # --- PAGE CONFIG ---
# st.set_page_config(layout="wide", page_title="TECH-STAR")
# db.init_db()

# # URL of your running FastAPI backend handling the Daraja STK Push requests
# FASTAPI_BACKEND_URL = "http://127.0.0.1:8000" 

# # --- FUNCTION DEFINITIONS ---
# def save_uploaded_file(uploaded_file):
#     if not os.path.exists("uploads"): 
#         os.makedirs("uploads")
#     file_path = os.path.join("uploads", f"{uuid.uuid4()}_{uploaded_file.name}")
#     with open(file_path, "wb") as f: 
#         f.write(uploaded_file.getbuffer())
#     return file_path

# def trigger_stk_push(phone_number, profile_id, amount, payment_type):
#     """Helper to dispatch the STK push payload request over to the FastAPI engine"""
#     url = f"{FASTAPI_BACKEND_URL}/mpesa/stk-push"
#     payload = {
#         "phone_number": phone_number,
#         "amount": int(amount),
#         "profile_id": int(profile_id),
#         "payment_type": payment_type
#     }
#     try:
#         response = requests.post(url, json=payload, timeout=12.0)
#         return response.json()
#     except Exception as e:
#         return {"status": "error", "message": f"Could not connect to payment backend: {str(e)}"}

# # --- STATE ---
# if "admin_logged_in" not in st.session_state: 
#     st.session_state.admin_logged_in = False

# if "verified_chats" not in st.session_state:
#     st.session_state.verified_chats = set()

# if "verified_meetups" not in st.session_state:
#     st.session_state.verified_meetups = set()

# # --- CSS ---
# st.markdown("""
#     <style>
#     /* Clean up top header padding */
#     [data-testid="stHeader"] {
#         background-color: rgba(0, 0, 0, 0) !important;
#         height: 0px !important;
#     }
    
#     [data-testid="stSidebar"] { background-color: #FFC0CB !important; }
#     .navbar { background: linear-gradient(90deg, #ff69b4, #ff1493); padding: 15px; border-radius: 10px; color: white; }
#     .pay-box { background: #f9f9f9; padding: 20px; border: 2px dashed #ff1493; border-radius: 10px; margin-bottom: 15px; }
#     .rounded-img { border-radius: 50%; width: 110px; height: 110px; object-fit: cover; }
#     .welcome-banner { text-align: center; background-color: #fff0f5; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
#     </style> 
# """, unsafe_allow_html=True)

# # --- TOP NAVBAR ---
# col1, col2, col3 = st.columns([1, 4, 2])
# with col1:
#     img_path = "LOVE-IS-REAL.jpg"
#     if os.path.exists(img_path):
#         st.markdown(f'<div style="overflow:hidden; border-radius:50%; width:90px; height:90px;"><img src="data:image/jpeg;base64,{base64.b64encode(open(img_path, "rb").read()).decode()}" width="90" height="90" style="object-fit:cover;"></div>', unsafe_allow_html=True)
#     else:
#         st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=90)
# with col2:
#     st.markdown('<div class="navbar"><h2>MEET WITH YOUR FAVORITE LOVE ❤️</h2></div>', unsafe_allow_html=True)
# with col3:
#     st.markdown("📞 **Help:** +254728831770 <br> 📧 Support Center", unsafe_allow_html=True)

# # --- WELCOME BANNER ---
# st.markdown("""
#     <div class="welcome-banner">
#         <h2>🌍 Welcome to Regional Dating Platform</h2>
#         <p>Connect, Chat, and Build Meaningful Relationships Worldwide ❤️</p>
#     </div>
# """, unsafe_allow_html=True)

# # --- APP LOGIC ---
# if "selected" not in st.session_state:
#     # --- MARKETPLACE ---
#     profiles = db.get_available_profiles()
    
#     if not profiles:
#         st.info("✨ All profiles are currently in active sessions. Please check back shortly!")
#     else:
#         cols = st.columns(3) 
#         for idx, p in enumerate(profiles):
#             with cols[idx % 3]:
#                 # Safely handle dictionary conversions
#                 profile_dict = dict(p) if not isinstance(p, dict) else p
                
#                 # Use .get() with a default fallback of 0.0 to prevent any IndexError crashes
#                 chat_rate = profile_dict.get('chat_rate', profile_dict.get('rate', 0.0))
#                 meetup_rate = profile_dict.get('meetup_rate', 0.0)
                
#                 st.image(profile_dict['photo_url'], width='stretch')
#                 st.write(f"### {profile_dict['name']}")
#                 st.write(f"📍 **Location:** {profile_dict['country']}, {profile_dict['continent']}")
#                 st.write(f"💬 **Chat Rate:** KES {chat_rate:.2f}")
#                 st.write(f"🤝 **Meetup Rate:** KES {meetup_rate:.2f}")
                
#                 if st.button(f"Connect with {profile_dict['name']}", key=f"btn_{profile_dict['id']}"):
#                     st.session_state.selected = profile_dict
#                     st.rerun()
# else:
#     # --- PRIVATE SESSION ---
#     p = st.session_state.selected
#     st.title(f"🔒 Session: {p['name']}")
#     if st.button("⬅️ Back"):
#         del st.session_state.selected
#         st.rerun()
    
#     # 1. GATEKEEPER: REQUEST PHONE AND TRIGGER M-PESA POPUP FOR CHAT
#     if p['id'] not in st.session_state.verified_chats:
#         st.markdown(f"""
#         <div class="pay-box">
#             <h3>💰 Dynamic STK Push Checkout Required</h3>
#             <p>Enter your phone number below to receive an automated M-Pesa PIN prompt dialog directly on your phone.</p>
#             Service Selected: <b>Secure Direct Chat Line</b><br>
#             Amount: <b>KES {p["chat_rate"]:.2f}</b>
#         </div>
#         """, unsafe_allow_html=True)
        
#         chat_phone = st.text_input("📱 Enter M-Pesa Phone Number (e.g., 0712345678):", key=f"phone_chat_{p['id']}").strip()
        
#         if st.button("🚀 Send M-Pesa PIN Prompt", key=f"stk_chat_btn_{p['id']}"):
#             if chat_phone:
#                 with st.spinner("Firing secure payment connection line..."):
#                     res = trigger_stk_push(chat_phone, p['id'], p['chat_rate'], "chat")
#                     if res.get("status") == "initiated":
#                         st.success("✅ STK prompt dispatched! Enter your M-Pesa PIN on your phone, wait 5 seconds, then click verify below.")
#                     else:
#                         st.error(f"Failed to initiate transaction: {res.get('error', res.get('message'))}")
#             else:
#                 st.warning("Please type a valid active Safaricom number to receive the payment prompt.")
        
#         st.divider()
#         st.write("🔄 **Already approved the PIN prompt?**")
#         fallback_tx_id = st.text_input("Verification Step: Paste M-Pesa Transaction ID (e.g., SFT712XYZ0):", key=f"tx_chat_{p['id']}").strip()
        
#         if st.button("🔓 Check & Unlock Chat Session", key=f"verify_btn_{p['id']}"):
#             if db.claim_and_verify_transaction(fallback_tx_id, p['id'], "chat"):
#                 st.session_state.verified_chats.add(p['id'])
#                 st.success("🎉 Session unlocked successfully!")
#                 st.rerun()
#             else:
#                 st.error("We couldn't verify that payment yet. Ensure you entered your PIN correctly and supplied the right M-Pesa Code.")
#         st.stop()

#     # 2. CHAT & MEETUP FLOW
#     is_meetup_approved = db.check_meetup_status(p['id'])
    
#     if is_meetup_approved:
#         st.success("✅ Meetup Approved! Target logistical coordinates sent.")
#     else:
#         u_k = f"u_{p['id']}"
#         st.session_state[u_k] = st.session_state.get(u_k, 0)
        
#         msg = st.chat_input("Secure message...")
#         if msg:
#             st.session_state[u_k] += 1
#             st.chat_message("user").write(msg)
#             st.chat_message("assistant").write("Secure response.")
#             st.rerun()
        
#         st.caption(f"Progress: {st.session_state[u_k]}/10")
        
#         if st.session_state[u_k] >= 10:
#             # GATEKEEPER: REQUEST PHONE AND TRIGGER M-PESA POPUP FOR MEETUP
#             if p['id'] not in st.session_state.verified_meetups:
#                 st.markdown(f"""
#                 <div class="pay-box">
#                     <h3>🤝 Goal Unlocked: Authorize Meetup Routing</h3>
#                     <p>Enter your phone number to receive an active prompt to process the physical rendezvous logistics fee.</p>
#                     Amount: <b>KES {p['meetup_rate']:.2f}</b>
#                 </div>
#                 """, unsafe_allow_html=True)
                
#                 meetup_phone = st.text_input("📱 Enter M-Pesa Phone Number for Meetup Payment:", key=f"phone_meet_{p['id']}").strip()
                
#                 if st.button("🚀 Send Meetup STK Prompt", key=f"stk_meet_btn_{p['id']}"):
#                     if meetup_phone:
#                         with st.spinner("Requesting prompt payment access..."):
#                             res = trigger_stk_push(meetup_phone, p['id'], p['meetup_rate'], "meetup")
#                             if res.get("status") == "initiated":
#                                 st.success("✅ Meetup PIN Prompt sent! Check your phone handset screen.")
#                             else:
#                                 st.error(f"Error firing prompt: {res.get('message')}")
#                     else:
#                         st.warning("Please provide a phone number.")
                
#                 st.divider()
#                 fallback_meet_tx = st.text_input("Enter Meetup Payment Transaction ID to unlock:", key=f"tx_meet_{p['id']}").strip()
                
#                 if st.button("🔄 Verify Meetup Code", key=f"verify_meet_btn_{p['id']}"):
#                     if db.claim_and_verify_transaction(fallback_meet_tx, p['id'], "meetup"):
#                         st.session_state.verified_meetups.add(p['id'])
#                         st.rerun()
#                     else:
#                         st.error("Transaction code reference mismatch or payment still processing.")
#                 st.stop()
#             else:
#                 st.warning("Meetup remittance confirmed processing backend. Awaiting operational administrative assignment authorization.")
#                 st.stop()

# # --- SIDEBAR CONTENT PANEL ---
# with st.sidebar:
#     # ========================================================
#     # FEATURE IMPLEMENTATION: CLIENT PROFILE SUBMISSION BOX
#     # ========================================================
#     st.header("✨ Add Your Profile Display")
#     st.markdown("""
#     <div style="background-color: #ffffff; padding: 10px; border-radius: 5px; border: 1px solid #ff1493; color: black; font-size:13px; margin-bottom:10px;">
#         📢 <b>Want your profile listed?</b> Fill in your display details. Submission costs a standard verification processing fee of <b>KES 100.00</b>.
#     </div>
#     """, unsafe_allow_html=True)
    
#     with st.expander("📝 Fill Submission Form", expanded=False):
#         sub_name = st.text_input("Display Name", key="sub_name")
#         sub_cont = st.selectbox("Continent Location", ["Africa", "America", "Europe", "Asia"], key="sub_cont")
#         sub_coun = st.text_input("Country Location", key="sub_coun")
#         sub_bio = st.text_area("Short Bio/Intro", key="sub_bio")
#         sub_img = st.file_uploader("Upload Profile Image", type=['png', 'jpg'], key="sub_img")
        
#         st.divider()
#         st.markdown("**💳 M-Pesa Checkout**")
#         sub_phone = st.text_input("📱 M-Pesa Phone Number:", key="sub_phone_input", placeholder="07XXXXXXXX").strip()
        
#         if st.button("🚀 Pay KES 100 ", key="sub_pay_btn"):
#             if not sub_name or not sub_phone:
#                 st.warning("Please fill in your name and a valid Safaricom phone number to trigger payments.")
#             else:
#                 with st.spinner("Dispatching secure payment API line..."):
#                     # profile_id is 0 because the entry has not yet been logged into database row layout
#                     res = trigger_stk_push(sub_phone, 0, 100, "profile_submission")
#                     if res.get("status") == "initiated":
#                         st.success("✅ STK prompt dispatched! Approve the prompt on your handset, wait 5 seconds, then verify below.")
#                     else:
#                         st.error(f"Failed to initiate transaction: {res.get('message')}")
                        
#         st.divider()
#         sub_tx_id = st.text_input("Verification Step: Paste M-Pesa Code", key="sub_tx_verify").strip()
        
#         if st.button("🔓 Complete & Submit Profile", key="sub_verify_btn"):
#             if not sub_tx_id or not sub_name:
#                 st.error("Please ensure your name is written and your transaction code is copied accurately.")
#             else:
#                 if db.claim_and_verify_transaction(sub_tx_id, 0, "profile_submission"):
#                     f_url = save_uploaded_file(sub_img) if sub_img else "https://via.placeholder.com/150"
                    
#                     # Adds to the database with standard placeholder rates (Admin can edit these anytime later)
#                     db.add_single_profile(sub_name, sub_cont, sub_coun, sub_bio, 150.0, 2000.0, f_url)
#                     st.success("🎉 Payment verified! Your new profile has been added to the main display roster successfully.")
#                     time.sleep(2)
#                     st.rerun()
#                 else:
#                     st.error("Could not find a successful matching transaction code reference entry.")

#     st.divider()

#     # ========================================================
#     # SYSTEM CONTROL: EXISTING ADMIN PRIVILEGED MANAGEMENT PANEL
#     # ========================================================
#     st.header("Admin Management")
#     if not st.session_state.admin_logged_in:
#         pwd = st.text_input("Password", type="password", key="admin_pwd_entry")
#         if st.button("Login"):
#             if pwd == st.secrets["ADMIN_PASSWORD"]:
#                 st.session_state.admin_logged_in = True
#                 st.rerun()
#             else:
#                 st.error("Incorrect Password")
#     else:
#         if st.button("Logout"):
#             st.session_state.admin_logged_in = False
#             st.rerun()

#         st.divider()
#         st.subheader("🔍 Automated Operational Controls")
        
#         all_profiles = db.get_profiles()

#         # 1. System Managed Meetups Override
#         st.markdown("**Pending Meetups Approvals:**")
#         found_meetup = False
#         for p in all_profiles:
#             account_string = f"MEET016536{p['id']}"
#             conn = db.get_db()
#             has_paid_meet = conn.execute("SELECT 1 FROM transactions WHERE account_ref = ? AND type = 'meetup' AND status = 'completed'", (account_string,)).fetchone()
#             conn.close()

#             if has_paid_meet and not db.check_meetup_status(p['id']):
#                 found_meetup = True
#                 if st.button(f"Approve Meetup: {p['name']}", key=f"app_meet_{p['id']}"):
#                     db.approve_meetup(p['id'])
#                     st.rerun()
#         if not found_meetup:
#             st.write("No pending manual authorizations required.")

#         st.divider()
#         st.subheader("📋 Client Directory")
#         for p in all_profiles:
#             with st.expander(f"👤 {p['name']}"):
#                 n_n = st.text_input("Name", value=p['name'], key=f"en_{p['id']}")
#                 n_cr = st.number_input("Chat Rate (KES)", value=float(p['chat_rate']), key=f"ecr_{p['id']}")
#                 n_mr = st.number_input("Meetup Rate (KES)", value=float(p['meetup_rate']), key=f"emr_{p['id']}")
#                 up = st.file_uploader(f"Upload image for {p['name']}", type=['png', 'jpg'], key=f"up_{p['id']}")
                
#                 if st.button(f"Update {p['name']}", key=f"upd_{p['id']}"):
#                     f_u = save_uploaded_file(up) if up else p['photo_url']
#                     db.update_profile(p['id'], n_n, p['continent'], p['country'], p['bio'], n_cr, n_mr, f_u)
#                     st.success(f"Updated {p['name']}!")
#                     st.rerun()
                
#                 if st.button(f"Delete {p['name']}", key=f"del_{p['id']}"):
#                     db.delete_profile(p['id'])
#                     st.success(f"Deleted {p['name']}!")
#                     st.rerun()
        
#         st.divider()
#         with st.expander("➕ Add New Client Manually"):
#             new_name = st.text_input("Name", key="new_name_in")
#             col1, col2 = st.columns(2)
#             with col1:
#                 new_cont = st.selectbox("Continent", ["Africa", "America", "Europe", "Asia"], key="new_cont_in")
#                 new_chat_rate = st.number_input("Chat Rate (KES)", min_value=0.0, key="new_ch_rate_in")
#             with col2:
#                 new_coun = st.text_input("Country", key="new_coun_in")
#                 new_meet_rate = st.number_input("Meetup Rate (KES)", min_value=0.0, key="new_mt_rate_in")
            
#             new_up = st.file_uploader("Upload Image", type=['png', 'jpg'], key="new_add_img")
#             new_bio = st.text_area("Bio/Description", "Enter bio here...", key="new_bio_in")
            
#             if st.button("Save New Client"):
#                 photo_url = save_uploaded_file(new_up) if new_up else "https://via.placeholder.com/150"
#                 db.add_single_profile(new_name, new_cont, new_coun, new_bio, new_chat_rate, new_meet_rate, photo_url)
#                 st.success(f"Added {new_name} successfully!")
#                 st.rerun()

# # --- FOOTER ---
# st.markdown("---")
# st.markdown("""
#     <div style="text-align: center; color: grey; font-size: 12px; margin-top: 50px;">
#     &copy; 2026 TECH-STAR Regional Dating Platform. All rights reserved. <br>
#     Privacy Policy | Terms of Service | <a href="mailto:support@techstar.com">Contact Support</a>
#     </div>
# """, unsafe_allow_html=True)




import streamlit as st
import database as db
import os
import uuid
import base64
import requests  # Added to make requests to your FastAPI M-Pesa backend
import subprocess
import time

# --- EMBEDDED BACKEND BOOTSTRAPPER ---
# This forces FastAPI to run as a quiet background process on port 8000 inside the same container
if "backend_started" not in st.session_state:
    try:
        # Replace 'main:app' with the filename:variable of your FastAPI server
        # (e.g., if your FastAPI app code is in main.py, keep it as main:app)
        subprocess.Popen([
            "uvicorn", "main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        st.session_state.backend_started = True
        time.sleep(2) # Give the background process 2 seconds to bind to port 8000 safely
    except Exception as e:
        st.error(f"Internal wrapper failed to spin up background API gateway: {e}")

# --- PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="TECH-STAR")
db.init_db()

# URL of your running FastAPI backend handling the Daraja STK Push requests
FASTAPI_BACKEND_URL = "http://127.0.0.1:8000" 

# --- FUNCTION DEFINITIONS ---
def save_uploaded_file(uploaded_file):
    if not os.path.exists("uploads"): 
        os.makedirs("uploads")
    file_path = os.path.join("uploads", f"{uuid.uuid4()}_{uploaded_file.name}")
    with open(file_path, "wb") as f: 
        f.write(uploaded_file.getbuffer())
    return file_path

def trigger_stk_push(phone_number, profile_id, amount, payment_type):
    """Helper to dispatch the STK push payload request over to the FastAPI engine"""
    url = f"{FASTAPI_BACKEND_URL}/mpesa/stk-push"
    
    # Dynamic Account Reference linking your base business account with the specific profile action
    account_reference = f"446040-{payment_type[:3].upper()}{profile_id}"
    
    payload = {
        "phone_number": phone_number,
        "amount": int(amount),
        "paybill": "542542",                     # Your exact paybill configuration
        "account_number": "446040",      # Generates e.g., 446040-CHA12
        "profile_id": int(profile_id),
        "payment_type": payment_type
    }
    try:
        response = requests.post(url, json=payload, timeout=12.0)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": f"Could not connect to payment backend: {str(e)}"}

# --- STATE ---
if "admin_logged_in" not in st.session_state: 
    st.session_state.admin_logged_in = False

if "verified_chats" not in st.session_state:
    st.session_state.verified_chats = set()

if "verified_meetups" not in st.session_state:
    st.session_state.verified_meetups = set()

# --- CSS ---
st.markdown("""
    <style>
    /* Clean up top header padding */
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0) !important;
        height: 0px !important;
    }
    
    [data-testid="stSidebar"] { background-color: #FFC0CB !important; }
    .navbar { background: linear-gradient(90deg, #ff69b4, #ff1493); padding: 15px; border-radius: 10px; color: white; }
    .pay-box { background: #f9f9f9; padding: 20px; border: 2px dashed #ff1493; border-radius: 10px; margin-bottom: 15px; }
    .rounded-img { border-radius: 50%; width: 110px; height: 110px; object-fit: cover; }
    .welcome-banner { text-align: center; background-color: #fff0f5; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
    </style> 
""", unsafe_allow_html=True)

# --- TOP NAVBAR ---
col1, col2, col3 = st.columns([1, 4, 2])
with col1:
    img_path = "LOVE-IS-REAL.jpg"
    if os.path.exists(img_path):
        st.markdown(f'<div style="overflow:hidden; border-radius:50%; width:90px; height:90px;"><img src="data:image/jpeg;base64,{base64.b64encode(open(img_path, "rb").read()).decode()}" width="90" height="90" style="object-fit:cover;"></div>', unsafe_allow_html=True)
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=90)
with col2:
    st.markdown('<div class="navbar"><h2>MEET WITH YOUR FAVORITE LOVE ❤️</h2></div>', unsafe_allow_html=True)
with col3:
    st.markdown("📞 **Help:** +254728831770 <br> 📧 Support Center", unsafe_allow_html=True)

# --- WELCOME BANNER ---
st.markdown("""
    <div class="welcome-banner">
        <h2>🌍 Welcome to Regional Dating Platform</h2>
        <p>Connect, Chat, and Build Meaningful Relationships Worldwide ❤️</p>
    </div>
""", unsafe_allow_html=True)

# --- APP LOGIC ---
if "selected" not in st.session_state:
    # --- MARKETPLACE ---
    profiles = db.get_available_profiles()
    
    if not profiles:
        st.info("✨ All profiles are currently in active sessions. Please check back shortly!")
    else:
        cols = st.columns(3) 
        for idx, p in enumerate(profiles):
            with cols[idx % 3]:
                profile_dict = dict(p) if not isinstance(p, dict) else p
                
                chat_rate = profile_dict.get('chat_rate', profile_dict.get('rate', 0.0))
                meetup_rate = profile_dict.get('meetup_rate', 0.0)
                
                st.image(profile_dict['photo_url'], width='stretch')
                st.write(f"### {profile_dict['name']}")
                st.write(f"📍 **Location:** {profile_dict['country']}, {profile_dict['continent']}")
                st.write(f"💬 **Chat Rate:** KES {chat_rate:.2f}")
                st.write(f"🤝 **Meetup Rate:** KES {meetup_rate:.2f}")
                
                if st.button(f"Connect with {profile_dict['name']}", key=f"btn_{profile_dict['id']}"):
                    st.session_state.selected = profile_dict
                    st.rerun()
else:
    # --- PRIVATE SESSION ---
    p = st.session_state.selected
    st.title(f"🔒 Session: {p['name']}")
    if st.button("⬅️ Back"):
        del st.session_state.selected
        st.rerun()
    
    # 1. GATEKEEPER: REQUEST PHONE AND TRIGGER M-PESA POPUP FOR CHAT
    if p['id'] not in st.session_state.verified_chats:
        st.markdown(f"""
        <div class="pay-box">
            <h3>💰 Lipa Na M-Pesa Paybill Checkout Required</h3>
            <p>Enter your phone number below to receive an automated secure payment confirmation screen directly on your device.</p>
            <b>Payment Destination:</b> Lipa Na IMBANK<br>
            <b>Business Paybill:</b> 542542<br>
            <b>Account Target:</b> 446040-CHA{p['id']}<br>
            <b>Service Selected:</b> Secure Direct Chat Line<br>
            <b>Amount:</b> KES {p["chat_rate"]:.2f}
        </div>
        """, unsafe_allow_html=True)
        
        chat_phone = st.text_input("📱 Enter M-Pesa Phone Number (e.g., 0712345678):", key=f"phone_chat_{p['id']}").strip()
        
        if st.button("🚀 Send M-Pesa PIN Prompt", key=f"stk_chat_btn_{p['id']}"):
            if chat_phone:
                with st.spinner("Firing secure payment connection line..."):
                    res = trigger_stk_push(chat_phone, p['id'], p['chat_rate'], "chat")
                    if res.get("status") == "initiated":
                        st.success("✅ STK prompt dispatched! Enter your M-Pesa PIN on your phone, wait 5 seconds, then click verify below.")
                    else:
                        st.error(f"Failed to initiate transaction: {res.get('error', res.get('message'))}")
            else:
                st.warning("Please type a valid active Safaricom number to receive the payment prompt.")
        
        st.divider()
        st.write("🔄 **Already approved the PIN prompt?**")
        fallback_tx_id = st.text_input("Verification Step: Paste M-Pesa Transaction ID (e.g., SFT712XYZ0):", key=f"tx_chat_{p['id']}").strip()
        
        if st.button("🔓 Check & Unlock Chat Session", key=f"verify_btn_{p['id']}"):
            if db.claim_and_verify_transaction(fallback_tx_id, p['id'], "chat"):
                st.session_state.verified_chats.add(p['id'])
                st.success("🎉 Session unlocked successfully!")
                st.rerun()
            else:
                st.error("We couldn't verify that payment yet. Ensure you entered your PIN correctly and supplied the right M-Pesa Code.")
        st.stop()

    # 2. CHAT & MEETUP FLOW
    is_meetup_approved = db.check_meetup_status(p['id'])
    
    if is_meetup_approved:
        st.success("✅ Meetup Approved! Target logistical coordinates sent.")
    else:
        u_k = f"u_{p['id']}"
        st.session_state[u_k] = st.session_state.get(u_k, 0)
        
        msg = st.chat_input("Secure message...")
        if msg:
            st.session_state[u_k] += 1
            st.chat_message("user").write(msg)
            st.chat_message("assistant").write("Secure response.")
            st.rerun()
        
        st.caption(f"Progress: {st.session_state[u_k]}/10")
        
        if st.session_state[u_k] >= 10:
            if p['id'] not in st.session_state.verified_meetups:
                st.markdown(f"""
                <div class="pay-box">
                    <h3>🤝 Goal Unlocked: Authorize Meetup Routing</h3>
                    <p>Enter your phone number to receive an active prompt to process the physical rendezvous logistics fee.</p>
                    <b>Business Paybill:</b> 542542<br>
                    <b>Account Target:</b> 446040-MEE{p['id']}<br>
                    <b>Amount:</b> KES {p['meetup_rate']:.2f}
                </div>
                """, unsafe_allow_html=True)
                
                meetup_phone = st.text_input("📱 Enter M-Pesa Phone Number for Meetup Payment:", key=f"phone_meet_{p['id']}").strip()
                
                if st.button("🚀 Send Meetup STK Prompt", key=f"stk_meet_btn_{p['id']}"):
                    if meetup_phone:
                        with st.spinner("Requesting prompt payment access..."):
                            res = trigger_stk_push(meetup_phone, p['id'], p['meetup_rate'], "meetup")
                            if res.get("status") == "initiated":
                                st.success("✅ Meetup PIN Prompt sent! Check your phone handset screen.")
                            else:
                                st.error(f"Error firing prompt: {res.get('message')}")
                    else:
                        st.warning("Please provide a phone number.")
                
                st.divider()
                fallback_meet_tx = st.text_input("Enter Meetup Payment Transaction ID to unlock:", key=f"tx_meet_{p['id']}").strip()
                
                if st.button("🔄 Verify Meetup Code", key=f"verify_meet_btn_{p['id']}"):
                    if db.claim_and_verify_transaction(fallback_meet_tx, p['id'], "meetup"):
                        st.session_state.verified_meetups.add(p['id'])
                        st.rerun()
                    else:
                        st.error("Transaction code reference mismatch or payment still processing.")
                st.stop()
            else:
                st.warning("Meetup remittance confirmed processing backend. Awaiting operational administrative assignment authorization.")
                st.stop()

# --- SIDEBAR CONTENT PANEL ---
with st.sidebar:
    st.header("✨ Add Your Profile Display")
    st.markdown("""
    <div style="background-color: #ffffff; padding: 10px; border-radius: 5px; border: 1px solid #ff1493; color: black; font-size:13px; margin-bottom:10px;">
        📢 <b>Want your profile listed?</b> Fill in your display details. Submission costs a standard verification processing fee of <b>KES 100.00</b> via Paybill 542542.
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📝 Fill Submission Form", expanded=False):
        sub_name = st.text_input("Display Name", key="sub_name")
        sub_cont = st.selectbox("Continent Location", ["Africa", "America", "Europe", "Asia"], key="sub_cont")
        sub_coun = st.text_input("Country Location", key="sub_coun")
        sub_bio = st.text_area("Short Bio/Intro", key="sub_bio")
        sub_img = st.file_uploader("Upload Profile Image", type=['png', 'jpg'], key="sub_img")
        
        st.divider()
        st.markdown("**💳 M-Pesa Paybill Checkout**")
        sub_phone = st.text_input("📱 M-Pesa Phone Number:", key="sub_phone_input", placeholder="07XXXXXXXX").strip()
        
        if st.button("🚀 Pay KES 100 via STK Push", key="sub_pay_btn"):
            if not sub_name or not sub_phone:
                st.warning("Please fill in your name and a valid Safaricom phone number to trigger payments.")
            else:
                with st.spinner("Dispatching secure payment API line..."):
                    res = trigger_stk_push(sub_phone, 0, 100, "profile_submission")
                    if res.get("status") == "initiated":
                        st.success("✅ STK prompt dispatched! Approve the prompt on your handset, wait 5 seconds, then verify below.")
                    else:
                        st.error(f"Failed to initiate transaction: {res.get('message')}")
                        
        st.divider()
        sub_tx_id = st.text_input("Verification Step: Paste M-Pesa Code", key="sub_tx_verify").strip()
        
        if st.button("🔓 Complete & Submit Profile", key="sub_verify_btn"):
            if not sub_tx_id or not sub_name:
                st.error("Please ensure your name is written and your transaction code is copied accurately.")
            else:
                if db.claim_and_verify_transaction(sub_tx_id, 0, "profile_submission"):
                    f_url = save_uploaded_file(sub_img) if sub_img else "https://via.placeholder.com/150"
                    db.add_single_profile(sub_name, sub_cont, sub_coun, sub_bio, 150.0, 2000.0, f_url)
                    st.success("🎉 Payment verified! Your new profile has been added to the main display roster successfully.")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Could not find a successful matching transaction code reference entry.")

    st.divider()

    # Admin Privileged Management Panel
    st.header("Admin Management")
    if not st.session_state.admin_logged_in:
        pwd = st.text_input("Password", type="password", key="admin_pwd_entry")
        if st.button("Login"):
            if pwd == st.secrets["ADMIN_PASSWORD"]:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Incorrect Password")
    else:
        if st.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()

        st.divider()
        st.subheader("🔍 Automated Operational Controls")
        
        all_profiles = db.get_profiles()

        st.markdown("**Pending Meetups Approvals:**")
        found_meetup = False
        for p in all_profiles:
            # Replaced with Paybill structural string references matching your account profile logic
            account_string = f"446040-MEE{p['id']}"
            conn = db.get_db()
            has_paid_meet = conn.execute("SELECT 1 FROM transactions WHERE account_ref = ? AND type = 'meetup' AND status = 'completed'", (account_string,)).fetchone()
            conn.close()

            if has_paid_meet and not db.check_meetup_status(p['id']):
                found_meetup = True
                if st.button(f"Approve Meetup: {p['name']}", key=f"app_meet_{p['id']}"):
                    db.approve_meetup(p['id'])
                    st.rerun()
        if not found_meetup:
            st.write("No pending manual authorizations required.")

        st.divider()
        st.subheader("📋 Client Directory")
        for p in all_profiles:
            with st.expander(f"👤 {p['name']}"):
                n_n = st.text_input("Name", value=p['name'], key=f"en_{p['id']}")
                n_cr = st.number_input("Chat Rate (KES)", value=float(p['chat_rate']), key=f"ecr_{p['id']}")
                n_mr = st.number_input("Meetup Rate (KES)", value=float(p['meetup_rate']), key=f"emr_{p['id']}")
                up = st.file_uploader(f"Upload image for {p['name']}", type=['png', 'jpg'], key=f"up_{p['id']}")
                
                if st.button(f"Update {p['name']}", key=f"upd_{p['id']}"):
                    f_u = save_uploaded_file(up) if up else p['photo_url']
                    db.update_profile(p['id'], n_n, p['continent'], p['country'], p['bio'], n_cr, n_mr, f_u)
                    st.success(f"Updated {p['name']}!")
                    st.rerun()
                
                if st.button(f"Delete {p['name']}", key=f"del_{p['id']}"):
                    db.delete_profile(p['id'])
                    st.success(f"Deleted {p['name']}!")
                    st.rerun()
        
        st.divider()
        with st.expander("➕ Add New Client Manually"):
            new_name = st.text_input("Name", key="new_name_in")
            col1, col2 = st.columns(2)
            with col1:
                new_cont = st.selectbox("Continent", ["Africa", "America", "Europe", "Asia"], key="new_cont_in")
                new_chat_rate = st.number_input("Chat Rate (KES)", min_value=0.0, key="new_ch_rate_in")
            with col2:
                new_coun = st.text_input("Country", key="new_coun_in")
                new_meet_rate = st.number_input("Meetup Rate (KES)", min_value=0.0, key="new_mt_rate_in")
            
            new_up = st.file_uploader("Upload Image", type=['png', 'jpg'], key="new_add_img")
            new_bio = st.text_area("Bio/Description", "Enter bio here...", key="new_bio_in")
            
            if st.button("Save New Client"):
                photo_url = save_uploaded_file(new_up) if new_up else "https://via.placeholder.com/150"
                db.add_single_profile(new_name, new_cont, new_coun, new_bio, new_chat_rate, new_meet_rate, photo_url)
                st.success(f"Added {new_name} successfully!")
                st.rerun()

# --- FOOTER ---
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: grey; font-size: 12px; margin-top: 50px;">
    &copy; 2026 TECH-STAR Regional Dating Platform. All rights reserved. <br>
    Privacy Policy | Terms of Service | <a href="mailto:support@techstar.com">Contact Support</a>
    </div>
""", unsafe_allow_html=True)
