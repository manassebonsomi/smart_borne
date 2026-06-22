from config.database import db

class Evenement(db.Model):
    __tablename__ = "evenement"

    id_evenement = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(255))
    description = db.Column(db.Text)
    date_evenement = db.Column(db.DateTime)