# 📄 AI Resume Analyzer

An AI-powered resume analysis tool built with Google Gemini API and Streamlit.

## What It Does

- **General Analysis** — Upload your resume and get detailed feedback on strengths, weaknesses, missing skills, project quality, and ATS keywords
- **Job Match Analysis** — Paste any job description and get a match score with specific suggestions to tailor your resume

## Results
- Instant analysis in 10-15 seconds
- Structured feedback with actionable improvement steps
- Downloadable analysis report

## Tech Stack
Python · Google Gemini API · LangChain · PyPDF2 · Streamlit · python-dotenv

## How to Run

### 1. Clone the repo
```bash
git clone https://github.com/Rosesharma13/resume-analyzer.git
cd resume-analyzer
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API key
Create a `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key_here
```
Get your free API key at: https://aistudio.google.com/app/apikey

### 4. Run the app
```bash
streamlit run app.py
```

## Project Structure
```
resume-analyzer/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example        # API key 
├── .gitignore          # Ignores .env file
└── README.md           # Project documentation
```

## Screenshots


---
Built by [Rose Sharma](https://linkedin.com/in/rose-sharma13) · AI/ML Engineer
