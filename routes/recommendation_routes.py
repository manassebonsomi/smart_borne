from flask import Blueprint
from flask import jsonify

from controllers.recommandation_controller \
    import RecommendationController

recommandation_bp = Blueprint(
    "recommandation",
    __name__
)


@recommandation_bp.route(
    "/recommandation/<int:id_session>",
    methods=["GET"]
)
def get_recommandation(id_session):

    recommandation = \
        RecommendationController \
        .get_by_session(
            id_session
        )

    if not recommandation:

        return jsonify({

            "success": False,

            "message":
            "Aucune recommandation"
        })

    return jsonify({

        "success": True,

        "data": {

            "score":
            recommandation.score,

            "profil":
            recommandation.profil_detecte
        }
    })

