from datetime import datetime

from config.database import db

from models.session import SessionUtilisateur


class SessionManager:

    @staticmethod
    def create_session(
            utilisateur_id,
            campagne_id=None
    ):

        session = SessionUtilisateur(

            id_utilisateur=utilisateur_id,

            id_campagne=campagne_id,

            etat="ACCUEIL",

            question_actuelle=0
        )

        db.session.add(session)
        db.session.commit()

        return session

    @staticmethod
    def save_progress(
            session_id,
            question,
            etat
    ):

        session = \
            SessionUtilisateur.query.get(
                session_id
            )

        if session:
            session.question_actuelle = question

            session.etat = etat

            session.sauvegardee = True

            db.session.commit()

        return session

    @staticmethod
    def pause_session(session_id):

        session = \
            SessionUtilisateur.query.get(
                session_id
            )

        if session:

            session.etat = \
                "SESSION_INTERRUPTION"

            db.session.commit()

        return session

    @staticmethod
    def is_interrupted(
            session_id
    ):

        session = \
            SessionUtilisateur.query.get(
                session_id
            )

        if not session:
            return False

        return (

                session.etat ==
                "SESSION_INTERRUPTION"
        )

    @staticmethod
    def set_state(
            session_id,
            etat
    ):

        session = \
            SessionUtilisateur.query.get(
                session_id
            )

        if not session:
            return None

        session.etat = etat

        db.session.commit()

        return session



    @staticmethod
    def resume_session(session_id):

        session = \
            SessionUtilisateur.query.get(
                session_id
            )

        if session:

            session.etat = \
                "REPRISE_SESSION"

            db.session.commit()

        return session

    @staticmethod
    def update_inactivity(
            session_id,
            secondes
    ):

        session = \
            SessionUtilisateur.query.get(
                session_id
            )

        if session:
            session.temps_inactivite = \
                secondes

            db.session.commit()

    @staticmethod
    def get_session(
            session_id
    ):

        return \
            SessionUtilisateur.query.get(
                session_id
            )

    @staticmethod
    def get_last_session(
            utilisateur_id
    ):

        return \
            SessionUtilisateur.query \
                .filter_by(
                id_utilisateur=
                utilisateur_id
            ) \
                .order_by(SessionUtilisateur.id_session.desc()
            ) \
                .first()

    @staticmethod
    def restart_session(
            session_id
    ):

        session = \
            SessionUtilisateur.query.get(
                session_id
            )

        if session:
            session.question_actuelle = 0

            session.etat = \
                "ACCUEIL"

            session.temps_inactivite = 0

            db.session.commit()

        return session

    @staticmethod
    def get_interrupted_session(
            utilisateur_id
    ):

        return \
            SessionUtilisateur.query \
                .filter_by(
                id_utilisateur=utilisateur_id,
                etat="SESSION_INTERRUPTION"
            ) \
                .order_by(
                SessionUtilisateur.id_session.desc()
            ) \
                .first()

    @staticmethod
    def can_resume(
            utilisateur_id
    ):

        session = \
            SessionManager \
                .get_interrupted_session(
                utilisateur_id
            )

        return session is not None

    @staticmethod
    def restore_session(
            utilisateur_id
    ):

        session = \
            SessionManager.get_interrupted_session(
                utilisateur_id
            )

        if not session:
            return None

        session.etat = \
            "QUESTIONNAIRE"

        db.session.commit()

        return session



    @staticmethod
    def finish_if_inactive(
            session_id,
            limite=300
    ):

        session = \
            SessionUtilisateur.query.get(
                session_id
            )

        if not session:
            return None

        if session.temps_inactivite >= limite:
            session.etat = \
                "FIN_SESSION"

            db.session.commit()

        return session

    @staticmethod
    def close_session(session_id):

        session = \
            SessionUtilisateur.query.get(
                session_id
            )

        if session:

            session.date_fin = \
                datetime.now()

            session.etat = \
                "FIN_SESSION"

            db.session.commit()