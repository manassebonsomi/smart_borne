from services.session_manager \
    import SessionManager


class SessionController:

    @staticmethod
    def create(
            utilisateur_id,
            campagne_id=None
    ):

        return \
            SessionManager.create_session(

                utilisateur_id,

                campagne_id
            )

    @staticmethod
    def save_progress(

            id_session,

            question,

            state
    ):

        SessionManager.save_progress(

            id_session,

            question,

            state
        )

        return {

            "success": True,

            "message":
                "Progression sauvegardée"
        }

    @staticmethod
    def pause(
            id_session
    ):

        SessionManager.pause_session(
            id_session
        )

        return {

            "success": True,

            "message":
                "Session mise en pause"
        }

    @staticmethod
    def can_resume(utilisateur_id
    ):

        return \
            SessionManager.can_resume(
                utilisateur_id
            )

    @staticmethod
    def restore(
            utilisateur_id
    ):

        session = \
            SessionManager.restore_session(
                utilisateur_id
            )

        if not session:
            return {

                "success": False
            }

        return {

            "success": True,

            "id_session":
                session.id_session,

            "question":
                session.question_actuelle,

            "etat":
                session.etat
        }


    @staticmethod
    def resume(
            id_session
    ):

        session = \
            SessionManager.resume_session(
                id_session
            )

        return {

            "success": True,

            "session_id":
                session.id_session,

            "question_actuelle":
                session.question_actuelle,

            "etat":
                session.etat
        }

    @staticmethod
    def update_inactivity(

            id_session,

            secondes
    ):

        SessionManager.update_inactivity(

            id_session,

            secondes
        )

        return {

            "success": True
        }

    @staticmethod
    def get_last_session(
            utilisateur_id
    ):

        session = \
            SessionManager.get_last_session(
                utilisateur_id
            )

        if not session:

            return None

        return {

            "id_session":
                session.id_session,

            "etat":
                session.etat,

            "question_actuelle":
                session.question_actuelle
        }

    @staticmethod
    def restart(
            session_id
    ):

        session = \
            SessionManager.restart_session(
                session_id
            )

        return {

            "success": True,

            "id_session":
                session.id_session,

            "etat":
                session.etat
        }

    @staticmethod
    def close(
            session_id
    ):

        SessionManager.close_session(
            session_id
        )

        return {

            "success": True,

            "message":
                "Session terminée"
        }