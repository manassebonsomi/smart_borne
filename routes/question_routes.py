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


@question_bp.route(
    "/questions/<int:id_question>",
    methods=["GET"]
)
def get_question(id_question):

    question = \
        QuestionController.get_by_id(
            id_question
        )

    if not question:

        return jsonify({

            "success": False,

            "message":
                "Question introuvable"

        }), 404

    return jsonify({

        "success": True,

        "data": {

            "id_question":
                question.id_question,

            "texte_question":
                question.texte_question,

            "ordre_question":
                question.ordre_question,

            "active":
                question.active,

            "id_categorie":
                question.id_categorie
        }
    })


@question_bp.route(
    "/questions/<int:id_question>",
    methods=["PUT"]
)
def update_question(id_question):

    data = request.json

    question = \
        QuestionController.update(
            data["texte_question"],
            data["ordre_question"],
        )

    if not question:

        return jsonify({

            "success": False,

            "message":
                "Question introuvable"

        }), 404

    return jsonify({

        "success": True,

        "message":
            "Question modifiée",

        "id": id_question
    })


@question_bp.route(
    "/questions/<int:id_question>",
    methods=["DELETE"]
)
def delete_question(id_question):

    deleted = \
        QuestionController.delete(
            id_question
        )

    if not deleted:

        return jsonify({

            "success": False,

            "message":
                "Question introuvable"

        }), 404

    return jsonify({

        "success": True,

        "message":
            "Question supprimée"
    })


