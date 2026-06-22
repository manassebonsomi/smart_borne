from config.database import db

class Ville(db.Model):
    __tablename__ = "ville"

    id_ville = db.Column(db.Integer, primary_key=True)
    nom_ville = db.Column(db.String(100), unique=True, nullable=False)
    utilisateurs = db.relationship("Utilisateur", backref="ville", lazy=True)