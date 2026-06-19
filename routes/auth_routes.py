from flask import Blueprint, request, jsonify
from controllers.auth_controller import AuthController
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

auth_routes = Blueprint("auth_routes", __name__)


@auth_routes.route("auth/login", methods=["POST"])
def login():

    data = request.json
    resultat = AuthController.login(
            data["email"],
            data["mot_de_passe"]
        )

    if not resultat:
        return jsonify({
            "success":
                False,
            "message":
                "Email ou mot de passe incorrect"
        }), 401

    return jsonify({
        "success":
            True,
        "data":
            resultat
    })


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
    "/auth/profile",
    methods=["GET"]
)
@jwt_required()
def get_profile():

    user_id = get_jwt_identity()
    utilisateur = AuthController.get_by_id(
            int(user_id)
        )

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


@auth_routes.route(
    "/auth/profile/<int:id_formateur>",
    methods=["GET"]
)
def get_profile_by_id(
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