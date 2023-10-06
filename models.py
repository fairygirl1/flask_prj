from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

### Пользователи
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable = False)

### Администраторы
class Specialists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(100), nullable = False)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False) # специализация
    services = db.Column(db.String(100), nullable=False) # связь с оказывваемой услугой many to many



# Разные категории услуг - разные таблицы в бд
# на домашней странице будет выбор категорий (подтягиваются из бд), в каждой категории 
# свои услуги - они на отдельных страницах категорий в карусельке

# class Categories(db.Model):


class Nails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable = False)
    price = db.Column(db.Integer)
    masters = db.Column(db.String(100), nullable=False) #связь с мастером one to many

class Hair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable = False)
    masters = db.Column(db.String(100), nullable=False) #связь с мастером one to many

class Makeup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable = False)
    masters = db.Column(db.String(100), nullable=False) #связь с мастером one to many

class Massage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable = False)
    masters = db.Column(db.String(100), nullable=False) #связь с мастером one to many