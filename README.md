# 🩺 Multi-Modal Medical & Health Report Explainer

An AI-powered web application designed to bridge the communication gap between complex clinical lab tests and patients. It parses PDF and image reports using OCR, translates medical jargon into plain insights, and supports real-time multilingual accessibility.

## 🚀 Live Demo
👉 **[View Live Streamlit App](https://medical-report-explainer-kcvbgsmb9kvxbjzvnndcwx.streamlit.app)**

---

## 🛠️ Tech Stack & Architecture
* **Python** (Core logic)
* **Streamlit** (Web UI & Cloud Deployment)
* **PyMuPDF (`fitz`)** (PDF document parsing)
* **Tesseract OCR (`pytesseract`)** (Text extraction from images/scans)
* **Deep-Translator** (Real-time multilingual translation)

---

## ✨ Key Features
* **Multi-Modal Input:** Upload clinical lab tests as PDFs or scanned image formats (PNG, JPG).
* **Automated OCR & Parsing:** Extracts raw textual data smoothly from diverse document formats.
* **Multilingual Support:** Translate health report summaries instantly into Spanish, Hindi, Tamil, French, German, Arabic, and Chinese.
* **Resilient Error Handling:** Gracefully manages translation rate limits and provides fallback warnings without crashing.

---

## 💻 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/HariVishnuN/medical-report-explainer.git](https://github.com/HariVishnuN/medical-report-explainer.git)
   cd medical-report-explainer