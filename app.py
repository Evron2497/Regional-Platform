# import streamlit as st
# import database as db
# import os
# import uuid
# import base64
# import requests  
# import subprocess
# import time

# # --- EMBEDDED BACKEND BOOTSTRAPPER ---
# if "backend_started" not in st.session_state:
#      try:
#          subprocess.Popen([
#              "uvicorn", "main:app", 
#              "--host", "127.0.0.1", 
#              "--port", "8000"
#          ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#          st.session_state.backend_started = True
#          time.sleep(2) 
#      except Exception as e:
#          st.error(f"Internal wrapper failed to spin up background API gateway: {e}")

# # --- PAGE CONFIG ---
# st.set_page_config(layout="wide", page_title="TECH-STAR")
# db.init_db()

# FASTAPI_BACKEND_URL = "http://127.0.0.1:8000" 

# # --- FUNCTION DEFINITIONS ---
# def save_uploaded_file(uploaded_file):
#      if not os.path.exists("uploads"): 
#          os.makedirs("uploads")
#      file_path = os.path.join("uploads", f"{uuid.uuid4()}_{uploaded_file.name}")
#      with open(file_path, "wb") as f: 
#          f.write(uploaded_file.getbuffer())
#      return file_path

# # --- STATE ---
# if "admin_logged_in" not in st.session_state: 
#      st.session_state.admin_logged_in = False

# # --- CSS ---
# st.markdown("""
#      <style>
#      [data-testid="stAppToolbar"] > :not([data-testid="stMainMenu"]) {
#          display: none !important;
#      }
    
#      [data-testid="stDecoration"] {
#          display: none !important;
#      }
    
#      footer {
#          visibility: hidden !important;
#      }
    
#      [data-testid="stSidebar"] { background-color: #FFC0CB !important; }
#      .navbar { background: linear-gradient(90deg, #ff69b4, #ff1493); padding: 15px; border-radius: 10px; color: white; }
#      .pay-box { background: #f9f9f9; padding: 20px; border: 2px dashed #ff1493; border-radius: 10px; margin-bottom: 15px; color: black; }
#      .rounded-img { border-radius: 50%; width: 110px; height: 110px; object-fit: cover; }
#      .welcome-banner { text-align: center; background-color: #64F58B; padding: 15px; border-radius: 10px; margin-bottom: 20px; }

#      .mobile-sidebar-hint {
#          position: fixed;
#          bottom: 20px;
#          left: 20px;
#          background: linear-gradient(90deg, #ff1493, #ff69b4);
#          color: white;
#          padding: 12px 20px;
#          border-radius: 30px;
#          font-weight: bold;
#          box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.25);
#          z-index: 999999;
#          cursor: pointer;
#          font-size: 14px;
#          text-align: center;
#          display: flex;
#          align-items: center;
#          gap: 8px;
#          animation: pulseLeftHint 2s infinite;
#          white-space: nowrap;
#      }

#      .chevron-icon {
#          font-family: monospace;
#          font-weight: 900;
#          letter-spacing: -2px;
#          font-size: 16px;
#          opacity: 0.9;
#      }

#      @keyframes pulseLeftHint {
#          0% { transform: scale(1); }
#          50% { transform: scale(1.04); }
#          100% { transform: scale(1); }
#      }
#      </style> 
# """, unsafe_allow_html=True)

# st.markdown("""
#      <div class="mobile-sidebar-hint" onclick="document.querySelector('[data-testid=\'stSidebarCollapsedControl\'] button')?.click();">
#          <span class="chevron-icon">&gt;&gt;</span> Swipe / Open Options 🔑
#      </div>
# """, unsafe_allow_html=True)

# # --- TOP NAVBAR ---
# col1, col2, col3 = st.columns([1, 4, 2])
# with col1:
#      img_path = "LOVE-IS-REAL.jpg"
#      if os.path.exists(img_path):
#          st.markdown(f'<div style="overflow:hidden; border-radius:50%; width:90px; height:90px;"><img src="data:image/jpeg;base64,{base64.b64encode(open(img_path, "rb").read()).decode()}" width="90" height="90" style="object-fit:cover;"></div>', unsafe_allow_html=True)
#      else:
#          st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=90)
# with col2:
#      st.markdown('<div class="navbar"><h2>MY FAVORITE HELLO ❤️</h2></div>', unsafe_allow_html=True)
# with col3:
#      st.markdown("📞 **Help:** +254769065385 <br> 📧 Support Center", unsafe_allow_html=True)

# # --- WELCOME BANNER ---
# st.markdown("""
#      <div class="welcome-banner">
#          <h2>🌍 Welcome to Global Dating Platform</h2>
#          <p>Connect, Chat, and Build Meaningful Relationships Worldwide ❤️</p>
#      </div>
# """, unsafe_allow_html=True)

# # --- SIDEBAR CONTENT PANEL ---
# with st.sidebar:
#      st.header("🔑 Resume Session")
#      st.markdown("Enter your paid Transaction ID to recover your corresponding setup environment (Chat vs Meetup):")
    
#      recovery_tx_id = st.text_input("Enter M-Pesa Transaction ID:", key="sidebar_recovery_input").strip().upper()
#      if st.button("🚀 Restore My Chat Session", key="sidebar_recovery_btn"):
#          if recovery_tx_id:
#              all_profiles = db.get_profiles()
#              found_profile_id = None
#              transaction_type = "chat"
             
#              lookup = db.get_transaction_session_lookup(recovery_tx_id)
#              if lookup:
#                  found_profile_id = lookup['profile_id']
#                  transaction_type = lookup['type']
#              else:
#                  pending_list = db.get_pending_verifications()
#                  for verification in pending_list:
#                      if verification['transaction_id'] == recovery_tx_id:
#                          found_profile_id = verification.get('profile_id')
#                          transaction_type = verification.get('type', 'chat')
#                          break

#              if found_profile_id:
#                  matched_profile = next((dict(prof) for prof in all_profiles if prof['id'] == found_profile_id), None)
#                  if matched_profile:
#                      st.session_state.selected = matched_profile
#                      st.session_state[f"entered_tx_{transaction_type}_{found_profile_id}"] = recovery_tx_id
#                      st.success(f"Session Restored successfully for {matched_profile['name']}!")
#                      st.rerun()
#                  else:
#                      st.error("The profile associated with this code is no longer active.")
#              else:
#                  st.error("Transaction Code reference not found or unlinked. Verify entries.")
#          else:
#              st.warning("Please specify an operational Transaction string.")

#      st.divider()

