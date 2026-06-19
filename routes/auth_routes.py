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


@auth_routes.route(
    "/auth/logout",
    methods=["POST"]
)
def logout():

    return jsonify({

        "success":
            True,

        "message":
            "Déconnexion réussie"

    })


@auth_routes.route(
    "/auth/profile/<int:id_formateur>",
    methods=["GET"]
)
def profile(
        id_formateur
):

    try:

        utilisateur = \
            AuthController \
            .get_by_id(
                id_formateur
            )

        if not utilisateur:

            return jsonify({

                "success":
                    False

            }), 404

        return jsonify({

            "success":
                True,

            "data": {

                "id":
                    utilisateur.id_formateur,

                "nom":
                    utilisateur.nom,

                "email":
                    utilisateur.email
            }

        })

    except Exception as e:

        return jsonify({

            "success":
                False,

            "message":
                str(e)
        }), 400