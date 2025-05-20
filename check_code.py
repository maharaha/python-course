def check_user_code(code):
    try:
        local_vars = {}
        exec(code, {}, local_vars)
        return "Код выполнен успешно."
    except Exception as e:
        return f"Ошибка: {str(e)}"
