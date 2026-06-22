from flask import Blueprint, jsonify, request
from controllers.survey_controller import SurveyController

survey_routes = Blueprint("survey_routes", __name__)


@survey_routes.route("/survey/start/<int:id_session>", methods=["POST"])
def start(id_session):
    state = SurveyController.start_session(id_session)

    return jsonify({
        "success": True,
        "etat": state
    })


@survey_routes.route("/survey/profile/<int:id_session>", methods=["POST"])
def profile(id_session):
    state = SurveyController.profile_created(id_session)

    return jsonify({
        "success": True,
        "etat": state
    })

@survey_routes.route("/survey/complete/<int:id_session>", methods=["POST"])
def complete(id_session):
    state = SurveyController.survey_completed(id_session)

    return jsonify({
        "success": True,
        "etat": state
    })


@survey_routes.route("/survey/result/<int:id_session>", methods=["POST"])
def result(id_session):
    state = SurveyController.result_ready(id_session)

    return jsonify({
        "success": True,
        "etat": state
    })


@survey_routes.route("/survey/finish/<int:id_session>", methods=["POST"])
def finish(id_session):
    state = SurveyController.finish(id_session)

    return jsonify({
        "success": True,
        "etat": state
    })


@survey_routes.route("/survey/save-answer", methods=["POST"])
def save_answer():
    data = request.json
    reponse = SurveyController.save_answer(
            data["id_session"],
            data["id_question"],
            data["valeur_reponse"]
        )

    return jsonify({
        "success": True,
        "id_reponse": reponse.id_reponse
    })

