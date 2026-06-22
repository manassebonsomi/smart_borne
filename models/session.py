from config.database import db
from datetime import datetime

class SessionUtilisateur(db.Model):
    __tablename__ = "session_utilisateur"

    id_session = db.Column(db.Integer, primary_key=True)
    date_debut = db.Column(db.DateTime, default=datetime.utcnow)
    date_fin = db.Column(db.DateTime)
    etat = db.Column(db.String(50))
    sauvegardee = db.Column(db.Boolean, default=False)
    question_actuelle = db.Column(db.Integer, default=0)
    temps_inactivite = db.Column(db.Integer, default=0)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey("utilisateur.id_utilisateur"))
    id_campagne = db.Column(db.Integer, db.ForeignKey("campagne.id_campagne"))
    reponses = db.relationship("Reponse", backref="session", lazy=True)