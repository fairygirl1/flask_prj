from models import User, Specialists, Services, Reviews, db
from flask import Blueprint, jsonify, abort, request, current_app


api_bp = Blueprint("api", __name__, template_folder="templates", static_folder="static")

@api_bp.route('/all_services', methods=['GET'])
def all_services():
    ser_list = []

    services = db.session.query(Services.title, Services.description, Services.specialist, Services.price).all()

    for res in services:
        service_dict = {
            'service_title': res[0],
            'service_description': res[1],
            'service_specialist': res[2],
            'services_price': res[3],
        }
        ser_list.append(service_dict)


    return jsonify(ser_list)