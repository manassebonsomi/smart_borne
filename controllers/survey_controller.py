from services.state_machine import \
    StateMachine

from models.reponse import Reponse

from config.database import db


class SurveyController:

    @staticmethod
    def start_session(
            session_id
    ):

        return StateMachine.transition(

            "START",

            session_id
        )

    @staticmethod
    def profile_created(
            session_id
    ):

        return StateMachine.transition(

            "PROFILE_CREATED",

            session_id
        )

    @staticmethod
    def survey_completed(
            session_id
    ):

        return StateMachine.transition(

            "SURVEY_COMPLETED",

            session_id
        )

    @staticmethod
    def result_ready(
            session_id
    ):

        return StateMachine.transition(

            "RESULT_READY",

            session_id
        )

    @staticmethod
    def finish(
            session_id
    ):

        return StateMachine.transition(

            "FINISH",

            session_id
        )

    @staticmethod
    def save_answer(

            id_session,

            id_question,

            valeur_reponse
    ):

        reponse = Reponse(

            id_session=id_session,

            id_question=id_question,

            valeur_reponse=valeur_reponse
        )

        db.session.add(
            reponse
        )

        db.session.commit()

        return reponse