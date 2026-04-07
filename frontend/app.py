# import streamlit as st
# import requests
# from datetime import date
# import os

# # ------------------ CONFIG ------------------
# st.set_page_config(
#     page_title="AutoClaim AI",
#     layout="wide",
#     page_icon="🚗"
# )

# # ------------------ HEADER ------------------
# st.title("🚗 AutoClaim AI")
# st.caption("Intelligent Vehicle Insurance Claim Engine")

# st.divider()

# # ------------------ INPUT SECTION ------------------
# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("📸 Upload Vehicle Images")
#     images = st.file_uploader(
#         "Upload 2-4 images",
#         type=["jpg", "png", "jpeg"],
#         accept_multiple_files=True
#     )

# with col2:
#     st.subheader("📄 Upload Policy Schedule")
#     policy = st.file_uploader(
#         "Upload Policy PDF",
#         type=["pdf"]
#     )

# incident_date = st.date_input("📅 Incident Date", value=date.today())

# st.divider()

# # ------------------ PROCESS BUTTON ------------------
# if st.button("🚀 Process Claim", use_container_width=True):

#     if not images or not policy:
#         st.error("Please upload images and policy file")
#     else:
#         with st.spinner("Processing claim... Please wait ⏳"):

#             files = []

#             for img in images:
#                 files.append(("files", (img.name, img, img.type)))

#             files.append(("policy_schedule", (policy.name, policy, policy.type)))

#             response = requests.post(
#                 "http://127.0.0.1:8000/claim/process",
#                 files=files,
#                 data={"incident_date": str(incident_date)}
#             )

#             # ✅ STORE RESULT IN SESSION
#             st.session_state["result"] = response.json()

#         st.success("✅ Claim Processed Successfully")

# # ------------------ DISPLAY RESULT ------------------
# if "result" in st.session_state:

#     result = st.session_state["result"]

#     # ------------------ TABS ------------------
#     tab1, tab2, tab3, tab4 = st.tabs([
#         "📊 Summary",
#         "🚗 Vehicle",
#         "📄 Policy",
#         "💰 Financial"
#     ])

#     # ------------------ SUMMARY ------------------
#     with tab1:
#         col1, col2, col3 = st.columns(3)

#         col1.metric("Claim ID", result["claim_id"])
#         col2.metric("Status", result["status"])
#         col3.metric("Fraud Check", result["fraud_check"])

#         st.write("### 🛠 Damage Details")
#         st.write(f"Damages Detected: {result['damages_detected']}")
#         st.write(f"Damages Covered: {result['damages_covered']}")

#     # ------------------ VEHICLE ------------------
#     with tab2:
#         v = result["vehicle"]
#         st.write("### 🚗 Vehicle Information")
#         st.write(f"Make: {v['make']}")
#         st.write(f"Model: {v['model']}")
#         st.write(f"Year: {v['year']}")
#         st.write(f"Confidence: {v['confidence']}%")

#     # ------------------ POLICY ------------------
#     with tab3:
#         p = result["schedule_data"]
#         st.write("### 📄 Policy Details")
#         st.write(f"Insurer: {p['insurer']}")
#         st.write(f"Policy Type: {p['policy_type']}")
#         st.write(f"IDV: ₹{p['idv']}")
#         st.write(f"Vehicle Number: {p['vehicle_number']}")

#         st.write("### ➕ Add-ons")
#         for addon in p["addons"]:
#             st.success(addon)

#     # ------------------ FINANCIAL ------------------
#     with tab4:
#         st.write("### 💰 Financial Summary")

#         col1, col2, col3 = st.columns(3)

#         col1.metric("IDV", f"₹{result['idv']}")
#         col2.metric("Repair Cost", f"₹{result['total_repair_cost']}")
#         col3.metric("Final Claim", f"₹{result['final_claimable']}")

#         st.write("Deductible: ₹1000")

#     # ------------------ SHAP EXPLANATION ------------------
#     st.divider()
#     st.subheader("🧠 Explainability (SHAP)")

#     for exp in result["shap_explanations"]:
#         st.info(exp)

#     # ------------------ DOWNLOAD PDF ------------------
#     st.divider()
#     st.subheader("📥 Download Report")

#     pdf_path = result["pdf_report"]

#     # Fix Windows path
#     pdf_path = pdf_path.replace("\\", "/")

#     # Fix relative path (frontend → root)
#     pdf_path = os.path.join("..", pdf_path)

#     try:
#         with open(pdf_path, "rb") as f:
#             st.download_button(
#                 "Download Claim Report",
#                 f,
#                 file_name="claim_report.pdf"
#             )
#     except:
#         st.warning("PDF not found")

# else:
#     st.info("Upload files and click 'Process Claim' to start")



# import streamlit as st
# import requests
# from datetime import date
# import os

# # ------------------ CONFIG ------------------
# st.set_page_config(
#     page_title="AutoClaim AI",
#     layout="wide",
#     page_icon="🚗"
# )

