def validate_user_data(user, form, **fields):
    if user.objects.filter(username=fields.get('username')).exists():
        form.add_error('login', 'Пользователь с таким логином уже существует.')
    elif user.objects.filter(email=fields.get('email')).exists():
        form.add_error('email', 'Пользователь с таким e-mail уже существует.')
    elif user.objects.filter(phone=fields.get('phone')).exists():
        form.add_error('phone', 'Пользователь с таким телефоном уже существует.')
