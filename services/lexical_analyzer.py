# services/lexical_analyzer.py

import re

from services.token import Token
from services.reserved_words import RESERVED_WORDS
from services.command_suggester import CommandSuggester


class LexicalAnalyzer:

    # ==========================================================
    # MOTS IGNORÉS
    # ==========================================================

    IGNORED_WORDS = {

        "LE",
        "LA",
        "LES",

        "DE",
        "DU",
        "DES",

        "UN",
        "UNE",

        "ET",

        "D",
        "L"
    }

    # ==========================================================
    # TOKENIZE
    # ==========================================================

    @staticmethod
    def tokenize(command):

        if command is None:

            raise ValueError(
                "Commande vide."
            )

        command = str(command).strip()

        if not command:

            raise ValueError(
                "Commande vide."
            )

        command = command.upper()

        words = re.findall(
            r"\d+|[A-ZÀ-ÖØ-Ý]+",
            command
        )

        tokens = []

        for word in words:

            # --------------------------------------------------
            # Articles / mots ignorés
            # --------------------------------------------------

            if word in LexicalAnalyzer.IGNORED_WORDS:

                continue

            # --------------------------------------------------
            # Nombre
            # --------------------------------------------------

            if word.isdigit():

                tokens.append(
                    Token(
                        "NUMERO",
                        int(word)
                    )
                )

                continue

            # --------------------------------------------------
            # Mot réservé
            # --------------------------------------------------

            if word in RESERVED_WORDS:

                tokens.append(
                    Token(
                        RESERVED_WORDS[word],
                        word
                    )
                )

                continue

            # --------------------------------------------------
            # Mot inconnu
            # --------------------------------------------------

            suggestion = (
                CommandSuggester
                .suggest(word)
            )

            if suggestion:

                raise Exception(
                    f"Token inconnu : "
                    f"{word}. "
                    f"Voulez-vous dire "
                    f"'{suggestion}' ?"
                )

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