# # ------------------ CUSTOM CSS ------------------
# st.markdown("""
# <style>
# .main {
#     background-color: #0E1117;
# }

# h1, h2, h3 {
#     color: #FFFFFF;
# }

# .card {
#     background-color: #1E1E1E;
#     padding: 20px;
#     border-radius: 15px;
#     margin-bottom: 15px;
#     box-shadow: 0px 0px 10px rgba(0,0,0,0.3);
# }

# .metric-box {
#     background: linear-gradient(135deg, #1D2671, #C33764);
#     padding: 20px;
#     border-radius: 12px;
#     color: white;
#     text-align: center;
# }

# .upload-box {
#     background-color: #1E1E1E;
#     padding: 15px;
#     border-radius: 10px;
# }
# </style>
# """, unsafe_allow_html=True)

# # ------------------ HEADER ------------------
# st.markdown("""
# <h1 style='text-align: center;'>🚗 AutoClaim AI</h1>
# <p style='text-align: center; color: gray;'>
# AI-Powered Insurance Claim Processing System
# </p>
# """, unsafe_allow_html=True)

# st.divider()

# # ------------------ INPUT SECTION ------------------
# col1, col2 = st.columns(2)

# with col1:
#     st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
#     st.subheader("📸 Upload Vehicle Images")
#     images = st.file_uploader(
#         "Upload 2-4 images",
#         type=["jpg", "png", "jpeg"],
#         accept_multiple_files=True
#     )
#     st.markdown("</div>", unsafe_allow_html=True)

# with col2:
#     st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
#     st.subheader("📄 Upload Policy Schedule")
#     policy = st.file_uploader(
#         "Upload Policy PDF",
#         type=["pdf"]
#     )
#     st.markdown("</div>", unsafe_allow_html=True)

# incident_date = st.date_input("📅 Incident Date", value=date.today())

# # ------------------ IMAGE PREVIEW ------------------
# if images:
#     st.subheader("📸 Uploaded Images Preview")
#     cols = st.columns(len(images))
#     for i, img in enumerate(images):
#         cols[i].image(img, use_column_width=True)

# st.divider()

# # ------------------ PROCESS BUTTON ------------------
# if st.button("🚀 Process Claim", use_container_width=True):

#     if not images or not policy:
#         st.error("Please upload images and policy file")
#     else:
#         with st.spinner("Processing claim... Please wait ⏳"):

#             files = []

#             for img in images:
#                 files.append(("files", (img.name, img, img.type)))

#             files.append(("policy_schedule", (policy.name, policy, policy.type)))

#             response = requests.post(
#                 "http://127.0.0.1:8000/claim/process",
#                 files=files,
#                 data={"incident_date": str(incident_date)}
#             )

#             st.session_state["result"] = response.json()

#         st.success("✅ Claim Processed Successfully")

# # ------------------ DISPLAY RESULT ------------------
# if "result" in st.session_state:

#     result = st.session_state["result"]

#     tab1, tab2, tab3, tab4 = st.tabs([
#         "📊 Summary",
#         "🚗 Vehicle",
#         "📄 Policy",
#         "💰 Financial"
#     ])

#     # ------------------ SUMMARY ------------------
#     with tab1:
#         st.markdown("### 📊 Claim Overview")

#         col1, col2, col3 = st.columns(3)

#         col1.markdown(f"""
#         <div class="metric-box">
#             <h4>Claim ID</h4>
#             <h2>{result['claim_id']}</h2>
#         </div>
#         """, unsafe_allow_html=True)

#         col2.markdown(f"""
#         <div class="metric-box">
#             <h4>Status</h4>
#             <h2>{result['status']}</h2>
#         </div>
#         """, unsafe_allow_html=True)

#         col3.markdown(f"""
#         <div class="metric-box">
#             <h4>Fraud</h4>
#             <h2>{result['fraud_check']}</h2>
#         </div>
#         """, unsafe_allow_html=True)

#         st.markdown(f"""
#         <div class="card">
#             <h4>Damage Summary</h4>
#             <p>Damages Detected: {result['damages_detected']}</p>
#             <p>Damages Covered: {result['damages_covered']}</p>
#         </div>
#         """, unsafe_allow_html=True)

#     # ------------------ VEHICLE ------------------
#     with tab2:
#         v = result["vehicle"]
#         st.markdown(f"""
#         <div class="card">
#             <h3>🚗 Vehicle Details</h3>
#             <p><b>Make:</b> {v['make']}</p>
#             <p><b>Model:</b> {v['model']}</p>
#             <p><b>Year:</b> {v['year']}</p>
#             <p><b>Confidence:</b> {v['confidence']}%</p>
#         </div>
#         """, unsafe_allow_html=True)

