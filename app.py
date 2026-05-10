# ================================
# app.py
# ================================

from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# ================================
# DATABASE CONNECTION
# ================================

def connect_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ================================
# CREATE TABLE
# ================================

def create_table():
    conn = connect_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT,
        interest TEXT
    )
    """)

    conn.commit()
    conn.close()

create_table()

# ================================
# YOUTUBE VIDEOS DATA
# ================================

courses = {
    "Python": [
        {
            "title": "Python Full Course",
            "link": "https://www.youtube.com/watch?v=_uQrJ0TkZlc"
        },
        {
            "title": "Python Tutorial",
            "link": "https://www.youtube.com/watch?v=rfscVS0vtbw"
        },
        {
            "title": "Python Projects",
            "link": "https://www.youtube.com/watch?v=8ext9G7xspg"
        },
        {
            "title": "Flask Tutorial",
            "link": "https://www.youtube.com/watch?v=Z1RJmh_OqeA"
        },
        {
            "title": "Python OOP",
            "link": "https://www.youtube.com/watch?v=Ej_02ICOIgs"
        }
    ],

    "Web Development": [
        {
            "title": "HTML Full Course",
            "link": "https://www.youtube.com/watch?v=qz0aGYrrlhU"
        },
        {
            "title": "CSS Tutorial",
            "link": "https://www.youtube.com/watch?v=OXGznpKZ_sA"
        },
        {
            "title": "JavaScript Tutorial",
            "link": "https://www.youtube.com/watch?v=W6NZfCO5SIk"
        },
        {
            "title": "Responsive Web Design",
            "link": "https://www.youtube.com/watch?v=srvUrASNj0s"
        },
        {
            "title": "Full Stack Development",
            "link": "https://www.youtube.com/watch?v=nu_pCVPKzTk"
        }
    ]
}

# ================================
# QUIZ QUESTIONS
# ================================

quiz_questions = [
    {
        "question": "What does AI stand for?",
        "options": [
            "Artificial Intelligence",
            "Advanced Internet",
            "Automated Input",
            "Artificial Interface"
        ],
        "answer": "Artificial Intelligence"
    },

    {
        "question": "Which language is used in Flask?",
        "options": [
            "Java",
            "Python",
            "PHP",
            "C++"
        ],
        "answer": "Python"
    },

    {
        "question": "Which database is used in this project?",
        "options": [
            "MongoDB",
            "Oracle",
            "SQLite",
            "Firebase"
        ],
        "answer": "SQLite"
    },

    {
        "question": "Which tag is used for heading in HTML?",
        "options": [
            "<p>",
            "<div>",
            "<h1>",
            "<span>"
        ],
        "answer": "<h1>"
    },

    {
        "question": "Which framework is used for backend?",
        "options": [
            "React",
            "Angular",
            "Flask",
            "Bootstrap"
        ],
        "answer": "Flask"
    }
]

# ================================
# HOME PAGE
# ================================

@app.route("/")
def home():
    return render_template("index.html")

# ================================
# REGISTER
# ================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        interest = request.form["interest"]

        conn = connect_db()

        conn.execute(
            "INSERT INTO users (name, email, password, interest) VALUES (?, ?, ?, ?)",
            (name, email, password, interest)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# ================================
# LOGIN
# ================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = connect_db()

        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()

        conn.close()

        if user:

            session["user"] = user["name"]
            session["interest"] = user["interest"]

            return redirect("/dashboard")

        else:
            return "Invalid Credentials"

    return render_template("login.html")

# ================================
# DASHBOARD
# ================================

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    interest = session["interest"]

    recommended_videos = courses.get(interest, [])

    return render_template(
        "dashboard.html",
        name=session["user"],
        interest=interest,
        videos=recommended_videos
    )

# ================================
# QUIZ PAGE
# ================================

@app.route("/quiz")
def quiz():
    return render_template(
        "quiz.html",
        questions=quiz_questions
    )

# ================================
# QUIZ SUBMIT
# ================================

@app.route("/submit_quiz", methods=["POST"])
def submit_quiz():

    score = 0

    for i, q in enumerate(quiz_questions):

        user_answer = request.form.get(f"q{i}")

        if user_answer == q["answer"]:
            score += 1

    return render_template(
        "result.html",
        score=score,
        total=len(quiz_questions)
    )

# ================================
# LOGOUT
# ================================

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================================
# RUN APP
# ================================

if __name__ == "__main__":
    app.run(debug=True)
