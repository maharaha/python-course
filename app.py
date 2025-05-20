
from flask import Flask, render_template, request
from lessons import lessons
from tests import tests
from quizzes import quizzes
from check_code import check_user_code

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", lessons=lessons)

@app.route("/lesson/<int:lesson_id>")
def lesson(lesson_id):
    lesson = lessons.get(lesson_id)
    return render_template("lesson.html", lesson=lesson, lesson_id=lesson_id)

@app.route("/test/<int:lesson_id>", methods=["GET", "POST"])
def test(lesson_id):
    test_data = tests.get(lesson_id, [])
    if request.method == "POST":
        user_answers = request.form
        correct = sum(1 for q in test_data if user_answers.get(str(q["id"])) == q["answer"])
        return render_template("result.html", correct=correct, total=len(test_data))
    return render_template("test.html", test=test_data, lesson_id=lesson_id)

@app.route("/quiz/<int:lesson_id>")
def quiz(lesson_id):
    quiz_data = quizzes.get(lesson_id, [])
    return render_template("quiz.html", quiz=quiz_data)

@app.route("/check", methods=["POST"])
def check():
    code = request.form.get("code", "")
    output = check_user_code(code)
    return render_template("check.html", output=output)

if __name__ == "__main__":
    app.run()
