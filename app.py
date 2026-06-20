# import streamlit as st
# import database as db
# import os
# import uuid
# import base64

# # --- PAGE CONFIG ---
# st.set_page_config(layout="wide", page_title="TECH-STAR")
# db.init_db()

# # --- FUNCTION DEFINITIONS ---
# def save_uploaded_file(uploaded_file):
#     if not os.path.exists("uploads"): 
#         os.makedirs("uploads")
#     file_path = os.path.join("uploads", f"{uuid.uuid4()}_{uploaded_file.name}")
#     with open(file_path, "wb") as f: 
#         f.write(uploaded_file.getbuffer())
#     return file_path

# # --- STATE ---
# if "admin_logged_in" not in st.session_state: 
#     st.session_state.admin_logged_in = False

# if "verified_chats" not in st.session_state:
#     st.session_state.verified_chats = set()

# if "verified_meetups" not in st.session_state:
#     st.session_state.verified_meetups = set()

# # --- CSS ---

# import streamlit as st

# import streamlit as st
# import streamlit as st


# # --- CSS ---
# st.markdown("""
#     <style>
#     # /* 1. Hide the Deploy button entirely */
#     # [data-testid="stDeploymentDropdown"] {
#     #     display: none !important;
#     # }
    
#     # /* 2. Hide the Options menu (the three dots / hamburger menu) */
#     # [data-testid="stToolbar"] {
#     #     display: none !important;
#     # }
    
#     /* 3. Clean up the top header padding so your app layout looks perfectly balanced */
#     [data-testid="stHeader"] {
#         background-color: rgba(0, 0, 0, 0) !important;
#         height: 0px !important;
#     }
    
#     /* Keep your existing styling intact below */
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
#                 # UPDATED: Replaced deprecated use_container_width=True with modern width='stretch'
#                 st.image(p['photo_url'], width='stretch')
#                 st.write(f"### {p['name']}")
#                 st.write(f"📍 **Location:** {p['country']}, {p['continent']}")
#                 st.write(f"💰 **Rate:** KES {p['rate']:.2f}")
                
#                 if st.button(f"Connect with {p['name']}", key=f"btn_{p['id']}"):
#                     st.session_state.selected = dict(p)
#                     st.rerun()
# else:
#     # --- PRIVATE SESSION ---
#     p = st.session_state.selected
#     st.title(f"🔒 Session: {p['name']}")
#     if st.button("⬅️ Back"):
#         del st.session_state.selected
#         st.rerun()
    
#     # 1. GATEKEEPER: VERIFY M-PESA TRANSACTION ID FOR CHAT
#     if p['id'] not in st.session_state.verified_chats:
#         st.markdown(f"""
#         <div class="pay-box">
#             <h3>💰 Instant Paybill Payment Required</h3>
#             <p>Please complete payment via M-Pesa to generate your receipt transaction code.</p>
#             Business Till: <b>482394</b><br>
#             Account Number: <b style="color:#ff1493; font-size:18px;">880200381648{p['id']}</b><br>
#             Amount: <b>KES {p["rate"]:.2f}</b>
#         </div>
#         """, unsafe_allow_html=True)
        
#         user_tx_id = st.text_input("✍️ Enter M-Pesa Transaction ID / Message Confirmation Code:", key=f"tx_chat_{p['id']}").strip()
        
#         if st.button("🔓 Verify & Unlock Chat", key=f"verify_btn_{p['id']}"):
#             if user_tx_id:
#                 if db.claim_and_verify_transaction(user_tx_id, p['id'], "chat"):
#                     st.session_state.verified_chats.add(p['id'])
#                     st.success("🎉 Transaction identity authenticated! Routing connection line...")
#                     st.rerun()
#                 else:
#                     st.error("Invalid Transaction ID or reference match mismatch. Check your M-Pesa text statement again.")
#             else:
#                 st.warning("Please enter your M-Pesa receipt confirmation string to continue.")
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
#             half = p['rate'] / 2
            
#             # GATEKEEPER: VERIFY M-PESA TRANSACTION ID FOR MEETUP
#             if p['id'] not in st.session_state.verified_meetups:
#                 st.markdown(f"""
#                 <div class="pay-box">
#                     <h3>🤝 Goal Unlocked: Authorize Meetup Routing</h3>
#                     <p>Contribute your 50% split registration tier through Paybill.</p>
#                     Business Till: <b>482394</b><br>
#                     Account Number: <b style="color:#ff1493; font-size:18px;">MEET016536{p['id']}</b><br>
#                     Amount: <b>KES {half:.2f}</b>
#                 </div>
#                 """, unsafe_allow_html=True)
                
#                 user_meet_tx = st.text_input("✍️ Enter Meetup Payment Transaction ID:", key=f"tx_meet_{p['id']}").strip()
                
