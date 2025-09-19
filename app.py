import os
import warnings
import logging

# 🚫 Hide TensorFlow & Keras logs/warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 0 = all logs, 1 = info, 2 = warnings, 3 = errors only
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.getLogger("tensorflow").setLevel(logging.ERROR)

import streamlit as st
from modules import ai_analyzer, file_handler, visualizer, web_scraper

# ✅ Streamlit page setup
st.set_page_config(page_title="AI Data Analyzer", layout="wide")

st.title("🧠 AI-Powered Data Analyzer with Python")
st.markdown("Upload a file or enter a URL to analyze sentiment, summarize, and extract insights using AI.")

# 📌 Input type selection
option = st.radio("Choose Input Type:", ["📁 File Upload", "🌐 URL"])

text = ""  # 🔒 Ensure default

# =========================
# 📁 File Upload Section
# =========================
if option == "📁 File Upload":
    uploaded = st.file_uploader("Upload a file", type=["pdf", "csv", "xlsx", "docx", "txt", "png", "jpg", "jpeg"])
    if uploaded:
        ext = uploaded.name.split(".")[-1].lower()
        with st.spinner("Extracting content..."):
            if ext == "pdf":
                text = file_handler.extract_from_pdf(uploaded)
            elif ext == "csv":
                text = file_handler.extract_from_csv(uploaded)
            elif ext == "xlsx":
                text = file_handler.extract_from_excel(uploaded)
            elif ext == "docx":
                text = file_handler.extract_from_docx(uploaded)
            elif ext == "txt":
                text = file_handler.extract_from_txt(uploaded)
            elif ext in ["png", "jpg", "jpeg"]:
                text = file_handler.extract_from_image(uploaded)
            else:
                st.error("❌ Unsupported file type.")
                text = ""

# =========================
# 🌐 URL Input Section
# =========================
else:
    url = st.text_input("Enter a URL to analyze:")
    if url:
        with st.spinner("Scraping website content..."):
            text = web_scraper.scrape_text_from_url(url)

# =========================
# 🧠 Analysis Section
# =========================
if text and text.strip() and "No readable content" not in text:
    st.subheader("📄 Extracted Text")
    st.text_area("Text", value=text, height=300)

    if st.button("🔍 Analyze"):
        with st.spinner("Analyzing with AI..."):
            sentiment, subjectivity = ai_analyzer.analyze_sentiment(text)
            summary = ai_analyzer.summarize_text(text)
            keywords = ai_analyzer.extract_keywords(text)

        st.success("✅ Analysis Complete")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📈 Sentiment Score")
            visualizer.plot_sentiment(sentiment)
            st.write(f"🔍 Subjectivity: `{subjectivity:.2f}`")

        with col2:
            st.subheader("🧠 Word Cloud")
            visualizer.display_wordcloud(text)

        st.subheader("📝 Summary")
        st.info(summary)

        st.subheader("🔑 Keywords")
        st.write(", ".join(keywords))

else:
    if "No readable content" in text:
        st.warning("⚠️ The uploaded file or URL does not contain any extractable text.")
    elif text.strip() == "":
        st.info("Please upload a file or enter a valid URL to begin analysis.")
