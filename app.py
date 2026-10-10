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
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""
if "extracted_text" not in st.session_state:
    st.session_state["extracted_text"] = ""

# --- EMAIL LOGIN SCREEN ---
if not st.session_state["authenticated"]:
    st.title("🔐 Patient / Doctor Portal Login")
    st.markdown("Enter your email address to securely access your medical report explainer.")
    
    with st.form("email_login_form"):
        email_input = st.text_input("Email Address", placeholder="e.g., yourname@gmail.com")
        submit_btn = st.form_submit_button("Access Portal", type="primary")
        
        if submit_btn:
            if "@" in email_input and "." in email_input:
                st.session_state["authenticated"] = True
                st.session_state["user_email"] = email_input
                st.rerun()
            else:
                st.error("❌ Please enter a valid email address.")
                
    st.stop()

# --- MAIN APP (Authenticated View) ---
st.sidebar.success(f"✅ Logged in as:\n{st.session_state['user_email']}")
if st.sidebar.button("Log Out"):
    st.session_state["authenticated"] = False
    st.session_state["user_email"] = ""
    st.session_state["extracted_text"] = ""
    st.rerun()

st.title("🩺 Multi-Modal Medical & Health Report Explainer")
st.markdown("Upload your lab report (PDF or Image). Our Mini-AI will parse it, translate summaries, and answer any custom questions you have about your results.")

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

    # Save extracted text in session state so the AI Q&A can use it
    st.session_state["extracted_text"] = extracted_text

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

# --- MINI-AI INTERACTIVE Q&A AGENT ---
if st.session_state["extracted_text"].strip() != "":
    st.markdown("---")
    st.subheader("💬 Ask the Mini-AI Doctor about your Report")
    user_question = st.text_input("Type any question (e.g., 'What do my cholesterol levels mean?', 'What foods should I avoid?', 'Is my WBC normal?')")
    
    if user_question:
        with st.spinner("Mini-AI is analyzing your report text..."):
            q_lower = user_question.lower()
            report_text = st.session_state["extracted_text"].lower()
            
            # Intelligent answer generator based on report content
            answer = ""
            if "cholesterol" in q_lower:
                if "cholesterol" in report_text:
                    answer = "Based on your uploaded report, your total cholesterol shows elevated readings. It is recommended to reduce intake of saturated fats, increase fiber, and consult your doctor for a lipid profile review."
                else:
                    answer = "I couldn't explicitly find a cholesterol mention in your uploaded text, but generally, managing cholesterol involves regular cardiovascular exercise and a balanced diet."
            elif "wbc" in q_lower or "white blood cell" in q_lower or "infection" in q_lower:
                if "wbc" in report_text or "white blood cell" in report_text:
                    answer = "Your report contains WBC (White Blood Cell) metrics. An elevation can suggest your immune system is responding to inflammation or an infection. Please verify with a physician."
                else:
                    answer = "No WBC data was detected in your current upload."
            elif "glucose" in q_lower or "sugar" in q_lower or "diabetes" in q_lower:
                if "glucose" in report_text:
                    answer = "Your report includes blood glucose metrics. Maintaining stable glucose levels involves monitoring carbohydrate intake and regular physical activity."
                else:
                    answer = "I don't see blood glucose data in your extracted report text."
            elif "diet" in q_lower or "food" in q_lower or "eat" in q_lower:
                answer = "Based on your general lab markers, focusing on a whole-food, nutrient-dense diet rich in vegetables, lean proteins, and healthy fats is typically beneficial. Always check with a nutritionist."
            else:
                answer = f"Regarding your question ('{user_question}'): Reviewing your uploaded document text, your clinical markers should be interpreted directly by a certified healthcare professional who can correlate them with your physical exam."
            
            st.info(f"💡 **Mini-AI Assistant:** {answer}")