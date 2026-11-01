# AI Job Application Assistant

A Streamlit web application that helps job seekers compare their resume with a job description using Generative AI. Upload a PDF resume, paste a target job posting, and receive a structured match analysis powered by the Groq API.

## Problem Statement

Applying for jobs often means rewriting a resume and preparing for interviews without clear feedback on how well your experience matches a specific role. Manual comparison is slow and easy to get wrong. This project gives candidates a fast, honest AI-assisted review of resume-to-job fit so they can improve their materials and prepare more effectively.

## Main Features

- Upload a PDF resume and extract text locally with `pypdf`
- Paste a job description for comparison
- Request AI analysis with a single **Analyze Application** button
- Receive a structured AI analysis dashboard with match score, matching skills, missing skills, relevant experience, suggestions, a tailored professional summary, and interview questions
- Keep the last successful analysis visible across Streamlit reruns using session state
- Download the analysis as Markdown and, when parsing succeeds, as JSON
- Fall back to the original Groq response if structured JSON parsing fails
- Load the Groq API key securely from a local `.env` file

## Technologies Used

- **Python**
- **Streamlit** — web UI and session-state persistence
- **Groq API** (`groq`) — Generative AI analysis
- **pypdf** — local PDF text extraction
- **python-dotenv** — environment variable loading for the API key

## How the Application Works

1. The user uploads a resume PDF. Text is extracted on the local machine.
2. The user pastes a job description into a text area.
3. When the user clicks **Analyze Application**, the app validates inputs and sends the extracted resume text and job description to Groq.
4. Groq returns a JSON analysis. The app stores both the raw response and the parsed result in Streamlit session state, then shows a dashboard in the UI.
5. If JSON parsing fails, the original response is shown as Markdown so the app does not break.
6. The user can download the analysis or continue interacting with the app without triggering another API call until they click **Analyze Application** again.

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

## Privacy Note

Your resume PDF is processed locally for text extraction. Extracted resume text and the job description are sent to Groq **only when you explicitly click Analyze Application**. The Groq API key is stored in a local `.env` file and should never be committed to Git.
