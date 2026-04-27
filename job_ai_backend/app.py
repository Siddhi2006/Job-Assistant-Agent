from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
from gemini_client import ask_gemini

app = Flask(__name__)
CORS(app)

# ---------------------------
# HOME ROUTE (FIX NOT FOUND ERROR)
# ---------------------------
@app.route("/")
def home():
    return "AI Job Assistant Backend Running 🚀"


# ---------------------------
# PDF TEXT EXTRACTION
# ---------------------------
def extract_text_from_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        return text.strip()

    except Exception as e:
        return ""


# ---------------------------
# MAIN API
# ---------------------------
@app.route("/process", methods=["POST"])
def process():

    module = request.form.get("module")
    question = request.form.get("question", "")
    role = request.form.get("role", "")

    resume = ""

    # PDF FILE HANDLING
    if "resume" in request.files:
        file = request.files["resume"]
        resume = extract_text_from_pdf(file)

    # ---------------- PROMPTS ----------------
    if module == "resume":
        prompt = f"Analyze this resume and give summary:\n{resume}"

    elif module == "skills":
        prompt = f"Extract technical and soft skills from this resume:\n{resume}"

    elif module == "jobs":
        prompt = f"Suggest job roles for this skill: {role}"

    elif module == "match":
        prompt = f"Match suitable jobs for this resume:\n{resume}"

    elif module == "recommend":
        prompt = f"Give career recommendations based on this resume:\n{resume}"

    elif module == "gap":
        prompt = f"Find skill gaps and improvements:\n{resume}"

    elif module == "roadmap":
        prompt = f"Create a learning roadmap step by step:\n{resume}"

    elif module == "chat":
        prompt = question

    else:
        return jsonify({"result": "Invalid module"})

    result = ask_gemini(prompt)

    return jsonify({"result": result})


# ---------------------------
# RUN SERVER
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)