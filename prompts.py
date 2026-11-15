"""
prompts.py - Prompt library for the AI Job Application Assistant
=================================================================

Each prompt below uses a DIFFERENT prompt-engineering technique, so the
project shows that prompts were designed for a purpose, not just written.

    1. RCTF_PROMPT           Role-Context-Task-Format   -> full analysis (default)
    2. ONE_SHOT_PROMPT       One example                -> skill-gap table
    3. FEW_SHOT_PROMPT       Several examples           -> interview questions
    4. LONG_DETAILED_PROMPT  Long, rule-heavy prompt    -> strict, safe, high-stakes output

Plus: PROMPT_QUALITY_COMPARISON (worst / average / best) for the README.

Placeholders used in every prompt:
    {resume}              -> the candidate's resume text
    {job_description}     -> the job posting text

Use build_prompt(template, resume, job_description) to fill them in.
(We use .replace() instead of .format() so curly braces in examples never break.)
"""

# ---------------------------------------------------------------------------
# Shared responsible-AI rules (reused so every prompt behaves safely)
# ---------------------------------------------------------------------------
RESPONSIBLE_AI_RULES = """\
- Use ONLY information that appears in the resume. Never invent skills, jobs, degrees, dates, or achievements.
- If something is unclear or not stated, write "Not found in resume" instead of guessing.
- Mark uncertain conclusions with "(uncertain)".
- Do not predict hiring outcomes. Your output is advice, not a decision."""


# ---------------------------------------------------------------------------
# 1. RCTF  (Role - Context - Task - Format)   -> BEST DEFAULT for the main analysis
# ---------------------------------------------------------------------------
RCTF_PROMPT = """\
ROLE:
You are an experienced career coach and technical recruiter who specializes in AI and software roles.

CONTEXT:
A candidate is applying for the job below. They want an honest comparison of their resume against the
job requirements so they can improve their application. The candidate is early-career, so be encouraging
but truthful.

RESUME:
{resume}

JOB DESCRIPTION:
{job_description}

TASK:
Compare the resume to the job description and produce:
1. A match score from 0 to 100 and a match level (Low / Medium / High).
2. Skills the candidate already has that the job requires.
3. Missing or weak skills.
4. Relevant experience or projects from the resume (quote or closely paraphrase them).
5. A tailored 3-sentence professional summary the candidate could put on their CV.
6. Three to five concrete suggestions to improve the resume.

RULES:
""" + RESPONSIBLE_AI_RULES + """

FORMAT:
Return the answer in Markdown using exactly these headings:
## Match Score
## Strong Matches
## Missing or Weak Skills
## Relevant Experience
## Tailored Professional Summary
## Resume Improvement Suggestions
Use bullet points. Keep each bullet to one line.
"""


# ---------------------------------------------------------------------------
# 2. ONE-SHOT  (one worked example)   -> consistent skill-gap table
# ---------------------------------------------------------------------------
ONE_SHOT_PROMPT = """\
You compare a resume with a job description and produce a skill-gap table.
Only mark a skill as "Present" if the resume clearly shows it. Never invent skills.

### Example
Job requires: Python, Machine Learning, TensorFlow, Git, Docker
Resume says: "Built an image classifier in Python using TensorFlow. Studied machine learning."

Output:
| Skill            | Status  | Evidence from resume                         |
|------------------|---------|----------------------------------------------|
| Python           | Present | "Built an image classifier in Python"        |
| Machine Learning | Present | "Studied machine learning"                   |
| TensorFlow       | Present | "using TensorFlow"                           |
| Git              | Missing | Not found in resume                          |
| Docker           | Missing | Not found in resume                          |

Gap summary: 3 of 5 required skills found. Priority to learn: Git, then Docker.

### Your turn
Job description:
{job_description}

Resume:
{resume}

Output (same table format, then a one-line gap summary):
"""


# ---------------------------------------------------------------------------
# 3. FEW-SHOT  (several examples)   -> interview questions in a fixed style
# ---------------------------------------------------------------------------
FEW_SHOT_PROMPT = """\
You are an interviewer preparing questions for a candidate. Create questions in three groups:
Technical, Missing-Skill, and HR/Behavioral. Base them on the job description and the resume.
Each question must be followed by a one-line "What the interviewer wants to hear".

### Example 1
Skill: Overfitting (technical, candidate has ML experience)
Q: Your model has 98% training accuracy but 70% test accuracy. What is happening and how would you fix it?
Looking for: Recognizes overfitting; mentions regularization, more data, dropout, or early stopping.

### Example 2
Skill: Docker (missing from resume)
Q: You have not used Docker yet. How would you go about learning it to deploy a small ML app?
Looking for: Honesty about the gap plus a realistic learning plan (docs, small project, containerizing a Streamlit app).

### Example 3
Skill: Teamwork (HR/Behavioral)
Q: Tell me about a time you disagreed with a teammate on a project. What did you do?
Looking for: A specific story with the situation, the action taken, and the result.

### Your turn
Job description:
{job_description}

Resume:
{resume}

Generate 3 Technical, 3 Missing-Skill, and 2 HR/Behavioral questions in exactly the format shown above.
""" + "Rules:\n" + RESPONSIBLE_AI_RULES + "\n"


