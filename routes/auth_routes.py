from flask import Blueprint, request, jsonify
from controllers.auth_controller import AuthController

auth_routes = Blueprint("auth_routes", __name__)


@auth_routes.route("/login", methods=["POST"])
def login():
    # data = request.get_json()
    data = request.json

    email = data.get("email")
    password = data.get("password")

    formateur = AuthController.login(email, password)

    if formateur:
        return jsonify({
            "status": "success",
            "message": "Connexion réussie",
            "data": {
                "id": formateur.id_formateur,
                "email": formateur.email,
                "nom":  formateur.nom
            }
        }), 200

    return jsonify({
        "status": "error",
        "message": "Email ou mot de passe incorrect"
    }), 401