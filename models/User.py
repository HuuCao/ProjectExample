from .base import db

class User(db.Model):
   id = db.Column('id', db.Integer, autoincrement=True, primary_key = True)
   username = db.Column(db.String(256), nullable=False)
   password = db.Column(db.String(256), nullable=False)
   isAdmin = db.Column(db.Boolean, nullable=False)
   createdAt = db.Column(db.DateTime, nullable=False, server_default=db.text("NOW()"))
   isActivate = db.Column(db.Boolean, default=True, server_default="True")

   # builds = db.relationship('Build', backref='user')
   # pc_builds = db.relationship('Build'),
