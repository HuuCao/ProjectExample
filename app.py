import os

from flask import Flask

from dotenv import load_dotenv

from .models.base import db, migrate
from .blueprint_register import register_blueprint

load_dotenv()

# os.environ = {
#    "SERVER":'lgfzkc111',
#    "DATABASE":  'example'
# }

# size = 32
# SECRET_KEY = os.urandom(size)
# SERVER = 'localhost'
# DATABASE = 'example'
# USERNAME = 'postgres'
# PASSWORD = 'lgfzkc111'
# DATABASE_CONNECTION = f'postgresql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}'

app = Flask (__name__)

app.config['JWT_SECRET_KEY'] = os.environ.get("SECRET_KEY")
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNECTION_STRING
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_CONNECTION_STRING")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ.get(
   "DB_TRACK_MODIFICATIONS"
)
      #   app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

db.init_app(app)
migrate.init_app(app)

register_blueprint(app)
# db = SQLAlchemy(app)
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port='3001')  ## start với lệnh python app.py

if __name__ == "__main__":
   app.run(debug=True) ## start với lệnh flask run