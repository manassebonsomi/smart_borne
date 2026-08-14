from config.database import db
from datetime import datetime
from sqlalchemy import CheckConstraint, Index

class SessionUtilisateur(db.Model):
    __tablename__ = "session_utilisateur"

    id_session = db.Column(db.Integer, primary_key=True)
    date_debut = db.Column(db.DateTime, default=datetime.utcnow)
    date_fin = db.Column(db.DateTime)
    etat = db.Column(db.String(50))
    sauvegardee = db.Column(db.Boolean, default=False,  nullable=False)
    question_actuelle = db.Column(db.Integer, default=0,  nullable=False)
    temps_inactivite = db.Column(db.Integer, default=0,  nullable=False)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey("utilisateur.id_utilisateur"),  index=True)
    id_campagne = db.Column(db.Integer, db.ForeignKey("campagne.id_campagne"),  index=True)
    reponses = db.relationship("Reponse", backref="session", lazy=True)

    __table_args__ = (CheckConstraint("question_actuelle >= 0", name="ck_session_question_actuelle"),
        CheckConstraint("temps_inactivite >= 0", name="ck_session_temps_inactivite"),)