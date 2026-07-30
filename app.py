from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO users(username,password) VALUES(?,?)",(u,p))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?",(u,p))
        user = cur.fetchone()
        conn.close()
        if user:
            session['user'] = u
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html')
    return redirect('/login')

@app.route('/notes')
def notes():
    notes_list = [
        {"title": "Python Notes", "link": "#"},
        {"title": "DBMS Notes", "link": "#"},
        {"title": "Computer Network Notes", "link": "#"}
    ]
    return render_template('notes.html', notes=notes_list)

@app.route('/updates')
def updates():
    updates = [
        "📅 DDSET Exam date declared",
        "📚 New syllabus uploaded",
        "📝 Mock test available now"
    ]
    return render_template('updates.html', updates=updates)

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/result', methods=['POST'])
def result():
    score = 0
    if request.form.get('q1') == 'a':
        score += 1
    if request.form.get('q2') == 'b':
        score += 1
    return render_template('result.html', score=score)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

app.run(debug=True)
