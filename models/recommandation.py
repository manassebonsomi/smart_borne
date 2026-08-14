from config.database import db
from datetime import datetime
from sqlalchemy import CheckConstraint

class Recommandation(db.Model):
    __tablename__ = "recommandation"

    id_recommandation = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float)
    profil_detecte = db.Column(db.String(100))
    commentaire = db.Column(db.Text)
    date_generation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_session = db.Column(db.Integer, db.ForeignKey("session_utilisateur.id_session"), nullable=False, unique=True,  index=True)
    id_parcours = db.Column(db.Integer, db.ForeignKey("parcours.id_parcours"), nullable=False,  index=True)

    __table_args__ = (CheckConstraint("score >= 0", name="ck_recommandation_score_positif"),)