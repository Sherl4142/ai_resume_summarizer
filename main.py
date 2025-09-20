import os
import streamlit as st
import pandas as pd
import plotly.express as px
import fitz  # PyMuPDF
import docx

# -----------------------------
# 1️⃣ Setup
# -----------------------------
st.set_page_config(page_title="AI Resume Summarizer", page_icon="📄", layout="wide")

# Ensure temp_resume folder exists
os.makedirs("temp_resume", exist_ok=True)

st.title("📄 AI Resume Summarizer - Multi Resume Dashboard")

# -----------------------------
# 2️⃣ File Upload
# -----------------------------
uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
if uploaded_file is not None:
    save_path = os.path.join("temp_resume", uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Resume saved to {save_path}")

# -----------------------------
# 3️⃣ Function to Extract Resume Text
# -----------------------------
def extract_text(file_path: str) -> str:
    text = ""
    if file_path.endswith(".pdf"):
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    return text

# -----------------------------
# 4️⃣ Skills & Evaluation Logic
# -----------------------------
SKILLS = ["Python", "Java", "C++", "SQL", "Machine Learning", "Deep Learning", "NLP"]

def evaluate_resume(resume_text: str) -> dict:
    matched_skills = [skill for skill in SKILLS if skill.lower() in resume_text.lower()]
    fit_score = min(len(matched_skills) / len(SKILLS) * 100, 100)
    if fit_score >= 70:
        fit_level = "High Fit ✅"
    elif fit_score >= 40:
        fit_level = "Medium Fit ⚠️"
    else:
        fit_level = "Low Fit ❌"
    return {"matched_skills": matched_skills, "fit_score": fit_score, "fit_level": fit_level}

# -----------------------------
# 5️⃣ Scan All Resumes in temp_resume
# -----------------------------
resume_files = [f for f in os.listdir("temp_resume") if f.endswith((".pdf", ".docx"))]

if resume_files:
    st.subheader("🤖 Evaluating All Resumes...")
    results = []

    for file_name in resume_files:
        path = os.path.join("temp_resume", file_name)
        text = extract_text(path)
        eval_result = evaluate_resume(text)
        results.append({
            "Resume": file_name,
            "Fit Score": eval_result["fit_score"],
            "Fit Level": eval_result["fit_level"],
            "Matched Skills": ", ".join(eval_result["matched_skills"]) if eval_result["matched_skills"] else "None"
        })

    df_results = pd.DataFrame(results)
    st.dataframe(df_results)

    # -----------------------------
    # 6️⃣ Aggregate Dashboard
    # -----------------------------
    st.subheader("📊 Aggregate Dashboard")

    fig_fit = px.bar(df_results, x="Resume", y="Fit Score", color="Fit Score",
                     color_continuous_scale=["red", "yellow", "green"],
                     title="Resume Fit Scores")
    st.plotly_chart(fig_fit, use_container_width=True)

    # Skill match heatmap
    st.subheader("📊 Skill Match Overview")
    skill_matrix = []
    for file_name in resume_files:
        text = extract_text(os.path.join("temp_resume", file_name))
        skill_matrix.append([1 if skill.lower() in text.lower() else 0 for skill in SKILLS])
    df_skills = pd.DataFrame(skill_matrix, columns=SKILLS, index=resume_files)

    fig_skills = px.imshow(df_skills, text_auto=True, aspect="auto",
                           color_continuous_scale=["white", "green"],
                           title="Skills Matched per Resume")
    st.plotly_chart(fig_skills, use_container_width=True)
else:
    st.info("No resumes found in temp_resume folder. Upload a PDF or DOCX to begin evaluation.")
