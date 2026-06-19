from flask import Blueprint
from flask import jsonify
from flask import request
from controllers.utilisateur_controller import UtilisateurController

utilisateur_bp = Blueprint(
    "utilisateur",
    __name__
)


@utilisateur_bp.route(
    "/utilisateurs",
    methods=["GET"]
)
def get_utilisateurs():

    users = \
        UtilisateurController.get_all()

    return jsonify([

        {

            "id":
                u.id_utilisateur,

            "nom":
                u.nom,

            "prenom":
                u.prenom,

            "age":
                u.age,

            "profil":
                u.type_profil

        }

        for u in users
    ])


@utilisateur_bp.route(
    "/utilisateurs/<int:id_utilisateur>",
    methods=["GET"]
)
def get_utilisateur(
        id_utilisateur
):

    utilisateur = \
        UtilisateurController \
        .get_by_id(
            id_utilisateur
        )

    if not utilisateur:

        return jsonify({

            "success": False,

            "message":
                "Utilisateur introuvable"

        }), 404

    return jsonify({

        "success": True,

        "data": {

            "id":
                utilisateur.id_utilisateur,

            "nom":
                utilisateur.nom,

            "prenom":
                utilisateur.prenom,

            "age":
                utilisateur.age,

            "niveau_scolaire":
                utilisateur.niveau_scolaire,

            "type_profil":
                utilisateur.type_profil,

            "id_ville":
                utilisateur.id_ville
        }
    })

@utilisateur_bp.route(
    "/utilisateurs",
    methods=["POST"]
)
def create_utilisateur():

    data = request.json

    utilisateur = \
        UtilisateurController.create(

            data["nom"],

            data["prenom"],

            data["age"],

            data[
                "niveau_scolaire"
            ],

            data[
                "type_profil"
            ],

            data["id_ville"]
        )

    return jsonify({

        "success": True,

        "id_utilisateur":
            utilisateur.id_utilisateur
    }), 201