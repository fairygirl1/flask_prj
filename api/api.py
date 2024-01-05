from flask import Flask, Blueprint, jsonify
from flask_restful import Api, Resource
from config import Config
from models import Services, Specialists, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

class ServicesApi(Resource):
    def get(self):
        services = Services.query.all()
        service_data = [{"id": service.id, "title": service.title, "description": service.description,
                        "specialist": service.specialist, "price": service.price} for service in services]
        return jsonify({"services": service_data})

class SpecialistsApi(Resource):
    def get(self):
        specialists = Specialists.query.all()
        specialist_data = [{"id": specialist.id, "name": specialist.name, "position": specialist.position}
                        for specialist in specialists]
        return jsonify({"specialists": specialist_data})

api.add_resource(ServicesApi, '/services')
api.add_resource(SpecialistsApi, '/specialists')

app.register_blueprint(api_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