#      st.header("✨ Add Your Profile Display")
#      st.markdown("""
#      <div style="background-color: #ffffff; padding: 10px; border-radius: 5px; border: 1px solid #ff1493; color: black; font-size:13px; margin-bottom:10px;">
#            📢 <b>Want your profile listed?</b> Fill registration metrics. Submission processing fee costs <b>KES 200.00</b> sent manually to <b>Paybill: 542542</b>, <b>Account No: 446040</b>.
#      </div>
#      """, unsafe_allow_html=True)
    
#      with st.expander("📝 Fill Submission Form (Client Side Only)", expanded=False):
#          sub_name = st.text_input("Display Name", key="sub_name")
#          sub_cont = st.selectbox("Continent Location", ["Africa", "America", "Europe", "Asia"], key="sub_cont")
#          sub_coun = st.text_input("Country Location", key="sub_coun")
#          sub_bio = st.text_area("Short Bio/Intro", key="sub_bio")
#          sub_img = st.file_uploader("Upload Profile Image", type=['png', 'jpg'], key="sub_img")
        
#          st.divider()
#          sub_tx_id = st.text_input("Verification Step: Paste M-Pesa Code", key="sub_tx_verify").strip().upper()
        
#          if st.button("🔓 Submit Profile for Verification", key="sub_verify_btn"):
#              if not sub_tx_id or not sub_name:
#                  st.error("Please ensure your name is written and your transaction code is copied accurately.")
#              else:
#                  saved_img_path = save_uploaded_file(sub_img) if sub_img else "https://via.placeholder.com/150"
#                  st.session_state[f"cache_form_{sub_tx_id}"] = {
#                      "name": sub_name, "continent": sub_cont, "country": sub_coun, "bio": sub_bio, "photo_url": saved_img_path
#                  }
#                  db.submit_manual_transaction(sub_tx_id, 0, "446040-SUB", 200.0, "profile_submission")
#                  st.info("📨 Form data and reference code submitted to Admin panel queue.")
#                  st.rerun()

#      st.divider()

#      # --- ADMIN PRIVILEGED MANAGEMENT PANEL ---
#      st.header("Admin Management")
#      if not st.session_state.admin_logged_in:
#          pwd = st.text_input("Password", type="password", key="admin_pwd_entry")
#          if st.button("Login"):
#              if pwd == st.secrets["ADMIN_PASSWORD"]:
#                  st.session_state.admin_logged_in = True
#                  st.rerun()
#              else:
#                  st.error("Incorrect Password")
#      else:
#          if st.button("Logout"):
#              st.session_state.admin_logged_in = False
#              st.rerun()

#          st.divider()
#          st.subheader("🔍 Pending Client Verifications")
        
#          pending_list = db.get_pending_verifications()
#          if not pending_list:
#              st.write("No incoming verification claims.")
#          else:
#              for item in pending_list:
#                  st.markdown(f"""
#                  📌 **Type:** `{item['type'].upper()}` <br>
#                  👤 **Target Client:** {item['profile_name'] if item['profile_name'] else 'New Submission'}<br>
#                  💵 **Code Claimed:** `{item['transaction_id']}`<br>
#                  💰 **Amount Paid:** KES {item['amount']:.2f}
#                  """, unsafe_allow_html=True)
                
#                  if item['type'] == "profile_submission":
#                      form_cache_key = f"cache_form_{item['transaction_id']}"
#                      if form_cache_key in st.session_state:
#                          st.info("📋 Assign Profile Pricing parameters below before approving:")
#                          admin_chat_rate = st.number_input(f"Assign Chat Rate (KES) for {st.session_state[form_cache_key]['name']}", min_value=0.0, step=10.0, key=f"adm_ch_{item['transaction_id']}")
#                          admin_meet_rate = st.number_input(f"Assign Meetup Rate (KES) for {st.session_state[form_cache_key]['name']}", min_value=0.0, step=50.0, key=f"adm_mt_{item['transaction_id']}")
                        
#                          if st.button(f"Approve, Rate & Publish {item['transaction_id']}", key=f"approve_{item['transaction_id']}"):
#                              db.admin_approve_transaction(item['transaction_id'])
#                              form_data = st.session_state[form_cache_key]
                            
#                              db.add_single_profile(
#                                  name=form_data["name"],
#                                  continent=form_data["continent"],
#                                  country=form_data["country"],
#                                  bio=form_data["bio"],
#                                  chat_rate=admin_chat_rate,
#                                  meetup_rate=admin_meet_rate,
#                                  photo_url=form_data["photo_url"],
#                                  status='browsing'
#                              )
#                              del st.session_state[form_cache_key]
#                              st.success(f"Profile published immediately with your assigned rates!")
#                              st.rerun()
#                      else:
#                          st.warning("Form cached dataset missing or cleared.")
#                  else:
#                      if st.button(f"Approve & Unlock {item['transaction_id']}", key=f"approve_{item['transaction_id']}"):
#                          db.admin_approve_transaction(item['transaction_id'])
                        
#                          if item['type'] in ("chat", "meetup"):
#                              conn = db.get_db()
#                              conn.execute("UPDATE profiles SET status = 'booked' WHERE id = ?", (item['profile_id'],))
#                              conn.commit()
#                              conn.close()
                            
#                              if item['type'] == "meetup":
#                                  db.approve_meetup(item['profile_id'])
                        
#                          st.success(f"Transaction code {item['transaction_id']} approved!")
#                          st.rerun()
#                  st.divider()

#          # --- ADD NEW CLIENT MANUALLY ---
#          st.subheader("➕ Create Client Account")
#          with st.expander("Manually Provision New Client Profile", expanded=False):
#              new_name = st.text_input("Name", key="new_name_in")
#              col1, col2 = st.columns(2)
#              with col1:
#                  new_cont = st.selectbox("Continent", ["Africa", "America", "Europe", "Asia"], key="new_cont_in")
#                  new_chat_rate = st.number_input("Chat Rate (KES)", min_value=0.0, key="new_ch_rate_in")
#              with col2:
#                  new_coun = st.text_input("Country", key="new_coun_in")
#                  new_meet_rate = st.number_input("Meetup Rate (KES)", min_value=0.0, key="new_mt_rate_in")
            
#              new_up = st.file_uploader("Upload Image Asset", type=['png', 'jpg'], key="new_add_img")
#              new_bio = st.text_area("Bio/Description Parameters", "Enter bio here...", key="new_bio_in")
            
#              if st.button("Save New Client", key="save_manual_client_btn"):
#                  if not new_name:
#                      st.error("A profile must have an assigned name label.")
#                  else:
#                      photo_url = save_uploaded_file(new_up) if new_up else "https://via.placeholder.com/150"
#                      db.add_single_profile(new_name, new_cont, new_coun, new_bio, new_chat_rate, new_meet_rate, photo_url, status='browsing')
#                      st.success(f"Added {new_name} successfully!")
#                      st.rerun()

