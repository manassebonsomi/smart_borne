from flask import Blueprint
from flask import jsonify

from controllers.utilisateur_controller \
    import UtilisateurController

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