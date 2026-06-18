from config.database import db

from models.question import Question

from services.audit_service import \
    AuditService


class QuestionController:

    @staticmethod
    def create(
            texte_question,
            ordre_question,
            id_categorie
    ):

        try:

            question = Question(

                texte_question=
                texte_question,

                ordre_question=
                ordre_question,

                id_categorie=
                id_categorie,

                active=True
            )

            db.session.add(question)

            db.session.commit()

            AuditService.log(

                action="QUESTION",

                objet="AJOUT",

                resultat="SUCCES",

                details=texte_question
            )

            return question

        except Exception as e:

            db.session.rollback()

            AuditService.log_error(
                str(e)
            )

            return None

    @staticmethod
    def get_all():

        return Question.query.order_by(
            Question.ordre_question
        ).all()

    @staticmethod
    def get_by_id(id_question):

        return Question.query.get(
            id_question
        )

    @staticmethod
    def update(
            id_question,
            texte_question=None,
            ordre_question=None,
            active=None
    ):

        try:

            question = Question.query.get(
                id_question
            )

            if not question:

                return None

            if texte_question is not None:

                question.texte_question = \
                    texte_question

            if ordre_question is not None:

                question.ordre_question = \
                    ordre_question

            if active is not None:

                question.active = active

            db.session.commit()

            AuditService.log(

                action="QUESTION",

                objet="MODIFICATION",

                resultat="SUCCES",

                details=
                f"Question {id_question}"
            )

            return question

        except Exception as e:

            db.session.rollback()

            AuditService.log_error(
                str(e)
            )

            return None

    @staticmethod
    def delete(id_question):

        try:

            question = Question.query.get(
                id_question
            )

            if not question:

                return False

            db.session.delete(question)

            db.session.commit()

            return True

        except Exception:

            db.session.rollback()

            return False