#     # ------------------ POLICY ------------------
#     with tab3:
#         p = result["schedule_data"]
#         st.markdown(f"""
#         <div class="card">
#             <h3>📄 Policy Details</h3>
#             <p><b>Insurer:</b> {p['insurer']}</p>
#             <p><b>Policy Type:</b> {p['policy_type']}</p>
#             <p><b>IDV:</b> ₹{p['idv']}</p>
#             <p><b>Vehicle Number:</b> {p['vehicle_number']}</p>
#         </div>
#         """, unsafe_allow_html=True)

#         st.markdown("### ➕ Add-ons")
#         for addon in p["addons"]:
#             st.success(addon)

#     # ------------------ FINANCIAL ------------------
#     with tab4:
#         st.markdown("### 💰 Financial Summary")

#         col1, col2, col3 = st.columns(3)

#         col1.metric("IDV", f"₹{result['idv']}")
#         col2.metric("Repair Cost", f"₹{result['total_repair_cost']}")
#         col3.metric("Final Claim", f"₹{result['final_claimable']}")

#         st.markdown("""
#         <div class="card">
#             <h4>Deductible</h4>
#             <h2>₹1000</h2>
#         </div>
#         """, unsafe_allow_html=True)

#     # ------------------ SHAP ------------------
#     st.divider()
#     st.subheader("🧠 Explainability (SHAP)")

#     for exp in result["shap_explanations"]:
#         st.markdown(f"""
#         <div class="card">{exp}</div>
#         """, unsafe_allow_html=True)

#     # ------------------ DOWNLOAD PDF ------------------
#     st.divider()
#     st.subheader("📥 Download Report")

#     pdf_path = result["pdf_report"]
#     pdf_path = pdf_path.replace("\\", "/")
#     pdf_path = os.path.join("..", pdf_path)

#     try:
#         with open(pdf_path, "rb") as f:
#             st.download_button(
#                 "Download Claim Report",
#                 f,
#                 file_name="claim_report.pdf"
#             )
#     except:
#         st.warning("PDF not found")

# else:
#     st.info("Upload files and click 'Process Claim' to start")



# import streamlit as st
# import requests
# from datetime import date
# import os

# # ---------------- CONFIG ----------------
# st.set_page_config(
#     page_title="AutoClaim AI",
#     layout="wide",
#     page_icon="🚗"
# )

# # ---------------- CLEAN CSS ----------------
# st.markdown("""
# <style>
# body {
#     background-color: #0E1117;
# }

# .block-container {
#     padding-top: 2rem;
#     padding-bottom: 2rem;
# }

# .section {
#     background-color: #161B22;
#     padding: 20px;
#     border-radius: 12px;
#     margin-bottom: 20px;
# }

# .title {
#     font-size: 36px;
#     font-weight: 700;
#     text-align: center;
# }

# .subtitle {
#     text-align: center;
#     color: #8b949e;
#     margin-bottom: 30px;
# }

# .kpi {
#     background-color: #1f2937;
#     padding: 15px;
#     border-radius: 10px;
#     text-align: center;
# }

# .kpi h3 {
#     margin: 0;
#     font-size: 14px;
#     color: #9ca3af;
# }

# .kpi h2 {
#     margin: 5px 0;
# }
# </style>
# """, unsafe_allow_html=True)

# # ---------------- SIDEBAR ----------------
# st.sidebar.title("🚗 AutoClaim AI")
# page = st.sidebar.radio("Navigation", ["📥 Upload", "📊 Results"])

# # ---------------- HEADER ----------------
# st.markdown("<div class='title'>AutoClaim AI</div>", unsafe_allow_html=True)
# st.markdown("<div class='subtitle'>AI-Powered Insurance Claim Processing</div>", unsafe_allow_html=True)

# # =========================
# # 📥 UPLOAD PAGE
# # =========================
# if page == "📥 Upload":

#     col1, col2 = st.columns(2)

#     with col1:
#         st.markdown("<div class='section'>", unsafe_allow_html=True)
#         st.subheader("📸 Vehicle Images")
#         images = st.file_uploader("Upload Images", type=["jpg", "png"], accept_multiple_files=True)
#         st.markdown("</div>", unsafe_allow_html=True)

#     with col2:
#         st.markdown("<div class='section'>", unsafe_allow_html=True)
#         st.subheader("📄 Policy Document")
#         policy = st.file_uploader("Upload Policy PDF", type=["pdf"])
#         st.markdown("</div>", unsafe_allow_html=True)

#     incident_date = st.date_input("📅 Incident Date", value=date.today())

#     # Image preview
#     if images:
#         st.markdown("### Preview")
#         cols = st.columns(len(images))
#         for i, img in enumerate(images):
#             cols[i].image(img, use_column_width=True)

#     if st.button("🚀 Process Claim", use_container_width=True):

#         if not images or not policy:
#             st.error("Please upload all inputs")
#         else:
#             with st.spinner("Processing..."):

#                 files = []
#                 for img in images:
#                     files.append(("files", (img.name, img, img.type)))

#                 files.append(("policy_schedule", (policy.name, policy, policy.type)))

