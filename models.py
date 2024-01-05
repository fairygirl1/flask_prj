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
    role = db.Column(db.String(25), default='client')

### Администраторы
class Specialists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False) # специализация
    services_id = db.Column(db.Integer, db.ForeignKey('service.id')) # связь с оказывваемой услугой one to many


class Services(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    specialist = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(10), nullable=False)

class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mark = db.Column(db.Integer, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(2048), nullable=False) 