# 📄 AI Resume Summarizer

## **Problem Statement**
Screening multiple resumes manually is time-consuming and error-prone. The **AI Resume Summarizer** automates this process by extracting text from PDF and DOCX resumes, evaluating candidates based on predefined skills, and generating an interactive dashboard for quick decision-making.

---

## **Features**
- Upload and evaluate multiple resumes (PDF/DOCX).  
- Extract and match technical skills like Python, SQL, ML, NLP.  
- Compute **fit score** and classify **fit level** (High, Medium, Low).  
- Interactive dashboards: bar chart for fit scores, heatmap for skill matches.  

---

## **Installation**

1. Clone the repository:  
```bash
git clone <repo-url>
cd ai_resume_summarizer
Create a virtual environment (optional but recommended):

python -m venv venv


Activate the environment:

Windows: venv\Scripts\activate

Mac/Linux: source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Usage

Run the Streamlit app:

streamlit run main.py


Upload resumes in PDF or DOCX format via the browser.

View fit scores, matched skills, and dashboard visualizations.

Technologies Used

Python, Streamlit, PyMuPDF, python-docx, Pandas, Plotly Express