#                 response = requests.post(
#                     "http://127.0.0.1:8000/claim/process",
#                     files=files,
#                     data={"incident_date": str(incident_date)}
#                 )

#                 st.session_state["result"] = response.json()

#             st.success("✅ Claim Processed")

# # =========================
# # 📊 RESULTS PAGE
# # =========================
# if page == "📊 Results":

#     if "result" not in st.session_state:
#         st.warning("Process a claim first")
#     else:
#         result = st.session_state["result"]

#         # -------- KPI ROW --------
#         col1, col2, col3 = st.columns(3)

#         col1.markdown(f"""
#         <div class="kpi">
#             <h3>Claim ID</h3>
#             <h2>{result['claim_id']}</h2>
#         </div>
#         """, unsafe_allow_html=True)

#         col2.markdown(f"""
#         <div class="kpi">
#             <h3>Status</h3>
#             <h2>{result['status']}</h2>
#         </div>
#         """, unsafe_allow_html=True)

#         col3.markdown(f"""
#         <div class="kpi">
#             <h3>Fraud Check</h3>
#             <h2>{result['fraud_check']}</h2>
#         </div>
#         """, unsafe_allow_html=True)

#         st.markdown("---")

#         # -------- VEHICLE + POLICY --------
#         col1, col2 = st.columns(2)

#         with col1:
#             v = result["vehicle"]
#             st.markdown("<div class='section'>", unsafe_allow_html=True)
#             st.subheader("🚗 Vehicle")
#             st.write(f"Make: {v['make']}")
#             st.write(f"Model: {v['model']}")
#             st.write(f"Year: {v['year']}")
#             st.write(f"Confidence: {v['confidence']}%")
#             st.markdown("</div>", unsafe_allow_html=True)

#         with col2:
#             p = result["schedule_data"]
#             st.markdown("<div class='section'>", unsafe_allow_html=True)
#             st.subheader("📄 Policy")
#             st.write(f"Insurer: {p['insurer']}")
#             st.write(f"Type: {p['policy_type']}")
#             st.write(f"IDV: ₹{p['idv']}")
#             st.write(f"Vehicle No: {p['vehicle_number']}")
#             st.markdown("</div>", unsafe_allow_html=True)

#         # -------- FINANCIAL --------
#         st.markdown("<div class='section'>", unsafe_allow_html=True)
#         st.subheader("💰 Financial Summary")

#         col1, col2, col3 = st.columns(3)
#         col1.metric("IDV", f"₹{result['idv']}")
#         col2.metric("Repair", f"₹{result['total_repair_cost']}")
#         col3.metric("Final", f"₹{result['final_claimable']}")
#         st.markdown("</div>", unsafe_allow_html=True)

#         # -------- SHAP --------
#         st.markdown("<div class='section'>", unsafe_allow_html=True)
#         st.subheader("🧠 Explainability")

#         for exp in result["shap_explanations"]:
#             st.write(f"• {exp}")

#         st.markdown("</div>", unsafe_allow_html=True)

#         # -------- DOWNLOAD --------
#         st.markdown("<div class='section'>", unsafe_allow_html=True)
#         st.subheader("📥 Report")

#         pdf_path = result["pdf_report"]
#         pdf_path = pdf_path.replace("\\", "/")
#         pdf_path = os.path.join("..", pdf_path)

#         try:
#             with open(pdf_path, "rb") as f:
#                 st.download_button("Download PDF", f, file_name="claim.pdf")
#         except:
#             st.warning("PDF not found")

#         st.markdown("</div>", unsafe_allow_html=True)





# import streamlit as st
# import requests
# from datetime import date
# import os

# # ---------------- CONFIG ----------------
# st.set_page_config(
#     page_title="AutoClaim AI",
#     layout="wide",
#     page_icon="🚗"
# )

# # ---------------- CLEAN CSS ----------------
# st.markdown("""
# <style>
# body {
#     background-color: #0E1117;
# }
# .section {
#     background-color: #161B22;
#     padding: 20px;
#     border-radius: 12px;
#     margin-bottom: 20px;
# }
# .title {
#     font-size: 36px;
#     font-weight: 700;
#     text-align: center;
# }
# .subtitle {
#     text-align: center;
#     color: #8b949e;
#     margin-bottom: 30px;
# }
# .kpi {
#     background-color: #1f2937;
#     padding: 15px;
#     border-radius: 10px;
#     text-align: center;
# }
# .card {
#     background-color:#1f2937;
#     padding:15px;
#     border-radius:10px;
#     margin-bottom:10px;
# }
# .high {color:#ef4444;}
# .medium {color:#f59e0b;}
# .low {color:#10b981;}
# </style>
# """, unsafe_allow_html=True)

# # ---------------- SIDEBAR ----------------
# st.sidebar.title("🚗 AutoClaim AI")
# page = st.sidebar.radio("Navigation", ["📥 Upload", "📊 Results"])

