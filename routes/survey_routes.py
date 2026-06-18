from flask import Blueprint, jsonify
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