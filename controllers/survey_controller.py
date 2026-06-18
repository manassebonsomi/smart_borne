from config.database import db

from models.question import Question
from models.reponse import Reponse
from models.session import SessionUtilisateur

from services.survey_engine import \
    SurveyEngine

from services.session_manager import \
    SessionManager

from controllers.recommandation_controller \
    import RecommendationController

from services.audit_service \
    import AuditService


class SurveyController:

    @staticmethod
    def start(
            id_session
    ):

        session = \
            SessionUtilisateur.query.get(
                id_session
            )

        if not session:

            raise Exception(
                "Session introuvable"
            )

        premiere = \
            SurveyEngine.get_question_by_order(
                1
            )

        if not premiere:

            raise Exception(
                "Aucune question disponible"
            )

        session.question_actuelle = 1

        db.session.commit()

        return {

            "session":
                id_session,

            "question":

                {

                    "id":
                        premiere.id_question,

                    "texte":
                        premiere.texte_question,

                    "ordre":
                        premiere.ordre_question
                }
        }

    @staticmethod
    def answer(
            id_session,
            id_question,
            valeur
    ):

        reponse = \
            Reponse(

                valeur=
                valeur,

                id_session=
                id_session,

                id_question=
                id_question
            )

        db.session.add(
            reponse
        )

        db.session.commit()

        AuditService.log(

            action=
            "REPONSE",

            objet=
            f"Question {id_question}",

            resultat=
            "SUCCES",

            details=
            valeur
        )

        question = \
            Question.query.get(
                id_question
            )

        suivante = \
            SurveyEngine.get_next_question(

                question.ordre_question
            )

        if suivante:

            SessionManager.save_progress(

                id_session,

                suivante.ordre_question,

                "QUESTIONNAIRE"
            )

            return {

                "finished":
                    False,

                "question":

                    {

                        "id":
                            suivante.id_question,

                        "texte":
                            suivante.texte_question,

                        "ordre":
                            suivante.ordre_question
                    }
            }

        return {

            "finished":
                True
        }

    @staticmethod
    def finish(
            id_session
    ):

        resultat = \
            RecommendationController.generate(
                id_session
            )

        SessionManager.close_session(
            id_session
        )

        return {

            "success":
                True,

            "resultat":
                resultat
        }

    @staticmethod
    def get_question(
            ordre
    ):

        question = \
            SurveyEngine.get_question_by_order(
                ordre
            )

        if not question:

            return None

        return {

            "id":
                question.id_question,

            "texte":
                question.texte_question,

            "ordre":
                question.ordre_question
        }