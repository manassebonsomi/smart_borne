from flask import Blueprint, jsonify, request
from controllers.survey_controller import SurveyController

survey_routes = Blueprint("survey_routes", __name__)


@survey_routes.route("/questions", methods=["GET"])
def get_questions():

    questions = SurveyController.get_questions()

    return jsonify({
        "status": "success",
        "data": [
            {
                "id": q.id_question,
                "question": q.texte_question,
                "ordre": q.ordre_question
            }
            for q in questions
        ]
    }), 200


@survey_routes.route("/questions/<int:id_question>", methods=["GET"])
def get_question(id_question):

    question = SurveyController.get_question(id_question)

    if not question:
        return jsonify({
            "status": "error",
            "message": "Question introuvable"
        }), 404

    return jsonify({
        "status": "success",
        "data": {
            "id": question.id_question,
            "question": question.texte_question
        }
    }), 200


@survey_routes.route(
    "/survey/start",
    methods=["POST"]
)
def start_survey():

    try:

        data = request.get_json()

        id_session = data.get(
            "id_session"
        )

        resultat = \
            SurveyController.start(
                id_session
            )

        return jsonify(
            resultat
        ), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message":
                str(e)

        }), 400



# QUESTION PAR ORDRE
# GET /api/survey/question/1
# ==========================================

@survey_routes.route(
    "/survey/question/<int:ordre>",
    methods=["GET"]
)
def get_question(ordre):
    try:

        question = \
            SurveyController \
            .get_question(
                ordre
            )

        if not question:

            return jsonify({

                "success":
                    False,

                "message":
                    "Question introuvable"

            }), 404

        return jsonify({

            "success":
                True,

            "data":
                question

        }), 200

    except Exception as e:

        return jsonify({

            "success":
                False,

            "message":
                str(e)

        }), 400


# ==========================================
# REPONDRE QUESTION
# POST /api/survey/answer
# ==========================================

@survey_routes.route(
    "/survey/answer",
    methods=["POST"]
)
def answer_question():
    try:
        data = request.get_json()
        id_session = data.get(
            "id_session"
        )

        id_question = data.get(
            "id_question"
        )

        valeur = data.get(
            "valeur"
        )

        resultat = \
            SurveyController.answer(

                id_session,

                id_question,

                valeur
            )

        return jsonify({

            "success":
                True,

            "data":
                resultat

        }), 200

    except Exception as e:

        return jsonify({

            "success":
                False,

            "message":
                str(e)

        }), 400


# ==========================================
# TERMINER QUESTIONNAIRE
# POST /api/survey/finish
# ==========================================

@survey_routes.route(
    "/survey/finish",
    methods=["POST"]
)
def finish_survey():
    try:
        data = request.get_json()
        id_session = data.get(
            "id_session"
        )

        resultat = \
            SurveyController.finish(
                id_session
            )

        return jsonify(
            resultat
        ), 200

    except Exception as e:

        return jsonify({

            "success":
                False,

            "message":
                str(e)

        }), 400