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
            exec_globals = {"__builtins__": {}}
            exec_locals = {}
            exec(code, exec_globals, exec_locals)
            output = exec_locals.get("output", "✅ Код выполнен успешно.")
        except Exception as e:
            output = f"❌ Ошибка: {e}"
    return render_template("practice.html", output=output, code=code)

@app.route("/project", methods=["GET", "POST"])
def project():
    code = ""
    output = ""

    # Три проекта на выбор
    project_titles = {
        "1": "🔢 Калькулятор",
        "2": "🎲 Генератор паролей",
        "3": "🐢 Рисунок с turtle"
    }
    project_descriptions = {
        "1": "Создайте калькулятор, который выполняет операции: +, -, *, /.",
        "2": "Сделайте генератор, который создает случайные пароли из букв и цифр.",
        "3": "С помощью turtle нарисуйте звезду, цветок или домик."
    }

    selected = request.form.get("project")  # выбор проекта

    if selected and "code" in request.form:
        code = request.form.get("code", "")
        try:
            exec_globals = {"__builtins__": {}}
            exec_locals = {}
            exec(code, exec_globals, exec_locals)
            output = exec_locals.get("output", "✅ Код выполнен успешно.")
        except Exception as e:
            output = f"❌ Ошибка: {e}"

    return render_template(
        "project.html",
        selected=selected,
        code=code,
        output=output,
        project_title=project_titles.get(selected),
        project_description=project_descriptions.get(selected)
    )

if __name__ == "__main__":
    app.run(debug=True)

