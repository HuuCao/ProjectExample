from .controllers.health_check import health_check_bp
from .controllers.auth import auth_bp
from .controllers.part import part_bp
from .controllers.build import build_bp

def register_blueprint(app):
    app.register_blueprint(health_check_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(part_bp)
    app.register_blueprint(build_bp)