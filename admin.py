from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import User, Specialists, Services, Reviews, db

admin = Admin(name='Admin Panel', template_mode='bootstrap3')

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Specialists, db.session))
admin.add_view(ModelView(Reviews, db.session))
admin.add_view(ModelView(Services, db.session))
