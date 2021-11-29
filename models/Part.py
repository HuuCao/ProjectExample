import datetime

from .base import db

class Part(db.Model):
   id = db.Column('id', db.Integer, autoincrement=True, primary_key = True)
   name = db.Column(db.String(256), nullable=False)
   type = db.Column(db.String(256), nullable=False)
   price = db.Column(db.Boolean, nullable=False)
   createdAt = db.Column(db.DateTime, nullable=False, server_default=db.text("NOW()"))
   isActivate = db.Column(db.Boolean, default=True, server_default="True")
   # part_build = relationship('part_build', backref='part_build')

   builds = db.relationship(
      "Build",
      secondary="Part_Build",
      primaryjoin="Part.id == Part_Build.idBuild",
      secondaryjoin="Part_Build.idPart == Build.id",
   )