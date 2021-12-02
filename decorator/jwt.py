import os
import traceback

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
# from ..app import SECRET_KEY
from ..models import User
from ..models.base import db
# imports for PyJWT authentication

import jwt
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, os.environ.get("JWT_SECRET_KEY"), algorithms=["HS256"])
            current_user = User.query\
                .filter_by(id = data['id'])\
                .first()
            request.user = current_user
            # returns the current logged in users contex to the routes
            return f(*args, **kwargs)
        except Exception as error:
            print(error)
            traceback.print_exc()
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        
  
    return decorated