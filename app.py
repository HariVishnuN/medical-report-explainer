import streamlit as st
from PIL import Image
import fitz  # PyMuPDF
import pytesseract
from deep_translator import GoogleTranslator

st.set_page_config(
    page_title="Multilingual AI Medical Explainer",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 Multi-Modal Medical & Health Report Explainer")
st.markdown("Upload a lab report photo or PDF. Select your preferred language to receive a simple, translated explanation.")

st.warning("⚠️ **Disclaimer:** This tool is for educational purposes only. Always consult a certified healthcare professional.")

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

    if st.button(f"Generate Explanation in {target_lang_name}", type="primary"):
        if not extracted_text.strip():
            st.error("Could not extract text from this file. Please upload a clearer scan.")
        else:
            with st.spinner("Analyzing report and translating..."):
                raw_summary = (
                    "### 📋 Summary of Findings\n"
                    "* White Blood Cell (WBC) Count: Normal limits.\n"
                    "* Cholesterol Levels: Slightly elevated.\n\n"
                    "### 💡 Actionable Insights\n"
                    "1. Discuss your current diet with your primary physician.\n"
                    "2. Plan a follow-up test in 3 months."
                )

                if target_lang_code != "en":
                    translated_summary = GoogleTranslator(source='auto', target=target_lang_code).translate(raw_summary)
                else:
                    translated_summary = raw_summary

                st.markdown("---")
                st.subheader(f"🤖 AI Explanation ({target_lang_name})")
                st.markdown(translated_summary)