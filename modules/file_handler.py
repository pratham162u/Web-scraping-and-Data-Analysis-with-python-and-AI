import pandas as pd
import pytesseract
import docx
import fitz
from PIL import Image, ImageFilter, ImageEnhance

# ✅ Set path to Tesseract executable (you must have it installed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # 🔄 Update if different

# 🔒 Word limit to improve speed and prevent overload
MAX_WORDS = 3000

def truncate_text(text):
    """Trims text to first N words for safety."""
    return " ".join(text.split()[:MAX_WORDS])

def extract_from_pdf(file):
    try:
        text = ""
        doc = fitz.open(stream=file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
        if not text.strip():
            text = "No readable content found in this file."
    except Exception as e:
        text = f"PDF extraction failed: {str(e)}"
    return truncate_text(text)

def extract_from_csv(file):
    try:
        df = pd.read_csv(file)
        text = df.to_string()
    except Exception:
        text = "Unable to read CSV file."
    if not text.strip():
        text = "No readable content found in this file."
    return truncate_text(text)

def extract_from_excel(file):
    try:
        df = pd.read_excel(file)
        text = df.to_string()
    except Exception:
        text = "Unable to read Excel file."
    if not text.strip():
        text = "No readable content found in this file."
    return truncate_text(text)

def extract_from_docx(file):
    try:
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
    except Exception:
        text = "Unable to read DOCX file."
    if not text.strip():
        text = "No readable content found in this file."
    return truncate_text(text)

def extract_from_txt(file):
    try:
        text = file.read().decode("utf-8")
    except Exception:
        text = "Unable to read TXT file."
    if not text.strip():
        text = "No readable content found in this file."
    return truncate_text(text)

def extract_from_image(file):
    try:
        img = Image.open(file).convert('L')  # Grayscale
        img = img.filter(ImageFilter.SHARPEN)
        img = ImageEnhance.Contrast(img).enhance(2)
        text = pytesseract.image_to_string(img)
    except Exception as e:
        text = f"Image OCR failed: {str(e)}"
    if not text.strip():
        text = "No readable content found in this image."
    return truncate_text(text)
