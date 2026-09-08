from flask import Flask, render_template, request, jsonify
import sqlite3, re, math
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
DB = Path("student_memory.db")
DOCS = Path("data/college_knowledge.txt")

def init_db():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS memory
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, key TEXT UNIQUE, value TEXT)""")
    con.commit()
    con.close()

def remember(key, value):
    con = sqlite3.connect(DB)
    con.execute("INSERT OR REPLACE INTO memory(key,value) VALUES(?,?)", (key, value))
    con.commit()
    con.close()

def get_memory():
    con = sqlite3.connect(DB)
    rows = con.execute("SELECT key,value FROM memory").fetchall()
    con.close()
    return dict(rows)

def load_docs():
    text = DOCS.read_text(encoding="utf-8")
    chunks = [x.strip() for x in text.split("\n\n") if x.strip()]
    return chunks

CHUNKS = load_docs()
VECTORIZER = TfidfVectorizer(stop_words="english")
MATRIX = VECTORIZER.fit_transform(CHUNKS)

def retrieve(query, k=3):
    q = VECTORIZER.transform([query])
    scores = cosine_similarity(q, MATRIX)[0]
    ids = scores.argsort()[::-1][:k]
    return [(CHUNKS[i], float(scores[i])) for i in ids if scores[i] > 0.08]

def tool_call(query):
    q = query.lower()

    # Attendance calculator
    m = re.search(r'(\d+)\s*(?:classes|class|hours)?\s*(?:attended|present).*?(\d+)\s*(?:classes|class|hours)?', q)
    if m:
        attended, total = int(m.group(1)), int(m.group(2))
        if total > 0 and attended <= total:
            return f"Attendance calculation: {attended}/{total} = {attended/total*100:.2f}%."

    # Simple percentage calculator
    m = re.search(r'(\d+(?:\.\d+)?)\s*(?:out of|/)\s*(\d+(?:\.\d+)?)', q)
    if m:
        a, b = float(m.group(1)), float(m.group(2))
        if b != 0:
            return f"Calculation: {a:g}/{b:g} = {a/b*100:.2f}%."

    # CGPA average helper
    nums = re.findall(r'\b(?:10(?:\.0)?|[0-9](?:\.\d+)?)\b', q)
    if ("cgpa" in q or "gpa" in q) and len(nums) >= 2:
        vals = [float(x) for x in nums]
        avg = sum(vals) / len(vals)
        return f"Simple average of the supplied GPA/CGPA values: {avg:.2f}."

    return None

def answer(query):
    memory = get_memory()

    # Memory extraction
    name = re.search(r'\bmy name is ([A-Za-z ]{2,40})', query, re.I)
    if name:
        remember("name", name.group(1).strip().title())
        return f"Nice to meet you, {name.group(1).strip().title()}! I’ll remember your name for this session."

    course = re.search(r'\b(?:i am studying|i study|my course is|my branch is)\s+(.+)', query, re.I)
    if course and len(course.group(1).strip()) < 60:
        remember("course", course.group(1).strip())
        return f"Got it. I’ll remember that your course/branch is {course.group(1).strip()}."

    if "what is my name" in query.lower() or "remember my name" in query.lower():
        return f"Your remembered name is {memory.get('name', 'not saved yet')}."

    if "what do i study" in query.lower() or "my course" in query.lower():
        return f"Your remembered course/branch is {memory.get('course', 'not saved yet')}."

    tool = tool_call(query)
    if tool:
        return tool

    results = retrieve(query)
    if results:
        best = results[0][0]
        # The project deliberately returns retrieved knowledge rather than inventing policy.
        return f"According to the college knowledge base:\n\n{best}\n\nSource confidence: {results[0][1]:.2f}"

    return ("I couldn't find a reliable answer in the college knowledge base. "
            "Please ask your college office or faculty member for an official answer.")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    query = data.get("message", "").strip()
    if not query:
        return jsonify({"answer": "Please enter a question."})
    return jsonify({"answer": answer(query), "memory": get_memory()})

@app.route("/api/memory", methods=["GET"])
def memory():
    return jsonify(get_memory())

if __name__ == "__main__":
    init_db()
    print("AI Student Support Assistant running at http://127.0.0.1:5000")
    app.run(debug=True)