# # ---------------- HEADER ----------------
# st.markdown("<div class='title'>AutoClaim AI</div>", unsafe_allow_html=True)
# st.markdown("<div class='subtitle'>AI-Powered Insurance Claim Processing</div>", unsafe_allow_html=True)

# # =========================
# # 📥 UPLOAD PAGE
# # =========================
# if page == "📥 Upload":

#     col1, col2 = st.columns(2)

#     with col1:
#         st.markdown("<div class='section'>", unsafe_allow_html=True)
#         st.subheader("📸 Vehicle Images")
#         images = st.file_uploader("Upload Images", type=["jpg", "png"], accept_multiple_files=True)
#         st.markdown("</div>", unsafe_allow_html=True)

#     with col2:
#         st.markdown("<div class='section'>", unsafe_allow_html=True)
#         st.subheader("📄 Policy Document")
#         policy = st.file_uploader("Upload Policy PDF", type=["pdf"])
#         st.markdown("</div>", unsafe_allow_html=True)

#     incident_date = st.date_input("📅 Incident Date", value=date.today())

#     # Preview
#     if images:
#         st.markdown("### Preview")
#         cols = st.columns(len(images))
#         for i, img in enumerate(images):
#             cols[i].image(img, width=300)

#     if st.button("🚀 Process Claim", use_container_width=True):

#         if not images or not policy:
#             st.error("Please upload all inputs")
#         else:
#             with st.spinner("Processing..."):

#                 files = []
#                 for img in images:
#                     files.append(("files", (img.name, img, img.type)))

#                 files.append(("policy_schedule", (policy.name, policy, policy.type)))

#                 response = requests.post(
#                     "http://127.0.0.1:8000/claim/process",
#                     files=files,
#                     data={"incident_date": str(incident_date)}
#                 )

#                 st.session_state["result"] = response.json()

#             st.success("✅ Claim Processed")

# # =========================
# # 📊 RESULTS PAGE
# # =========================
# if page == "📊 Results":

#     if "result" not in st.session_state:
#         st.warning("Process a claim first")
#     else:
#         result = st.session_state["result"]

#         # KPI
#         col1, col2, col3 = st.columns(3)
#         col1.metric("Claim ID", result["claim_id"])
#         col2.metric("Status", result["status"])
#         col3.metric("Fraud", result["fraud_check"])

#         st.markdown("---")

#         # Vehicle + Policy
#         col1, col2 = st.columns(2)

#         with col1:
#             v = result["vehicle"]
#             st.markdown("<div class='section'>", unsafe_allow_html=True)
#             st.subheader("🚗 Vehicle")
#             st.write(f"Make: {v['make']}")
#             st.write(f"Model: {v['model']}")
#             st.write(f"Year: {v['year']}")
#             st.write(f"Confidence: {v['confidence']}%")
#             st.markdown("</div>", unsafe_allow_html=True)

#         with col2:
#             p = result["schedule_data"]
#             st.markdown("<div class='section'>", unsafe_allow_html=True)
#             st.subheader("📄 Policy")
#             st.write(f"Insurer: {p['insurer']}")
#             st.write(f"Type: {p['policy_type']}")
#             st.write(f"IDV: ₹{p['idv']}")
#             st.write(f"Vehicle No: {p['vehicle_number']}")
#             st.markdown("</div>", unsafe_allow_html=True)

#         # Financial
#         st.markdown("<div class='section'>", unsafe_allow_html=True)
#         st.subheader("💰 Financial Summary")
#         col1, col2, col3 = st.columns(3)
#         col1.metric("IDV", f"₹{result['idv']}")
#         col2.metric("Repair", f"₹{result['total_repair_cost']}")
#         col3.metric("Final", f"₹{result['final_claimable']}")
#         st.markdown("</div>", unsafe_allow_html=True)

#         # Explainability
#         st.markdown("<div class='section'>", unsafe_allow_html=True)
#         st.subheader("🧠 Explainability")
#         for exp in result["shap_explanations"]:
#             st.write(f"• {exp}")
#         st.markdown("</div>", unsafe_allow_html=True)

#         # =========================
#         # 🔥 DAMAGE ANALYSIS
#         # =========================
#         st.markdown("<div class='section'>", unsafe_allow_html=True)
#         st.subheader("📸 Damage Analysis")

#         # Images
#         if "debug_images" in result:
#             st.markdown("### 🧠 AI Detection Output")
#             cols = st.columns(3)
#             for i, img_path in enumerate(result["debug_images"]):
#                 if os.path.exists(img_path):
#                     with cols[i % 3]:
#                         st.image(img_path, width=300)

#         st.markdown("---")

#         # Cards
#         st.markdown("### 🔧 Detected Damages")

#         damages = result.get("coverage_details", [])

#         for i, d in enumerate(damages):
#             severity = d.get("severity", "low")

