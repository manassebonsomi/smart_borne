from services.lexical_analyzer import LexicalAnalyzer
from services.ll1_parser import LL1Parser


commandes = [

    "AFFICHER STATISTIQUES",

    "AFFICHER ERREURS",

    "AFFICHER LES STATISTIQUES",

    "AFFICHER LES ERREURS",

    "LANCER ENQUETE CYBERSECURITE",

    "LANCER CAMPAGNE ECOLE",

    "CHERCHER ENFANTS KINSHASA",

    "CHERCHER ADOLESCENTS INTERESSES PAR PYTHON",

    "AJOUTER QUESTION",

    "MODIFIER QUESTION 3",

    "SUPPRIMER QUESTION 3",

    "EXPORTER RAPPORT",

    "RECOMMENCER SESSION",

    "QUITTER"
]


for commande in commandes:

    print()
    print("=" * 60)
    print(commande)
    print("=" * 60)

    try:

        tokens = LexicalAnalyzer.tokenize(
            commande
        )

        result = LL1Parser.parse(
            tokens,
            return_trace=True
        )

        print(
            "SUCCESS :",
            result["success"]
        )

        print(
            "MESSAGE :",
            result.get("message")
        )

    except Exception as e:

        print(
            "ERREUR :",
            str(e)
        )