# ---------------------------------------------------------------------------
# 4. LONG DETAILED  (step-by-step reasoning, strict rules, self-check)
#    Best when output quality and safety matter more than token cost.
# ---------------------------------------------------------------------------
LONG_DETAILED_PROMPT = """\
You are a careful AI career assistant. Work through the steps below IN ORDER before writing the final answer.

<inputs>
<resume>
{resume}
</resume>
<job_description>
{job_description}
</job_description>
</inputs>

<steps>
Step 1 - Extract: List every required skill, tool, and qualification in the job description.
Distinguish "required" from "nice to have".
Step 2 - Evidence: For each item from Step 1, search the resume for direct evidence.
Classify it as: Strong (clear evidence), Partial (related but not exact), or Missing (no evidence).
Step 3 - Score: Give a match score from 0-100. Weight required skills about twice as much as nice-to-have skills.
Show the one-line reasoning behind the score.
Step 4 - Improve: For Partial skills, suggest how the candidate can reword or expand EXISTING resume content.
For Missing skills, suggest what to learn or build, never what to falsely claim.
Step 5 - Prepare: Write 3 technical, 3 missing-skill, and 2 behavioral interview questions.
Step 6 - Self-check: Re-read your answer and delete any claim that is not supported by the resume text.
</steps>

<rules>
""" + RESPONSIBLE_AI_RULES + """
- Be specific: refer to actual resume lines or job requirements, not generic advice.
- Tone: professional, honest, encouraging.
- Do not output Steps 1-2 or 6; show only the final report.
</rules>

<output_format>
## Match Score  (number + one-line reasoning)
## Skill Evidence Table  (Skill | Required/Nice-to-have | Strong/Partial/Missing | Evidence)
## Resume Improvements  (for Partial and Missing skills)
## Tailored Professional Summary  (3 sentences, only true statements)
## Interview Preparation  (Technical / Missing-Skill / Behavioral)
## Disclaimer  (one sentence: AI suggestions should be reviewed by the user and are not hiring predictions)
</output_format>
"""


# ---------------------------------------------------------------------------
# Registry so app.py can switch between prompts easily
# ---------------------------------------------------------------------------
PROMPTS = {
    "Full Analysis (RCTF)": RCTF_PROMPT,
    "Skill Gap Table (One-shot)": ONE_SHOT_PROMPT,
    "Interview Questions (Few-shot)": FEW_SHOT_PROMPT,
    "Deep Report (Long detailed)": LONG_DETAILED_PROMPT,
}


def build_prompt(template: str, resume: str, job_description: str) -> str:
    """Fill the {resume} and {job_description} placeholders safely."""
    return template.replace("{resume}", resume.strip()).replace(
        "{job_description}", job_description.strip()
    )


# ---------------------------------------------------------------------------
# WORST / AVERAGE / BEST - same task, three quality levels.
# Use this section in your README to show WHY prompt design matters.
# ---------------------------------------------------------------------------
PROMPT_QUALITY_COMPARISON = {
    "worst": {
        "prompt": "Analyze this CV.\n\n{resume}\n\n{job_description}",
        "problems": [
            "No role, so the tone and expertise are unpredictable.",
            "No task details: the model guesses what 'analyze' means.",
            "No output format, so results change every run and are hard to display in Streamlit.",
            "No safety rules, so the model may invent skills (hallucination).",
        ],
    },
    "average": {
        "prompt": (
            "Compare this resume with the job description. List matching skills, "
            "missing skills, and 5 interview questions.\n\n"
            "Resume: {resume}\n\nJob: {job_description}"
        ),
        "problems": [
            "Clear task and short (low token cost), which is good.",
            "Still no role, no format, and no rule against making things up.",
            "Output is usable but inconsistent between runs.",
        ],
    },
    "best": {
        "prompt": RCTF_PROMPT,
        "strengths": [
            "Role gives the model the right expertise and tone.",
            "Context explains the situation (early-career applicant, wants honesty).",
            "Task is numbered, so nothing is skipped.",
            "Rules block hallucination and flags uncertainty (responsible AI).",
            "Fixed Markdown headings make the output predictable and easy to parse in the app.",
        ],
    },
}


# ---------------------------------------------------------------------------
# Quick test: run `python prompts.py` to preview a built prompt.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sample_resume = "Python developer. Built an image classifier with TensorFlow. Completed Google AI Essentials."
    sample_job = "AI Engineer Intern. Required: Python, Machine Learning, TensorFlow, Git, LLMs."
    for name, template in PROMPTS.items():
        built = build_prompt(template, sample_resume, sample_job)
        print("=" * 70)
        print(name, "| characters:", len(built))
    print("=" * 70)
    print("Preview of RCTF prompt:\n")
    print(build_prompt(RCTF_PROMPT, sample_resume, sample_job))
