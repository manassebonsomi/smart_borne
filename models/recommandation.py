from config.database import db
from datetime import datetime

class Recommandation(db.Model):
    __tablename__ = "recommandation"

    id_recommandation = db.Column(
        db.Integer,
        primary_key=True
    )

    score = db.Column(
        db.Float
    )

    profil_detecte = db.Column(
        db.String(100)
    )

    commentaire = db.Column(
        db.Text
    )

    date_generation = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    id_session = db.Column(
        db.Integer,
        db.ForeignKey(
            "session_utilisateur.id_session"
        ),
        unique=True
    )

    id_parcours = db.Column(
        db.Integer,
        db.ForeignKey(
            "parcours.id_parcours"
        )
    )