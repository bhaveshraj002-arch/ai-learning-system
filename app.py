from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from recommender import recommend_courses

app = Flask(__name__)
app.secret_key = 'secretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    interest = db.Column(db.String(100))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=request.form['password'],
            interest=request.form['interest']
        )

        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        user = User.query.filter_by(
            email=request.form['email'],
            password=request.form['password']
        ).first()

        if user:
            session['user'] = user.name
            session['interest'] = user.interest
            return redirect('/dashboard')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():

    if 'user' in session:
        recommendations = recommend_courses(session['interest'])

        return render_template(
            'dashboard.html',
            user=session['user'],
            recommendations=recommendations
        )

    return redirect('/login')

@app.route('/admin')
def admin():
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/quiz')
def quiz():

    questions = [
        {
            'question': 'Which language is used for AI?',
            'answer': 'Python'
        },
        {
            'question': 'Which framework is used?',
            'answer': 'Flask'
        }
    ]

    return render_template('quiz.html', questions=questions)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)