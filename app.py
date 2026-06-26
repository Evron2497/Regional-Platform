import streamlit as st
import database as db
import os
import uuid
import base64
import requests  
import subprocess
import time

# --- EMBEDDED BACKEND BOOTSTRAPPER ---
if "backend_started" not in st.session_state:
    try:
        subprocess.Popen([
            "uvicorn", "main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        st.session_state.backend_started = True
        time.sleep(2) 
    except Exception as e:
        st.error(f"Internal wrapper failed to spin up background API gateway: {e}")

# --- PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="TECH-STAR")
db.init_db()

FASTAPI_BACKEND_URL = "http://127.0.0.1:8000" 

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

# --- CSS ---
# st.markdown("""
#     <style>
#     [data-testid="stHeader"] {
#         background-color: rgba(0, 0, 0, 0) !important;
#         height: 0px !important;
#     }
#     [data-testid="stSidebar"] { background-color: #FFC0CB !important; }
#     .navbar { background: linear-gradient(90deg, #ff69b4, #ff1493); padding: 15px; border-radius: 10px; color: white; }
#     .pay-box { background: #f9f9f9; padding: 20px; border: 2px dashed #ff1493; border-radius: 10px; margin-bottom: 15px; color: black; }
#     .rounded-img { border-radius: 50%; width: 110px; height: 110px; object-fit: cover; }
#     .welcome-banner { text-align: center; background-color: #64F58B; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
#     </style> 
# """, unsafe_allow_html=True)
# --- CSS ---
st.markdown("""
    <style>
    /* Hide everything in the top-right toolbar EXCEPT the three-dots main menu */
    [data-testid="stAppToolbar"] > :not([data-testid="stMainMenu"]) {
        display: none !important;
    }
    
    /* Hides the top right colored decoration badge shown in image_2921bb.png */
    [data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* Hides the default Streamlit footer branding */
    footer {
        visibility: hidden !important;
    }
    
    [data-testid="stSidebar"] { background-color: #FFC0CB !important; }
    .navbar { background: linear-gradient(90deg, #ff69b4, #ff1493); padding: 15px; border-radius: 10px; color: white; }
    .pay-box { background: #f9f9f9; padding: 20px; border: 2px dashed #ff1493; border-radius: 10px; margin-bottom: 15px; color: black; }
    .rounded-img { border-radius: 50%; width: 110px; height: 110px; object-fit: cover; }
    .welcome-banner { text-align: center; background-color: #64F58B; padding: 15px; border-radius: 10px; margin-bottom: 20px; }

    /* --- FLOATING LEFT BOTTOM SWIPE INDICATOR (image_2b5494.png) --- */
    .mobile-sidebar-hint {
        position: fixed;
        bottom: 20px;
        left: 20px; /* Locked to the left bottom side */
        background: linear-gradient(90deg, #ff1493, #ff69b4);
        color: white;
        padding: 12px 20px;
        border-radius: 30px;
        font-weight: bold;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.25);
        z-index: 999999;
        cursor: pointer;
        font-size: 14px;
        text-align: center;
        display: flex;
        align-items: center;
        gap: 8px;
        animation: pulseLeftHint 2s infinite;
        white-space: nowrap;
    }

    .chevron-icon {
        font-family: monospace;
        font-weight: 900;
        letter-spacing: -2px;
        font-size: 16px;
        opacity: 0.9;
    }

    @keyframes pulseLeftHint {
        0% { transform: scale(1); }
        50% { transform: scale(1.04); }
        100% { transform: scale(1); }
    }
    </style> 
""", unsafe_allow_html=True)

# Floating action trigger at the left bottom layout edge
st.markdown("""
    <div class="mobile-sidebar-hint" onclick="document.querySelector('[data-testid=\'stSidebarCollapsedControl\'] button')?.click();">
        <span class="chevron-icon">&gt;&gt;</span> Swipe / Open Options 🔑
    </div>
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
    st.markdown('<div class="navbar"><h2>MY FAVORITE HELLO ❤️</h2></div>', unsafe_allow_html=True)
with col3:
    st.markdown("📞 **Help:** +254769065385 <br> 📧 Support Center", unsafe_allow_html=True)

# --- WELCOME BANNER ---
st.markdown("""
    <div class="welcome-banner">
        <h2>🌍 Welcome to Global Dating Platform</h2>
        <p>Connect, Chat, and Build Meaningful Relationships Worldwide ❤️</p>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTENT PANEL ---
with st.sidebar:
    # --- NEW FEATURE: RESUME CLIENT SESSION VIA TRANSACTION ID ---
    st.header("🔑 Resume Session")
    st.markdown("If you already paid, enter your Transaction ID to quickly resume your secure chat line:")
    
    recovery_tx_id = st.text_input("Enter M-Pesa Transaction ID:", key="sidebar_recovery_input").strip().upper()
    if st.button("🚀 Restore My Chat Session", key="sidebar_recovery_btn"):
        if recovery_tx_id:
            # Look up transaction claims inside db to discover associated target profiles
            pending_list = db.get_pending_verifications()
            all_profiles = db.get_profiles()
            
            # Find matching metadata across transactions database
            found_profile_id = None
            conn = db.get_db()
            cursor = conn.cursor()
            try:
                # Query the manual transactions repository for a match
                cursor.execute("SELECT profile_id FROM manual_transactions WHERE transaction_id = ?", (recovery_tx_id,))
                row = cursor.fetchone()
                if row:
                    found_profile_id = row[0]
            except Exception:
                # Fallback sweep over the profile records lookup if transaction mapping table differs
                pass
            finally:
                conn.close()

            # If not explicitly matched via lookup query, check fallback structure from active profile arrays
            if not found_profile_id:
                for verification in pending_list:
                    if verification['transaction_id'] == recovery_tx_id:
                        found_profile_id = verification.get('profile_id')
                        break

            if found_profile_id:
                matched_profile = next((dict(prof) for prof in all_profiles if prof['id'] == found_profile_id), None)
                if matched_profile:
                    st.session_state.selected = matched_profile
                    # Seed verification tracking states to bypass gatekeeper roadblock
                    st.session_state[f"entered_tx_chat_{found_profile_id}"] = recovery_tx_id
                    st.success(f"Session Restored successfully for room: {matched_profile['name']}!")
                    st.rerun()
                else:
                    st.error("The profile associated with this verification code is no longer active.")
            else:
                st.error("Transaction Code reference not found or unlinked. Verify entries.")
        else:
            st.warning("Please specify an operational Transaction string.")

    st.divider()

    st.header("✨ Add Your Profile Display")
    st.markdown("""
    <div style="background-color: #ffffff; padding: 10px; border-radius: 5px; border: 1px solid #ff1493; color: black; font-size:13px; margin-bottom:10px;">
        📢 <b>Want your profile listed?</b> Fill registration metrics. Submission processing fee costs <b>KES 100.00</b> sent manually to <b>Paybill: 542542</b>, <b>Account No: 446040</b>.
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📝 Fill Submission Form (Client Side Only)", expanded=False):
        sub_name = st.text_input("Display Name", key="sub_name")
        sub_cont = st.selectbox("Continent Location", ["Africa", "America", "Europe", "Asia"], key="sub_cont")
        sub_coun = st.text_input("Country Location", key="sub_coun")
        sub_bio = st.text_area("Short Bio/Intro", key="sub_bio")
        sub_img = st.file_uploader("Upload Profile Image", type=['png', 'jpg'], key="sub_img")
        
        st.divider()
        sub_tx_id = st.text_input("Verification Step: Paste M-Pesa Code", key="sub_tx_verify").strip().upper()
        
        if st.button("🔓 Submit Profile for Verification", key="sub_verify_btn"):
            if not sub_tx_id or not sub_name:
                st.error("Please ensure your name is written and your transaction code is copied accurately.")
            else:
                saved_img_path = save_uploaded_file(sub_img) if sub_img else "https://via.placeholder.com/150"
                st.session_state[f"cache_form_{sub_tx_id}"] = {
                    "name": sub_name, "continent": sub_cont, "country": sub_coun, "bio": sub_bio, "photo_url": saved_img_path
                }
                db.submit_manual_transaction(sub_tx_id, 0, "446040-SUB", 100.0, "profile_submission")
                st.info("📨 Form data and reference code submitted to Admin panel queue.")
                st.rerun()

    st.divider()

    # --- ADMIN PRIVILEGED MANAGEMENT PANEL ---
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
        st.subheader("🔍 Pending Client Verifications")
        
        pending_list = db.get_pending_verifications()
        if not pending_list:
            st.write("No incoming verification claims.")
        else:
            for item in pending_list:
                st.markdown(f"""
                📌 **Type:** `{item['type'].upper()}` <br>
                👤 **Target Client:** {item['profile_name'] if item['profile_name'] else 'New Submission'}<br>
                💵 **Code Claimed:** `{item['transaction_id']}`<br>
                💰 **Amount Paid:** KES {item['amount']:.2f}
                """, unsafe_allow_html=True)
                
                if item['type'] == "profile_submission":
                    form_cache_key = f"cache_form_{item['transaction_id']}"
                    if form_cache_key in st.session_state:
                        st.info("📋 Assign Profile Pricing parameters below before approving:")
                        admin_chat_rate = st.number_input(f"Assign Chat Rate (KES) for {st.session_state[form_cache_key]['name']}", min_value=0.0, step=10.0, key=f"adm_ch_{item['transaction_id']}")
                        admin_meet_rate = st.number_input(f"Assign Meetup Rate (KES) for {st.session_state[form_cache_key]['name']}", min_value=0.0, step=50.0, key=f"adm_mt_{item['transaction_id']}")
                        
                        if st.button(f"Approve, Rate & Publish {item['transaction_id']}", key=f"approve_{item['transaction_id']}"):
                            db.admin_approve_transaction(item['transaction_id'])
                            form_data = st.session_state[form_cache_key]
                            
                            db.add_single_profile(
                                name=form_data["name"],
                                continent=form_data["continent"],
                                country=form_data["country"],
                                bio=form_data["bio"],
                                chat_rate=admin_chat_rate,
                                meetup_rate=admin_meet_rate,
                                photo_url=form_data["photo_url"],
                                status='browsing'
                            )
                            del st.session_state[form_cache_key]
                            st.success(f"Profile published immediately with your assigned rates!")
                            st.rerun()
                    else:
                        st.warning("Form cached dataset missing or cleared.")
                else:
                    if st.button(f"Approve & Unlock {item['transaction_id']}", key=f"approve_{item['transaction_id']}"):
                        db.admin_approve_transaction(item['transaction_id'])
                        
                        if item['type'] in ("chat", "meetup"):
                            conn = db.get_db()
                            conn.execute("UPDATE profiles SET status = 'booked' WHERE id = ?", (item['profile_id'],))
                            conn.commit()
                            conn.close()
                            
                            if item['type'] == "meetup":
                                db.approve_meetup(item['profile_id'])
                        
                        st.success(f"Transaction code {item['transaction_id']} approved!")
                        st.rerun()
                st.divider()

        # --- ADD NEW CLIENT MANUALLY ---
        st.subheader("➕ Create Client Account")
        with st.expander("Manually Provision New Client Profile", expanded=False):
            new_name = st.text_input("Name", key="new_name_in")
            col1, col2 = st.columns(2)
            with col1:
                new_cont = st.selectbox("Continent", ["Africa", "America", "Europe", "Asia"], key="new_cont_in")
                new_chat_rate = st.number_input("Chat Rate (KES)", min_value=0.0, key="new_ch_rate_in")
            with col2:
                new_coun = st.text_input("Country", key="new_coun_in")
                new_meet_rate = st.number_input("Meetup Rate (KES)", min_value=0.0, key="new_mt_rate_in")
            
            new_up = st.file_uploader("Upload Image Asset", type=['png', 'jpg'], key="new_add_img")
            new_bio = st.text_area("Bio/Description Parameters", "Enter bio here...", key="new_bio_in")
            
            if st.button("Save New Client", key="save_manual_client_btn"):
                if not new_name:
                    st.error("A profile must have an assigned name label.")
                else:
                    photo_url = save_uploaded_file(new_up) if new_up else "https://via.placeholder.com/150"
                    db.add_single_profile(new_name, new_cont, new_coun, new_bio, new_chat_rate, new_meet_rate, photo_url, status='browsing')
                    st.success(f"Added {new_name} successfully!")
                    st.rerun()

        st.divider()
        st.subheader("📋 Client Directory")
        all_profiles = db.get_profiles()
        for directory_p in all_profiles:
            with st.expander(f"👤 {directory_p['name']} (ID: {directory_p['id']}) - Status: {directory_p['status']}"):
                n_n = st.text_input("Name", value=directory_p['name'], key=f"en_{directory_p['id']}")
                n_cr = st.number_input("Chat Rate (KES)", value=float(directory_p['chat_rate']), key=f"ecr_{directory_p['id']}")
                n_mr = st.number_input("Meetup Rate (KES)", value=float(directory_p['meetup_rate']), key=f"emr_{directory_p['id']}")
                up = st.file_uploader(f"Upload image for {directory_p['name']}", type=['png', 'jpg'], key=f"up_{directory_p['id']}")
                
                if st.button(f"Update {directory_p['name']}", key=f"upd_{directory_p['id']}"):
                    f_u = save_uploaded_file(up) if up else directory_p['photo_url']
                    db.update_profile(directory_p['id'], n_n, directory_p['continent'], directory_p['country'], directory_p['bio'], n_cr, n_mr, f_u)
                    st.success(f"Updated {directory_p['name']}!")
                    st.rerun()
                
                if st.button(f"Delete {directory_p['name']}", key=f"del_{directory_p['id']}"):
                    db.delete_profile(directory_p['id'])
                    st.success(f"Deleted {directory_p['name']}!")
                    st.rerun()

        # --- ADMIN LIVE INTERVENTION OPERATOR CHAT MATRIX ---
        st.divider()
        st.subheader("🗣️ Admin Live Chat Panel")
        
        chat_active_profiles = db.get_profiles()
        room_choices = {cp['id']: cp['name'] for cp in chat_active_profiles}
        
        if room_choices:
            chosen_room_id = st.selectbox("Monitor Chat Room:", options=list(room_choices.keys()), format_func=lambda x: room_choices[x], key="admin_room_picker")
            
            st.caption(f"Timeline Log: {room_choices[chosen_room_id]}")
            with st.container(height=180):
                room_history = db.get_chat_history(chosen_room_id)
                for r_msg in room_history:
                    st.markdown(f"**{r_msg['sender']}:** {r_msg['message']}")
            
            admin_identity = st.radio("Send Message As:", [room_choices[chosen_room_id], "System Admin"], horizontal=True, key="admin_identity_choice")
            admin_response_msg = st.text_input("Type response message:", key="admin_text_input")
            
            if st.button("✉️ Dispatch Message", key="admin_dispatch_btn"):
                if admin_response_msg.strip():
                    db.save_chat_message(chosen_room_id, admin_identity, admin_response_msg.strip())
                    st.rerun()

# --- MAIN APP LOGIC ---
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
                
                st.image(profile_dict['photo_url'], use_container_width=True)
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
    st.title(f"🔒 Private Session Locked to My Chat: {p['name']}")
    if st.button("⬅️ Back to Directory"):
        del st.session_state.selected
        st.rerun()
    
    # 1. GATEKEEPER: CHAT TRANSACTION VALIDATION
    chat_input_tracker_key = f"entered_tx_chat_{p['id']}"
    tracked_chat_code = st.session_state.get(chat_input_tracker_key, "").strip().upper()
    
    is_chat_unlocked = db.claim_and_verify_transaction(tracked_chat_code, p['id'], "chat") if tracked_chat_code else False

    if not is_chat_unlocked:
        st.markdown(f"""
        <div class="pay-box">
            <h3>💰 Lipa Na M-Pesa Payment Instructions</h3>
            <p>To unlock your direct secure chat line, make a manual payment using the billing details below as Business No-542542, Account No-446040 . Don't include CHAR:</p>
            <hr>
            <b>1. Go to M-PESA Menu</b><br>
            <b>2. Select Lipa Na M-PESA -> Paybill</b><br>
            <b>3. Enter Business No:</b> <span style="color:#ff1493; font-weight:bold;">542542</span> (Lipa Na IMBANK)<br>
            <b>4. Enter Account No:</b> <span style="color:#ff1493; font-weight:bold;">446040     CHAR{p['id']}</span><br>
            <b>5. Enter Amount:</b> <span style="color:#ff1493; font-weight:bold;">KES {p["chat_rate"]:.2f}</span><br>
            <hr>
            <p>Once paid, paste your official M-Pesa Transaction ID below for instant admin evaluation.</p>
        </div>
        """, unsafe_allow_html=True)
        
        fallback_tx_id = st.text_input("Verification Step: Paste M-Pesa Transaction ID (e.g., SFT712XYZ0):", key=f"tx_chat_{p['id']}").strip().upper()
        
        if st.button("🔓 Submit Code to Admin for Verification", key=f"verify_btn_{p['id']}"):
            if fallback_tx_id:
                db.submit_manual_transaction(fallback_tx_id, p['id'], f"446040-CHA{p['id']}", p['chat_rate'], "chat")
                st.session_state[chat_input_tracker_key] = fallback_tx_id
                st.rerun()
            else:
                st.warning("Please paste a valid transaction ID before submitting.")
        
        if tracked_chat_code:
            st.warning("⏳ Access Status: Awaiting Admin Approval. Click refresh below to update your line link status.")
            if st.button("🔄 Refresh Status Window"):
                st.rerun()
        st.stop()

    # 2. CHAT & MEETUP FLOW (PERSISTENT SECURED DATABASE ROOM)
    is_meetup_approved = db.check_meetup_status(p['id'])
    
    if is_meetup_approved:
        st.success("✅ Meetup Approved! Target logistical coordinates sent.")
    
    st.subheader(f"💬 Live Secured Chat Room: Unlocked Session with {p['name']}")
    
    # Render the persistent database timeline container
    chat_container = st.container(height=400)
    with chat_container:
        history = db.get_chat_history(p['id'])
        if not history:
            st.caption("✨ Line established securely. Start typing your message below...")
        else:
            for msg in history:
                role = "user" if msg['sender'] == "Client" else "assistant"
                with st.chat_message(role):
                    st.markdown(f"**{msg['sender']}:** {msg['message']}")
    
    # Standard Client Input Area
    client_msg = st.chat_input("Type your message here...", key=f"chat_input_client_{p['id']}")
    if client_msg:
        db.save_chat_message(p['id'], "Client", client_msg)
        st.rerun()
        
    # --- MEETUP BARRIER ---
    total_messages = len(db.get_chat_history(p['id']))
    st.caption(f"Progress Metric: {total_messages}/10 interactions recorded.")
    
    if total_messages >= 10:
        meet_input_tracker_key = f"entered_tx_meet_{p['id']}"
        tracked_meet_code = st.session_state.get(meet_input_tracker_key, "").strip().upper()
        
        is_meet_unlocked = db.claim_and_verify_transaction(tracked_meet_code, p['id'], "meetup") if tracked_meet_code else False
        
        if not is_meet_unlocked:
            st.markdown(f"""
            <div class="pay-box">
                <h3>🤝 Goal Unlocked: Meetup Routing Account Details</h3>
                <p>To authorize standard meetup routing arrangements, settle the setup invoice manually:</p>
                <hr>
                <b>1. Paybill Business No:</b> <span style="color:#ff1493; font-weight:bold;">542542</span><br>
                <b>2. Account Reference Target:</b> <span style="color:#ff1493; font-weight:bold;">446040-MEE{p['id']}</span><br>
                <b>3. Required Amount:</b> <span style="color:#ff1493; font-weight:bold;">KES {p['meetup_rate']:.2f}</span><br>
                <hr>
                <p>Paste your receipt's unique verification code below to ping administrative oversight logs.</p>
            </div>
            """, unsafe_allow_html=True)
            
            fallback_meet_tx = st.text_input("Enter Meetup Payment Transaction ID to unlock:", key=f"tx_meet_{p['id']}").strip().upper()
            
            if st.button("🔄 Submit Meetup Code to Admin", key=f"verify_meet_btn_{p['id']}"):
                if fallback_meet_tx:
                    db.submit_manual_transaction(fallback_meet_tx, p['id'], f"446040-MEE{p['id']}", p['meetup_rate'], "meetup")
                    st.session_state[meet_input_tracker_key] = fallback_meet_tx
                    st.rerun()
                else:
                    st.warning("Please specify an operational Transaction reference string.")
            
            if tracked_meet_code:
                st.warning("⏳ Awaiting Administrative Approval for physical routing activation parameters.")
                if st.button("🔄 Check Authorization Status"):
                    st.rerun()
            st.stop()

# --- FOOTER ---
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: grey; font-size: 12px; margin-top: 50px;">
    &copy; 2026 TECH-STAR Regional Dating Platform. All rights reserved. <br>
    Privacy Policy | Terms of Service | <a href="mailto:support@techstar.com">Contact Support</a>
    </div>
""", unsafe_allow_html=True)
