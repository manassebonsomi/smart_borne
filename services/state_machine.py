from services.session_manager import SessionManager


class StateMachine:

    transitions = {

        "ACCUEIL": {

            "START":
                "PROFIL"
        },

        "PROFIL": {

            "PROFILE_CREATED":
                "QUESTIONNAIRE"
        },

        "QUESTIONNAIRE": {

            "SURVEY_COMPLETED":
                "ANALYSE"
        },

        "ANALYSE": {

            "RESULT_READY":
                "RESULTAT"
        },

        "RESULTAT": {

            "FINISH":
                "FIN_SESSION"
        },

        "FIN_SESSION": {}
    }

    def __init__(self):

        self.state = "ACCUEIL"

    def transition(

            self,

            event,

            session_id=None
    ):

        if event not in \
                self.transitions[
                    self.state
                ]:

            raise Exception(

                f"Transition invalide : "
                f"{self.state} -> {event}"
            )

        self.state = \
            self.transitions[
                self.state
            ][event]

        # Synchronisation BDD

        if session_id:

            SessionManager.set_state(

                session_id,

                self.state
            )

        return self.state

    def get_state(self):

        return self.state