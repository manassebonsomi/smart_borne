# services/command_interaction.py

class CommandInteraction:

    # ==========================================================
    # DEMANDER CONFIRMATION
    # ==========================================================

    @staticmethod
    def ask_confirmation(suggestion):
        """
        Demande à l'utilisateur de confirmer une suggestion.

        Retourne :
            True  -> OUI
            False -> NON
        """

        print()
        print("=" * 70)
        print("SUGGESTION DE COMMANDE")
        print("=" * 70)

        print()
        print("Voulez-vous dire :")
        print()
        print(f"  {suggestion} ?")
        print()

        while True:

            response = input(
                "Répondez Oui ou Non : "
            ).strip().upper()

            if response in (
                "OUI",
                "O",
                "YES",
                "Y"
            ):
                return True

            if response in (
                "NON",
                "N",
                "NO"
            ):
                return False

            print(
                "Réponse invalide. "
                "Veuillez répondre Oui ou Non."
            )

    # ==========================================================
    # TRAITEMENT D'UNE DÉCISION
    # ==========================================================

    @classmethod
    def handle(cls, result):
        """
        Traite le résultat de CommandCorrector.

        VALID
            → retourne directement la commande corrigée.

        AUTO_CORRECT
            → retourne directement la commande corrigée.

        SUGGEST
            → demande confirmation à l'utilisateur.

        REFORMULATE
            → demande une nouvelle commande.
        """

        if not isinstance(result, dict):

            raise TypeError(
                "Le résultat doit être un dictionnaire."
            )

        mode = result.get("mode")

        corrected = result.get(
            "corrected"
        )

        suggestion = result.get(
            "suggestion"
        )

        trace = list(
            result.get(
                "trace",
                []
            )
        )

        # ------------------------------------------------------
        # VALID
        # ------------------------------------------------------

        if mode == "VALID":

            trace.append(
                "INTERACTION : commande valide, "
                "aucune confirmation nécessaire."
            )

            return {
                "success": True,
                "accepted": True,
                "mode": "VALID",
                "command": corrected,
                "trace": trace
            }

        # ------------------------------------------------------
        # AUTO_CORRECT
        # ------------------------------------------------------

        if mode == "AUTO_CORRECT":

            trace.append(
                "INTERACTION : AUTO_CORRECT, "
                "confirmation non requise."
            )

            return {
                "success": True,
                "accepted": True,
                "mode": "AUTO_CORRECT",
                "command": corrected,
                "trace": trace
            }

        # ------------------------------------------------------
        # SUGGEST
        # ------------------------------------------------------

        if mode == "SUGGEST":

            if not suggestion:

                trace.append(
                    "INTERACTION : aucune suggestion disponible."
                )

                return {
                    "success": False,
                    "accepted": False,
                    "mode": "REFORMULATE",
                    "command": None,
                    "trace": trace
                }

            trace.append(
                f"INTERACTION : confirmation demandée "
                f"pour '{suggestion}'."
            )

            accepted = cls.ask_confirmation(
                suggestion
            )

            # --------------------------------------------------
            # OUI
            # --------------------------------------------------

            if accepted:

                trace.append(
                    "INTERACTION : suggestion acceptée."
                )

                return {
                    "success": True,
                    "accepted": True,
                    "mode": "SUGGEST_ACCEPTED",
                    "command": suggestion,
                    "trace": trace
                }

            # --------------------------------------------------
            # NON
            # --------------------------------------------------

            trace.append(
                "INTERACTION : suggestion refusée."
            )

            trace.append(
                "INTERACTION : reformulation demandée."
            )

            return {
                "success": False,
                "accepted": False,
                "mode": "REFORMULATE",
                "command": None,
                "trace": trace
            }

        # ------------------------------------------------------
        # REFORMULATE
        # ------------------------------------------------------

        if mode == "REFORMULATE":

            trace.append(
                "INTERACTION : reformulation nécessaire."
            )

            return {
                "success": False,
                "accepted": False,
                "mode": "REFORMULATE",
                "command": None,
                "trace": trace
            }

        # ------------------------------------------------------
        # MODE INCONNU
        # ------------------------------------------------------

        trace.append(
            f"INTERACTION : mode inconnu '{mode}'."
        )

        return {
            "success": False,
            "accepted": False,
            "mode": "REFORMULATE",
            "command": None,
            "trace": trace
        }

    # ==========================================================
    # TRACE
    # ==========================================================

    @staticmethod
    def trace(result):
        """
        Transforme le résultat d'interaction
        en trace exploitable.
        """

        if not isinstance(result, dict):

            raise TypeError(
                "Le résultat doit être un dictionnaire."
            )

        return {
            "component": "CommandInteraction",
            "mode": result.get("mode"),
            "accepted": result.get("accepted"),
            "success": result.get("success"),
            "command": result.get("command"),
            "trace": result.get(
                "trace",
                []
            )
        }

    # ==========================================================
    # AFFICHAGE TRACE
    # ==========================================================

    @staticmethod
    def display_trace(result):

        print()
        print("=" * 70)
        print("TRACE COMMAND INTERACTION")
        print("=" * 70)

        print(
            f"Mode : {result.get('mode')}"
        )

        print(
            f"Acceptée : {result.get('accepted')}"
        )

        print(
            f"Succès : {result.get('success')}"
        )

        print(
            f"Commande : {result.get('command')}"
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