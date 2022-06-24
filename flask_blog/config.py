# Здесь будут основные настройки для БД.

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' # Данный файл будет в пакете проекта.
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245' # Нужен для защиты от злоумышленника.