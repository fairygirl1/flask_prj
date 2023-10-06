from config import Config

from flask import Flask, render_template, url_for, request, redirect, make_response, session,flash,get_flashed_messages
from models import Specialists, User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message

import os
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.secret_key = os.environ.get('secret_key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

@app.route('/home')
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/specialists')
def show_specialists_count():
    # Получение количества записей в таблице Specialists
    count = Specialists.query.count()
    
    return render_template('index.html', count=count)


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    """Авторизация"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            user = User.query.filter(User.username == username).one()
        except:
            flash("No same user")
            return redirect("/auth")
        if check_password_hash(user.password, password):

            return render_template('auth.html', username=user.name, )
        else:
            flash("Wrong password")
            return redirect("/auth")
    return render_template("auth.html")


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    """Регистрация"""
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        password = generate_password_hash(password, "sha256")
        new_user = User(name=name, username=username, password=password)

        try:
            db.session.add(new_user)
            db.session.commit()
        except BaseException as err:
            # Надо выводить пользователю информацию об неуспешной регистрации
            flash("Something bad!")
            raise err
        # Надо выводить пользователю информацию об успешной регистрации
        flash("Succesfull registration!")
        time.sleep(0.5)
        return redirect("/auth")
        
    return render_template('registration.html')




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)