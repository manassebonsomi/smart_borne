from flask import Blueprint, jsonify, request
from controllers.survey_controller import SurveyController

survey_routes = Blueprint("survey_routes", __name__)


@survey_routes.route(
    "/survey/start/<int:id_session>",
    methods=["POST"]
)
def start(id_session):

    state = \
        SurveyController.start_session(
            id_session
        )

    return jsonify({

        "success": True,
        "etat": state
    })


@survey_routes.route(
    "/survey/profile/<int:id_session>",
    methods=["POST"]
)
def profile(id_session):

    state = \
        SurveyController.profile_created(
            id_session
        )

    return jsonify({
        "success": True,
        "etat": state
    })

@survey_routes.route(
    "/survey/complete/<int:id_session>",
    methods=["POST"]
)
def complete(id_session):

    state = \
        SurveyController.survey_completed(
            id_session
        )

    return jsonify({

        "success": True,

        "etat": state
    })



@survey_routes.route(
    "/survey/result/<int:id_session>",
    methods=["POST"]
)
def result(id_session):

    state = \
        SurveyController.result_ready(
            id_session
        )

    return jsonify({

        "success": True,

        "etat": state
    })


@survey_routes.route(
    "/survey/finish/<int:id_session>",
    methods=["POST"]
)
def finish(id_session):

    state = \
        SurveyController.finish(
            id_session
        )

    return jsonify({

        "success": True,

        "etat": state
    })


@survey_routes.route(
    "/survey/save-answer",
    methods=["POST"]
)
def save_answer():

    data = request.json

    reponse = \
        SurveyController.save_answer(

            data["id_session"],

            data["id_question"],

            data["valeur_reponse"]
        )

    return jsonify({

        "success": True,

        "id_reponse":
            reponse.id_reponse
    })







# @survey_routes.route("/questions/<int:id_question>", methods=["GET"])
# def get_question(id_question):
#
#     question = SurveyController.get_question(id_question)
#
#     if not question:
#         return jsonify({
#             "status": "error",
#             "message": "Question introuvable"
#         }), 404
#
#     return jsonify({
#         "status": "success",
#         "data": {
#             "id": question.id_question,
#             "question": question.texte_question
#         }
#     }), 200
#
#
# @survey_routes.route(
#     "/survey/start",
#     methods=["POST"]
# )
# def start_survey():
#
#     try:
#
#         data = request.get_json()
#
#         id_session = data.get(
#             "id_session"
#         )
#
#         resultat = \
#             SurveyController.start_session(
#                 id_session
#             )
#
#         return jsonify(
#             resultat
#         ), 200
#
#     except Exception as e:
#
#         return jsonify({
#
#             "success": False,
#
#             "message":
#                 str(e)
#
#         }), 400
#
#
#
# # QUESTION PAR ORDRE
# # GET /api/survey/question/1
# # ==========================================
#
#
# @survey_routes.route(
#     "/survey/question/<int:ordre>",
#     methods=["GET"]
# )
# def get_question_by_order(ordre):
#     try:
#
#         question = \
#             SurveyController \
#             .get_question(
#                 ordre
#             )
#
#         if not question:
#
#             return jsonify({
#
#                 "success":
#                     False,
#
#                 "message":
#                     "Question introuvable"
#
#             }), 404
#
#         return jsonify({
#
#             "success":
#                 True,
#
#             "data":
#                 question
#
#         }), 200
#
#     except Exception as e:
#
#         return jsonify({
#
#             "success":
#                 False,
#
#             "message":
#                 str(e)
#
#         }), 400
#
#
# # ==========================================
# # REPONDRE QUESTION
# # POST /api/survey/answer
# # ==========================================
#
# @survey_routes.route(
#     "/survey/answer",
#     methods=["POST"]
# )
# def answer_question():
#     try:
#         data = request.get_json()
#         id_session = data.get(
#             "id_session"
#         )
#
#         id_question = data.get(
#             "id_question"
#         )
#
#         valeur = data.get(
#             "valeur"
#         )
#
#         resultat = \
#             SurveyController.answer(
#
#                 id_session,
#
#                 id_question,
#
#                 valeur
#             )
#
#         return jsonify({
#
#             "success":
#                 True,
#
#             "data":
#                 resultat
#
#         }), 200
#
#     except Exception as e:
#
#         return jsonify({
#
#             "success":
#                 False,
#
#             "message":
#                 str(e)
#
#         }), 400
#
#
# # ==========================================
# # TERMINER QUESTIONNAIRE
# # POST /api/survey/finish
# # ==========================================
#
# @survey_routes.route(
#     "/survey/finish",
#     methods=["POST"]
# )
# def finish_survey():
#     try:
#         data = request.get_json()
#         id_session = data.get(
#             "id_session"
#         )
#
#         resultat = \
#             SurveyController.finish(
#                 id_session
#             )
#
#         return jsonify(
#             resultat
#         ), 200
#
#     except Exception as e:
#
#         return jsonify({
#
#             "success":
#                 False,
#
#             "message":
#                 str(e)
#
#         }), 400