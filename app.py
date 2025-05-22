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

@app.route("/practice", methods=["GET", "POST"])
def practice():
    code = ""
    output = ""
    if request.method == "POST":
        code = request.form.get("code", "")
        try:
            # Безопасное окружение без встроенных функций
            exec_globals = {"__builtins__": {}}
            exec_locals = {}
            exec(code, exec_globals, exec_locals)
            output = exec_locals.get("output", "✅ Код выполнен успешно.")
        except Exception as e:
            output = f"❌ Ошибка: {e}"
    return render_template("practice.html", output=output, code=code)

if __name__ == "__main__":
    app.run()
