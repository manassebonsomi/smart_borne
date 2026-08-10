from services.lexical_analyzer import LexicalAnalyzer
from services.ll1_parser import LL1Parser


commands = [
    "AFFICHER QUESTION",
    "MODIFIER STATISTIQUES",
    "LANCER QUESTION",
    "MODIFIER QUESTION",
    "SUPPRIMER QUESTION",
    "QUITTER QUESTION",
    "AFFICHER STATISTIQUES QUESTION",
]


for command in commands:

    print()
    print("=" * 80)
    print(f"COMMANDE : {command}")
    print("=" * 80)

    try:

        tokens = LexicalAnalyzer.tokenize(
            command
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

        print()
        print("NOMBRE D'ERREURS :")
        print(
            len(
                result.get(
                    "errors",
                    []
                )
            )
        )

        LL1Parser.display_trace(
            result
        )

    except Exception as e:

        print()
        print(
            "ERREUR LEXICALE :",
            e
        )