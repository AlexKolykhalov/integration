from flask             import render_template, flash, redirect, url_for, request, Markup
from werkzeug.urls     import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login       import current_user, login_user, logout_user, login_required
from app               import redis_store
from app.auth          import bp
from app.auth.forms    import LoginForm, RegistrationForm, ProfileForm
from models            import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))        
    form = LoginForm()
    # заполняем SelectField пользователями сайта 
    choices = [(key, redis_store.hgetall(key)['username']) for key in redis_store.hkeys('site_users')]
    if len(choices) > 0:
        form.username.choices = choices
    if form.validate_on_submit():        
        user          = redis_store.exists(form.username.data)
        password_hash = '' if redis_store.hget(form.username.data, 'password_hash') == None else redis_store.hget(form.username.data, 'password_hash')        
        if not user or not check_password_hash(password_hash, form.password.data):            
            flash('Неверный логин или пароль!')
            return redirect(url_for('auth.login'))        
        user_data       = redis_store.hgetall(form.username.data)
        user_id         = form.username.data        
        username        = user_data['username']
        # email           = user_data['email']
        password_hash   = user_data['password_hash']
        operating_mode  = user_data['operating_mode']
        role            = user_data['role']
        user = User(user_id=user_id, username=username, password_hash=password_hash, operating_mode=operating_mode, role=role)
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():        
        # # добавляем текущий email в базу emails для проверки 
        # redis_store.sadd('emails', form.email.data)
        # добавляем данные текущего пользователя         
        id = 0 if redis_store.get('counter') == None else int(redis_store.get('counter'))
        redis_store.hset(id, 'username', form.username.data)
        #redis_store.hset(id, 'email', form.email.data)
        redis_store.hset(id, 'password_hash', generate_password_hash(form.password.data))
        redis_store.hset(id, 'operating_mode', 'test')
        redis_store.hset(id, 'role', 'user')
        # добавляем пользователя в список пользователей сайта
        redis_store.hset('site_users', id, id)       
        flash(Markup('<strong>'+form.username.data+'</strong> успешно зарегистрирован!'))
        redis_store.set('counter', id+1)        
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():    
    form = ProfileForm()
    if form.validate_on_submit():
        # добавляем данные текущего пользователя
        redis_store.hset(current_user.id, 'username', form.username.data)
        redis_store.hset(current_user.id, 'role', form.role.data)
        flash('Данные сохранены!')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.role.data = current_user.role
    return render_template('auth/profile.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))