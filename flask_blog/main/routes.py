# Здесь будет и вьюшка (views.py), и маршрут (urls.py).
from flask import render_template, Blueprint, url_for
from flask_blog.models import User

main = Blueprint('main', __name__) # Это инициализация нового блюпринта. Раз мы его создали, то надо и зарегистрировать.


#Маршруты и вьюшки:
@main.route("/") # Этот декоратор означает какой путь надо обработать.
@main.route("/home") # Этот декоратор означает какой путь надо обработать.
def home():
    return render_template('home.html')

@main.route("/posts")
def posts():
    return render_template('posts.html')

@main.route("/about")
def about():
    return render_template('about.html')

@main.route("/contact")
def contact():
    return render_template('contact.html')
