from .base import db

class Part_Build(db.Model):
   __table_args__ = (db.PrimaryKeyConstraint("idPart", "idBuild"),)

   idPart = db.Column('idPart', db.Integer, db.ForeignKey('part.id'))
   idBuild = db.Column('idBuild', db.Integer, db.ForeignKey('build.id'))