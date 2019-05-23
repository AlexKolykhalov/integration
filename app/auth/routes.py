from flask             import render_template, flash, redirect, url_for, request
from werkzeug.urls     import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login       import current_user, login_user, logout_user
from app               import redis_store
from app.auth          import bp
from app.auth.forms    import LoginForm, RegistrationForm
from models            import User


@bp.route('/login', methods=['get', 'post'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))        
    form = LoginForm()
    if form.validate_on_submit():
        user          = redis_store.exists(form.username.data)
        password_hash = '' if redis_store.hget(form.username.data, 'password_hash') == None else redis_store.hget(form.username.data, 'password_hash') 
        if not user or not check_password_hash(password_hash, form.password.data):            
            flash('Неверный логин или пароль!')
            return redirect(url_for('auth.login'))        
        user_data       = redis_store.hgetall(form.username.data)
        user_id         = form.username.data        
        username        = user_data['username']
        email           = user_data['email']
        password_hash   = user_data['password_hash']
        operating_mode  = user_data['operating_mode']
        user = User(user_id=user_id, username=username, email=email, password_hash=password_hash, operating_mode=operating_mode)
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', form=form)

@bp.route('/register', methods=['get', 'post'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():        
        # добавляем текущий email в базу для проверки 
        redis_store.sadd('emails', form.email.data)
        # добавляем данные текущего пользователя 
        redis_store.hset(form.username.data, 'username', 'username')
        redis_store.hset(form.username.data, 'email', form.email.data)        
        redis_store.hset(form.username.data, 'password_hash', generate_password_hash(form.password.data))
        redis_store.hset(form.username.data, 'operating_mode', 'test')        
        flash('Вы успешно зарегистрированы!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))