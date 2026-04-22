import streamlit as st
import PyPDF2

from src.parser import clean_text
from src.matcher import match_resume
from src.skills import extract_skills

# Page setup
st.set_page_config(page_title="Resume Screening System", page_icon="📄", layout="wide")

# 🎨 MODERN UI CSS (WORKING)
st.markdown("""
<style>

/* BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

/* MAIN CONTAINER TEXT */
[data-testid="stAppViewContainer"] * {
    color: white;
}

/* TITLE */
.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: #38bdf8;
    margin-bottom: 10px;
}

/* LABELS */
label {
    font-size: 20px !important;
    font-weight: bold !important;
}

/* INPUT BOX */
textarea {
    background-color: #111827 !important;
    color: #e5e7eb !important;
    border-radius: 10px !important;
    border: 1px solid #38bdf8 !important;
}

/* RADIO */
div[data-baseweb="radio"] label {
    font-size: 18px !important;
    color: #e5e7eb !important;
}

/* FILE UPLOADER */
section[data-testid="stFileUploader"] {
    background-color: #111827;
    border-radius: 10px;
    padding: 10px;
}

/* BUTTON */
div.stButton > button {
    background: linear-gradient(45deg, #ff416c, #ff4b2b);
    color: white !important;
    font-size: 18px !important;
    font-weight: bold;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    transition: 0.3s;
}

div.stButton > button:hover {
    transform: scale(1.05);
    background: linear-gradient(45deg, #ff4b2b, #ff416c);
}

/* RESULT CARD (GLASS EFFECT) */
.card {
    background: rgba(255, 255, 255, 0.08);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0px 8px 30px rgba(0,0,0,0.5);
    margin-top: 20px;
}

/* RESULT TEXT */
.result {
    font-size: 20px;
    margin: 10px 0;
}

/* COLORS */
.high { color: #22c55e; font-weight: bold; }
.medium { color: #facc15; font-weight: bold; }
.low { color: #ef4444; font-weight: bold; }

.skills { color: #38bdf8; }
.missing { color: #ef4444; }

</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">📄 Resume Screening System</div>', unsafe_allow_html=True)

# Layout
col1, col2 = st.columns(2)

with col1:
    job_desc = st.text_area("💼 Enter Job Description", height=200)

with col2:
    option = st.radio(
        "📄 Choose Resume Input",
        ["Paste Resume Text", "Upload Resume (PDF)"]
    )

    resume = ""

    if option == "Paste Resume Text":
        resume = st.text_area("📄 Paste Resume Text", height=200)

    else:
        uploaded_file = st.file_uploader("📥 Upload Resume (PDF)", type=["pdf"])

        if uploaded_file:
            try:
                reader = PyPDF2.PdfReader(uploaded_file)
                pdf_text = ""

                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        pdf_text += text

                resume = pdf_text

            except:
                st.error("Error reading PDF")

# Button
if st.button("🚀 Analyze Candidate"):

    if job_desc.strip() == "" or resume.strip() == "":
        st.warning("⚠ Please fill both fields")

    else:
        clean_job = clean_text(job_desc)
        clean_resume = clean_text(resume)

        score = match_resume(clean_job, clean_resume)

        job_skills = extract_skills(clean_job)
        resume_skills = extract_skills(clean_resume)

        missing_skills = list(set(job_skills) - set(resume_skills))

        # Ranking
        if score > 70:
            rank = "⭐ Highly Suitable"
            rank_class = "high"
        elif score > 40:
            rank = "👍 Moderately Suitable"
            rank_class = "medium"
        else:
            rank = "❌ Not Suitable"
            rank_class = "low"

        # Display
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown(
            f"<div class='result'>📊 Match Score: <span class='{rank_class}'>{score}%</span></div>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<div class='result'>🏆 Ranking: <span class='{rank_class}'>{rank}</span></div>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<div class='result'>🧠 Resume Skills: <span class='skills'>{resume_skills}</span></div>",
            unsafe_allow_html=True
        )

        if missing_skills:
            st.markdown(
                f"<div class='result missing'>⚠ Missing Skills: {missing_skills}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div class='result high'>✅ No Missing Skills</div>",
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)