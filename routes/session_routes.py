from flask import Blueprint
from flask import request
from flask import jsonify

from controllers.session_controller \
    import SessionController

session_bp = Blueprint(
    "session",
    __name__
)


@session_bp.route(
    "/session/start",
    methods=["POST"]
)
def start_session():

    data = request.json

    session = \
        SessionController.create(

            data["id_utilisateur"],

            data.get(
                "id_campagne"
            )
        )

    return jsonify({

        "success": True,

        "data": {

            "id_session":
                session.id_session
        }
    })


@session_bp.route(
    "/session/save",
    methods=["POST"]
)
def save_progress():

    data = request.json

    result = \
        SessionController.save_progress(

            data["id_session"],

            data["question"],

            data["etat"]
        )

    return jsonify(result)


@session_bp.route(
    "/session/pause",
    methods=["POST"]
)
def pause_session():

    data = request.json

    result = \
        SessionController.pause(

            data["id_session"]
        )

    return jsonify(result)



@session_bp.route(
    "/session/can-resume/<int:id_utilisateur>",
    methods=["GET"]
)
def can_resume(
        id_utilisateur
):

    return jsonify({

        "success": True,

        "resume":
            SessionController.can_resume(
                id_utilisateur
            )
    })



@session_bp.route(
    "/session/restore/<int:id_utilisateur>",
    methods=["POST"]
)
def restore(
        id_utilisateur
):

    result = \
        SessionController.restore(
            id_utilisateur
        )

    return jsonify(result)

@session_bp.route(
    "/session/resume",
    methods=["POST"]
)
def resume_session():

    data = request.json

    result = \
        SessionController.resume(

            data["id_session"]
        )

    return jsonify(result)


@session_bp.route(
    "/session/user/<int:id_utilisateur>",
    methods=["GET"]
)
def last_session(
        id_utilisateur
):

    result = \
        SessionController.get_last_session(
            id_utilisateur
        )

    return jsonify({

        "success": True,

        "data": result
    })


@session_bp.route(
    "/session/inactivity",
    methods=["POST"]
)
def inactivity():

    data = request.json

    result = \
        SessionController.update_inactivity(

            data["id_session"],

            data["secondes"]
        )

    return jsonify(result)


@session_bp.route(
    "/session/restart",
    methods=["POST"]
)
def restart():

    data = request.json

    result = \
        SessionController.restart(

            data["id_session"]
        )

    return jsonify(result)


@session_bp.route(
    "/session/close",
    methods=["POST"]
)
def close():

    data = request.json

    result = \
        SessionController.close(
            data["id_session"]
        )

    return jsonify(result)