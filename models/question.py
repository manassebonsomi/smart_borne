from config.database import db

class Question(db.Model):
    __tablename__ = "question"

    id_question = db.Column(db.Integer, primary_key=True)
    texte_question = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, default=True)
    ordre_question = db.Column(db.Integer, nullable=False)
    id_categorie = db.Column(db.Integer, db.ForeignKey("categorie_question.id_categorie"))
    reponses = db.relationship("Reponse", backref="question", lazy=True)