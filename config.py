
class Config():
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask_beauty.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'sdojcm;lmfjlsdmfsld,vnmnf'
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '0194067@gmail.com'
    MAIL_PASSWORD = '26ifyouaskme09'
    MAIL_DEFAULT_SENDER = '0194067@gmail.com'

    UPLOAD_FOLDER_SERVICES = '/static/images/services'
    
