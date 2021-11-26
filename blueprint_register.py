from .controllers.health_check import health_check_bp
from .controllers.auth import auth_bp

# def register_blueprint(app):
#     app.register_blueprint(health_check_bp)

def register_blueprint(app):
    app.register_blueprint(auth_bp)