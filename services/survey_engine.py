from models.question import Question


class SurveyEngine:

    @staticmethod
    def get_questions():
        return Question.query.filter_by(active=True).order_by(Question.ordre_question.asc()).all()

    @staticmethod
    def get_question_by_order(ordre):
        return Question.query.filter_by(active=True, ordre_question=ordre).first()

    @staticmethod
    def get_next_question(ordre_actuel):
        return Question.query.filter(Question.active == True, Question.ordre_question > ordre_actuel).order_by(Question.ordre_question.asc()).first()

    @staticmethod
    def get_previous_question(ordre_actuel):
        return Question.query.filter(Question.active == True, Question.ordre_question < ordre_actuel).order_by(Question.ordre_question.desc()).first()

    @staticmethod
    def is_finished(ordre_actuel):
        prochaine = SurveyEngine.get_next_question(ordre_actuel)
        return prochaine is None