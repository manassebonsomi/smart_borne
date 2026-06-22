from config.database import db
from datetime import datetime

class Erreur(db.Model):
    __tablename__ = "erreur"

    id_erreur = db.Column(db.Integer, primary_key=True)
    type_erreur = db.Column(db.String(100))
    message = db.Column(db.Text)
    corrigee = db.Column(db.Boolean, default=False)
    date_erreur = db.Column(db.DateTime, default=datetime.utcnow)