#                 if st.button("🔄 Verify Meetup Code", key=f"verify_meet_btn_{p['id']}"):
#                     if db.claim_and_verify_transaction(user_meet_tx, p['id'], "meetup"):
#                         st.session_state.verified_meetups.add(p['id'])
#                         st.rerun()
#                     else:
#                         st.error("Transaction code confirmation reference mismatch or unpaid entry registry.")
#                 st.stop()
#             else:
#                 st.warning("Meetup remittance confirmed processing backend. Awaiting operational administrative assignment authorization.")
#                 st.stop()

# # --- ADMIN SIDEBAR ---
# with st.sidebar:
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
#             has_paid_meet = conn.execute("SELECT 1 FROM transactions WHERE account_ref = ? AND type = 'meetup'", (account_string,)).fetchone()
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
#                 n_r = st.number_input("Rate (KES)", value=float(p['rate']), key=f"er_{p['id']}")
#                 up = st.file_uploader(f"Upload image for {p['name']}", type=['png', 'jpg'], key=f"up_{p['id']}")
                
#                 if st.button(f"Update {p['name']}", key=f"upd_{p['id']}"):
#                     f_u = save_uploaded_file(up) if up else p['photo_url']
#                     db.update_profile(p['id'], n_n, p['continent'], p['country'], p['bio'], n_r, f_u)
#                     st.success(f"Updated {p['name']}!")
#                     st.rerun()
                
#                 if st.button(f"Delete {p['name']}", key=f"del_{p['id']}"):
#                     db.delete_profile(p['id'])
#                     st.success(f"Deleted {p['name']}!")
#                     st.rerun()
        
#         st.divider()
#         with st.expander("➕ Add New Client"):
#             new_name = st.text_input("Name", key="new_name_in")
#             col1, col2 = st.columns(2)
#             with col1:
#                 new_cont = st.selectbox("Continent", ["Africa", "America", "Europe", "Asia"], key="new_cont_in")
#                 new_rate = st.number_input("Rate (KES)", min_value=0.0, key="new_rate_in")
#             with col2:
#                 new_coun = st.text_input("Country", key="new_coun_in")
#                 new_up = st.file_uploader("Upload Image", type=['png', 'jpg'], key="new_add_img")
            
#             new_bio = st.text_area("Bio/Description", "Enter bio here...", key="new_bio_in")
            
#             if st.button("Save New Client"):
#                 photo_url = save_uploaded_file(new_up) if new_up else "https://via.placeholder.com/150"
#                 db.add_single_profile(new_name, new_cont, new_coun, new_bio, new_rate, photo_url)
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
    payload = {
        "phone_number": phone_number,
        "amount": int(amount),
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

# --- APP LOGIC ---# --- APP LOGIC ---
if "selected" not in st.session_state:
    # --- MARKETPLACE ---
    profiles = db.get_available_profiles()
    
    if not profiles:
        st.info("✨ All profiles are currently in active sessions. Please check back shortly!")
    else:
        cols = st.columns(3) 
        for idx, p in enumerate(profiles):
            with cols[idx % 3]:
                st.image(p['photo_url'], width='stretch')
                st.write(f"### {p['name']}")
                st.write(f"📍 **Location:** {p['country']}, {p['continent']}")
                st.write(f"💬 **Chat Rate:** KES {p['chat_rate']:.2f}")
                st.write(f"🤝 **Meetup Rate:** KES {p['meetup_rate']:.2f}")
                
                # Directly assign the clean dictionary p to session state
                if st.button(f"Connect with {p['name']}", key=f"btn_{p['id']}"):
                    st.session_state.selected = p
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
            <h3>💰 Dynamic STK Push Checkout Required</h3>
            <p>Enter your phone number below to receive an automated M-Pesa PIN prompt dialog directly on your phone.</p>
            Service Selected: <b>Secure Direct Chat Line</b><br>
            Amount: <b>KES {p["chat_rate"]:.2f}</b>
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
            # GATEKEEPER: REQUEST PHONE AND TRIGGER M-PESA POPUP FOR MEETUP
            if p['id'] not in st.session_state.verified_meetups:
                st.markdown(f"""
                <div class="pay-box">
                    <h3>🤝 Goal Unlocked: Authorize Meetup Routing</h3>
                    <p>Enter your phone number to receive an active prompt to process the physical rendezvous logistics fee.</p>
                    Amount: <b>KES {p['meetup_rate']:.2f}</b>
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

# --- ADMIN SIDEBAR ---
with st.sidebar:
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

        # 1. System Managed Meetups Override
        st.markdown("**Pending Meetups Approvals:**")
        found_meetup = False
        for p in all_profiles:
            account_string = f"MEET016536{p['id']}"
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
        with st.expander("➕ Add New Client"):
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
