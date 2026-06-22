from config.database import db

class Campagne(db.Model):
    __tablename__ = "campagne"

    id_campagne = db.Column(db.Integer, primary_key=True)
    nom_campagne = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    date_debut = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    active = db.Column(db.Boolean, default=True)
    sessions = db.relationship("SessionUtilisateur", backref="campagne", lazy=True)