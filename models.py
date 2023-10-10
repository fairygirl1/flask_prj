from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField

db = SQLAlchemy()

### Пользователи
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

### Администраторы
class Specialists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(100), nullable = False)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False) # специализация
    services = db.Column(db.String(100), nullable=False) # связь с оказывваемой услугой one to many

class Services(db.Model):
    title = db.Column(db.String(100), primary_key=True, nullable=False)
    # image = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    specialist = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(10), nullable=False)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(2048), nullable=False)
    pictures = db.Column(db.String(100), nullable=False) #картинок будет по 2 на каждой странице

# модель на отзывы