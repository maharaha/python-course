from flask import Flask, render_template, request, redirect, url_for
from lessons import lessons
from check_code import check_user_code

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", lessons=lessons)

@app.route("/lesson/<int:lesson_id>", methods=["GET", "POST"])
def lesson(lesson_id):
    if lesson_id < 0 or lesson_id >= len(lessons):
        return "Урок не найден", 404

    lesson = lessons[lesson_id]
    result = ""
    if request.method == "POST":
        code = request.form.get("code", "")
        result = check_user_code(code)
    return render_template("lesson.html", lesson=lesson, lesson_id=lesson_id, result=result)

if __name__ == "__main__":
    app.run()
