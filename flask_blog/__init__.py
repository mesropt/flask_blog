from flask import Flask # Импортируем класс-конструктор Flask, экземпляр которого будет нашим веб-приложением.
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_blog.config import Config
from flask_bcrypt import Bcrypt

#Здесь мы будем регистрировать блюпринты (приложения).
db = SQLAlchemy()
login_manager = LoginManager() # Это батарейка для авторизации клиентов. Его РЕГИСТРИРУЕМ (см. ниже)
bcrypt = Bcrypt() # bcrypt тоже надо зарегистрировать. Его РЕГИСТРИРУЕМ (см. ниже)

def create_app():
    #print(__name__)
    app = Flask(__name__) # __name__ - обязательный параметр, который соответствует названию пакета, в котором Flask будет искать статические файлы, шаблоны и т.д.
    db.init_app(app)
    #--Подключение Config и инициализация взаимодействия проекта с БД:
    app.config.from_object(Config)
    #--Ниже регистрация блюпринта main:
    from flask_blog.main.routes import main # main - это ссылка на объект нашего блюпринта (см. __init__.py), мы его регистрируем. На этой строчки импортируем объект приложения, на следующей - регистрируем.
    app.register_blueprint(main) # На этой строчке регистрируем объект блюпринта.
    #--Ниже регистрация блюпринта users:
    from flask_blog.users.routes import users
    app.register_blueprint(users)
    #--Ниже регистрация компонент login_manager:
    login_manager.init_app(app) # Связываем блюпринт с батарейкой для авторизации клиентов.
    #--Ниже регистрация bcrypt:
    bcrypt.init_app(app)
    #----
    return app
