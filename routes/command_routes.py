from flask import Blueprint
from flask import request
from flask import jsonify
from flask_jwt_extended import jwt_required
from controllers.command_controller import CommandController

command_bp = Blueprint(
    "command",
    __name__
)

@command_bp.route(
    "/commands/execute",
    methods=["POST"]
)
@jwt_required()
def execute_command():

    data = request.json

    result = CommandController.execute(
            data["command"]
        )

    return jsonify(result)