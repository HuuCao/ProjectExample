from flask import Blueprint, request, jsonify, make_response, current_app
from datetime import datetime, timedelta

from flask.views import MethodView

from models.Part import Part

from ..models import Part_Build
from ..models import Build
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
            parts = Build.parts
            print(parts)

            if not data_name:
                return jsonify({ 'message': 'Missing Name!' }), 400


            # new_build = Build(
            #     name = data_name,
            #     isActivate = True
            # )
            # print (new_build)
            # db.session.add(new_build)
            # db.session.commit()


            return jsonify({ 'message': 'Part created successfully!' }), 201

        except Exception as error:
            print(error)
            return jsonify({ 'message': 'Create Fail!' }), 500

build_view = BuildAPI.as_view("build_api")

build_bp.add_url_rule(
    "/api/builds", view_func = build_view, methods=["POST", "GET"]
)