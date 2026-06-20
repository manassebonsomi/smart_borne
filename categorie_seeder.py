from app import app

from config.database import db

from models.categorie_question \
    import CategorieQuestion


CATEGORIES = [

    "Créativité",

    "Logique",

    "Programmation",

    "Leadership",

    "Numérique"
]


with app.app_context():

    for nom in CATEGORIES:

        existe = \
            CategorieQuestion.query.filter_by(

                nom_categorie=nom

            ).first()

        if not existe:

            db.session.add(

                CategorieQuestion(

                    nom_categorie=nom
                )
            )

    db.session.commit()

    print("Catégories créées.")