#          st.divider()
#          st.subheader("📋 Client Directory")
#          all_profiles = db.get_profiles()
#          for directory_p in all_profiles:
#              with st.expander(f"👤 {directory_p['name']} (ID: {directory_p['id']}) - Status: {directory_p['status']}"):
#                  n_n = st.text_input("Name", value=directory_p['name'], key=f"en_{directory_p['id']}")
#                  n_cr = st.number_input("Chat Rate (KES)", value=float(directory_p['chat_rate']), key=f"ecr_{directory_p['id']}")
#                  n_mr = st.number_input("Meetup Rate (KES)", value=float(directory_p['meetup_rate']), key=f"emr_{directory_p['id']}")
#                  up = st.file_uploader(f"Upload image for {directory_p['name']}", type=['png', 'jpg'], key=f"up_{directory_p['id']}")
                
#                  if st.button(f"Update {directory_p['name']}", key=f"upd_{directory_p['id']}"):
#                      f_u = save_uploaded_file(up) if up else directory_p['photo_url']
#                      db.update_profile(directory_p['id'], n_n, directory_p['continent'], directory_p['country'], directory_p['bio'], n_cr, n_mr, f_u)
#                      st.success(f"Updated {directory_p['name']}!")
#                      st.rerun()
                
#                  if st.button(f"Delete {directory_p['name']}", key=f"del_{directory_p['id']}"):
#                      db.delete_profile(directory_p['id'])
#                      st.success(f"Deleted {directory_p['name']}!")
#                      st.rerun()

#          # --- ADMIN LIVE INTERVENTION OPERATOR CHAT MATRIX ---
#          st.divider()
#          st.subheader("🗣️ Admin Live Chat Panel")
        
#          chat_active_profiles = db.get_profiles()
#          room_choices = {cp['id']: cp['name'] for cp in chat_active_profiles}
        
#          if room_choices:
#              chosen_room_id = st.selectbox("Monitor Chat Room:", options=list(room_choices.keys()), format_func=lambda x: room_choices[x], key="admin_room_picker")
            
#              st.caption(f"Timeline Log: {room_choices[chosen_room_id]}")
#              with st.container(height=180):
#                  room_history = db.get_chat_history(chosen_room_id)
#                  for r_msg in room_history:
#                      st.markdown(f"**{r_msg['sender']}:** {r_msg['message']}")
            
#              admin_identity = st.radio("Send Message As:", [room_choices[chosen_room_id], "System Admin"], horizontal=True, key="admin_identity_choice")
#              admin_response_msg = st.text_input("Type response message:", key="admin_text_input")
            
#              if st.button("✉️ Dispatch Message", key="admin_dispatch_btn"):
#                  if admin_response_msg.strip():
#                      db.save_chat_message(chosen_room_id, admin_identity, admin_response_msg.strip())
#                      st.rerun()

# # --- MAIN APP LOGIC ---
# # --- MARKETPLACE ---
# profiles = db.get_available_profiles()

# if not profiles:
#      st.info("✨ No profiles currently active. Please check back shortly!")
# else:
#      cols = st.columns(3) 
#      for idx, p in enumerate(profiles):
#           with cols[idx % 3]:
#                profile_dict = dict(p) if not isinstance(p, dict) else p
              
#                chat_rate = profile_dict.get('chat_rate', 0.0)
#                bio_text = profile_dict.get('bio', 'No bio available.')
              
#                st.image(profile_dict['photo_url'], use_container_width=True)
#                st.write(f"### {profile_dict['name']}")
#                st.write(f"📍 **Location:** {profile_dict['country']}, {profile_dict['continent']}")
#                st.write(f"💬 **Chat Rate:** KES {chat_rate:.2f}")
#                st.write(f"📝 **Bio:** {bio_text}") # <-- Added bio display here
              
#                if st.button(f"Connect with {profile_dict['name']}", key=f"btn_{profile_dict['id']}"):
#                     st.session_state.selected = profile_dict
#                     st.rerun()
# else:
#      # --- PRIVATE SESSION ---
#      p = st.session_state.selected
#      st.title(f"🔒 Private Session Locked to My Chat: {p['name']}")
#      if st.button("⬅️ Back to Directory"):
#          del st.session_state.selected
#          st.rerun()
    
#      # 1. GATEKEEPER: CHAT TRANSACTION VALIDATION
#      chat_input_tracker_key = f"entered_tx_chat_{p['id']}"
#      tracked_chat_code = st.session_state.get(chat_input_tracker_key, "").strip().upper()
    
#      is_chat_unlocked = db.claim_and_verify_transaction(tracked_chat_code, p['id'], "chat") if tracked_chat_code else False

#      if not is_chat_unlocked:
#          st.markdown(f"""
#          <div class="pay-box">
#                 <h3>💰 Lipa Na M-Pesa Payment Instructions</h3>
#                 <p>To unlock your direct secure chat line, make a manual payment using the billing details below as Business No-542542, Account No-446040:</p>
#                 <hr>
#                 <b>1. Go to M-PESA Menu</b><br>
#                 <b>2. Select Lipa Na M-PESA -> Paybill</b><br>
#                 <b>3. Enter Business No:</b> <span style="color:#ff1493; font-weight:bold;">542542</span> (Lipa Na IMBANK)<br>
#                 <b>4. Enter Account No:</b> <span style="color:#ff1493; font-weight:bold;">446040      CHAR{p['id']}</span><br>
#                 <b>5. Enter Amount:</b> <span style="color:#ff1493; font-weight:bold;">KES {p["chat_rate"]:.2f}</span><br>
#                 <hr>
#                 <p>Once paid, paste your official M-Pesa Transaction ID below for instant admin evaluation.</p>
#          </div>
#          """, unsafe_allow_html=True)
        
#          fallback_tx_id = st.text_input("Verification Step: Paste M-Pesa Transaction ID:", key=f"tx_chat_{p['id']}").strip().upper()
        
#          if st.button("🔓 Submit Code to Admin for Verification", key=f"verify_btn_{p['id']}"):
#              if fallback_tx_id:
#                  db.submit_manual_transaction(fallback_tx_id, p['id'], f"446040-CHA{p['id']}", p['chat_rate'], "chat")
#                  st.session_state[chat_input_tracker_key] = fallback_tx_id
#                  st.rerun()
#              else:
#                  st.warning("Please paste a valid transaction ID before submitting.")
        
#          if tracked_chat_code:
#              st.warning("⏳ Access Status: Awaiting Admin Approval. Click refresh below to update your line link status.")
#              if st.button("🔄 Refresh Status Window"):
#                  st.rerun()
#          st.stop()

#      # 2. CHAT FLOW
#      is_meetup_approved = db.check_meetup_status(p['id'])
    
