from flask import Blueprint
from flask import request
from flask import jsonify

from controllers.campagne_controller \
    import CampagneController

campagne_bp = Blueprint(
    "campagne",
    __name__
)


@campagne_bp.route(
    "/campagnes",
    methods=["GET"]
)
def get_campagnes():

    campagnes = \
        CampagneController.get_all()

    return jsonify([

        {

            "id":
                c.id_campagne,

            "nom":
                c.nom_campagne,

            "active":
                c.active

        }

        for c in campagnes
    ])


@campagne_bp.route(
    "/campagnes",
    methods=["POST"]
)
def create_campagne():

    data = request.json

    campagne = \
        CampagneController.create(

            data["nom_campagne"],

            data["description"],

            data["date_debut"],

            data["date_fin"]
        )

    return jsonify({

        "id":
            campagne.id_campagne
    })