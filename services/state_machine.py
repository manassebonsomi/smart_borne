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

    @staticmethod
    def transition(event, session_id):
        current_state = SessionManager.get_state(session_id)

        if not current_state:
            raise Exception("Session introuvable")

        if current_state not in StateMachine.transitions:

            raise Exception(
                f"Etat inconnu : "
                f"{current_state}"
            )

        if event not in StateMachine.transitions[current_state]:
            raise Exception(
                f"Transition invalide : "
                f"{current_state} -> {event}"
            )

        next_state = StateMachine.transitions[current_state][event]
        SessionManager.set_state(session_id, next_state)

        return next_state