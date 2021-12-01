from .base import db

class Part(db.Model):
   id = db.Column('id', db.Integer, autoincrement=True, primary_key = True)
   name = db.Column(db.String(256), nullable=False)
   type = db.Column(db.String(256), nullable=False)
   price = db.Column(db.Numeric(), nullable=False)
   createdAt = db.Column(db.DateTime, nullable=False, server_default=db.text("NOW()"))
   isActivate = db.Column(db.Boolean, default=True, server_default="True")
   # part_build = db.relationship('Part_Build', backref='part_build')

   # builds = db.relationship(
   #    "Build",
   #    secondary="part__build",
   #    primaryjoin="Part.id == Part_Build.idPart",
   #    secondaryjoin="Part_Build.idBuild == Build.id",
   # )