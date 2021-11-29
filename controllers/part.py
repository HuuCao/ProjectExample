import jwt
import os

from flask import Blueprint, request, jsonify, make_response, current_app
from datetime import datetime, timedelta

from flask.views import MethodView
from ..models import Part
from ..models.base import db
from ..decorator.jwt import token_required

# current_app.config.get("DB_NAME")

part_bp = Blueprint("part_bp", __name__)

class PartAPI(MethodView):
    @token_required
    def get(self):
        current_user = request.user
        print(current_user.isAdmin)
        if current_user.isAdmin is not True:
            return jsonify({ 'message' : 'Cannot perform that function!' })

        # parts = Part.query.all()
        parts = Part.query.filter_by( isActivate=True ).all()
        output = []
        for part in parts:
            part_data = {}
            part_data['id'] = part.id
            part_data['username'] = part.name
            part_data['type'] = part.type
            part_data['price'] = part.price
            part_data['createdAt'] = part.createdAt
            part_data['isActivate'] = part.isActivate
            output.append(part_data)
        # print(output)
        return make_response(jsonify({'users': output}), 201)
        
    @token_required
    def post (self):
        try:
            data = request.get_json()

            current_user = request.user
            print(current_user)
            if current_user.isAdmin is not True:
                return jsonify({ 'message' : 'You are not an admin. Not allowed to create Part!' })

            if not data['name']:
                return jsonify({ 'message': 'Missing Name!' }), 400
            if not data['type']:
                return jsonify({ 'message': 'Missing Type!' }), 400
            if not data['price']:
                return jsonify({ 'message': 'Missing Price!' }), 400
            
            if data['type'] is not 'cpu' or\
                data['type'] is not 'ram' or\
                data['type'] is not 'gpu' or\
                data['type'] is not 'storage' or\
                data['type'] is not 'psu' or\
                data['type'] is not 'case':
                    return jsonify({ 'message': 'Invalid type!' })
            
            check_part = Part.query.filter_by(name = data['name']).first()

            if check_part:
                return jsonify({ 'message': 'Name already exists!' })

            new_part = Part(
                name = data['name'],
                type = data['type'],
                price = data['price'],
                isActivate = True
            )

            db.session.add(new_part)
            db.session.commit()

        except Exception as error:
            print(error)
            return jsonify({ 'message': 'Create Fail!' })

class UpdateAPI(MethodView):
    @token_required
    def put(self, id):
        try:
            data = request.get_json()
            current_user = request.user
            print(current_user)
            if current_user.isAdmin is not True:
                return jsonify({ 'message' : 'Cannot perform that function!' })

            update_part = Part\
                .query\
                .get(id)

            name = data['name']
            type = data['type']
            price = data['price']
            isActivate = data['isActivate']  

            update_part.name = name
            update_part.type = type
            update_part.price = price
            update_part.isActivate = isActivate

            db.session.commit()
            return jsonify({ 'message': 'Updated successfully!' })

        except Exception as err:
            print("================")
            print(err)
            return jsonify({ 'message': 'Update fail!' })


part_view = PartAPI.as_view("part_api")

part_bp.add_url_rule(
    "/api/part", view_func = part_view, methods=["POST", "GET"]
)