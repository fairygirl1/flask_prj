from flask import Flask, render_template, url_for, request, redirect, make_response, session,flash,get_flashed_messages
from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_beauty.db'
app.secret_key = os.environ.get('secret_key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

@app.route('/index')
@app.route('/home')
@app.route('/')


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
        except:
            return "Error"
        return redirect("/auth")
    return render_template('registration.html')




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)