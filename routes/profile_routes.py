from flask import Blueprint
from flask import request
from flask import jsonify
from controllers.profile_controller import ProfileController

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/profile", methods=["POST"])
def create_profile():
    data = request.json
    utilisateur = ProfileController.create(data)

    return jsonify({
        "success": True,
        "data": {
            "id": utilisateur.id_utilisateur
        },
        "message": "Utilisateur créé"
    })

@profile_bp.route("/profile", methods=["GET"])
def get_profiles():
    utilisateurs = ProfileController.get_all()

    return jsonify({
        "success": True,
        "data": [
            {
                "id": u.id_utilisateur,
                "nom": u.nom,
                "prenom": u.prenom
            }
            for u in utilisateurs
        ]
    })