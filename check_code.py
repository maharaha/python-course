
def check_user_code(user_code, lesson_id):
    try:
        # Ограниченная среда выполнения (эмуляция)
        allowed_builtins = {'print': print}
        local_vars = {}
        exec(user_code, {'__builtins__': allowed_builtins}, local_vars)
        return "✅ Код выполнен без ошибок!"
    except Exception as e:
        return f"❌ Ошибка: {e}"
