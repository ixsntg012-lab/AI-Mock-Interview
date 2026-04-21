"""
AI Mock Interview System — Final
==================================
No flask-session dependency.
Questions stored in a temp JSON file to avoid cookie size limit.
"""

from flask import Flask, render_template, request, session, redirect
import google.generativeai as genai
import json, re, os, uuid

app = Flask(__name__)
app.secret_key = "mock_interview_2026_xyz"

# ── Gemini Setup ──────────────────────────────────────────────────────────
GEMINI_API_KEY = "AIzaSyDdgB7mzfvIF8IjN_t9n9qpfTbPoMSwci4"   # ← నీ key ఇక్కడ పెట్టు
genai.configure(api_key=GEMINI_API_KEY)
gemini = genai.GenerativeModel("models/gemini-3.1-flash-lite-preview")

# ── Store data in JSON files (avoids session size limit) ──────────────────
DATA_DIR = "interview_data"
os.makedirs(DATA_DIR, exist_ok=True)

def save_data(sid, data):
    with open(f"{DATA_DIR}/{sid}.json", "w") as f:
        json.dump(data, f)

def load_data(sid):
    path = f"{DATA_DIR}/{sid}.json"
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None

# ── Helpers ───────────────────────────────────────────────────────────────
def generate_questions(role, experience, num=5):
    prompt = f"""You are an expert technical interviewer.
Generate exactly {num} interview questions for:
Role: {role}
Experience: {experience}
Rules: mix technical + behavioral, numbered 1. 2. 3., no extra text.
"""
    response  = gemini.generate_content(prompt)
    lines     = [l.strip() for l in response.text.strip().split("\n") if l.strip()]
    questions = []
    for line in lines:
        clean = re.sub(r"^\d+[\.\)]\s*", "", line).strip()
        if clean and len(clean) > 10:
            questions.append(clean)
    return questions[:num]


def evaluate_answer(role, question, answer):
    if not answer.strip():
        return {"score":0,"feedback":"No answer provided.",
                "strengths":[],"improvements":["Please provide an answer."],"sample":""}
    prompt = f"""You are an expert interviewer.
Role: {role}
Question: {question}
Answer: {answer}
Respond ONLY with valid JSON (no markdown):
{{"score":<0-10>,"feedback":"<2-3 sentences>","strengths":["s1","s2"],"improvements":["i1","i2"],"sample":"<1 sentence>"}}
"""
    response = gemini.generate_content(prompt)
    text     = re.sub(r"```json|```", "", response.text.strip()).strip()
    try:
        return json.loads(text)
    except Exception:
        return {"score":5,"feedback":text[:300],"strengths":[],"improvements":[],"sample":""}


# ── Routes ────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    role       = request.form.get("role","").strip()
    experience = request.form.get("experience","Entry Level")
    name       = request.form.get("name","Candidate").strip()

    if not role:
        return render_template("index.html", error="Please enter a job role.")

    questions = generate_questions(role, experience, num=5)
    if not questions:
        return render_template("index.html", error="Could not generate questions. Try again.")

    # Create unique session ID
    sid = str(uuid.uuid4())
    session["sid"] = sid

    # Save all data to file
    save_data(sid, {
        "role": role, "experience": experience, "name": name,
        "questions": questions, "current": 0,
        "answers": [], "scores": []
    })

    return render_template("interview.html",
        name=name, role=role,
        question=questions[0], q_num=1, total=len(questions))


@app.route("/evaluate", methods=["POST"])
def evaluate():
    sid  = session.get("sid")
    data = load_data(sid) if sid else None

    if not data:
        return redirect("/")

    answer    = request.form.get("answer","").strip()
    current   = data["current"]
    questions = data["questions"]
    role      = data["role"]
    name      = data["name"]

    if current >= len(questions):
        return redirect("/results")

    question = questions[current]
    result   = evaluate_answer(role, question, answer)

    data["answers"].append({"question":question,"answer":answer,"eval":result})
    data["scores"].append(result.get("score",0))
    data["current"] = current + 1
    save_data(sid, data)

    next_q  = current + 1
    is_last = (next_q >= len(questions))

    return render_template("feedback.html",
        name=name, role=role,
        question=question, answer=answer, result=result,
        q_num=current+1, total=len(questions),
        is_last=is_last,
        next_q_num=next_q+1,
        next_question=questions[next_q] if not is_last else None)


@app.route("/next_question", methods=["POST"])
def next_question():
    sid  = session.get("sid")
    data = load_data(sid) if sid else None

    if not data:
        return redirect("/")

    current   = data["current"]
    questions = data["questions"]

    if current >= len(questions):
        return redirect("/results")

    return render_template("interview.html",
        name=data["name"], role=data["role"],
        question=questions[current],
        q_num=current+1, total=len(questions))


@app.route("/results")
def results():
    sid  = session.get("sid")
    data = load_data(sid) if sid else None

    if not data or not data.get("answers"):
        return redirect("/")

    answers     = data["answers"]
    scores      = data["scores"]
    total_score = sum(scores)
    max_score   = len(scores)*10
    percentage  = round((total_score/max_score)*100) if max_score>0 else 0

    if percentage >= 75:
        verdict = ("Strong Candidate","green","🎉")
    elif percentage >= 50:
        verdict = ("Needs Improvement","orange","📈")
    else:
        verdict = ("Keep Practicing","red","💪")

    return render_template("results.html",
        name=data["name"], role=data["role"],
        answers=answers, scores=scores,
        total_score=total_score, max_score=max_score,
        percentage=percentage, verdict=verdict)


if __name__ == "__main__":
    app.run(debug=True)