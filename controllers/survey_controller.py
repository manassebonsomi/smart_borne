from services.state_machine import StateMachine
from models.reponse import Reponse
from config.database import db

from services.session_manager import SessionManager


class SurveyController:

    machine = StateMachine()

    @staticmethod
    def start_session(
            session_id
    ):

        return \
            SurveyController.machine \
                .transition(

                "START",

                session_id
            )

    @staticmethod
    def profile_created(
            session_id
    ):

        return \
            SurveyController.machine \
                .transition(

                "PROFILE_CREATED",

                session_id
            )

    @staticmethod
    def survey_completed(
            session_id
    ):

        return \
            SurveyController.machine \
                .transition(

                "SURVEY_COMPLETED",

                session_id
            )

    @staticmethod
    def result_ready(
            session_id
    ):

        return \
            SurveyController.machine \
                .transition(

                "RESULT_READY",

                session_id
            )

    @staticmethod
    def finish(
            session_id
    ):

        return \
            SurveyController.machine \
                .transition(

                "FINISH",

                session_id
            )

    @staticmethod
    def save_answer(

            id_session,

            id_question,

            valeur
    ):
        reponse = Reponse(

            id_session=id_session,

            id_question=id_question,

            valeur=valeur
        )

        db.session.add(
            reponse
        )

        db.session.commit()

        return reponse