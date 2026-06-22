from app import app
from config.database import db
from models.question import Question


QUESTIONS = [

    # CREATIVITE (ID = 1)
    {
        "texte": "Aimes-tu dessiner ?",
        "ordre": 1,
        "categorie": 1
    },
    {
        "texte": "Aimes-tu inventer des histoires ?",
        "ordre": 2,
        "categorie": 1
    },
    {
        "texte": "Aimes-tu créer des animations ?",
        "ordre": 3,
        "categorie": 1
    },
    {
        "texte": "Aimes-tu fabriquer des objets ?",
        "ordre": 4,
        "categorie": 1
    },
    {
        "texte": "Aimes-tu imaginer de nouveaux jeux ?",
        "ordre": 5,
        "categorie": 1
    },
    {
        "texte": "Aimes-tu personnaliser tes créations ?",
        "ordre": 6,
        "categorie": 1
    },
    {
        "texte": "Aimes-tu inventer des personnages ?",
        "ordre": 7,
        "categorie": 1
    },
    {
        "texte": "Aimes-tu créer des projets artistiques ?",
        "ordre": 8,
        "categorie": 1
    },


    # LOGIQUE (ID = 2)
    {
        "texte": "Aimes-tu résoudre des énigmes ?",
        "ordre": 9,
        "categorie": 2
    },
    {
        "texte": "Aimes-tu les casse-têtes ?",
        "ordre": 10,
        "categorie": 2
    },

    {
        "texte": "Aimes-tu trouver des solutions ?",
        "ordre": 11,
        "categorie": 2
    },

    {
        "texte": "Aimes-tu les jeux de réflexion ?",
        "ordre": 12,
        "categorie": 2
    },

    {
        "texte": "Aimes-tu comprendre comment les choses fonctionnent ?",
        "ordre": 13,
        "categorie": 2
    },

    {
        "texte": "Aimes-tu les mathématiques ?",
        "ordre": 14,
        "categorie": 2
    },

    {
        "texte": "Aimes-tu relever des défis ?",
        "ordre": 15,
        "categorie": 2
    },

    {
        "texte": "Aimes-tu organiser des informations ?",
        "ordre": 16,
        "categorie": 2
    },


    # PROGRAMMATION (ID = 3)
    {
        "texte": "Aimes-tu programmer ?",
        "ordre": 17,
        "categorie": 3
    },

    {
        "texte": "Aimes-tu créer des applications ?",
        "ordre": 18,
        "categorie": 3
    },

    {
        "texte": "Aimes-tu comprendre le fonctionnement des ordinateurs ?",
        "ordre": 19,
        "categorie": 3
    },

    {
        "texte": "Aimes-tu créer des jeux vidéo ?",
        "ordre": 20,
        "categorie": 3
    },

    {
        "texte": "Aimes-tu apprendre Python ?",
        "ordre": 21,
        "categorie": 3
    },

    {
        "texte": "Aimes-tu créer des robots ?",
        "ordre": 22,
        "categorie": 3
    },

    {
        "texte": "Aimes-tu développer des sites web ?",
        "ordre": 23,
        "categorie": 3
    },

    {
        "texte": "Aimes-tu automatiser des tâches ?",
        "ordre": 24,
        "categorie": 3
    },


    # LEADERSHIP (ID = 4)

    {
        "texte": "Aimes-tu aider les autres ?",
        "ordre": 25,
        "categorie": 4
    },

    {
        "texte": "Aimes-tu expliquer des choses ?",
        "ordre": 26,
        "categorie": 4
    },

    {
        "texte": "Aimes-tu enseigner ?",
        "ordre": 27,
        "categorie": 4
    },

    {
        "texte": "Aimes-tu diriger une équipe ?",
        "ordre": 28,
        "categorie": 4
    },

    {
        "texte": "Aimes-tu prendre des initiatives ?",
        "ordre": 29,
        "categorie": 4
    },

    {
        "texte": "Aimes-tu organiser des activités ?",
        "ordre": 30,
        "categorie": 4
    },

    {
        "texte": "Aimes-tu motiver les autres ?",
        "ordre": 31,
        "categorie": 4
    },

    {
        "texte": "Aimes-tu partager tes connaissances ?",
        "ordre": 32,
        "categorie": 4
    },


    # NUMERIQUE (ID = 5)
    {
        "texte": "Aimes-tu utiliser un ordinateur ?",
        "ordre": 33,
        "categorie": 5
    },

    {
        "texte": "Aimes-tu découvrir de nouvelles technologies ?",
        "ordre": 34,
        "categorie": 5
    },

    {
        "texte": "Aimes-tu utiliser Internet ?",
        "ordre": 35,
        "categorie": 5
    },

    {
        "texte": "Aimes-tu apprendre des outils numériques ?",
        "ordre": 36,
        "categorie": 5
    },

    {
        "texte": "Aimes-tu travailler sur tablette ?",
        "ordre": 37,
        "categorie": 5
    },

    {
        "texte": "Aimes-tu explorer des logiciels ?",
        "ordre": 38,
        "categorie": 5
    },

    {
        "texte": "Aimes-tu utiliser des applications ?",
        "ordre": 39,
        "categorie": 5
    },

    {
        "texte": "Aimes-tu découvrir l'intelligence artificielle ?",
        "ordre": 40,
        "categorie": 5
    }
]


with app.app_context():

    for q in QUESTIONS:
        existe = Question.query.filter_by(ordre_question=q["ordre"]).first()

        if not existe:
            question = Question(
                texte_question=q["texte"],
                ordre_question=q["ordre"],
                active=True,
                id_categorie=q["categorie"]
            )
            db.session.add(question)
    db.session.commit()

    print("questions insérées avec succès.")