#             st.markdown(f"""
#             <div class="card">
#                 <h4>🔧 Damage {i+1}</h4>
#                 <p><b>Part:</b> {d.get('part')}</p>
#                 <p><b>Type:</b> {d.get('damage_type')}</p>
#                 <p class="{severity}"><b>Severity:</b> {severity.upper()}</p>
#                 <p><b>Confidence:</b> {d.get('confidence')}%</p>
#                 <p><b>Area:</b> {d.get('area', 'N/A')}</p>
#                 <p><b>Damage Ratio:</b> {d.get('damage_ratio', 'N/A')}</p>
#             </div>
#             """, unsafe_allow_html=True)

#         st.markdown("</div>", unsafe_allow_html=True)

#         # Download
#         st.markdown("<div class='section'>", unsafe_allow_html=True)
#         st.subheader("📥 Report")

#         pdf_path = result["pdf_report"].replace("\\", "/")
#         pdf_path = os.path.join("..", pdf_path)

#         try:
#             with open(pdf_path, "rb") as f:
#                 st.download_button("Download PDF", f, file_name="claim.pdf")
#         except:
#             st.warning("PDF not found")

#         st.markdown("</div>", unsafe_allow_html=True)






# import streamlit as st
# import requests
# from datetime import date
# import os

# # ---------------- CONFIG ----------------
# st.set_page_config(
#     page_title="AutoClaim AI",
#     layout="wide",
#     page_icon="🚗"
# )

# # ---------------- CLEAN CSS ----------------
# st.markdown("""
# <style>
# body {background-color: #0E1117;}
# .section {
#     background-color: #161B22;
#     padding: 20px;
#     border-radius: 12px;
#     margin-bottom: 20px;
# }
# .title {
#     font-size: 36px;
#     font-weight: 700;
#     text-align: center;
# }
# .subtitle {
#     text-align: center;
#     color: #8b949e;
#     margin-bottom: 30px;
# }
# .card {
#     background-color:#1f2937;
#     padding:15px;
#     border-radius:10px;
#     margin-bottom:10px;
# }
# .high {color:#ef4444;}
# .medium {color:#f59e0b;}
# .low {color:#10b981;}
# </style>
# """, unsafe_allow_html=True)

# # ---------------- SIDEBAR ----------------
# st.sidebar.title("🚗 AutoClaim AI")
# page = st.sidebar.radio("Navigation", ["📥 Upload", "📊 Results"])

# # ---------------- HEADER ----------------
# st.markdown("<div class='title'>AutoClaim AI</div>", unsafe_allow_html=True)
# st.markdown("<div class='subtitle'>AI-Powered Insurance Claim Processing</div>", unsafe_allow_html=True)

# # =========================
# # 📥 UPLOAD PAGE
# # =========================
# if page == "📥 Upload":

#     col1, col2 = st.columns(2)

#     with col1:
#         st.markdown("<div class='section'>", unsafe_allow_html=True)
#         st.subheader("📸 Vehicle Images")
#         images = st.file_uploader("Upload Images", type=["jpg", "png"], accept_multiple_files=True)
#         st.markdown("</div>", unsafe_allow_html=True)

#     with col2:
#         st.markdown("<div class='section'>", unsafe_allow_html=True)
#         st.subheader("📄 Policy Document")
#         policy = st.file_uploader("Upload Policy PDF", type=["pdf"])
#         st.markdown("</div>", unsafe_allow_html=True)

#     incident_date = st.date_input("📅 Incident Date", value=date.today())

#     # Preview
#     if images:
#         st.markdown("### Preview")
#         cols = st.columns(len(images))
#         for i, img in enumerate(images):
#             cols[i].image(img, width=300)

#     if st.button("🚀 Process Claim", use_container_width=True):

#         if not images or not policy:
#             st.error("Please upload all inputs")
#         else:
#             with st.spinner("Processing..."):

#                 files = []
#                 for img in images:
#                     files.append(("files", (img.name, img, img.type)))

#                 files.append(("policy_schedule", (policy.name, policy, policy.type)))

#                 response = requests.post(
#                     "http://127.0.0.1:8000/claim/process",
#                     files=files,
#                     data={"incident_date": str(incident_date)}
#                 )

#                 st.session_state["result"] = response.json()

#             st.success("✅ Claim Processed")

# # =========================
# # 📊 RESULTS PAGE
# # =========================
# if page == "📊 Results":

#     if "result" not in st.session_state:
#         st.warning("Process a claim first")
#     else:
#         result = st.session_state["result"]

#         # KPI
#         col1, col2, col3 = st.columns(3)
#         col1.metric("Claim ID", result["claim_id"])
#         col2.metric("Status", result["status"])
#         col3.metric("Fraud", result["fraud_check"])

#         st.markdown("---")

#         # Vehicle + Policy
#         col1, col2 = st.columns(2)

