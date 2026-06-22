from config.database import db

class Parcours(db.Model):
    __tablename__ = "parcours"

    id_parcours = db.Column(db.Integer, primary_key=True)
    nom_parcours = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    recommandations = db.relationship("Recommandation", backref="parcours", lazy=True)