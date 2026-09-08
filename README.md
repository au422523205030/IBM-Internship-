# AI Student Support Assistant

A simple final-project prototype based on the selected use case:

**AI Student Support Assistant — RAG + Tools + Memory**

## Features
1. **RAG (Retrieval-Augmented Generation style retrieval)**  
   Searches a college knowledge base using TF-IDF and cosine similarity before answering.
2. **Tools**
   - Attendance percentage calculator
   - General percentage calculator
   - Simple GPA/CGPA averaging helper
3. **Memory**
   - Remembers a student's name
   - Remembers course/branch
   - Stores memory in SQLite
4. **Web UI**
   - Chat interface
   - Suggested questions
   - Mobile-friendly layout

## Project structure
```
AI_Student_Support_Assistant/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── college_knowledge.txt
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## How to run

### 1. Install Python
Python 3.10+ is recommended.

### 2. Open terminal in this project folder
```bash
cd AI_Student_Support_Assistant
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the application
```bash
python app.py
```

### 5. Open in browser
Go to:
`http://127.0.0.1:5000`

## Demo questions
- What is the attendance policy?
- What is the project submission procedure?
- What should I know about placement?
- My name is Arun
- What is my name?
- I study B.Tech IT
- What do I study?
- 75 out of 90
- 80 classes attended out of 100 classes

## Viva explanation
**Why RAG?** To retrieve relevant college information from a knowledge base instead of relying only on a general model.

**Why tools?** Some questions require exact calculations. A calculator tool gives deterministic results.

**Why memory?** It lets the assistant remember useful student details such as name and course.

**Is it classification or regression?** Neither is the main task. This is an information-retrieval/conversational assistant with tool calling and memory.

**Future improvement:** Connect the retrieval layer to an LLM, add PDF ingestion, authentication, admin upload, vector database, multilingual Tamil/English support, and live college APIs.