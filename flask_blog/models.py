from datetime import datetime # Необходим для записи даты поста
from flask_blog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): # db.model - это базовый класс модели, как и в Django. А UserMixin нужен для дальнейшей корректной авторизации клиента, так как у этого класса есть необходимый интерфейс.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
# db.relationship - указание на те посты (таблицы), которые есть у нашего автора.
# backref - это ссылка на запись, чтобы потому в модели Post можно было отслеживать кто есть автор поста.
# lazy=True - стандартная опция, означает, что содержимое таблиц загружается параллалельно, то есть сразу и user, и все его посты.

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Связь с таблицей User - автор поста.