

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from config import Config

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField
from werkzeug.utils import secure_filename

from models import User, Specialists, Services, Reviews, db
from admin import admin

from api.api import api_bp

from flask import Flask, render_template, url_for, request, redirect, make_response, session,flash,get_flashed_messages
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message


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

admin.init_app(app)

db.init_app(app)
mail = Mail(app)

app.register_blueprint(api_bp, url_prefix="/api")

def sessions():
    """Сессии"""
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return session

def service_base():
    service = Services.query.all()
    return render_template("service_base.html", service=service)


@app.route('/', methods=["GET"])
def index():
    """Домашняя страница"""
    visits = sessions().get('visits', 0)
    return render_template('index.html', visits=visits)

@app.route('/thanks')
def thanks():
    """Промежуточная страница. Вывод флеш-сообщений"""
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
            username=user.name
            flash(f"Glad to see you, {username}!")
            session['data'] = {'id': user.id, 'role': user.role}
            print(session)
            return render_template('thanks.html', username=user.name,)
        else:
            flash("Wrong password")
            return redirect("/auth")
            
    return render_template("auth.html")


@app.route('/signup', methods=['POST', 'GET'])
def registration():
    """Регистрация"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
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
        return render_template("auth.html")
        
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
        flash("Letter is sent!", 'success')
        return redirect("/thanks")

    return render_template("claim.html")


@app.route('/all_services', methods=['GET'])
def all_services():
    service = Services.query.all()
    return render_template("all_services.html", service=service)


@app.route('/services/<int:serviceId>', methods=['GET'])
def service(serviceId):
    ser = Services.query.get_or_404(serviceId)
    return render_template("services.html", ser=ser)


@app.route('/search', methods=['GET'])
def search():
    title = request.args.get('title')
    service = db.session.query(Services.id, Services.title, Services.price, Services.specialist).filter(Services.title==title).all()
    return render_template("all_services.html", service=service)

@app.route('/specialists', methods=['GET'])
def specialists():
    specialist = Specialists.query.all()
    return render_template("specialists.html", specialist=specialist)

@app.route('/reviews', methods=['GET'])
def reviews():
    review = Reviews.query.all()
    return render_template("reviews.html", review=review)

@app.route('/del_sessions')
def del_sessions():
    session.pop('visits', None)
    return redirect('/')


@app.route('/out_user')
def out_user():
    session.pop('data', None)
    return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)