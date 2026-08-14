from controllers.dashboard_controller import DashboardController
from controllers.question_controller import QuestionController
from controllers.utilisateur_controller import UtilisateurController
from controllers.campagne_controller import CampagneController
from controllers.erreur_controller import ErreurController
from controllers.report_controller import ReportController
from services.session_manager import SessionManager


class CommandHandler:

    # ==========================================================
    # HANDLE
    # ==========================================================

    def handle(self, command, data=None):

        action = self._get_action(
            command
        )

        # ------------------------------------------------------
        # AFFICHER STATISTIQUES
        # ------------------------------------------------------

        if action == "AFFICHER_STATISTIQUES":

            return {
                "action": action,
                "success": True,
                "data":
                    DashboardController.statistics()
            }

        # ------------------------------------------------------
        # AFFICHER ERREURS
        # ------------------------------------------------------

        if action == "AFFICHER_ERREURS":

            erreurs = ErreurController.get_all()

            return {
                "action": action,
                "success": True,
                "nombre": len(erreurs),
                "data": [
                    {
                        "id": e.id_erreur,
                        "type": e.type_erreur,
                        "message": e.message,
                        "corrigee": e.corrigee
                    }
                    for e in erreurs
                ]
            }

        # ------------------------------------------------------
        # ENQUÊTE CYBERSÉCURITÉ
        # ------------------------------------------------------

        if action == "ENQUETE_CYBERSECURITE":

            return {
                "action": action,
                "success": True,
                "etat": "ENQUETE_LANCEE"
            }

        # ------------------------------------------------------
        # CAMPAGNE ÉCOLE
        # ------------------------------------------------------

        if action == "CAMPAGNE_ECOLE":

            campagne = CampagneController.create(
                nom_campagne="Campagne Ecole",
                description="Campagne créée via commande"
            )

            return {
                "action": action,
                "success": campagne is not None,
                "campagne_id":
                    campagne.id_campagne
                    if campagne
                    else None,
                "etat": "CAMPAGNE_LANCEE"
            }

        # ------------------------------------------------------
        # RECHERCHE ENFANTS
        # ------------------------------------------------------

        if action == "RECHERCHE_ENFANTS":

            utilisateurs = (
                UtilisateurController.search_children()
            )

            return {
                "action": action,
                "success": True,
                "nombre": len(utilisateurs),
                "resultats": [
                    {
                        "id": u.id_utilisateur,
                        "nom": u.nom,
                        "prenom": u.prenom,
                        "age": u.age
                    }
                    for u in utilisateurs
                ]
            }

        # ------------------------------------------------------
        # RECHERCHE ADOLESCENTS PYTHON
        # ------------------------------------------------------

        if action == "RECHERCHE_ADOS_PYTHON":

            utilisateurs = (
                UtilisateurController.search_adolescents()
            )

            return {
                "action": action,
                "success": True,
                "nombre": len(utilisateurs),
                "resultats": [
                    {
                        "id": u.id_utilisateur,
                        "nom": u.nom,
                        "prenom": u.prenom,
                        "age": u.age
                    }
                    for u in utilisateurs
                ]
            }

        # ------------------------------------------------------
        # AJOUTER QUESTION
        # ------------------------------------------------------

        if action == "AJOUTER_QUESTION":

            if not data:

                return {
                    "action": action,
                    "success": False,
                    "etat": "ATTENTE_DONNEES",
                    "show_form": True,
                    "form_type": "add_question",
                    "message":
                        "Les données de la question sont manquantes."
                }

            question = QuestionController.create(
                data["texte_question"],
                data["ordre_question"],
                data["id_categorie"]
            )

            return {
                "action": action,
                "success": question is not None,
                "question_id":
                    question.id_question
                    if question
                    else None
            }

        # ------------------------------------------------------
        # MODIFIER QUESTION
        # ------------------------------------------------------

        if action == "MODIFIER_QUESTION":

            numero = self._get_question_id(
                command
            )

            if not data:

                return {
                    "action": action,
                    "success": False,
                    "etat": "ATTENTE_DONNEES",
                    "show_form": True,
                    "form_type": "edit_question",
                    "question_id": numero,
                    "message":
                        "Les données de la question sont manquantes."
                }

            question = QuestionController.update(
                int(numero),
                texte_question=data.get(
                    "texte_question"
                ),
                ordre_question=data.get(
                    "ordre_question"
                ),
                active=data.get(
                    "active"
                )
            )

            return {
                "action": action,
                "success": question is not None,
                "question_id": numero
            }

        # ------------------------------------------------------
        # SUPPRIMER QUESTION
        # ------------------------------------------------------

        if action == "SUPPRIMER_QUESTION":

            numero = self._get_question_id(
                command
            )

            success = False

            if numero is not None:

                success = QuestionController.delete(
                    int(numero)
                )

            return {
                "action": action,
                "success": success,
                "question_id": numero
            }

        # ------------------------------------------------------
        # EXPORTER RAPPORT
        # ------------------------------------------------------

        if action == "EXPORTER_RAPPORT":

            rapport = ReportController.export_pdf()

            return {
                "action": action,
                "success":
                    rapport.get(
                        "success",
                        False
                    ),
                "rapport": rapport
            }

        # ------------------------------------------------------
        # RECOMMENCER SESSION
        # ------------------------------------------------------

        if action == "RECOMMENCER_SESSION":

            derniere_session = (
                SessionManager.get_last_session(1)
            )

            if derniere_session:

                SessionManager.restart_session(
                    derniere_session.id_session
                )

            return {
                "action": action,
                "success": True
            }

        # ------------------------------------------------------
        # QUITTER
        # ------------------------------------------------------

        if action == "QUITTER":

            derniere_session = (
                SessionManager.get_last_session(1)
            )

            if derniere_session:

                SessionManager.close_session(
                    derniere_session.id_session
                )

            return {
                "action": action,
                "success": True
            }

        # ------------------------------------------------------
        # ACTION INCONNUE
        # ------------------------------------------------------

        return {
            "action": action,
            "success": False,
            "message":
                f"Action non prise en charge : {action}"
        }

    # ==========================================================
    # UTILITAIRES
    # ==========================================================

    @staticmethod
    def _get_action(command):

        if isinstance(command, dict):

            return command.get(
                "action"
            )

        return getattr(
            command,
            "action",
            None
        )

    @staticmethod
    def _get_question_id(command):

        if isinstance(command, dict):

            # --------------------------------------------------
            # ARGUMENTS STRUCTURES
            # --------------------------------------------------

            arguments = command.get(
                "arguments",
                {}
            )

            if isinstance(arguments, dict):

                numero = arguments.get(
                    "numero"
                )

                if numero is not None:
                    return numero

            # --------------------------------------------------
            # COMPATIBILITE ANCIEN FORMAT
            # --------------------------------------------------

            return (
                    command.get("question_id")
                    or command.get("numero")
            )

        # ------------------------------------------------------
        # OBJET COMMAND
        # ------------------------------------------------------

        arguments = getattr(
            command,
            "arguments",
            {}
        )

        if isinstance(arguments, dict):

            numero = arguments.get(
                "numero"
            )

            if numero is not None:
                return numero

        return (
                getattr(
                    command,
                    "question_id",
                    None
                )
                or
                getattr(
                    command,
                    "numero",
                    None
                )
        )