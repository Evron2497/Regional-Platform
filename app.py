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

# # --- CSS ---
# st.markdown("""
#     <style>
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

# # --- REAL-TIME REACTIVE PAYWALL FRAGMENTS ---

# @st.fragment(run_every=3.0)
# def real_time_chat_gatekeeper(profile_id, rate):
#     """Monitors the chat payment status in the database every 3 seconds."""
#     if not db.check_if_paid(profile_id):
#         st.markdown(f"""
#         <div class="pay-box">
#             <h3>💰 Instant Paybill Payment Required</h3>
#             <p>Please pay manually via M-Pesa tool to unlock secure chat routing immediately.</p>
#             Business Paybill: <b>3043935</b><br>
#             Account Number: <b style="color:#ff1493; font-size:18px;">016536784672{profile_id}</b><br>
#             Amount: <b>KES {rate:.2f}</b>
#         </div>
#         """, unsafe_allow_html=True)
#         st.info("⏳ Monitoring transaction registry in real-time... The screen will unlock automatically when payment arrives.")
#     else:
#         st.success("🎉 Payment detected! Unlocking chat channel...")
#         st.rerun()  # Forces a main page reload once background transaction matches

# @st.fragment(run_every=3.0)
# def real_time_meetup_gatekeeper(profile_id, half_rate):
#     """Monitors the meetup deposit status in the database every 3 seconds."""
#     if not db.check_if_meetup_paid(profile_id):
#         st.markdown(f"""
#         <div class="pay-box">
#             <h3>🤝 Goal Unlocked: Authorize Meetup Routing</h3>
#             <p>Contribute your 50% split registration tier through Paybill.</p>
#             Business Paybill: <b>3043935</b><br>
#             Account Number: <b style="color:#ff1493; font-size:18px;">MEET016536{profile_id}</b><br>
#             Amount: <b>KES {half_rate:.2f}</b>
#         </div>
#         """, unsafe_allow_html=True)
#         st.info("⏳ Tracking meetup deposit settlement records... Portal updates instantly upon confirmation.")
#     else:
#         st.rerun()

# # --- APP LOGIC ---
# if "selected" not in st.session_state:
#     # --- MARKETPLACE ---
#     profiles = db.get_profiles()
#     cols = st.columns(3) 
#     for idx, p in enumerate(profiles):
#         with cols[idx % 3]:
#             st.image(p['photo_url'], use_container_width=True)
#             st.write(f"### {p['name']}")
            
#             # Display Location and Amount
#             st.write(f"📍 **Location:** {p['country']}, {p['continent']}")
#             st.write(f"💰 **Rate:** KES {p['rate']:.2f}")
            
#             if st.button(f"Connect with {p['name']}", key=f"btn_{p['id']}"):
#                 # Cast row to explicit dictionary to safeguard multi-threaded state reads
#                 st.session_state.selected = dict(p)
#                 st.rerun()
# else:
#     # --- PRIVATE SESSION ---
#     p = st.session_state.selected
#     st.title(f"🔒 Session: {p['name']}")
#     if st.button("⬅️ Back"):
#         del st.session_state.selected
#         st.rerun()
    
#     # 1. GATEKEEPER: CHAT AUTOMATED CHECK (No buttons required)
#     if not db.check_if_paid(p['id']):
#         real_time_chat_gatekeeper(p['id'], p['rate'])
#         st.stop()  # Halt execution of downstream chat widgets until paid

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
            
#             # Execute real-time verification gate for meetups
#             if not db.check_if_meetup_paid(p['id']):
#                 real_time_meetup_gatekeeper(p['id'], half)
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
#             if db.check_if_meetup_paid(p['id']) and not db.check_meetup_status(p['id']):
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
#                     st.rerun()
                
#                 if st.button(f"Delete {p['name']}", key=f"del_{p['id']}"):
#                     db.delete_profile(p['id'])
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

# --- PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="TECH-STAR")
db.init_db()

# --- FUNCTION DEFINITIONS ---
def save_uploaded_file(uploaded_file):
    if not os.path.exists("uploads"): 
        os.makedirs("uploads")
    file_path = os.path.join("uploads", f"{uuid.uuid4()}_{uploaded_file.name}")
    with open(file_path, "wb") as f: 
        f.write(uploaded_file.getbuffer())
    return file_path

# --- STATE ---
if "admin_logged_in" not in st.session_state: 
    st.session_state.admin_logged_in = False

if "verified_chats" not in st.session_state:
    st.session_state.verified_chats = set()

if "verified_meetups" not in st.session_state:
    st.session_state.verified_meetups = set()

# --- CSS ---

import streamlit as st

