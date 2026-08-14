# services/command_suggester.py

from difflib import (
    SequenceMatcher,
    get_close_matches
)

from services.reserved_words import (
    RESERVED_WORDS
)

from services.correction_config import (
    CorrectionConfig
)


class CommandSuggester:

    # ==========================================================
    # SIMILARITÉ
    # ==========================================================

    @staticmethod
    def similarity(
        word,
        candidate
    ):
        """
        Calcule la similarité entre deux mots.

        Retourne une valeur comprise entre 0.0 et 1.0.
        """

        if not word or not candidate:

            return 0.0

        return SequenceMatcher(
            None,
            str(word).upper(),
            str(candidate).upper()
        ).ratio()

    # ==========================================================
    # SUGGESTION UNIQUE
    # ==========================================================

    @classmethod
    def suggest(
            cls,
            word,
            limit=3
    ):
        """
        Retourne plusieurs suggestions structurées.

        Exemple :

        suggest("STATISTIQ")

        retourne :

        [
            {
                "word": "STATISTIQUES",
                "score": 0.8571
            }
        ]
        """

        if not word:
            return []

        word = str(word).upper()

        mots = list(
            RESERVED_WORDS.keys()
        )

        candidates = get_close_matches(
            word,
            mots,
            n=limit,
            cutoff=CorrectionConfig.SUGGEST_THRESHOLD
        )

        suggestions = []

        for candidate in candidates:
            score = cls.similarity(
                word,
                candidate
            )

            suggestions.append(
                {
                    "word": candidate,
                    "score": score
                }
            )

        return suggestions

    # ==========================================================
    # SUGGESTIONS MULTIPLES
    # ==========================================================

    @classmethod
    def suggest_multiple(
            cls,
            word,
            limit=3
    ):
        """
        Retourne plusieurs suggestions sous forme
        d'une liste de mots.

        Exemple :

        suggest_multiple("STATISTIQ")

        retourne :

        [
            "STATISTIQUES",
            ...
        ]
        """

        if not word:
            return []

        word = str(word).upper()

        mots = list(
            RESERVED_WORDS.keys()
        )

        suggestions = get_close_matches(
            word,
            mots,
            n=limit,
            cutoff=CorrectionConfig.SUGGEST_THRESHOLD
        )

        return suggestions

    # ==========================================================
    # DÉCISION
    # ==========================================================

    @classmethod
    def decide(
            cls,
            word
    ):
        """
        Détermine la décision pour un mot :

        AUTO_CORRECT
        SUGGEST
        REFORMULATE
        """

        if not word:
            return {
                "mode": "REFORMULATE",
                "input": word,
                "word": word,
                "candidate": None,
                "suggestion": None,
                "score": 0.0,
                "trace": [
                    "Mot vide."
                ]
            }

        word = str(word).upper()

        # ==========================================================
        # MOT DÉJÀ VALIDE
        # ==========================================================

        if word in RESERVED_WORDS:
            return {
                "mode": "VALID",
                "input": word,
                "word": word,
                "candidate": word,
                "suggestion": word,
                "score": 1.0,
                "trace": [
                    f"{word} est un mot réservé valide."
                ]
            }

        # ==========================================================
        # RECHERCHE DU MEILLEUR CANDIDAT
        # ==========================================================

        mots = list(
            RESERVED_WORDS.keys()
        )

        candidates = get_close_matches(
            word,
            mots,
            n=1,
            cutoff=CorrectionConfig.SUGGEST_THRESHOLD
        )

        # ==========================================================
        # AUCUN CANDIDAT
        # ==========================================================

        if not candidates:
            return {
                "mode": "REFORMULATE",
                "input": word,
                "word": word,
                "candidate": None,
                "suggestion": None,
                "score": 0.0,
                "trace": [
                    (
                        f"Aucun candidat trouvé "
                        f"pour {word}."
                    ),
                    "Décision : REFORMULATE"
                ]
            }

        # ==========================================================
        # MEILLEUR CANDIDAT
        # ==========================================================

        candidate = candidates[0]

        score = cls.similarity(
            word,
            candidate
        )

        trace = [
            (
                f"Candidat : {candidate}"
            ),
            (
                f"Score de similarité : "
                f"{score:.4f}"
            )
        ]

        # ==========================================================
        # AUTO_CORRECT
        # ==========================================================

        if (
                score
                >=
                CorrectionConfig.AUTO_CORRECT_THRESHOLD
        ):
            trace.append(
                "Décision : AUTO_CORRECT"
            )

            return {
                "mode": "AUTO_CORRECT",
                "input": word,
                "word": word,
                "candidate": candidate,
                "suggestion": candidate,
                "score": score,
                "trace": trace
            }

        # ==========================================================
        # SUGGEST
        # ==========================================================

        if (
                score
                >=
                CorrectionConfig.SUGGEST_THRESHOLD
        ):
            trace.append(
                "Décision : SUGGEST"
            )

            return {
                "mode": "SUGGEST",
                "input": word,
                "word": word,
                "candidate": candidate,
                "suggestion": candidate,
                "score": score,
                "trace": trace
            }

        # ==========================================================
        # REFORMULATE
        # ==========================================================

        trace.append(
            "Décision : REFORMULATE"
        )

        return {
            "mode": "REFORMULATE",
            "input": word,
            "word": word,
            "candidate": candidate,
            "suggestion": None,
            "score": score,
            "trace": trace
        }

    # ==========================================================
    # ANALYSE
    # ==========================================================

    @classmethod
    def analyze(
        cls,
        word
    ):
        """
        Analyse complète d'un mot.
        """

        decision = cls.decide(
            word
        )

        suggestions = cls.suggest_multiple(
            word
        )

        decision["suggestions"] = suggestions

        return decision

    # ==========================================================
    # TRACE
    # ==========================================================

    @staticmethod
    def trace(result):
        """
        Transforme une décision de correction
        en trace exploitable.
        """

        if not isinstance(result, dict):
            raise TypeError(
                "Le résultat doit être un dictionnaire."
            )

        return {
            "component": "CommandSuggester",

            "input": result.get("input", result.get("word")
            ),

            "mode": result.get(
                "mode"
            ),

            "score": result.get(
                "score"
            ),

            "candidate": result.get(
                "candidate"
            ),

            "suggestions": result.get(
                "suggestions",
                []
            )
        }


    @classmethod
    def display_trace(
        cls,
        result
    ):
        """
        Affiche la trace d'une décision.
        """

        print()
        print("=" * 70)
        print("TRACE COMMAND SUGGESTER")
        print("=" * 70)

        print(
            f"Mot : "
            f"{result.get('word')}"
        )

        print(
            f"Mode : "
            f"{result.get('mode')}"
        )

        print(
            f"Score : "
            f"{result.get('score', 0.0):.4f}"
        )

        print(
            f"Suggestion : "
            f"{result.get('suggestion')}"
        )

        print()

        for step in result.get(
            "trace",
            []
        ):

            print(
                f"  - {step}"
            )

