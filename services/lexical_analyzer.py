import re

from services.token import Token


class LexicalAnalyzer:

    RESERVED_WORDS = {

        "AFFICHER": "AFFICHER",

        "LANCER": "LANCER",

        "CHERCHER": "CHERCHER",

        "AJOUTER": "AJOUTER",

        "MODIFIER": "MODIFIER",

        "SUPPRIMER": "SUPPRIMER",

        "EXPORTER": "EXPORTER",

        "RECOMMENCER": "RECOMMENCER",

        "QUITTER": "QUITTER",

        "STATISTIQUES": "STATISTIQUES",

        "ERREURS": "ERREURS",

        "ENQUETE": "ENQUETE",

        "CAMPAGNE": "CAMPAGNE",

        "ENFANTS": "ENFANTS",

        "ADOLESCENTS": "ADOLESCENTS",

        "QUESTION": "QUESTION",

        "RAPPORT": "RAPPORT",

        "SESSION": "SESSION",

        "CYBERSECURITE":
            "CYBERSECURITE",

        "ECOLE":
            "ECOLE",

        "PYTHON":
            "PYTHON",

        "KINSHASA":
            "KINSHASA",

        "INTERESSES":
            "INTERESSES",

        "PAR":
            "PAR",

        "LES":
            "LES",

        "LA":
            "LA"

    }

    @staticmethod
    def tokenize(command):

        command = command.upper()

        words = re.findall(
            r'\d+|[A-Z]+',
            command
        )

        tokens = []

        for word in words:

            if word.isdigit():

                tokens.append(
                    Token(
                        "NUMERO",
                        int(word)
                    )
                )

            elif word in \
                    LexicalAnalyzer \
                    .RESERVED_WORDS:

                tokens.append(

                    Token(
                        LexicalAnalyzer
                        .RESERVED_WORDS[word],

                        word
                    )
                )

            else:

                raise Exception(

                    f"Token inconnu : {word}"
                )

        tokens.append(
            Token(
                "EOF",
                "EOF"
            )
        )

        return tokens