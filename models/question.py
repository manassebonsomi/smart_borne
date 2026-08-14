from config.database import db
from sqlalchemy import CheckConstraint, Index

class Question(db.Model):
    __tablename__ = "question"

    id_question = db.Column(db.Integer, primary_key=True)
    texte_question = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, default=True)
    ordre_question = db.Column(db.Integer, nullable=False)
    id_categorie = db.Column(db.Integer, db.ForeignKey("categorie_question.id_categorie"), index=True)
    reponses = db.relationship("Reponse", backref="question", lazy=True)

    __table_args__ = (CheckConstraint("ordre_question > 0", name="ck_question_ordre_positif"),
        Index("ix_question_active", "active"),)