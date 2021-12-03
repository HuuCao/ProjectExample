import traceback

from flask import Blueprint, request, jsonify, make_response, current_app
from datetime import datetime, timedelta

from flask.views import MethodView

from ..models import Part_Build, Build, Part
from ..models.base import db
from ..decorator.jwt import token_required

build_bp = Blueprint("build_bp", __name__)

class BuildAPI(MethodView):     
## ===================== Create Build ===================== ##   
    @token_required
    def post (self):
        try:
            data = request.get_json()

            build_name = data['name']
            check_name = Build.query.filter_by(name = build_name).first()
            if check_name:
                return jsonify({ 'message': 'Name already exists!' }), 400

            including_parts = Part.query.filter(Part.id.in_(data['parts'])).all()
            # data_part = including_parts.parts
            print(including_parts)
            
            new_build = Build(name=build_name, price=0)
            for part in including_parts:
                new_build.price += part.price
                new_build.parts.append(part)
            new_build.idUser = request.user.id

            db.session.commit()
            # build.parts
            
            # db.session.add(new_build)
            # db.session.flush()

            # for part in including_parts:
            #     new_part_build = Part_Build(idBuild=new_build.id, idPart=part.id)
            #     db.session.add(new_part_build)
            return jsonify({ 'message': 'Part created successfully!' }), 201
        except Exception as error:
            traceback.print_exc()
            print(error)
            return jsonify({ 'message': 'Create Fail!' }), 500

## ===================== Get All Build ===================== ##
    @token_required
    def get(self):
        current_user = request.user
        
        if current_user.isAdmin is not True:
            return jsonify({ 'message' : 'Cannot perform that function!' })
            
        name = request.args.get('name')
        search = "%{}%".format(name or '')
        
        if name is not None:
            builds = Build.query.filter(Build.isActivate.is_(True), Build.name.ilike(search)).all()
        else:
            builds = Build.query.filter(Build.isActivate.is_(True)).all()

        output = []
        for build in builds:
            build_data = {}
            build_parts = build.parts
            build_parts_for_response = []

            for part in build_parts:
                build_parts_for_response.append({
                    "id": part.id,
                    "name": part.name,
                    "price": part.price,
                })
            build_data['id'] = build.id
            build_data['name'] = build.name
            build_data['price'] = build.price
            # build_data['user'] = build.owner
            build_data['parts'] = build_parts_for_response
            build_data['createdAt'] = build.createdAt
            build_data['isActivate'] = build.isActivate
            output.append(build_data)
        # print(output)
        return make_response(jsonify({'builds': output}), 200)

## ===================== Get Build By Id Build ===================== ##
class GetBuildByIdAPI(MethodView):
    @token_required
    def get(self, id):
        build = Build.query.filter_by(id=id).first()
        # data_part = build.parts

        if not build:
            return jsonify({ 'message': 'Part not found!' }), 400
        build_parts_for_response = []
        build_parts = build.parts
        for part in build_parts:
            build_parts_for_response.append({
                "id": part.id,
                "name": part.name,
                "price": part.price,
            })

        user_for_response = []
        users = build.owner
        for user in users:
            user_for_response.append({
                "id": user.id,
                "username": user.username,
                "password": user.password,
                "isAdmin": user.isAdmin,
                "createdAt": user.createdAt,
                "isActivate": user.isActivate,
            })
        build_data = {}
        build_data['id'] = build.id
        build_data['name'] = build.name
        build_data['parts'] = build_parts_for_response
        build_data['parts'] = user_for_response
        build_data['price'] = build.price
        build_data['createdAt'] = build.createdAt
        build_data['isActivate'] = build.isActivate
            # output.append(part_data)
        # print(output)
        return make_response(jsonify({'builds': build_data}), 201)

## ===================== Update Build ===================== ##

class UpdateAPI(MethodView):
    @token_required
    def put(self, id):
        try:
            data = request.get_json()
 
            existing_build = Build\
                .query\
                .get(id)
            
            name = data['name']
            isActivate = data['isActivate']  

            # check_name = Build.query.filter_by(name = name).first()
            # if check_name:
            #     return jsonify({ 'message': 'Name already exists!' }), 400

            existing_build.name = name
            existing_build.isActivate = isActivate

            # update parts
            existing_build.parts = []
            existing_build.price = 0
            including_parts = Part.query.filter(Part.id.in_(data['parts'])).all()
            for part in including_parts :
                existing_build.price += part.price
                existing_build.parts.append(part)

            db.session.commit()
            return jsonify({ 'message': 'Updated successfully!' })

        except Exception as err:
            import traceback
            traceback.print_exc()
            print("================")
            print(err)
            return jsonify({ 'message': 'Update fail!' })

build_view = BuildAPI.as_view("build_api")
update_view = UpdateAPI.as_view("update_api")
get_build_by_id_view = GetBuildByIdAPI.as_view("get_build_by_id_api")

build_bp.add_url_rule(
    "/api/builds", view_func = build_view, methods=["POST", "GET"]
)
build_bp.add_url_rule(
    "/api/builds/<int:id>", view_func = get_build_by_id_view, methods=["GET"]
)
build_bp.add_url_rule(
    "/api/builds/<int:id>", view_func = update_view, methods=["PUT"]
)