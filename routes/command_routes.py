from flask import Blueprint, request, jsonify

from controllers.command_controller import CommandController
from models.commande import Commande

command_bp = Blueprint("command", __name__)


# EXÉCUTER UNE COMMANDE
@command_bp.route("/commands/execute", methods=["POST"])
def execute_command():

    # VALIDATION JSON
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "error": "INVALID_JSON",
            "message": "Le corps de la requête doit être un objet JSON."
        }), 400

    # VALIDATION COMMAND
    command = data.get("command")
    if command is None:
        return jsonify({
            "success": False,
            "error": "MISSING_COMMAND",
            "message": "Le champ 'command' est obligatoire."
        }), 400

    if not isinstance(command, str):
        return jsonify({
            "success": False,
            "error": "INVALID_COMMAND",
            "message": "Le champ 'command' doit être une chaîne de caractères."
        }), 400

    # EXÉCUTION
    result = CommandController.execute(texte_commande=command, id_formateur=None, data=None)

    # RÉSULTAT
    return jsonify(result), 200

# HISTORIQUE DES COMMANDES
@command_bp.route("/commands", methods=["GET"])
def get_commands():
    commands = (Commande.query.order_by(Commande.id_commande.desc()).all())
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