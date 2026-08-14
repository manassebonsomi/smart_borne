from services.command_suggester import CommandSuggester
from services.correction_config import CorrectionConfig
from services.reserved_words import RESERVED_WORDS


class CommandCorrector:

    # ==========================================================
    # CORRECTION D'UNE COMMANDE
    # ==========================================================

    @classmethod
    def correct(cls, command):
        """
        Analyse une commande complète et détermine :

        VALID
        AUTO_CORRECT
        SUGGEST
        REFORMULATE

        Le correcteur prépare la commande pour le lexer
        et le parser LL(1).

        Il ne remplace PAS la validation syntaxique
        du parser.
        """

        trace = []

        # ------------------------------------------------------
        # VALIDATION DE L'ENTRÉE
        # ------------------------------------------------------

        if command is None:

            return {
                "success": False,
                "mode": "REFORMULATE",
                "original": command,
                "corrected": None,
                "suggestion": None,
                "score": 0.0,
                "suggestions": [],
                "trace": [
                    "Commande vide ou inexistante.",
                    "DÉCISION FINALE : REFORMULATE"
                ]
            }

        original_command = command

        command = str(command).strip()

        if not command:

            return {
                "success": False,
                "mode": "REFORMULATE",
                "original": original_command,
                "corrected": None,
                "suggestion": None,
                "score": 0.0,
                "suggestions": [],
                "trace": [
                    "Commande vide.",
                    "DÉCISION FINALE : REFORMULATE"
                ]
            }

        # ------------------------------------------------------
        # VALIDATION CONFIGURATION
        # ------------------------------------------------------

        if not CorrectionConfig.validate():

            return {
                "success": False,
                "mode": "REFORMULATE",
                "original": original_command,
                "corrected": None,
                "suggestion": None,
                "score": 0.0,
                "suggestions": [],
                "trace": [
                    "Configuration des seuils invalide.",
                    "DÉCISION FINALE : REFORMULATE"
                ]
            }

        # ------------------------------------------------------
        # NORMALISATION
        # ------------------------------------------------------

        normalized_command = command.upper()

        trace.append(
            f"Commande reçue : {original_command}"
        )

        trace.append(
            f"Commande normalisée : {normalized_command}"
        )

        # ------------------------------------------------------
        # DÉCOUPAGE
        # ------------------------------------------------------

        words = normalized_command.split()

        trace.append(
            f"Nombre de tokens textuels : {len(words)}"
        )

        # ------------------------------------------------------
        # VALIDATION DIRECTE
        # ------------------------------------------------------
        #
        # Un mot est considéré comme directement valide si :
        #
        # 1. il appartient aux mots réservés
        # OU
        # 2. il s'agit d'un nombre
        #
        # Les nombres sont valides pour le lexer :
        #
        # MODIFIER QUESTION 3
        # SUPPRIMER QUESTION 25
        #
        # La validité syntaxique finale reste assurée
        # par le parser LL(1).
        # ------------------------------------------------------

        all_valid = all(
            (
                word in RESERVED_WORDS
                or word.isdigit()
            )
            for word in words
        )

        if all_valid:

            trace.append(
                "Tous les éléments sont lexicalement connus."
            )

            trace.append(
                "Mots réservés et numéros reconnus."
            )

            trace.append(
                "DÉCISION FINALE : VALID"
            )

            return {
                "success": True,
                "mode": "VALID",
                "original": original_command,
                "corrected": normalized_command,
                "suggestion": None,
                "score": 1.0,
                "suggestions": [],
                "trace": trace
            }

        # ------------------------------------------------------
        # ANALYSE FUZZY
        # ------------------------------------------------------

        corrected_words = []
        word_suggestions = []

        has_auto_correct = False
        has_suggest = False
        has_reformulate = False

        for word in words:

            # --------------------------------------------------
            # NUMERO
            # --------------------------------------------------

            if word.isdigit():

                corrected_words.append(word)

                trace.append(
                    f"{word} : NUMERO valide."
                )

                continue

            # --------------------------------------------------
            # MOT RESERVE
            # --------------------------------------------------

            if word in RESERVED_WORDS:

                corrected_words.append(word)

                trace.append(
                    f"{word} : mot réservé valide."
                )

                continue

            # --------------------------------------------------
            # RECHERCHE DE SUGGESTIONS
            # --------------------------------------------------

            suggestions = CommandSuggester.suggest(
                word
            )

            # --------------------------------------------------
            # AUCUN CANDIDAT
            # --------------------------------------------------

            if not suggestions:

                corrected_words.append(word)

                has_reformulate = True

                trace.append(
                    f"{word} : aucun candidat proche."
                )

                trace.append(
                    f"DÉCISION : REFORMULATE pour {word}"
                )

                continue

            # --------------------------------------------------
            # MEILLEUR CANDIDAT
            # --------------------------------------------------

            best = suggestions[0]

            candidate = best["word"]
            score = best["score"]

            word_suggestions.append(
                {
                    "original": word,
                    "suggestion": candidate,
                    "score": score,
                    "suggestions": suggestions
                }
            )

            trace.append(
                f"{word} → {candidate} "
                f"(score={score:.4f})"
            )

            # --------------------------------------------------
            # AUTO_CORRECT
            # --------------------------------------------------

            if (
                score
                >=
                CorrectionConfig.AUTO_CORRECT_THRESHOLD
            ):

                corrected_words.append(candidate)

                has_auto_correct = True

                trace.append(
                    f"DÉCISION : AUTO_CORRECT "
                    f"pour {word}"
                )

                continue

            # --------------------------------------------------
            # SUGGEST
            # --------------------------------------------------

            if (
                score
                >=
                CorrectionConfig.SUGGEST_THRESHOLD
            ):

                corrected_words.append(word)

                has_suggest = True

                trace.append(
                    f"DÉCISION : SUGGEST "
                    f"pour {word}"
                )

                continue

            # --------------------------------------------------
            # REFORMULATE
            # --------------------------------------------------

            corrected_words.append(word)

            has_reformulate = True

            trace.append(
                f"DÉCISION : REFORMULATE "
                f"pour {word}"
            )

        # ------------------------------------------------------
        # DÉCISION GLOBALE
        # ------------------------------------------------------

        if has_reformulate:

            mode = "REFORMULATE"

        elif has_suggest:

            mode = "SUGGEST"

        elif has_auto_correct:

            mode = "AUTO_CORRECT"

        else:

            mode = "VALID"

        # ------------------------------------------------------
        # COMMANDE CORRIGÉE
        # ------------------------------------------------------

        corrected_command = " ".join(
            corrected_words
        )

        # ------------------------------------------------------
        # CONSTRUCTION DE LA SUGGESTION COMPLÈTE
        # ------------------------------------------------------
        #
        # IMPORTANT :
        # On utilise suggested_words et NON corrected_words.
        #
        # Les numéros sont conservés tels quels.
        # ------------------------------------------------------

        suggestion_command = None

        if word_suggestions:

            suggested_words = []

            for word in words:

                # --------------------------------------------------
                # NUMERO
                # --------------------------------------------------

                if word.isdigit():

                    suggested_words.append(word)

                    continue

                # --------------------------------------------------
                # MOT RESERVE
                # --------------------------------------------------

                if word in RESERVED_WORDS:

                    suggested_words.append(word)

                    continue

                # --------------------------------------------------
                # RECHERCHE DE SUGGESTION
                # --------------------------------------------------

                suggestions = CommandSuggester.suggest(
                    word
                )

                if suggestions:

                    suggested_words.append(
                        suggestions[0]["word"]
                    )

                else:

                    suggested_words.append(word)

            suggestion_command = " ".join(
                suggested_words
            )

        # ------------------------------------------------------
        # MEILLEUR SCORE
        # ------------------------------------------------------

        if word_suggestions:

            best_score = max(
                item["score"]
                for item in word_suggestions
            )

        else:

            best_score = 0.0

        # ------------------------------------------------------
        # TRACE FINALE
        # ------------------------------------------------------

        trace.append(
            f"DÉCISION FINALE : {mode}"
        )

        # ------------------------------------------------------
        # RÉSULTAT
        # ------------------------------------------------------

        # ------------------------------------------------------
        # INTERACTION UTILISATEUR
        # ------------------------------------------------------

        return {
            "success": mode != "REFORMULATE",
            "mode": mode,
            "original": original_command,
            "corrected": corrected_command,
            "suggestion": suggestion_command,
            "score": best_score,
            "suggestions": word_suggestions,
            "trace": trace
        }

    # ==========================================================
    # AFFICHAGE DE LA TRACE
    # ==========================================================

    @staticmethod
    def display_trace(result):

        print()
        print("=" * 70)
        print("TRACE DE CORRECTION")
        print("=" * 70)

        print(
            f"Commande originale : "
            f"{result.get('original')}"
        )

        print(
            f"Mode : "
            f"{result.get('mode')}"
        )

        print(
            f"Score : "
            f"{result.get('score', 0.0):.4f}"
        )

        if result.get("corrected"):

            print(
                f"Commande corrigée : "
                f"{result.get('corrected')}"
            )

        if result.get("suggestion"):

            print(
                f"Suggestion : "
                f"{result.get('suggestion')}"
            )

        print()
        print("Décisions :")

        for step in result.get(
            "trace",
            []
        ):

            print(
                f"  - {step}"
            )

        print()