
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from models import db, User
from lessons import lessons
from tests import tests
from quizzes import quizzes
from check_code import check_user_code

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html', lessons=lessons)

@app.route('/lesson/<int:number>')
@login_required
def lesson(number):
    title = lessons[number - 1]
    return render_template('lesson.html', number=number, title=title)

@app.route('/test/<int:number>', methods=['GET', 'POST'])
@login_required
def test(number):
    questions = tests.get(number, [])
    if request.method == 'POST':
        user_answers = request.form
        correct = sum(1 for i, q in enumerate(questions) if user_answers.get(f'q{i}') == q['answer'])
        return render_template('result.html', correct=correct, total=len(questions))
    return render_template('test.html', number=number, questions=questions)

@app.route('/quiz/<int:number>', methods=['GET', 'POST'])
@login_required
def quiz(number):
    questions = quizzes.get(number, [])
    if request.method == 'POST':
        user_answers = request.form
        correct = sum(1 for i, q in enumerate(questions) if user_answers.get(f'q{i}') == q['answer'])
        return render_template('result.html', correct=correct, total=len(questions))
    return render_template('quiz.html', number=number, questions=questions)

@app.route('/check', methods=['POST'])
@login_required
def check():
    code = request.form['code']
    result = check_user_code(code)
    return render_template('check.html', result=result)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Пользователь уже существует')
            return redirect(url_for('register'))
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация прошла успешно! Войдите в систему.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            return redirect(url_for('index'))
        flash('Неверное имя пользователя или пароль')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
