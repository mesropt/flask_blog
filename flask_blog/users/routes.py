from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_blog import db, bcrypt
from flask_blog.models import User, Post
from flask_blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from flask_blog.users.utils import save_picture

users = Blueprint('users', __name__) # Инициируем создание нового блюпринта (это не регистрация, её мы будем выполнять в файле __init__.py пакета проекта)

# Роутер и контроллер:
@users.route("/register", methods=['GET', 'POST']) # Говорит, если заходим на ссылку, заканчивающуюся на /register, то срабатывает контроллер register
def register():
    if current_user.is_authenticated: # Если пользователь уже зарегистрирован, то перекидываем его на главную страницу.
        return redirect(url_for('main.home')) # main - название нашего блюпринта, а home - наша вьюшка.
    form = RegistrationForm() # Если же регистрации не было, то выполняем создание объекта формы регистрации.
    if form.validate_on_submit(): # Затем выполняем валидацию формы. Если валидация прошла успешно, то записываем пароль в БД.
        hashed_password = bcrypt.generetate_password_hash(form.password.data).decode('utf-8') # Теперь мы из формы получаем пароль и хешируем его через компонент bcrypt и тем самым получаем хеш пароля (hashed_password).
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) # Через ORM (через модель  User) создаём объект этой модели user.
        db.session.add(user) # Через сессию отправляем данные в БД.
        db.session.commit() # Затем подтверждаем отправку.
        flash('Ваша учётная запись была создана!'
              'Теперь вы можете войти в систему', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form) # Рендерим шаблон и передаём в него контекст - title и form.

# bcrypt - это объект специального одноимённого класса, который применяется для получения хешей паролей.

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): # Проверяем совпадает ли хеш пароля в БД с хешем пароля из формы
            login_user(user, remember=form.remember.data) # Если хеши паролей совпадают, то выполняем авторизацию.

            return redirect(url_for('main.home'))
        else:
            flash('Войти не удалось. Пожалуйста, проверьте электронную почту и пароль', 'внимание')
    return render_template('login.html', title='Аутентификация', form=form)

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data: # Берём фото из формы
            picture_file = save_picture(form.picture.data)  # Кладём фото в БД
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.datadb.session.commit()
        flash('Ваш аккаунт был обновлён!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET': # Показать текущие данные профиля в форме
        form.username.data = current_user.username
        form.email.data = current_user.email
        page = request.args.get('page', 1, type=int)
        user = User.query.filter_by(username=form.username.data).first_or_404()
        posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file) # Получение объекта фото для его вывода в шаблоне.
        return render_template('account.html', title='Account', image_file=image_file, form=form, posts=posts, user=user)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))