from flask import Blueprint, request, jsonify
from controllers.command_controller import CommandController
from controllers.command_controller import CommandController
from services.command_executor import CommandExecutor
from models.commande import Commande

from config.database import db

command_bp = Blueprint("command", __name__)


# =========================
# EXECUTE COMMAND
# =========================
@command_bp.route("/commands/execute", methods=["POST"])
def execute_command():

    data = request.json

    result = CommandController.execute(
        data["command"]
    )

    return jsonify(result)


# =========================
# GET ALL COMMANDS
# =========================
@command_bp.route("/commands", methods=["GET"])
def get_commands():

    commands = Commande.query.order_by(
        Commande.id_commande.desc()
    ).all()

    return jsonify({
        "success": True,
        "data": [
            {
                "id_commande": c.id_commande,
                "texte_commande": c.texte_commande,
                "tokens": c.tokens,
                "resultat": c.resultat,
                "valide": c.valide,
                "date_execution": str(c.date_execution)
            }
            for c in commands
        ]
    })