#         with col1:
#             v = result["vehicle"]
#             st.markdown("<div class='section'>", unsafe_allow_html=True)
#             st.subheader("🚗 Vehicle")
#             st.write(f"Make: {v['make']}")
#             st.write(f"Model: {v['model']}")
#             st.write(f"Year: {v['year']}")
#             st.write(f"Confidence: {v['confidence']}%")
#             st.markdown("</div>", unsafe_allow_html=True)

#         with col2:
#             p = result["schedule_data"]
#             st.markdown("<div class='section'>", unsafe_allow_html=True)
#             st.subheader("📄 Policy")
#             st.write(f"Insurer: {p['insurer']}")
#             st.write(f"Type: {p['policy_type']}")
#             st.write(f"IDV: ₹{p['idv']}")
#             st.write(f"Vehicle No: {p['vehicle_number']}")
#             st.markdown("</div>", unsafe_allow_html=True)

#         # Financial
#         st.markdown("<div class='section'>", unsafe_allow_html=True)
#         st.subheader("💰 Financial Summary")
#         col1, col2, col3 = st.columns(3)
#         col1.metric("IDV", f"₹{result['idv']}")
#         col2.metric("Repair", f"₹{result['total_repair_cost']}")
#         col3.metric("Final", f"₹{result['final_claimable']}")
#         st.markdown("</div>", unsafe_allow_html=True)

#         # Explainability
#         st.markdown("<div class='section'>", unsafe_allow_html=True)
#         st.subheader("🧠 Explainability")
#         for exp in result["shap_explanations"]:
#             st.write(f"• {exp}")
#         st.markdown("</div>", unsafe_allow_html=True)

#         # =========================
#         # 🔥 DAMAGE ANALYSIS
#         # =========================
#         st.markdown("<div class='section'>", unsafe_allow_html=True)
#         st.subheader("📸 Damage Analysis")

#         tab1, tab2 = st.tabs(["🖼️ Detection Images", "📊 Damage Details"])

#         # ---------------- IMAGE TAB ----------------
#         with tab1:
#             if "debug_images" in result:
#                 st.markdown("### 🧠 AI Detection Output")

#                 cols = st.columns(3)

#                 for i, img_path in enumerate(result["debug_images"]):
#                     fixed_path = os.path.join("..", img_path)

#                     if os.path.exists(fixed_path):
#                         with cols[i % 3]:
#                             st.image(fixed_path, caption="Detected Damage", width=300)
#                     else:
#                         st.warning(f"Image not found: {fixed_path}")

#         # ---------------- DETAILS TAB ----------------
#         with tab2:
#             st.markdown("### 🔧 Detected Damages")

#             damages = result.get("coverage_details", [])

#             if len(damages) == 0:
#                 st.info("No damages detected")
#             else:
#                 st.markdown(f"**Total Damages:** {len(damages)}")

#                 for i, d in enumerate(damages):
#                     severity = d.get("severity", "low")

#                     st.markdown(f"""
#                     <div class="card">
#                         <h4>🔧 Damage {i+1}</h4>
#                         <p><b>Part:</b> {d.get('part')}</p>
#                         <p><b>Type:</b> {d.get('damage_type')}</p>
#                         <p class="{severity}"><b>Severity:</b> {severity.upper()}</p>
#                         <p><b>Confidence:</b> {d.get('confidence')}%</p>
#                         <p><b>Area:</b> {d.get('area', 'N/A')}</p>
#                         <p><b>Damage Ratio:</b> {d.get('damage_ratio', 'N/A')}</p>
#                     </div>
#                     """, unsafe_allow_html=True)

#         st.markdown("</div>", unsafe_allow_html=True)

#         # Download
#         st.markdown("<div class='section'>", unsafe_allow_html=True)
#         st.subheader("📥 Report")

#         pdf_path = result["pdf_report"].replace("\\", "/")
#         pdf_path = os.path.join("..", pdf_path)

#         try:
#             with open(pdf_path, "rb") as f:
#                 st.download_button("Download PDF", f, file_name="claim.pdf")
#         except:
#             st.warning("PDF not found")

#         st.markdown("</div>", unsafe_allow_html=True)


import streamlit as st
import requests
from datetime import date
import os

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="AutoClaim AI",
    layout="wide",
    page_icon="🚗"
)

