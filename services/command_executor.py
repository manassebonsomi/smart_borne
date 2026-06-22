from controllers.dashboard_controller import DashboardController
from controllers.question_controller import QuestionController
from controllers.utilisateur_controller import UtilisateurController
from controllers.campagne_controller import CampagneController
from controllers.erreur_controller import ErreurController
from controllers.report_controller import ReportController
from services.session_manager import SessionManager


class CommandExecutor:

    @staticmethod
    def execute(tokens, data=None):
        token_types = [
            token.type
            for token in tokens
            if token.type != "EOF"
        ]

        # AFFICHER STATISTIQUES

        if token_types == [
            "AFFICHER",
            "STATISTIQUES"
        ]:

            return {
                "action": "AFFICHER_STATISTIQUES",
                "success": True,
                "data": DashboardController.statistics()
            }

        # AFFICHER ERREURS
        elif token_types == [
            "AFFICHER",
            "ERREURS"
        ]:

            erreurs = ErreurController.get_all()

            return {
                "action": "AFFICHER_ERREURS",
                "success": True,
                "nombre": len(erreurs),
                "data":
                    [
                        {
                            "id": e.id_erreur,
                            "type": e.type_erreur,
                            "message": e.message,
                            "corrigee": e.corrigee
                        }
                        for e in erreurs
                    ]
            }

        # LANCER ENQUETE CYBERSECURITE
        elif token_types == [
            "LANCER",
            "ENQUETE",
            "CYBERSECURITE"
        ]:
            return {
                "action": "ENQUETE_CYBERSECURITE",
                "success": True,
                "etat": "ENQUETE_LANCEE"
            }

        # LANCER CAMPAGNE ECOLE
        elif token_types == [
            "LANCER",
            "CAMPAGNE",
            "ECOLE"
        ]:

            campagne = CampagneController.create(
                nom_campagne="Campagne Ecole",
                description="Campagne créée via commande"
            )
            return {
                "action":"CAMPAGNE_ECOLE",
                "success": True,
                "campagne_id":campagne.id_campagne,
                "etat":"CAMPAGNE_LANCEE"
            }


        # CHERCHER ENFANTS KINSHASA
        elif token_types == [
            "CHERCHER",
            "ENFANTS",
            "KINSHASA"
        ]:
            utilisateurs = UtilisateurController.search_children()

            return {
                "action":"RECHERCHE_ENFANTS",
                "success":True,
                "nombre":len(utilisateurs),
                "resultats":
                    [
                        {
                            "id":u.id_utilisateur,
                            "nom":u.nom,
                            "prenom":u.prenom,
                            "age":u.age
                        }
                        for u in utilisateurs
                    ]
            }

        # CHERCHER ADOLESCENTS PYTHON
        elif token_types == [
            "CHERCHER",
            "ADOLESCENTS",
            "INTERESSES",
            "PAR",
            "PYTHON"
        ]:
            utilisateurs = UtilisateurController.search_adolescents()

            return {
                "action":"RECHERCHE_ADOS_PYTHON",
                "success":True,
                "nombre":len(utilisateurs),
                "resultats":
                    [
                        {
                            "id":u.id_utilisateur,
                            "nom":u.nom,
                            "prenom":u.prenom,
                            "age":u.age
                        }
                        for u in utilisateurs
                    ]
            }


        # AJOUTER QUESTION
        elif token_types == [
            "AJOUTER",
            "QUESTION"
        ]:
            if not data:
                return {
                    "action": "AJOUTER_QUESTION",
                    "success": False,
                    "etat": "ATTENTE_DONNEES",
                    "show_form": True,
                    "form_type": "add_question",
                    "message":"Les données de la question sont manquantes et en attente"
                }

            question = QuestionController.create(
                data["texte_question"],
                data["ordre_question"],
                data["id_categorie"]
            )

            return {
                "action": "AJOUTER_QUESTION",
                "success": question is not None,
                "question_id":question.id_question if question else None
            }


        # MODIFIER QUESTION NUMERO X
        elif (
                len(token_types) >= 2
                and
                token_types[0:2] == [
                    "MODIFIER",
                    "QUESTION"
                ]
        ):
            numero = next(
                (
                    token.value
                    for token in tokens
                    if token.type == "NUMERO"
                ),
                None
            )

            if data:
                question = QuestionController.update(
                        int(numero),
                        texte_question=data.get("texte_question"),
                        ordre_question=data.get("ordre_question"),
                        active=data.get("active"))

                return {
                    "action":"MODIFIER_QUESTION",
                    "success": question is not None,
                    "question_id": numero
                }

            else:
                return {
                    "action": "MODIFIER_QUESTION",
                    "success": False,
                    "etat": "ATTENTE_DONNEES",
                    "show_form": True,
                    "form_type": "edit_question",
                    "question_id": numero,
                    "message": "Les données de la question sont manquantes et en attente"
                }


        # SUPPRIMER QUESTION NUMERO X
        elif (
            len(token_types) >= 2
            and
            token_types[0:2] == [
                "SUPPRIMER",
                "QUESTION"
            ]
        ):
            numero = next(
                (
                    token.value
                    for token in tokens
                    if token.type == "NUMERO"
                ),
                None
            )
            success = False

            if numero:
                success = QuestionController.delete(int(numero))

            return {
                "action":"SUPPRIMER_QUESTION",
                "success":success,
                "question_id":numero
            }

        # EXPORTER RAPPORT
        elif token_types == [
            "EXPORTER",
            "RAPPORT"
        ]:

            rapport = ReportController.export_pdf()

            return {
                "action":"EXPORTER_RAPPORT",
                "success":rapport.get("success", False),
                "rapport":rapport
            }

        # RECOMMENCER SESSION
        elif token_types == [
            "RECOMMENCER",
            "SESSION"
        ]:

            derniere_session = SessionManager.get_last_session(1)

            if derniere_session:
                SessionManager.restart_session(derniere_session.id_session)

            return {
                "action":"RECOMMENCER_SESSION",
                "success":True
            }


        # QUITTER
        elif token_types == [
            "QUITTER"
        ]:

            derniere_session = SessionManager.get_last_session(1)

            if derniere_session:
                SessionManager.close_session(derniere_session.id_session)

            return {
                "action":"QUITTER",
                "success":True}


        # COMMANDE INCONNUE
        return {
            "action": "INCONNUE",
            "success":False,
            "message":"Commande non reconnue"
        }