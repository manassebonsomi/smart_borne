from services.session_manager \
    import SessionManager


class SessionController:

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