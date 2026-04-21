# AI Mock Interview System

An AI-powered mock interview platform that generates role-specific interview questions, evaluates answers in real time, and provides personalized feedback — helping job seekers practice and improve before real interviews.

![Demo](screenshot.png)

---

## Problem Statement

Most job seekers practice interviews alone — without feedback, without knowing if their answers are good or bad. Hiring coaches are expensive. This system provides instant, honest, AI-generated feedback on every answer — available 24/7, completely free.

---

## What It Does

1. Enter your **name**, **job role**, and **experience level**
2. AI generates **5 role-specific interview questions** (mix of technical + behavioral)
3. You answer each question
4. AI evaluates your answer and gives:
   - Score (0–10)
   - Detailed feedback
   - Strengths in your answer
   - Areas to improve
   - What a strong answer would include
5. **Final report** with overall score, percentage, and per-question breakdown

---

## Features

| Feature | Description |
|---|---|
| Dynamic question generation | Gemini AI generates fresh questions for any job role |
| Real-time answer evaluation | Each answer scored and analyzed instantly |
| Strengths + improvements | Specific, actionable feedback per answer |
| Sample answer hint | AI shows what a great answer would include |
| Final scorecard | Overall percentage + verdict (Strong / Needs Improvement / Keep Practicing) |
| Any job role | Works for SWE, ML Engineer, Data Scientist, Product Manager, and more |
| Clean modern UI | Dark theme, progress bar, mobile-friendly |

---

## Tech Stack

| Component | Technology |
|---|---|
| AI / LLM | Google Gemini API |
| Backend | Python + Flask |
| Frontend | HTML + CSS (no frameworks) |
| Session Management | UUID-based JSON file storage |
| Deployment | Local / Render / Railway |

---

## How It Works

```
User Input (role + experience)
         │
         ▼
Gemini API → Generate 5 interview questions
         │
         ▼
User answers each question
         │
         ▼
Gemini API → Evaluate answer → JSON response
  {score, feedback, strengths, improvements, sample}
         │
         ▼
Final Results Page
  (total score, percentage, per-question breakdown)
```

---

## Installation

```bash
git clone https://github.com/ixsntg012-lab/ai-mock-interview.git
cd ai-mock-interview
pip install -r requirements.txt
```

Add your Gemini API key in `app.py`:
```python
GEMINI_API_KEY = "your_key_here"
```

Get a free API key at: [aistudio.google.com](https://aistudio.google.com)

---

## Usage

```bash
python app.py
```

Open browser: `http://localhost:5000`

---

## Project Structure

```
ai-mock-interview/
│
├── templates/
│   ├── index.html        ← Home page (role + experience input)
│   ├── interview.html    ← Question page
│   ├── feedback.html     ← Answer evaluation + feedback
│   └── results.html      ← Final scorecard
│
├── interview_data/       ← Session data (auto-created, gitignored)
├── app.py                ← Flask application
├── requirements.txt
└── README.md
```

---

## Current Limitations

- API key required (free tier available)
- No user accounts — sessions are temporary
- Questions generated fresh each time (no question bank)
- Text-only answers (no voice input yet)

---

## 🚀 Future Plans

### Phase 1 — Enhanced Evaluation
- **STAR method scoring** — automatically check if answer follows Situation, Task, Action, Result format
- **Domain-specific rubrics** — different scoring criteria for technical vs behavioral questions
- **Follow-up questions** — AI asks follow-up based on your answer, like a real interviewer

### Phase 2 — Voice & Video
- **Speech-to-text input** — answer questions by speaking, not typing
- **Filler word detection** — flag overuse of "um", "like", "you know"
- **Webcam mode** — practice eye contact and body language awareness

### Phase 3 — Personalization
- **User accounts** — save interview history and track improvement over time
- **Weakness tracking** — identify which question types you consistently score low on
- **Custom question bank** — upload company-specific questions for targeted practice
- **Resume-based questions** — upload resume → AI generates questions from your own experience

### Phase 4 — Deployment & Scale
- **Cloud deployment** — host on Render / Railway for public access
- **Multi-language support** — practice interviews in different languages
- **Company-specific modes** — FAANG style, startup style, consulting style
- **Peer practice** — connect two users for mock interviews with each other

---

## Author

**Swetha Kiran Veernapu**
MS Computer Science

---

## License

MIT License