from flask import Blueprint
from flask import request
from flask import jsonify

from controllers.question_controller \
    import QuestionController

question_bp = Blueprint(
    "question",
    __name__
)


@question_bp.route(
    "/questions",
    methods=["GET"]
)
def get_questions():

    questions = \
        QuestionController.get_all()

    return jsonify([

        {

            "id_question":
                q.id_question,

            "texte_question":
                q.texte_question,

            "ordre_question":
                q.ordre_question,

            "active":
                q.active

        }

        for q in questions
    ])


@question_bp.route(
    "/questions",
    methods=["POST"]
)
def create_question():

    data = request.json

    question = \
        QuestionController.create(

            data["texte_question"],

            data["ordre_question"],

            data["id_categorie"]
        )

    return jsonify({

        "id_question":
            question.id_question
    })