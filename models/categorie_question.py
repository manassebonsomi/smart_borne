from config.database import db

class CategorieQuestion(db.Model):
    __tablename__ = "categorie_question"

    id_categorie = db.Column(
        db.Integer,
        primary_key=True
    )

    nom_categorie = db.Column(
        db.String(100),
        nullable=False
    )

    questions = db.relationship(
        "Question",
        backref="categorie",
        lazy=True
    )