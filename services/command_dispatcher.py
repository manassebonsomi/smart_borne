from services.command_handler import CommandHandler


class CommandDispatcher:

    # ==========================================================
    # REGISTRE DES HANDLERS
    # ==========================================================

    HANDLERS = {
        "AFFICHER_STATISTIQUES": CommandHandler,
        "AFFICHER_ERREURS": CommandHandler,

        "ENQUETE_CYBERSECURITE": CommandHandler,
        "CAMPAGNE_ECOLE": CommandHandler,

        "RECHERCHE_ENFANTS": CommandHandler,
        "RECHERCHE_ADOS_PYTHON": CommandHandler,

        "AJOUTER_QUESTION": CommandHandler,
        "MODIFIER_QUESTION": CommandHandler,
        "SUPPRIMER_QUESTION": CommandHandler,

        "EXPORTER_RAPPORT": CommandHandler,

        "RECOMMENCER_SESSION": CommandHandler,
        "QUITTER": CommandHandler,
    }

    # ==========================================================
    # RESOLUTION DE L'ACTION METIER
    # ==========================================================

    @classmethod
    def resolve_action(cls, command):
        """
        Transforme une Command structurée en action métier.

        Exemple :

            AFFICHER + STATISTIQUES
            →
            AFFICHER_STATISTIQUES

        """

        if command is None:
            return None

        if isinstance(command, dict):

            action = command.get("action")
            subject = command.get("subject")

            arguments = command.get(
                "arguments",
                {}
            )

        else:

            action = getattr(
                command,
                "action",
                None
            )

            subject = getattr(
                command,
                "subject",
                None
            )

            arguments = getattr(
                command,
                "arguments",
                {}
            )

        if not action:
            return None

        # ------------------------------------------------------
        # AFFICHER
        # ------------------------------------------------------

        if action == "AFFICHER":

            if subject == "STATISTIQUES":

                return "AFFICHER_STATISTIQUES"

            if subject == "ERREURS":

                return "AFFICHER_ERREURS"

        # ------------------------------------------------------
        # LANCER
        # ------------------------------------------------------

        if action == "LANCER":

            if (
                subject == "ENQUETE"
                and
                arguments.get("nom")
                == "CYBERSECURITE"
            ):

                return "ENQUETE_CYBERSECURITE"

            if (
                subject == "CAMPAGNE"
                and
                arguments.get("nom")
                == "ECOLE"
            ):

                return "CAMPAGNE_ECOLE"

        # ------------------------------------------------------
        # CHERCHER
        # ------------------------------------------------------

        if action == "CHERCHER":

            tokens = arguments.get(
                "tokens",
                []
            )

            if (
                subject == "ENFANTS"
                and
                tokens == ["KINSHASA"]
            ):

                return "RECHERCHE_ENFANTS"

            if (
                subject == "ADOLESCENTS"
                and
                tokens
                ==
                [
                    "INTERESSES",
                    "PAR",
                    "PYTHON"
                ]
            ):

                return "RECHERCHE_ADOS_PYTHON"

        # ------------------------------------------------------
        # AJOUTER
        # ------------------------------------------------------

        if action == "AJOUTER":

            if subject == "QUESTION":

                return "AJOUTER_QUESTION"

        # ------------------------------------------------------
        # MODIFIER
        # ------------------------------------------------------

        if action == "MODIFIER":

            if subject == "QUESTION":

                return "MODIFIER_QUESTION"

        # ------------------------------------------------------
        # SUPPRIMER
        # ------------------------------------------------------

        if action == "SUPPRIMER":

            if subject == "QUESTION":

                return "SUPPRIMER_QUESTION"

        # ------------------------------------------------------
        # EXPORTER
        # ------------------------------------------------------

        if action == "EXPORTER":

            if subject == "RAPPORT":

                return "EXPORTER_RAPPORT"

        # ------------------------------------------------------
        # RECOMMENCER
        # ------------------------------------------------------

        if action == "RECOMMENCER":

            if subject == "SESSION":

                return "RECOMMENCER_SESSION"

        # ------------------------------------------------------
        # QUITTER
        # ------------------------------------------------------

        if action == "QUITTER":

            return "QUITTER"

        return None

    # ==========================================================
    # DISPATCH
    # ==========================================================

    @classmethod
    def dispatch(cls, command, data=None):

        # ------------------------------------------------------
        # VALIDATION
        # ------------------------------------------------------

        if command is None:

            return {
                "success": False,
                "action": "INCONNUE",
                "message":
                    "Aucune commande fournie."
            }

        # ------------------------------------------------------
        # RESOLUTION
        # ------------------------------------------------------

        action = cls.resolve_action(
            command
        )

        # ------------------------------------------------------
        # ACTION INVALIDE
        # ------------------------------------------------------

        if action is None:

            return {
                "success": False,
                "action": "INCONNUE",
                "message":
                    "Commande non reconnue."
            }

        # ------------------------------------------------------
        # HANDLER
        # ------------------------------------------------------

        handler_class = cls.HANDLERS.get(
            action
        )

        if handler_class is None:

            return {
                "success": False,
                "action": action,
                "message":
                    (
                        "Aucun handler enregistré "
                        f"pour {action}."
                    )
            }

        # ------------------------------------------------------
        # PREPARATION DE LA COMMANDE POUR LE HANDLER
        # ------------------------------------------------------

        if isinstance(command, dict):

            handler_command = dict(
                command
            )

        else:

            handler_command = command.to_dict()

        # L'action résolue devient l'action
        # utilisée par la couche métier.

        handler_command["action"] = action

        # ------------------------------------------------------
        # EXECUTION
        # ------------------------------------------------------

        handler = handler_class()

        return handler.handle(
            handler_command,
            data=data
        )