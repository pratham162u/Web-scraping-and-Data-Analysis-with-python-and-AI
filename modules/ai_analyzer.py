from textblob import TextBlob
from transformers import pipeline
import re
import textwrap

# Load summarizer once globally
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def summarize_text(text):
    # Clean and normalize
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", "", text)

    if not text or len(text.split()) < 30:
        return "Text too short to summarize."

    # Split into ~800-word chunks at sentence breaks
    chunks = textwrap.wrap(text, 1200, break_long_words=False, replace_whitespace=False)

    summaries = []
    for chunk in chunks:
        if len(chunk.split()) < 30:
            continue  # Avoid summarizing tiny content

        try:
            result = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
            summary = result[0].get("summary_text", "").strip()
            if summary:
                summaries.append(summary)
            else:
                summaries.append("[Empty summary]")
        except Exception as e:
            summaries.append(f"[Error summarizing chunk: {str(e)}]")

    if not summaries:
        return "No meaningful summary generated."
    
    return "\n\n".join(summaries)

def extract_keywords(text):
    return list(set(TextBlob(text).noun_phrases))[:10]
