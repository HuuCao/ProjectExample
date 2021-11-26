# GET /health_check
from flask import Blueprint

from flask.views import MethodView

# from decorator import isAuthenticated

health_check_bp = Blueprint("health_check_bp", __name__)

class HealthCheckAPI(MethodView):
    # @isAuthenticated
    def get(self):
        return "Server is up and ready!"
    
    # @isAuthenticated
    def post(self):
        pass
    def put(self):
        pass
    def delete(self):
        pass


health_check_view = HealthCheckAPI.as_view("health_check_api")

health_check_bp.add_url_rule(
    "/health_check", view_func=health_check_view, methods=["GET"]
)

# Node: middleware
# python: decorator