# AI Job Application Assistant

A Streamlit web application that helps job seekers compare their resume with a job description using Generative AI. Upload a PDF or DOCX resume, paste a target job posting, and receive a structured match analysis and a tailored cover letter powered by the Groq API.

## Problem Statement

Applying for jobs often means rewriting a resume and preparing for interviews without clear feedback on how well your experience matches a specific role. Manual comparison is slow and easy to get wrong. This project gives candidates a fast, honest AI-assisted review of resume-to-job fit so they can improve their materials and prepare more effectively.

## Main Features

- Upload a **PDF or DOCX** resume and extract the text locally (`pypdf` for PDF, `python-docx` for DOCX, including text stored in tables)
- Paste a job description for comparison
- Request AI analysis with a single **Analyze Application** button
- Get a **weighted match score** calculated in Python (not by the AI), based on four categories:
  - Technical Skills (40%)
  - Experience & Projects (30%)
  - Education & Qualifications (15%)
  - Responsibilities Alignment (15%)
- Review a structured dashboard with category evidence, matching skills, missing or unclear skills, relevant experience, improvement suggestions, a tailored professional summary, and interview questions
- Generate an **AI cover letter** from your resume and the job description, with an optional company name and job title and a choice of tone (Professional, Formal or Confident)
- Edit the cover letter in the app, then download it as **DOCX** or **TXT**
- Keep results visible across Streamlit reruns using session state; old results are cleared automatically when you upload a different resume or change the job description
- Download the analysis as a Markdown report and as JSON
- Handle problems gracefully: encrypted or scanned PDFs, corrupted files, cut-off AI responses, invalid JSON, and API errors (authentication and rate limits) all show clear messages
- Load the Groq API key securely from a local `.env` file

## Honesty by Design

The prompts instruct the AI to use only facts found in the resume and never invent skills, experience, education or projects. Missing skills mean "not clearly demonstrated", not "definitely absent". AI output can still contain mistakes, so always review the analysis and edit the cover letter before using it.

## Technologies Used

- **Python**
- **Streamlit**: web UI and session-state persistence
- **Groq API** (`groq`): Generative AI analysis and cover letter writing (model: `openai/gpt-oss-20b`)
- **pypdf**: local PDF text extraction
- **python-docx**: local DOCX text extraction and cover letter DOCX export
- **python-dotenv**: environment variable loading for the API key

## How the Application Works

1. The user uploads a resume (PDF or DOCX). Text is extracted on the local machine.
2. The user pastes a job description into a text area.
3. When the user clicks **Analyze Application**, the app validates the inputs and sends the resume text and job description to Groq.
4. Groq returns a JSON analysis with a 0 / 50 / 100 score for each category. The app calculates the final weighted score in Python, stores the result in Streamlit session state, and shows the dashboard.
5. If the response is cut off or is not valid JSON, the app explains the problem instead of breaking.
6. The user can optionally enter a company name, job title and tone, then click **Generate Cover Letter**. The letter appears in an editable box and can be downloaded as DOCX or TXT.
7. Results stay on screen without extra API calls until the user clicks a generate button again.

## Installation (Windows)

### 1. Prerequisites

- Python 3.10 or newer installed on Windows
- A Groq API key from [https://console.groq.com](https://console.groq.com)

### 2. Open the project folder

```powershell
cd "D:\python project\AI-Job-Application-Assistant"
```

### 3. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation, run this once for your user account, then activate again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure the Groq API key

1. Create a file named `.env` in the project root (`AI-Job-Application-Assistant`).
2. Add your key in this format (do not share or commit this file):

```env
GROQ_API_KEY=your_groq_api_key_here
```

3. Save the file. The app loads `.env` from the project folder automatically.

### 6. Run the Streamlit application

```powershell
streamlit run app.py
```

Then open the local URL shown in the terminal (usually `http://localhost:8501`).

## Project Structure

```text
AI-Job-Application-Assistant/
├── app.py             # Streamlit app: extraction, AI calls, dashboard, cover letter
├── requirements.txt   # Python dependencies
├── README.md          # Project documentation
├── .gitignore         # Keeps .env, virtual environments and cache files out of Git
└── .env               # Your private Groq API key (local only, never committed)
```

## Limitations

- Scanned or image-only resumes are not supported because the app does not use OCR. Upload a text-based PDF or DOCX.
- Only the first 18,000 characters of the resume and the first 10,000 characters of the job description are sent to the AI.
- The match score is an AI-assisted estimate. It does not predict hiring outcomes.
- AI-generated text can contain errors. Review everything before sending it to an employer.

## Privacy Note

Your resume file is processed locally for text extraction. The extracted resume text and the job description are sent to Groq **only when you explicitly click Analyze Application or Generate Cover Letter**. The Groq API key is stored in a local `.env` file and should never be committed to Git.
