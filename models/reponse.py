from config.database import db
from datetime import datetime

class Reponse(db.Model):
    __tablename__ = "reponse"

    id_reponse = db.Column(
        db.Integer,
        primary_key=True
    )

    valeur_reponse = db.Column(
        db.Text,
        nullable=False
    )

    date_reponse = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    id_session = db.Column(
        db.Integer,
        db.ForeignKey(
            "session_utilisateur.id_session"
        )
    )

    id_question = db.Column(
        db.Integer,
        db.ForeignKey(
            "question.id_question"
        )
    )