from config.database import db

class Formateur(db.Model):
    __tablename__ = "formateur"

    id_formateur = db.Column(
        db.Integer,
        primary_key=True
    )

    nom = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    mot_de_passe = db.Column(
        db.String(255),
        nullable=False
    )

    actif = db.Column(
        db.Boolean,
        default=True
    )

    commandes = db.relationship(
        "Commande",
        backref="formateur",
        lazy=True
    )