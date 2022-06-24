# Данный скрипт выполняет правильное сохранение аватарки.
import os
from secrets import token_hex # token_hex - это функция, которая вернёт строку в 16-ричном формате. Модуль secrets необходим для создания токенов. Например, сейчас так в гитхабе многие операции пожтверждаются токеном. Почему? Это необходимо для безопасности важных операций.
from PIL import Image # PIL - популярная библиотека для работы с картинками. В неё есть компонент-класс-конструктор Image, там есть всё для работы с фото.
from flask import url_for, current_app

def save_picture(form_picture):
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) # form_picture - это объект формы, где мы меняем фото. filename - новое имя файла.
    picture_fn = random_hex + f_ext  # Берём имя файла и соединяем с нашим токеном.
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn) # Будем сохранять фото по этому пути.

    output_size = (150, 150) # Параметры картинки
    i = Image.open(form_picture) # Берём объект форму
    i.thumbnail(output_size) # Указываем параметры
    i.save(picture_path) # Сохраняем

    return picture_fn # Функция в итоге вернёт объект нашей картинки, в том числе с токеном