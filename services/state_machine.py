from services.constants import *


class StateMachine:

    def __init__(self):

        self.state = STATE_ACCUEIL

    def get_state(self):

        return self.state

    def reset(self):

        self.state = STATE_ACCUEIL

    def transition(self, event):

        transitions = {

            (STATE_ACCUEIL, "START"):
                STATE_CHOIX_LANGUE,

            (STATE_CHOIX_LANGUE, "LANG_SELECTED"):
                STATE_IDENTIFICATION,

            (STATE_IDENTIFICATION, "PROFILE_CREATED"):
                STATE_ENQUETE,

            (STATE_ENQUETE, "START_SURVEY"):
                STATE_QUESTION,

            (STATE_QUESTION, "ANSWER_SAVED"):
                STATE_SAUVEGARDE,

            (STATE_SAUVEGARDE, "NEXT_QUESTION"):
                STATE_QUESTION,

            (STATE_QUESTION, "SURVEY_COMPLETED"):
                STATE_ANALYSE,

            (STATE_ANALYSE, "ANALYSIS_DONE"):
                STATE_RECOMMANDATION,

            (STATE_RECOMMANDATION, "RESULT_READY"):
                STATE_RESULTAT,

            (STATE_RESULTAT, "DISPLAY_DONE"):
                STATE_CONFIRMATION,

            (STATE_CONFIRMATION, "CONFIRM"):
                STATE_FIN,

            (STATE_QUESTION, "INTERRUPT"):
                STATE_INTERRUPTION,

            (STATE_INTERRUPTION, "RESUME"):
                STATE_REPRISE,

            (STATE_REPRISE, "CONTINUE"):
                STATE_QUESTION
        }

        key = (
            self.state,
            event
        )

        if key in transitions:

            self.state = transitions[key]

        else:

            self.state = STATE_ERREUR

        return self.state