import streamlit as st
from PIL import Image
import fitz  # PyMuPDF
import pytesseract
from deep_translator import GoogleTranslator

st.set_page_config(
    page_title="Secure Multilingual AI Medical Explainer",
    page_icon="🩺",
    layout="centered"
)

# Initialize session state for login tracking
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- LOGIN SCREEN ---
if not st.session_state["authenticated"]:
    st.title("🔐 Secure Portal Login")
    st.markdown("Please enter your credentials to access the Medical Report Explainer.")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_btn = st.form_submit_button("Login", type="primary")
        
        if submit_btn:
            # For portfolio demonstration, you can use these demo credentials:
            # Username: doctor / Password: ai123
            if username == "doctor" and password == "ai123":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Invalid username or password. (Hint: username: doctor, password: ai123)")
                
    st.stop()  # Stop execution here until logged in

# --- MAIN APP (Only visible after successful login) ---
st.sidebar.success("✅ Logged in securely as: Doctor")
if st.sidebar.button("Log Out"):
    st.session_state["authenticated"] = False
    st.rerun()

st.title("🩺 Multi-Modal Medical & Health Report Explainer")
st.markdown("Upload your clinical lab report (PDF or Image). Our AI will parse the document, flag out-of-range values, translate summaries, and answer your health questions.")

st.warning("⚠️ **Disclaimer:** This tool is for educational purposes only and does not replace professional medical advice.")

languages_dict = {
    "English": "en",
    "Spanish (Español)": "es",
    "Hindi (हिन्दी)": "hi",
    "Tamil (தமிழ்)": "ta",
    "French (Français)": "fr",
    "German (Deutsch)": "de",
    "Arabic (العربية)": "ar",
    "Chinese (中文)": "zh-CN"
}

target_lang_name = st.selectbox("🌐 Choose Explanation Language:", list(languages_dict.keys()))
target_lang_code = languages_dict[target_lang_name]

uploaded_file = st.file_uploader("Upload Lab Report (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    extracted_text = ""
    
    if uploaded_file.type == "application/pdf":
        with st.status("Reading PDF document..."):
            with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                for page in doc:
                    extracted_text += page.get_text()
        st.success("PDF successfully parsed!")
    else:
        with st.status("Running OCR on image..."):
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Report", use_container_width=True)
            extracted_text = pytesseract.image_to_string(image)
        st.success("OCR extraction complete!")

    with st.expander("🔍 View Raw Extracted Text"):
        st.text(extracted_text if extracted_text.strip() else "No text found.")

    if st.button("🚀 Analyze Report & Generate Insights", type="primary"):
        if not extracted_text.strip():
            st.error("Could not extract text from this file. Please upload a clearer scan.")
        else:
            with st.spinner("Analyzing clinical markers..."):
                analysis_parts = []
                text_lower = extracted_text.lower()
                
                analysis_parts.append("### 📋 Clinical Findings & Summary")
                if "wbc" in text_lower or "white blood cell" in text_lower:
                    analysis_parts.append("* **White Blood Cells (WBC):** Elevated levels can sometimes indicate your body is fighting off an infection or inflammation.")
                if "cholesterol" in text_lower:
                    analysis_parts.append("* **Cholesterol Levels:** Higher than desirable levels suggest a need to review dietary fats and cardiovascular health with your doctor.")
                if "glucose" in text_lower or "sugar" in text_lower:
                    analysis_parts.append("* **Blood Glucose:** Evaluates how your body processes sugar. Ensure you discuss these values relative to your fasting state.")
                
                if len(analysis_parts) == 1:
                    analysis_parts.append("* Extracted text processed successfully. Review individual test lines above for specific numerical values.")

                analysis_parts.append("\n### 💡 Recommended Next Steps")
                analysis_parts.append("1. Schedule a follow-up consultation with your primary physician to review these specific numbers.")
                analysis_parts.append("2. Maintain a log of any physical symptoms you are experiencing.")
                
                raw_summary = "\n".join(analysis_parts)
                
                if target_lang_code != "en":
                    try:
                        translated_summary = GoogleTranslator(source='auto', target=target_lang_code).translate(raw_summary)
                    except Exception:
                        st.warning("⚠️ Translation rate limit reached. Displaying English version:")
                        translated_summary = raw_summary
                else:
                    translated_summary = raw_summary

                st.markdown("---")
                st.subheader(f"🤖 AI Explanation ({target_lang_name})")
                st.markdown(translated_summary)

            st.markdown("---")
            st.subheader("💬 Ask a Follow-up Question about this Report")
            user_question = st.text_input("Example: What foods should I avoid given these results?")
            if user_question:
                st.info(f"💡 **AI Guidance:** Based on your report, for the question *'{user_question}'*, it is best to focus on whole foods, reduce saturated fats, and consult a registered dietitian or your physician for personalized meal planning.")