import streamlit as st
import PyPDF2
import os
from groq import Groq

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .title { color: #1A56A0; font-size: 2.2rem; font-weight: 700; }
    .subtitle { color: #555; font-size: 1rem; margin-bottom: 1.5rem; }
    .section-box {
        background: white; border-radius: 10px; padding: 1.5rem;
        margin: 1rem 0; border-left: 4px solid #1A56A0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    </style>
""", unsafe_allow_html=True)


def get_client():
    try:
        api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    except Exception:
        api_key = os.environ.get("GROQ_API_KEY")
    return Groq(api_key=api_key)


def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()


def analyze_resume(resume_text, job_role):
    client = get_client()
    prompt = f"""You are an expert AI career advisor and technical recruiter with 10+ years of experience hiring for AI/ML, Data Science, and Software Engineering roles.

Analyze the following resume for the role: **{job_role}**

Resume:
---
{resume_text}
---

Provide honest analysis in this format:

## 1. Overall Score
Score out of 10 with a one-line verdict.

## 2. Strengths (Top 3-5)
What is genuinely strong for the target role.

## 3. Weaknesses & Gaps (Top 3-5)
Be direct and specific about what is missing or weak.

## 4. Skills Assessment
- Skills present and relevant to {job_role}
- Important skills missing for {job_role}

## 5. Project Feedback
Are the projects strong enough? What can be improved?

## 6. Specific Improvements (5 Action Items)
Specific, actionable things to improve this resume.

## 7. ATS Keywords Missing
Important keywords for {job_role} missing from this resume.

Be direct and specific. No generic advice."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.3
    )
    return response.choices[0].message.content


def analyze_job_match(resume_text, job_description):
    client = get_client()
    prompt = f"""You are an expert technical recruiter. Compare the resume against the job description.

Resume:
---
{resume_text}
---

Job Description:
---
{job_description}
---

Provide analysis in this format:

## Match Score
Percentage match with explanation.

## Matching Skills & Experience
What directly matches the job requirements.

## Missing Requirements
What the job needs that the resume lacks.

## Recommendation
Should they apply? What to highlight in cover letter?

## Suggested Resume Tweaks
3-4 specific changes to better target this job.

Be direct and specific."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0.3
    )
    return response.choices[0].message.content


# UI
st.markdown('<p class="title">📄 AI Resume Analyzer</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload your resume and get honest AI-powered feedback instantly</p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 General Analysis", "🎯 Job Match Analysis"])

with tab1:
    st.subheader("Analyze Your Resume")
    job_role = st.text_input("Target Role", placeholder="e.g. Junior AI/ML Engineer, Data Scientist")
    uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"], key="general")

    if st.button("🔍 Analyze Resume", key="btn_general"):
        if not uploaded_file:
            st.warning("Please upload your resume PDF.")
        elif not job_role:
            st.warning("Please enter your target role.")
        else:
            with st.spinner("Analyzing your resume..."):
                try:
                    resume_text = extract_text_from_pdf(uploaded_file)
                    if len(resume_text) < 100:
                        st.error("Could not extract text. Make sure it's not a scanned image PDF.")
                    else:
                        analysis = analyze_resume(resume_text, job_role)
                        st.success("Analysis complete!")
                        st.markdown('<div class="section-box">', unsafe_allow_html=True)
                        st.markdown(analysis)
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.download_button("📥 Download Analysis", data=analysis, file_name="resume_analysis.txt", mime="text/plain")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

with tab2:
    st.subheader("Match Resume to a Job Description")
    uploaded_file2 = st.file_uploader("Upload Resume (PDF only)", type=["pdf"], key="match")
    job_desc = st.text_area("Paste Job Description Here", height=200, placeholder="Copy and paste the full job description.")

    if st.button("🎯 Check Job Match", key="btn_match"):
        if not uploaded_file2:
            st.warning("Please upload your resume PDF.")
        elif not job_desc:
            st.warning("Please paste the job description.")
        else:
            with st.spinner("Matching your resume to the job..."):
                try:
                    resume_text = extract_text_from_pdf(uploaded_file2)
                    if len(resume_text) < 100:
                        st.error("Could not extract text. Make sure it's not a scanned image PDF.")
                    else:
                        match_result = analyze_job_match(resume_text, job_desc)
                        st.success("Match analysis complete!")
                        st.markdown('<div class="section-box">', unsafe_allow_html=True)
                        st.markdown(match_result)
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.download_button("📥 Download Match Report", data=match_result, file_name="job_match_report.txt", mime="text/plain")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

st.markdown("---")
st.markdown("<p style='text-align:center; color:#aaa; font-size:0.8rem;'>Built by Rose Sharma · AI/ML Engineer</p>", unsafe_allow_html=True)