#      if is_meetup_approved:
#          st.success("✅ Meetup Approved! Target logistical coordinates sent.")
    
#      st.subheader(f"💬 Live Secured Chat Room: Unlocked Session with {p['name']}")
    
#      chat_container = st.container(height=400)
#      with chat_container:
#          history = db.get_chat_history(p['id'])
#          if not history:
#              st.caption("✨ Line established securely. Start typing your message below...")
#          else:
#              for msg in history:
#                  role = "user" if msg['sender'] == "Client" else "assistant"
#                  with st.chat_message(role):
#                      st.markdown(f"**{msg['sender']}:** {msg['message']}")
    
#      client_msg = st.chat_input("Type your message here...", key=f"chat_input_client_{p['id']}")
#      if client_msg:
#          db.save_chat_message(p['id'], "Client", client_msg)
#          st.rerun()
        
#      # --- MEETUP BARRIER ---
#      total_messages = len(db.get_chat_history(p['id']))
#      st.caption(f"Progress Metric: {total_messages}/10 interactions recorded.")
    
#      if total_messages >= 10:
#          meet_input_tracker_key = f"entered_tx_meet_{p['id']}"
#          tracked_meet_code = st.session_state.get(meet_input_tracker_key, "").strip().upper()
        
#          is_meet_unlocked = db.claim_and_verify_transaction(tracked_meet_code, p['id'], "meetup") if tracked_meet_code else False
        
#          if not is_meet_unlocked:
#              # Fetch meetup rate dynamically if available
#              rates = db.get_single_profile_rates(p['id'])
#              m_rate = rates['meetup_rate'] if rates else 0.0
#              st.markdown(f"""
#              <div class="pay-box">
#                     <h3>🤝 Goal Unlocked: Meetup Routing Account Details</h3>
#                     <p>To authorize standard meetup routing arrangements, settle the setup invoice manually:</p>
#                     <hr>
#                     <b>1. Paybill Business No:</b> <span style="color:#ff1493; font-weight:bold;">542542</span><br>
#                     <b>2. Account Reference Target:</b> <span style="color:#ff1493; font-weight:bold;">446040-MEE{p['id']}</span><br>
#                     <b>3. Required Amount:</b> <span style="color:#ff1493; font-weight:bold;">KES {m_rate:.2f}</span><br>
#                     <hr>
#                     <p>Paste your receipt's unique verification code below to ping administrative oversight logs.</p>
#              </div>
#              """, unsafe_allow_html=True)
            
#              fallback_meet_tx = st.text_input("Enter Meetup Payment Transaction ID to unlock:", key=f"tx_meet_{p['id']}").strip().upper()
            
#              if st.button("🔄 Submit Meetup Code to Admin", key=f"verify_meet_btn_{p['id']}"):
#                  if fallback_meet_tx:
#                      db.submit_manual_transaction(fallback_meet_tx, p['id'], f"446040-MEE{p['id']}", m_rate, "meetup")
#                      st.session_state[meet_input_tracker_key] = fallback_meet_tx
#                      st.rerun()
#                  else:
#                      st.warning("Please specify an operational Transaction reference string.")
            
#              if tracked_meet_code:
#                  st.warning("⏳ Awaiting Administrative Approval for physical routing activation parameters.")
#                  if st.button("🔄 Check Authorization Status"):
#                      st.rerun()
#              st.stop()

# # --- FOOTER ---
# st.markdown("---")
# st.markdown("""
#      <div style="text-align: center; color: grey; font-size: 12px; margin-top: 50px;">
#      &copy; 2026 TECH-STAR Regional Dating Platform. All rights reserved. <br>
#      Privacy Policy | Terms of Service | <a href="mailto:support@techstar.com">Contact Support</a>
#      </div>
# """, unsafe_allow_html=True)





