from config.database import db
from datetime import datetime

class Commande(db.Model):
    __tablename__ = "commande"

    id_commande = db.Column(db.Integer, primary_key=True)
    texte_commande = db.Column(db.Text, nullable=False)
    tokens = db.Column(db.Text)
    resultat = db.Column(db.Text)
    valide = db.Column(db.Boolean)
    date_execution = db.Column(db.DateTime,default=datetime.utcnow)
    id_formateur = db.Column(db.Integer, db.ForeignKey("formateur.id_formateur"))