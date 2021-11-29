from .base import db

class Build(db.Model):
   id = db.Column('id', db.Integer, autoincrement=True, primary_key = True)
   name = db.Column(db.String(256), nullable=False)
   price = db.Column(db.Boolean, nullable=False)
   createdAt = db.Column(db.DateTime, nullable=False, server_default=db.text("NOW()"))
   isActivate = db.Column(db.Boolean, default=True, server_default="True")
   # Relationship with User
   idUser = db.Column(db.Integer, db.ForeignKey('user.id'))
   owner = db.relationship('user', foreign_keys=[idUser], backref="pc_builds")
   # Relationship with Part_Build
   parts = db.relationship(
      "part",
      secondary="Part_Build",
      primaryjoin="Build.id == Part_Build.idBuild",
      secondaryjoin="Part_Build.idPart == Part.id",
   )
   # part_build = relationship('part_build', backref='part_build')