from flask import Flask, render_template, request
from lessons import lessons

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/structure")
def structure():
    return render_template("structure.html", lessons=lessons)

@app.route("/lesson/<int:lesson_id>")
def lesson(lesson_id):
    lesson = lessons[lesson_id]
    return render_template("lesson.html", lesson=lesson, lesson_id=lesson_id)

if __name__ == "__main__":
    app.run()
