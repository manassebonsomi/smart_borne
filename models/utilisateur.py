from config.database import db
from datetime import datetime

class Utilisateur(db.Model):
    __tablename__ = "utilisateur"

    id_utilisateur = db.Column(db.Integer, primary_key=True)

    nom = db.Column(db.String(100), nullable=False)

    prenom = db.Column(db.String(100), nullable=False)

    age = db.Column(db.Integer, nullable=False)

    niveau_scolaire = db.Column(db.String(30), nullable=False)

    type_profil = db.Column(db.String(30), nullable=False)

    date_creation = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    id_ville = db.Column(
        db.Integer,
        db.ForeignKey("ville.id_ville")
    )

    sessions = db.relationship(
        "SessionUtilisateur",
        backref="utilisateur",
        lazy=True
    )