# ---------------- CLEAN CSS ----------------
st.markdown("""
<style>
body {background-color: #0E1117;}
.section {
    background-color: #161B22;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
}
.title {
    font-size: 36px;
    font-weight: 700;
    text-align: center;
}
.subtitle {
    text-align: center;
    color: #8b949e;
    margin-bottom: 30px;
}
.card {
    background-color:#1f2937;
    padding:15px;
    border-radius:10px;
    margin-bottom:10px;
}
.high {color:#ef4444;}
.medium {color:#f59e0b;}
.low {color:#10b981;}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🚗 AutoClaim AI")
page = st.sidebar.radio("Navigation", ["📥 Upload", "📊 Results"])

# ---------------- HEADER ----------------
st.markdown("<div class='title'>AutoClaim AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-Powered Insurance Claim Processing</div>", unsafe_allow_html=True)

# =========================
# 📥 UPLOAD PAGE
# =========================
if page == "📥 Upload":

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader("📸 Vehicle Images")
        images = st.file_uploader("Upload Images", type=["jpg", "png"], accept_multiple_files=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader("📄 Policy Document")
        policy = st.file_uploader("Upload Policy PDF", type=["pdf"])
        st.markdown("</div>", unsafe_allow_html=True)

    incident_date = st.date_input("📅 Incident Date", value=date.today())

    # Preview
    if images:
        st.markdown("### Preview")
        cols = st.columns(len(images))
        for i, img in enumerate(images):
            cols[i].image(img, width=300)

    if st.button("🚀 Process Claim", use_container_width=True):

        if not images or not policy:
            st.error("Please upload all inputs")
        else:
            with st.spinner("Processing..."):

                files = []
                for img in images:
                    files.append(("files", (img.name, img, img.type)))

                files.append(("policy_schedule", (policy.name, policy, policy.type)))

                response = requests.post(
                    "http://127.0.0.1:8000/claim/process",
                    files=files,
                    data={"incident_date": str(incident_date)}
                )

                st.session_state["result"] = response.json()

            st.success("✅ Claim Processed")

# =========================
# 📊 RESULTS PAGE
# =========================
if page == "📊 Results":

    if "result" not in st.session_state:
        st.warning("Process a claim first")
    else:
        result = st.session_state["result"]

        # KPI
        col1, col2, col3 = st.columns(3)
        col1.metric("Claim ID", result["claim_id"])
        col2.metric("Status", result["status"])
        col3.metric("Fraud", result["fraud_check"])

        st.markdown("---")

        # Vehicle + Policy
        col1, col2 = st.columns(2)

        with col1:
            v = result["vehicle"]
            st.markdown("<div class='section'>", unsafe_allow_html=True)
            st.subheader("🚗 Vehicle")
            st.write(f"Make: {v['make']}")
            st.write(f"Model: {v['model']}")
            st.write(f"Year: {v['year']}")
            st.write(f"Confidence: {v['confidence']}%")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            p = result["schedule_data"]
            st.markdown("<div class='section'>", unsafe_allow_html=True)
            st.subheader("📄 Policy")
            st.write(f"Insurer: {p['insurer']}")
            st.write(f"Type: {p['policy_type']}")
            st.write(f"IDV: ₹{p['idv']}")
            st.write(f"Vehicle No: {p['vehicle_number']}")
            st.markdown("</div>", unsafe_allow_html=True)

        # Financial
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader("💰 Financial Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("IDV", f"₹{result['idv']}")
        col2.metric("Repair", f"₹{result['total_repair_cost']}")
        col3.metric("Final", f"₹{result['final_claimable']}")
        st.markdown("</div>", unsafe_allow_html=True)

        # Explainability
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader("🧠 Explainability")
        for exp in result["shap_explanations"]:
            st.write(f"• {exp}")
        st.markdown("</div>", unsafe_allow_html=True)

        # =========================
        # 🔥 DAMAGE ANALYSIS (FINAL)
        # =========================
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader("📸 Damage Analysis")

        tab1, tab2, tab3 = st.tabs(["🖼️ Comparison", "🔥 Heatmap", "📊 Details"])

        # -------- COMPARISON --------
        with tab1:
            for img_path in result["debug_images"]:
                base = os.path.basename(img_path)

                original = os.path.join("..", "data/uploads", base)
                detected = os.path.join("..", img_path)

                col1, col2 = st.columns(2)

                with col1:
                    if os.path.exists(original):
                        st.image(original, caption="Original", width=350)

                with col2:
                    if os.path.exists(detected):
                        st.image(detected, caption="Detected", width=350)

        # -------- HEATMAP --------
        with tab2:
            for img_path in result["debug_images"]:
                base = os.path.basename(img_path)
                heatmap = os.path.join("..", "debug_outputs", f"heatmap_{base}")

                if os.path.exists(heatmap):
                    st.image(heatmap, caption="Damage Heatmap", width=400)

        # -------- DETAILS --------
        with tab3:
            damages = result.get("coverage_details", [])

            for i, d in enumerate(damages):
                with st.expander(f"🔧 Damage {i+1} - {d['part']}"):
                    st.write(f"Type: {d['damage_type']}")
                    st.write(f"Severity: {d['severity']}")
                    st.write(f"Confidence: {d['confidence']}%")
                    st.write(f"Area: {d['area']}")
                    st.write(f"Ratio: {d['damage_ratio']}")

        st.markdown("</div>", unsafe_allow_html=True)

        # Download
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader("📥 Report")

        pdf_path = result["pdf_report"].replace("\\", "/")
        pdf_path = os.path.join("..", pdf_path)

        try:
            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF", f, file_name="claim.pdf")
        except:
            st.warning("PDF not found")

        st.markdown("</div>", unsafe_allow_html=True)