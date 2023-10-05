from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

### пользователи
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable = False)

### администраторы
class Specialists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(100), nullable = False)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False) # специализация
    services = db.Column(db.String(100), nullable=False) # связь с оказывваемой услугой one to many

class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    specialist = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(10), nullable=False)
