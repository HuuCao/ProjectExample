import traceback

from flask import Blueprint, request, jsonify, make_response, current_app
from datetime import datetime, timedelta

from flask.views import MethodView

from ..models import Part_Build, Build, Part
from ..models.base import db
from ..decorator.jwt import token_required

# current_app.config.get("DB_NAME")

build_bp = Blueprint("build_bp", __name__)

class BuildAPI(MethodView):        
    @token_required
    def post (self):
        try:
            data = request.get_json()

            data_name = data['name']
            if not data_name:
                return jsonify({ 'message': 'Missing Name!' }), 400

            including_parts = Part.query.filter(Part.id.in_(data['parts'])).all()
            
            new_build = Build(name=data_name, price=0)
            for part in including_parts:
                new_build.price += part.price
                new_build.parts.append(part)
            
            new_build.idUser = request.user.id

            build.parts
            
            # db.session.add(new_build)
            # db.session.flush()

            # for part in including_parts:
            #     new_part_build = Part_Build(idBuild=new_build.id, idPart=part.id)
            #     db.session.add(new_part_build)
            
            db.session.commit()

            return jsonify({ 'message': 'Part created successfully!' }), 201

        except Exception as error:
            traceback.print_exc()
            print(error)
            return jsonify({ 'message': 'Create Fail!' }), 500

build_view = BuildAPI.as_view("build_api")

build_bp.add_url_rule(
    "/api/builds", view_func = build_view, methods=["POST", "GET"]
)