import streamlit as st

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            /* Target the specific deployment button container */
            [data-testid="stAppDeployButton"] {
                visibility: hidden;
                display: none;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# --- CSS ---
st.markdown("""
    <style>
    /* 1. Hide the Deploy button entirely */
    [data-testid="stDeploymentDropdown"] {
        display: none !important;
    }
    
    /* 2. Hide the Options menu (the three dots / hamburger menu) */
    [data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* 3. Clean up the top header padding so your app layout looks perfectly balanced */
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0) !important;
        height: 0px !important;
    }
    
    /* Keep your existing styling intact below */
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
                # UPDATED: Replaced deprecated use_container_width=True with modern width='stretch'
                st.image(p['photo_url'], width='stretch')
                st.write(f"### {p['name']}")
                st.write(f"📍 **Location:** {p['country']}, {p['continent']}")
                st.write(f"💰 **Rate:** KES {p['rate']:.2f}")
                
                if st.button(f"Connect with {p['name']}", key=f"btn_{p['id']}"):
                    st.session_state.selected = dict(p)
                    st.rerun()
else:
    # --- PRIVATE SESSION ---
    p = st.session_state.selected
    st.title(f"🔒 Session: {p['name']}")
    if st.button("⬅️ Back"):
        del st.session_state.selected
        st.rerun()
    
    # 1. GATEKEEPER: VERIFY M-PESA TRANSACTION ID FOR CHAT
    if p['id'] not in st.session_state.verified_chats:
        st.markdown(f"""
        <div class="pay-box">
            <h3>💰 Instant Paybill Payment Required</h3>
            <p>Please complete payment via M-Pesa to generate your receipt transaction code.</p>
            Business Paybill: <b>3043935</b><br>
            Account Number: <b style="color:#ff1493; font-size:18px;">016536784672{p['id']}</b><br>
            Amount: <b>KES {p["rate"]:.2f}</b>
        </div>
        """, unsafe_allow_html=True)
        
        user_tx_id = st.text_input("✍️ Enter M-Pesa Transaction ID / Message Confirmation Code:", key=f"tx_chat_{p['id']}").strip()
        
        if st.button("🔓 Verify & Unlock Chat", key=f"verify_btn_{p['id']}"):
            if user_tx_id:
                if db.claim_and_verify_transaction(user_tx_id, p['id'], "chat"):
                    st.session_state.verified_chats.add(p['id'])
                    st.success("🎉 Transaction identity authenticated! Routing connection line...")
                    st.rerun()
                else:
                    st.error("Invalid Transaction ID or reference match mismatch. Check your M-Pesa text statement again.")
            else:
                st.warning("Please enter your M-Pesa receipt confirmation string to continue.")
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
            half = p['rate'] / 2
            
            # GATEKEEPER: VERIFY M-PESA TRANSACTION ID FOR MEETUP
            if p['id'] not in st.session_state.verified_meetups:
                st.markdown(f"""
                <div class="pay-box">
                    <h3>🤝 Goal Unlocked: Authorize Meetup Routing</h3>
                    <p>Contribute your 50% split registration tier through Paybill.</p>
                    Business Paybill: <b>3043935</b><br>
                    Account Number: <b style="color:#ff1493; font-size:18px;">MEET016536{p['id']}</b><br>
                    Amount: <b>KES {half:.2f}</b>
                </div>
                """, unsafe_allow_html=True)
                
                user_meet_tx = st.text_input("✍️ Enter Meetup Payment Transaction ID:", key=f"tx_meet_{p['id']}").strip()
                
                if st.button("🔄 Verify Meetup Code", key=f"verify_meet_btn_{p['id']}"):
                    if db.claim_and_verify_transaction(user_meet_tx, p['id'], "meetup"):
                        st.session_state.verified_meetups.add(p['id'])
                        st.rerun()
                    else:
                        st.error("Transaction code confirmation reference mismatch or unpaid entry registry.")
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
            has_paid_meet = conn.execute("SELECT 1 FROM transactions WHERE account_ref = ? AND type = 'meetup'", (account_string,)).fetchone()
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
                n_r = st.number_input("Rate (KES)", value=float(p['rate']), key=f"er_{p['id']}")
                up = st.file_uploader(f"Upload image for {p['name']}", type=['png', 'jpg'], key=f"up_{p['id']}")
                
                if st.button(f"Update {p['name']}", key=f"upd_{p['id']}"):
                    f_u = save_uploaded_file(up) if up else p['photo_url']
                    db.update_profile(p['id'], n_n, p['continent'], p['country'], p['bio'], n_r, f_u)
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
                new_rate = st.number_input("Rate (KES)", min_value=0.0, key="new_rate_in")
            with col2:
                new_coun = st.text_input("Country", key="new_coun_in")
                new_up = st.file_uploader("Upload Image", type=['png', 'jpg'], key="new_add_img")
            
            new_bio = st.text_area("Bio/Description", "Enter bio here...", key="new_bio_in")
            
            if st.button("Save New Client"):
                photo_url = save_uploaded_file(new_up) if new_up else "https://via.placeholder.com/150"
                db.add_single_profile(new_name, new_cont, new_coun, new_bio, new_rate, photo_url)
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
