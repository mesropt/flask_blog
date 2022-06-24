from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_blog.models import User

# 1. Форма регистрации:
class RegistrationForm(FlaskForm): # Каждая форма - это класс. Обязательно описываем форму на базе FlaskForm.
    username = StringField('Имя пользователя:', validators=[DataRequired(), Length(min=2, max=20)]) # validators - валидация.
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')]) # EqualTo - валидатор, который проверяет соответствие пароля.
    submit = SubmitField('Зарегистрироваться')

    # Пользовательский метод валидации имени пользователя:
    def validate_username(self, username): # Проверяем свободно ли имя.
        user = User.query.filter_by(username=username.data).first() # username - это имя поля формы, data - его содержимое. Смотрим совпадает или нет.
        if user:
            raise ValidationError('Это имя занято. Пожалуйста, выберите другое.')

    # Пользовательский метод валидации электронной почтв:
    def validate_email(self, email): # Проверяем свободен ли email.
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email занят. Пожалуйста, выберите другой.')

# 2. Форма авторизации:
class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    remember = BooleanField('Напомнить пароль')
    submit = SubmitField('Войти')

# 3. Форма изменения параметров ЛК:
class UpdateAccountForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Обновить фото профиля', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Обновить')

    def validate_username(self, username):
        if username.data != current_user.username: # current_user - специальная встроенная переменная. она знает текущего юзера.
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Это имя занято.'
                                      'Пожалуйста, выберите другое.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(username=email.data).first()
            if user:
                raise ValidationError('Это email занят.'
                                      'Пожалуйста, выберите другой.')

# Форма восстановления пароля (состоит из двух подформ: форма запроса на восстановление + форма на изменение пароля):
# 4. Форма запроса на восстановление пароля:
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Изменить пароль')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Аккаунт с данным email-адресом отсутствует. Вы можете зарегистрировать его.')

# 5. Форма на изменение пароля
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Переустановить пароль')