import streamlit as st
import base64
import os
import datetime
import io

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(
    page_title="Longisa County Referral Hospital", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- LOAD LOCAL SVG COAT OF ARMS ---
def get_local_svg_base64(filepath):
    clean_path = os.path.normpath(filepath.replace("file:///", ""))
    try:
        if os.path.exists(clean_path):
            with open(clean_path, "rb") as f:
                svg_data = f.read()
            encoded = base64.b64encode(svg_data).decode("utf-8")
            return f"data:image/svg+xml;base64,{encoded}"
    except Exception:
        pass
    return "https://cdn-icons-png.flaticon.com/512/3063/3063189.png"

# Use exact local path
local_logo_path = r"C:\Users\Hi\Downloads\government-of-kenya-emblem-gok-vector-logo-seeklogo\government-of-kenya-emblem-gok-seeklogo.svg"
logo_base64 = get_local_svg_base64(local_logo_path)

# Default Fallbacks
DEFAULT_NEWS_IMG = "https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&q=80&w=600"
DEFAULT_DOC_IMG = "https://img.freepik.com/free-vector/doctor-character-background_1270-84.jpg"

# --- CUSTOM GLOBAL HEALTH THEME CSS ---
st.markdown("""
    <style>
    /* Prevent hiding the header entirely so the native sidebar toggle button remains visible */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
        z-index: 999;
    }
    
    /* Ensure the sidebar toggle button itself is styled clearly */
    [data-testid="collapsedControl"] {
        color: #004a99 !important;
        background-color: #ffffff !important;
        border-radius: 50%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    .main .block-container > div {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    .stApp { background-color: #f4f7f6; }
    
    /* End-to-End Topbar Style */
    .gov-topbar { 
        display: flex; 
        align-items: center; 
        justify-content: space-between; 
        background-color: #ffffff; 
        padding: 15px 40px; 
        border-bottom: 5px solid #008080; 
        margin-bottom: 10px; 
        width: 100%;
        box-shadow: 0 4px 10px rgba(0,0,0,0.06);
    }
    .gov-logo-section { display: flex; align-items: center; gap: 20px; }
    .gov-logo { height: 65px; width: auto; object-fit: contain; }
    
    .gov-title { 
        font-family: inherit;
        font-weight: 800; 
        color: #004a99; 
        font-size: 1.4rem; 
        line-height: 1.2; 
        letter-spacing: normal; 
    }
    .gov-subtitle { color: #008080; font-weight: 600; font-size: 0.9rem; }
    .hospital-tag { 
        text-align: right; 
        font-family: inherit;
        font-weight: 800; 
        color: #004a99; 
        font-size: 1.4rem; 
        border-right: 4px solid #ffcc00; 
        padding-right: 15px; 
    }
    
    /* Home Decor & Theme Modifications */
    .header-box { 
        background: linear-gradient(135deg, #004a99 0%, #0066cc 50%, #008080 100%); 
        color: white; 
        padding: 45px; 
        border-radius: 12px; 
        text-align: center; 
        margin-bottom: 30px;
        border-bottom: 5px solid #ffcc00;
        box-shadow: 0 4px 15px rgba(0,74,153,0.15);
    }
    
    /* Image Card styling with Overflow protection */
    .card { 
        background-color: white; 
        border-radius: 12px; 
        border-left: 6px solid #008080; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.04); 
        margin-bottom: 20px; 
        overflow: hidden;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .card-content {
        padding: 20px;
        flex-grow: 1;
    }
    .card-img {
        width: 100%;
        height: 250px;
        object-fit: cover;
        display: block;
    }
    
    /* Professionally Sized News/Articles Style */
    .news-card {
        background: #ffffff;
        border-radius: 10px;
        border-top: 5px solid #004a99;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        padding: 20px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .news-meta {
        font-size: 0.8rem;
        color: #008080;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .news-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #004a99;
        margin: 5px 0 12px 0;
        line-height: 1.3;
    }
    .news-text {
        font-size: 0.9rem;
        color: #444444;
        line-height: 1.5;
        flex-grow: 1;
        margin-bottom: 12px;
    }
    
    .section-header { border-bottom: 3px solid #008080; padding-bottom: 10px; margin-top: 35px; margin-bottom: 25px; color: #004a99; font-weight: 700; }
    .quick-box { background-color: #ffffff; padding: 22px; border-radius: 10px; border-top: 4px solid #004a99; height: 100%; box-shadow: 0 4px 8px rgba(0,0,0,0.03); margin-bottom: 15px; }
    .center-card { background-color: #eef7f7; padding: 18px; border-radius: 8px; border-left: 4px solid #008080; margin-bottom: 15px; }
    .testimonial-box { background-color: #ffffff; padding: 25px; border-radius: 10px; border-left: 6px solid #ffcc00; font-style: italic; box-shadow: 0 4px 10px rgba(0,0,0,0.03); }
    .summary-box { background-color: #eef5fc; padding: 20px; border-radius: 10px; border: 1px solid #bce0fd; margin-top: 20px; }
    .stButton>button { width: 100%; border-radius: 6px; font-weight: 600; }
    
    /* Perfect Circle Profile Fixes */
    .doctor-flex { display: flex; align-items: center; gap: 25px; }
    .doctor-avatar-container { width: 110px; height: 110px; min-width: 110px; max-width: 110px; position: relative; }
    .doctor-avatar { 
        width: 110px; 
        height: 110px; 
        border-radius: 50% !important; 
        object-fit: cover !important; 
        aspect-ratio: 1 / 1 !important;
        border: 3px solid #008080; 
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* =========================================================
       SIDEBAR CUSTOMIZATIONS - COLLAPSE / EXPAND ACTIVE
       ========================================================= */
    [data-testid="stSidebar"] {
        background-color: #003366 !important;
        border-right: 5px solid #ffcc00 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #ffcc00 !important;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    [data-testid="sidebar-user-features"] {
        display: none !important;
    }
    
    .sidebar-branding { text-align: center; padding: 15px 0; border-bottom: 2px solid #ffcc00; margin-bottom: 20px; }

    /* --- REUSABLE FOOTER STYLES --- */
    .global-footer {
        background-color: #002b5c;
        color: #ffffff;
        padding: 40px 20px;
        margin-top: 60px;
        border-top: 5px solid #ffcc00;
        font-size: 0.9rem;
    }
    .footer-container {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 30px;
    }
    .footer-section {
        flex: 1;
        min-width: 220px;
    }
    .footer-section h4 {
        color: #ffcc00;
        margin-bottom: 15px;
        border-bottom: 2px solid #008080;
        padding-bottom: 5px;
        font-weight: 700;
    }
    .footer-section p, .footer-section ul {
        line-height: 1.6;
        color: #d1d8e0;
    }
    .footer-section ul {
        list-style: none;
        padding-left: 0;
    }
    .footer-section ul li {
        margin-bottom: 8px;
    }
    .footer-bottom {
        text-align: center;
        padding-top: 25px;
        margin-top: 25px;
        border-top: 1px solid #004a99;
        color: #a5b1c2;
        font-size: 0.8rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- GOVERNMENT LOGO TOPBAR ---
st.markdown(f"""
    <style>
    .gov-topbar {{
        overflow: hidden;
    }}
    .hospital-tag {{
        overflow: hidden;
        white-space: nowrap;
        width: 350px;
        position: relative;
    }}
    .animated-hospital-text {{
        display: inline-block;
        white-space: nowrap;
        animation: scroll-right-to-left 10s linear infinite;
    }}
    @keyframes scroll-right-to-left {{
        0% {{ transform: translateX(100%); }}
        100% {{ transform: translateX(-100%); }}
    }}
    </style>

    <div class="gov-topbar">
        <div class="gov-logo-section">
            <img class="gov-logo" src="{logo_base64}" alt="Government of Kenya Logo">
            <div>
                <div class="gov-title">GOVERNMENT OF KENYA</div>
                <div class="gov-subtitle">Ministry of Health &bull; Bomet County Government</div>
            </div>
        </div>
        <div class="hospital-tag">
            <div class="animated-hospital-text">
                LONGISA COUNTY REFERRAL HOSPITAL
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 2. INITIAL SEED DATA FOR MEDICAL STAFF ---
if 'doctors' not in st.session_state:
    st.session_state.doctors = [
        {"id": "doc_1", "name": "Dr. Peris Mbatha Mutuku", "spec": "Nephrologist", "desc": "Seasoned medical professional with 12 years of experience as Consultant Physician and Lead Nephrologist.", "img": DEFAULT_DOC_IMG},
        {"id": "doc_2", "name": "Dr. Brian Omina Odari", "spec": "Global Health Management", "desc": "Specialist with 12 years of experience in global health management and international patient coordination.", "img": DEFAULT_DOC_IMG},
        {"id": "doc_3", "name": "Dr. Alex Gathura Kagia", "spec": "Obstetrician-Gynaecologist", "desc": "Obstetrician-Gynaecologist with eight years of specialised experience in reproductive health.", "img": DEFAULT_DOC_IMG},
        {"id": "doc_4", "name": "Dr. Fahmo Mohamed Yusuf", "spec": "Paediatrician", "desc": "Dedicated Senior Registrar and Paediatrician with 10 years of experience in child healthcare.", "img": DEFAULT_DOC_IMG},
        {"id": "doc_5", "name": "Dr. Joram Mugo Muthui", "spec": "Obstetrician-Gynaecologist", "desc": "Compassionate and dedicated specialist with seven years of experience in reproductive health.", "img": DEFAULT_DOC_IMG},
        {"id": "doc_6", "name": "Dr. Lauryn Busolo Mengesa", "spec": "Obstetrician-Gynaecologist", "desc": "Obstetrician-Gynaecologist with 12 years of experience, trained at the University of Nairobi.", "img": DEFAULT_DOC_IMG}
    ]

# --- 3. SEED DATA FOR DEPARTMENTS (Level 5 Hospital) ---
if 'departments' not in st.session_state:
    st.session_state.departments = [
        {"id": "dep_1", "name": "🩺 General & Specialized Internal Medicine", "desc": "Comprehensive clinical management of complex systemic chronic conditions, including hypertension, oncology interventions, and pulmonology."},
        {"id": "dep_2", "name": "🤰 Obstetrics & Gynecology (Maternity)", "desc": "Comprehensive Level 5 maternal infrastructure providing advanced antenatal care, safe high-risk deliveries, neonatal monitoring, and reproductive family planning."},
        {"id": "dep_3", "name": "👶 Pediatrics & Child Health Services", "desc": "A dedicated infant and adolescent clinic specializing in growth monitoring, immunizations, and pediatric emergency support."},
        {"id": "dep_4", "name": "🏥 Intensive Care Unit (ICU) & High Dependency Unit (HDU)", "desc": "State-of-the-art critical care facilities supporting continuous organ support, mechanical ventilation, and post-operative monitoring."},
        {"id": "dep_5", "name": "🧪 Dialysis & Renal Unit", "desc": "Modern medical infrastructure offering customized hemodialysis therapy and management plans for acute and end-stage kidney diseases."},
        {"id": "dep_6", "name": "🩻 Advanced Radiology & Imaging Services", "desc": "Premium imaging diagnostics including digital X-Rays, high-resolution CT scans, digital mammography, and ultrasound screenings."},
        # --- Additional Level 6 Departments ---
        {"id": "dep_7", "name": "🔪 General & Cardiothoracic Surgery", "desc": "Advanced surgical theatre equipped for complex cardiothoracic, abdominal, and reconstructive procedures."},
        {"id": "dep_8", "name": "🧠 Neurology & Neurosurgery", "desc": "Specialized care for neurological disorders, brain injury trauma, and advanced neurosurgical interventions."},
        {"id": "dep_9", "name": "🦴 Orthopedics & Trauma Center", "desc": "Focused management of musculoskeletal injuries, fracture repairs, spinal surgery, and joint replacement procedures."},
        {"id": "dep_10", "name": "👁️ Ophthalmology & ENT", "desc": "Specialized diagnostic and surgical services for complex eye, ear, nose, and throat conditions."},
        {"id": "dep_11", "name": "🧬 Laboratory & Pathology Services", "desc": "High-throughput diagnostic lab offering histology, hematology, microbiology, and molecular pathology services."},
        {"id": "dep_12", "name": "🩹 Physical Therapy & Rehabilitation", "desc": "Integrated recovery programs including physiotherapy, occupational therapy, and speech therapy for post-surgical or stroke patients."},
        {"id": "dep_13", "name": "💊 Pharmacy & Oncology Infusion Center", "desc": "Comprehensive pharmaceutical care and dedicated facilities for chemotherapy administration and pain management."}
    ]

# --- 4. SEED DATA FOR ABOUT US, CONTACTS & HOURS ---
if 'about_data' not in st.session_state:
    st.session_state.about_data = {
        "mission": "To provide high-quality, patient-centered clinical care, diagnostic interventions, and medical solutions under the principles of equity, competence, and professionalism.",
        "vision": "To be the premiere Level 5 Referral Hospital in East Africa, recognized for excellence, innovation, and training in health delivery.",
        "hours": """
* **Specialist Clinics:** Mon - Fri, 8:00 AM - 5:00 PM
* **Emergency Department:** Open 24/7 (Everyday)
* **Inpatient Visiting Hours:** 12:30 PM - 2:00 PM & 4:30 PM - 6:30 PM Daily
        """,
        "contacts": """
* **Emergency Desk Line:** +254 703 082000
* **General Enquiries Desk:** +254 (0) 52 22234
* **Official Registry Mail:** admin@longisa.or.ke
* **Mailing Address:** P.O. Box 25, Longisa, Bomet County, Kenya
        """
    }

# --- 5. SEED DATA FOR ARTICLES / NEWS ---
if 'articles' not in st.session_state: 
    st.session_state.articles = [
        {
            "id": "art_1",
            "title": "Understanding Universal Health Coverage in Bomet County",
            "date": "March 18, 2026",
            "content": "Longisa County Referral Hospital continues to expand accessible healthcare services under county health development initiatives. By focusing on primary healthcare models and establishing seamless local diagnostic laboratories, patients are now able to access vital treatments closer to home without travel fatigue.",
            "img": "https://res.cloudinary.com/jlengxni/image/upload/v1784122494/BOARD_LON_kcn1cd.jpg"
        },
        {
            "id": "art_2",
            "title": "Preventive Care: Managing Hypertension Locally",
            "date": "April 05, 2026",
            "content": "Hypertension remains one of the leading chronic challenges in our clinics. The clinical support staff recommends routine check-ups at our wellness center. Simple dietary adjustments combined with a routine 30-minute daily walk can decrease acute cardiac complications by up to 40%.",
            "img": "https://res.cloudinary.com/jlengxni/image/upload/v1784123012/DOC_LONG_pmlkhx.jpg"
        },
        {
            "id": "art_3",
            "title": "Triple ISO Certification Formally Awarded",
            "date": "Latest Operational Update",
            "content": "Longisa Hospital has formally secured environmental management and occupational safety certificates. By improving critical diagnostic pathways and updating care infrastructure, we keep serving with total adherence to national and global guidelines.",
            "img": "https://res.cloudinary.com/jlengxni/image/upload/v1784123362/SERVING_LONG_e1esb4.jpg"
        }
    ]

if 'admin_logged_in' not in st.session_state: st.session_state.admin_logged_in = False
if 'alpha_filter' not in st.session_state: st.session_state.alpha_filter = "All"
if 'current_tab' not in st.session_state: st.session_state.current_tab = "Home"

# --- Language bar ---
st.markdown("<p style='text-align: right; margin-right: 40px; color:#666; font-size:0.9rem;'>🌐 Language: English (EN) | Home 🇬🇧</p>", unsafe_allow_html=True)

# --- 6. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("""
    <div class="sidebar-branding" style="text-align:center;">
        <img src="https://res.cloudinary.com/jlengxni/image/upload/v1784122847/CONFE_fhyh4b.jpg"
             style="
                 width:180px;
                 height:180px;
                 border-radius:50%;
                 object-fit:cover;
                 display:block;
                 margin:0 auto 10px auto;
                 border:3px solid #ffffff;
                 box-shadow:0 2px 8px rgba(0,0,0,0.2);
             ">
        <h3 style="margin-bottom:2px;">Longisa Admin</h3>
        <span style="font-size:0.85rem; opacity:0.8;">
            Secure Admin Dashboard Access
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.error("🚨 **EMERGENCY LINE**\n\n+254 703 082000")
    st.markdown("---")

    menu = [
        "Home",
        "Find a Doctor",
        "Book an Appointment",
        "Departments",
        "Articles",
        "About Us",
        "About The Hospital",
        "Admin Panel",
    ]
    
    selected_menu = st.radio("🏥 Navigation Menu", menu, index=menu.index(st.session_state.current_tab))
    
    if selected_menu != st.session_state.current_tab:
        st.session_state.current_tab = selected_menu
        st.rerun()

def set_route(route_name):
    st.session_state.current_tab = route_name
    st.rerun()

# --- 7. APPLICATION LOGIC ---

# --- TAB: HOME ---
if st.session_state.current_tab == "Home":
    st.markdown("""
        <div class="header-box">
            <h1>🏥 LONGISA COUNTY REFERRAL HOSPITAL</h1>
            <p style='font-size:1.1rem; font-weight:400;'>SERVING WITH THE FEAR OF GOD</p>
            <p style='font-size:1.1rem; font-weight:400;'> LEVITICUS 25:17.</p>
        </div>
    """, unsafe_allow_html=True)
    
    intro_col1, intro_col2 = st.columns([1.6, 1.4], gap="large")
    with intro_col1:
        st.markdown("<h3 style='color:#004a99;'>Healthcare with Excellence</h3>", unsafe_allow_html=True)
        st.write(
            """
            Longisa County Referral Hospital has excelled in medical expertise and service provision, 
            deservedly earning widespread recognition throughout East Africa and beyond. 
            By integrating advanced clinical treatment pathways with standard-setting facility 
            infrastructure, we deliver high-impact clinical solutions to all communities.
            """
        )
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Explore Our Clinical Services ➜", key="home_srv_btn"):
                set_route("Departments")
        with col_btn2:
            if st.button("About Us ➜", key="home_abt_btn"):
                set_route("About Us, Contact & Hours")
        st.write("")
        st.info("💡 **Quick Hotlinks Ready**\n\nNeed access parameters fast? Use the toggle menu navigation index or the Quick Access matrix panels configured directly below.")
    
    with intro_col2:
        st.markdown("##### 📸 Longisa Hospital Gallery View")
        view_mode = st.radio("Select Facility Perspective:", ["Main Campus Entrance", "Clinical Landscape View"], horizontal=True, label_visibility="collapsed")
        if view_mode == "Main Campus Entrance":
            st.image("https://res.cloudinary.com/jlengxni/image/upload/v1784047255/LONGISA_GATE_dvsoxw.jpg", caption="Longisa County Referral Hospital Main Entrance Hub", use_container_width=True)
        else:
            st.image("https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRJuT108ODLoq3JHa1rkyouIQpv2Nx4gXERs1FKkr7wuK69mfjDbvdnWhE0-8FxIV9JmXKzzGXTCM3M3aE", caption="Clinical Facility Infrastructures at Longisa", use_container_width=True)

    # Quick Access Section
    st.markdown("<h2 class='section-header'>⚡ Quick Access</h2>", unsafe_allow_html=True)
    q_col1, q_col2, q_col3 = st.columns(3, gap="medium")

    with q_col1:
        st.markdown("""
            <div class="card">
                <img class="card-img" src="https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRr8TWHOgz46NyUcx_nVJTdSq1-FYuDpGlqX34OHrt2DW5mt0cw1JqTQVD2tH21INlSJTtYiMj71irR-Bg" alt="Doctor advising patient">
                <div class="card-content">
                    <h4 style="color:#008080; margin-top:0;">👨‍⚕️ Find a Doctor</h4>
                    <p style='font-size:0.9rem; color:#444;'>Connecting you to trusted Doctors anytime, anywhere. Whether you need a routine check-up, specialist advice, or urgent care.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Search Doctors", key="qa_search_doc", use_container_width=True):
            set_route("Find a Doctor")
            
    with q_col2:
        st.markdown("""
            <div class="card">
                <img class="card-img" src="https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcSQVZBWMrC9abAYU3MzC7K1j8r_voEL45OJ5tFuGs3GjHKAlE90PT8EAFyOvk5W5pieOhgN-oXaikNJZqo" alt="Stethoscope with passport and flight tickets">
                <div class="card-content">
                    <h4 style="color:#008080; margin-top:0;">🌍 Medical Tourism</h4>
                    <p style='font-size:0.9rem; color:#444;'>Discover our dedicated services for international patients, from travel assistance to world-class medical care. We're here to make your journey smooth.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Learn More", key="qa_tourism_learn", use_container_width=True):
            st.toast("Redirecting to International Health coordination systems...")
            
    with q_col3:
        st.markdown("""
            <div class="card">
                <img class="card-img" src="https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcQYGBSd6Vnay0IGL7dcBRCFsbpKKCRMKUKA4iBE8T5K5GCnduWlMYpC-MPf5dZOizp6iiJGLVu8EnqgEyo" alt="Red map pin pinpointing hospital building">
                <div class="card-content">
                    <h4 style="color:#008080; margin-top:0;">📍 Getting to the Hospital</h4>
                    <p style='font-size:0.9rem; color:#444;'>We want your visit to be easy. Find directions, parking infrastructure arrays, and transport info on our Location system mapping panel.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Get Directions", key="qa_get_dirs", use_container_width=True):
            st.toast("Opening routing coordination pathways...")

    # Dynamic Outpatient Centers
    st.markdown("<h2 class='section-header'>🏢 Outpatient Centers</h2>", unsafe_allow_html=True)
    st.write("Learn more about our outpatient centers or choose a specific location.")
    
    oc_col1, oc_col2, oc_col3, oc_col4 = st.columns(4)
    with oc_col1:
        st.markdown("""<div class='center-card'><b>🏢 Anderson Specialty Centre</b><br><small>Argwings Kodhek Road, Anderson Centre, 1st Floor</small></div>""", unsafe_allow_html=True)
        st.markdown("""<div class='center-card'><b>🏢 Kiambu Mall</b><br><small>Kiambu Mall, 2nd Floor, Kiambu Road</small></div>""", unsafe_allow_html=True)
    with oc_col2:
        st.markdown("""<div class='center-card'><b>🏢 Capital Centre</b><br><small>Capital Centre, 1st floor, Mombasa Road</small></div>""", unsafe_allow_html=True)
        st.markdown("""<div class='center-card'><b>🏢 Rosslyn Riviera</b><br><small>Rosslyn Riviera Mall, 3rd Floor, Limuru Rd</small></div>""", unsafe_allow_html=True)
    with oc_col3:
        st.markdown("""<div class='center-card'><b>🏢 Chandaria A & E Centre</b><br><small>Main Hospital Complex Campus</small></div>""", unsafe_allow_html=True)
        st.markdown("""<div class='center-card'><b>🏢 Southfield Mall</b><br><small>Southfield Mall, 2nd Floor, Airport North Road</small></div>""", unsafe_allow_html=True)
    with oc_col4:
        st.markdown("""<div class='center-card'><b>🏢 Galleria Mall</b><br><small>Galleria Shopping Mall, 2nd Floor, Lang'ata Road</small></div>""", unsafe_allow_html=True)
        if st.button("Explore All Locations", key="exp_all_locs_btn"):
            st.toast("Fetching outpatient medical annex schedules...")

    # DYNAMIC NEWS SECTION
    st.markdown("<h2 class='section-header'>📰 Latest News & Updates</h2>", unsafe_allow_html=True)
    
    articles_list = st.session_state.articles
    if len(articles_list) > 0:
        cols = st.columns(min(len(articles_list), 3), gap="medium")
        for i, art in enumerate(articles_list[:3]):
            with cols[i % 3]:
                img_src = art.get('img') if art.get('img') else DEFAULT_NEWS_IMG
                st.markdown(f"""
                    <div class="news-card">
                        <img src="{img_src}" style="width:100%; height:150px; object-fit:cover; border-radius:8px; margin-bottom:12px;">
                        <div>
                            <div class="news-meta">📅 {art.get('date', 'Recent Update')}</div>
                            <div class="news-title">{art['title']}</div>
                            <div class="news-text">{art['content'][:120]}...</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("Read Full Story", key=f"read_home_art_{art['id']}", use_container_width=True):
                    set_route("Articles")
    else:
        st.info("No news updates posted yet.")

# --- TAB: FIND A DOCTOR ---
elif st.session_state.current_tab == "Find a Doctor":
    st.header("Our Specialists")
    st.write("Get to know our doctors and their areas of expertise.")
    
    st.markdown("### 🔍 Narrow your search")
    filter_col1, filter_col2 = st.columns(2)
    
    with filter_col1:
        search_name = st.text_input("By Doctor's Name", placeholder="Type name...")
    with filter_col2:
        specialties_list = ["All Specialties"] + list(set([d['spec'] for d in st.session_state.doctors]))
        search_spec = st.selectbox("By Specialty Clinic", specialties_list)
        
    st.markdown("##### Filter by First Name")
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
    alpha_cols = st.columns(27)
    with alpha_cols[0]:
        if st.button("All", key="btn_all"):
            st.session_state.alpha_filter = "All"
    for idx, letter in enumerate(alphabet):
        with alpha_cols[idx + 1]:
            if st.button(letter, key=f"btn_{letter}"):
                st.session_state.alpha_filter = letter
                
    if st.button("Reset Filters", key="reset_all_filters"):
        st.session_state.alpha_filter = "All"
        st.rerun()
                
    if st.session_state.alpha_filter != "All":
        st.info(f"Showing results starting with letter: **{st.session_state.alpha_filter}**")
        
    st.markdown("---")
    
    filtered_docs = []
    for doc in st.session_state.doctors:
        if search_name and search_name.lower() not in doc['name'].lower():
            continue
        if search_spec != "All Specialties" and doc['spec'] != search_spec:
            continue
        clean_first_name = doc['name'].replace("Dr. ", "").strip()
        if st.session_state.alpha_filter != "All" and not clean_first_name.upper().startswith(st.session_state.alpha_filter):
            continue
            
        filtered_docs.append(doc)

    if len(filtered_docs) == 0:
        st.warning("No specialists match your selected filtration criteria.")
    else:
        for doc in filtered_docs:
            img_style = doc['img'] if isinstance(doc['img'], str) else DEFAULT_DOC_IMG
            
            st.markdown(f"""
            <div class="card">
                <div class="card-content">
                    <div class="doctor-flex">
                        <div class="doctor-avatar-container">
                            <img src="{img_style}" class="doctor-avatar">
                        </div>
                        <div>
                            <h3 style="color:#004a99; margin:0 0 5px 0;">👨‍⚕️ {doc['name']}</h3>
                            <p style='color: #008080; font-weight: bold; margin-bottom: 8px;'>{doc['spec']}</p>
                            <p style='font-size: 0.95rem; color: #444; margin:0;'>{doc.get('desc', 'Specialist Consultant.')}</p>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            btn_col1, btn_col2, _ = st.columns([1.5, 1.5, 3])
            with btn_col1:
                if st.button("Book an appointment", key=f"bk_{doc['id']}"):
                    set_route("Book an Appointment")
            with btn_col2:
                if st.button("View Profile", key=f"prof_{doc['id']}"):
                    st.success(f"Profile Page details for {doc['name']} loaded successfully.")
            st.write("")

# --- TAB: BOOK AN APPOINTMENT ---
elif st.session_state.current_tab == "Book an Appointment":
    st.header("Book Appointment")
    st.write("A simple, secure booking experience.")
    st.markdown("---")
    
    form_col, summary_col = st.columns([1.8, 1.2], gap="large")
    
    with form_col:
        st.markdown("#### 1. Select Clinical Service")
        services_options = [
            "-- choose a service --", "Gynae-Oncology Clinic", "Obstetrics & Antenatal", "Cardiology Clinic", "Dialysis Unit"
        ]
        chosen_service = st.selectbox("Select Service Unit", services_options)
        
        st.markdown("#### 2. Preferred Location")
        location_options = ["Main Campus Hospital", "Anderson Specialty Centre", "Kiambu Mall"]
        chosen_location = st.selectbox("Select Location", location_options)
        
        st.markdown("#### 3. Patient Details")
        pat_name = st.text_input("Full Name")
        pat_phone = st.text_input("Phone Number")
        
    with summary_col:
        st.markdown("<div class='summary-box'>", unsafe_allow_html=True)
        st.markdown("### 📋 Appointment Summary")
        st.markdown(f"**Service:** {chosen_service}")
        st.markdown(f"**Location:** {chosen_location}")
        if pat_name:
            st.markdown(f"**Patient:** {pat_name}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("Confirm Booking", type="primary"):
            if chosen_service == "-- choose a service --" or not pat_name or not pat_phone:
                st.error("Please fill in all fields.")
            else:
                st.success("Booking registered successfully!")

# --- TAB: DEPARTMENTS ---
elif st.session_state.current_tab == "Departments":
    st.header("🏥 Hospital Departments & Specialized Clinical Units")
