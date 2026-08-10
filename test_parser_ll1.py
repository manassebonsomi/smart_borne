from services.lexical_analyzer import LexicalAnalyzer
from services.ll1_parser import LL1Parser


COMMANDES_VALIDES = [

    "AFFICHER STATISTIQUES",

    "AFFICHER ERREURS",

    "LANCER ENQUETE CYBERSECURITE",

    "LANCER CAMPAGNE ECOLE",

    "CHERCHER ENFANTS KINSHASA",

    "CHERCHER ADOLESCENTS INTERESSES PAR PYTHON",

    "AJOUTER QUESTION",

    "MODIFIER QUESTION 3",

    "SUPPRIMER QUESTION 2",

    "EXPORTER RAPPORT",

    "RECOMMENCER SESSION",

    "QUITTER"
]


COMMANDES_INVALIDES = [

    "AFFICHER QUESTION",

    "MODIFIER STATISTIQUES",

    "LANCER QUESTION",

    "AJOUTER STATISTIQUES",

    "SUPPRIMER RAPPORT",

    "QUITTER QUESTION"
]


def tester_commande(command):

    print()
    print("=" * 80)
    print(
        f"COMMANDE : {command}"
    )
    print("=" * 80)

    try:

        tokens = LexicalAnalyzer.tokenize(
            command
        )

        print()
        print("TOKENS :")

        for token in tokens:

            print(
                f"  {token.type} "
                f"-> "
                f"{token.value}"
            )

        result = LL1Parser.parse(
            tokens,
            return_trace=True
        )

        print()
        print("RESULTAT :")

        print(
            result["message"]
        )

        LL1Parser.display_trace(
            result
        )

    except Exception as error:

        print()
        print(
            "ERREUR LEXICALE :"
        )

        print(
            str(error)
        )


print()
print("#" * 80)
print("COMMANDES VALIDES")
print("#" * 80)

for command in COMMANDES_VALIDES:

    tester_commande(
        command
    )


print()
print()
print("#" * 80)
print("COMMANDES INVALIDES")
print("#" * 80)

for command in COMMANDES_INVALIDES:

    tester_commande(
        command
    )