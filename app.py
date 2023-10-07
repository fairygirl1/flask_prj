import sqlite3

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from config import Config

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField
from werkzeug.utils import secure_filename


from flask import Flask, render_template, url_for, request, redirect, make_response, session,flash,get_flashed_messages
from models import Specialists, User, Services, Blog, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message

import time
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.secret_key = Config.SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS

app.config['MAIL_SERVER'] = Config.MAIL_SERVER
app.config['MAIL_PORT'] = Config.MAIL_PORT
app.config['MAIL_USE_TLS'] = Config.MAIL_USE_TLS
app.config['MAIL_USERNAME'] = Config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = Config.MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = Config.MAIL_DEFAULT_SENDER

db.init_app(app)
mail = Mail(app)

@app.route('/admin')
def admin_index():
    return render_template('admin_index.html')

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/auth', methods=['POST', 'GET'])
def auth():
    """Авторизация"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = User.query.filter(User.email == email).one()
        except:
            flash("No same user")
            return redirect("/auth")
        if check_password_hash(user.password, password):

            return render_template('auth.html', username=user.name, )
        else:
            flash("Wrong password")
            return redirect("/auth")
    return render_template("auth.html")


@app.route('/signup', methods=['POST', 'GET'])
def registration():
    """Регистрация"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password = generate_password_hash(password, "pbkdf2:sha256")
        new_user = User(name=name, email=email, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError as err:
            print(err)
            db.session.rollback() 
            flash("User exists!", 'error')
            return render_template("signup.html")
        except BaseException as err:
            flash("Something bad!", 'error')
            raise err
        flash("Succesfull registration!", 'success')
        return redirect("/auth")
        
    return render_template('signup.html')

@app.route('/about', methods=["GET"])
def about():
    """Страница информации"""
    return render_template('about.html')

@app.route('/claim', methods=['POST', 'GET'])
def claim():
    """Запись"""
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        comment = request.form['comment']

        try:
            msg = Message('Новая заявка', recipients=[app.config['MAIL_USERNAME']])
        
            msg.body = f'Имя: {name}\nНомер телефона: {phone_number}\nКомментарий: {comment}'
        
            mail.send(msg)
        except BaseException as err:
            flash("Something bad!", 'error')
            raise err
        flash("Succesfull registration!", 'success')
        return redirect("/thanks")

    return render_template("claim.html")

@app.route('/admin_services', methods=['POST', 'GET'])
def admin_services():
    """Создание нового сервиса"""
    form = FlaskForm()
    if request.method == 'POST' and form.validate_on_submit():
        title = request.form['title']
        description = request.form['description']
        specialist = request.form['specialist']
        price = request.form['price']

        image = form.image.data
        if image:
            filename = secure_filename(image.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER_SERVICES'], filename)
            image.save(file_path)
        
        new_service = Services(title=title, description=description, specialist=specialist, price=price)
        try:
            db.session.add(new_service)
            db.session.commit()
        except BaseException as err:
            # Надо выводить пользователю информацию об неуспешной регистрации
            print(err)
            flash("Something bad!", 'error')
            raise err
        flash("Succesfull creation new service!", 'success')
        return redirect("/thanks")
        
    return render_template('admin_services.html', form=form)

@app.route('/services', methods=['GET'])
def all_service():
    return render_template("all_services.html")

@app.route('/services/<string:serviceName>', methods=['GET'])
def service(serviceName):
    service = Services.query.get_or_404(serviceName)
    return render_template("services.html", service=service)

# ('/specialists')
# ('/reviews') # отзывы
# admin_specialists
# all_specialists
# reviews
# admin_blog





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)