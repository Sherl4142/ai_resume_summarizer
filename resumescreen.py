import os
import glob
import fitz  # PyMuPDF for PDFs
import docx  # python-docx for DOCX files
import pandas as pd
import nltk
from nltk.corpus import stopwords
import spacy
import matplotlib.pyplot as plt

# ---------------------------
# NLTK setup
# ---------------------------
nltk.download('stopwords')
nltk.download('punkt')

# ---------------------------
# Load spaCy model
# ---------------------------
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("SpaCy model not found. Run: python -m spacy download en_core_web_sm")
    raise

# ---------------------------
# Helper functions
# ---------------------------
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def clean_text_spacy(text):
    doc = nlp(text.lower())
    tokens = [token.text for token in doc if token.is_alpha and not token.is_stop]
    return ' '.join(tokens)

def score_resume(text, required_skills):
    found = [skill for skill in required_skills if skill.lower() in text.lower()]
    missing = list(set(required_skills) - set(found))
    match_ratio = len(found) / len(required_skills)
    
    if match_ratio >= 0.75:
        fit = 'High Fit'
    elif match_ratio >= 0.4:
        fit = 'Medium Fit'
    else:
        fit = 'Low Fit'
    
    return pd.Series([fit, found, missing])

# ---------------------------
# Main evaluation function
# ---------------------------
def evaluate_resume(folder_path):
    """
    Evaluates resumes in a folder (PDF & DOCX), scores them based on required skills,
    and plots fit distribution. Returns a DataFrame.
    """
    # Collect files
    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
    docx_files = glob.glob(os.path.join(folder_path, "*.docx"))
    all_files = pdf_files + docx_files
    
    if not all_files:
        print(f"No PDF or DOCX files found in {folder_path}")
        return pd.DataFrame()
    
    # Extract text
    data = []
    for file in all_files:
        ext = os.path.splitext(file)[1].lower()
        if ext == ".pdf":
            text = extract_text_from_pdf(file)
        elif ext == ".docx":
            text = extract_text_from_docx(file)
        else:
            continue
        
        data.append({
            "file_name": os.path.basename(file),
            "resume_text": text
        })
    
    df_resumes = pd.DataFrame(data)
    
    # Clean text
    df_resumes["cleaned_text"] = df_resumes["resume_text"].apply(clean_text_spacy)
    
    # Define required skills
    required_skills = [
        "python", "sql", "machine learning", "data visualization", "nlp",
        "cloud platforms", "resume parsing", "dashboarding", "streamlit", "communication"
    ]
    
    # Score resumes
    df_resumes[["fit_level", "matched_skills", "missing_skills"]] = \
        df_resumes["cleaned_text"].apply(lambda x: score_resume(x, required_skills))
    
    # Sort by fit
    fit_order = {"High Fit": 0, "Medium Fit": 1, "Low Fit": 2}
    df_resumes["fit_rank"] = df_resumes["fit_level"].map(fit_order)
    df_sorted = df_resumes.sort_values(by="fit_rank").drop(columns=["cleaned_text", "fit_rank"])
    
    # Plot distribution
    plt.figure(figsize=(6, 6))
    df_sorted["fit_level"].value_counts().plot.pie(
        autopct="%1.2f%%", colors=["#66b3ff", "#99ff99", "#ff9999"]
    )
    plt.title("Resume Fit Distribution")
    plt.ylabel("")
    plt.show()
    
    return df_sorted[["file_name", "fit_level", "matched_skills", "missing_skills"]]


