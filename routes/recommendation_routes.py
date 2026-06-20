from flask import Blueprint
from flask import jsonify

from controllers.recommandation_controller \
    import RecommendationController

recommandation_bp = Blueprint(
    "recommandation",
    __name__
)

@recommandation_bp.route(
    "/recommandation/generate/<int:id_session>",
    methods=["POST"]
)
def generate_recommandation(
        id_session
):

    try:

        result = \
            RecommendationController.generate(
                id_session
            )

        return jsonify({

            "success": True,

            "data": result

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 400




@recommandation_bp.route(
    "/recommandation/<int:id_session>",
    methods=["GET"]
)
def get_recommandation(
        id_session
):

    try:

        recommandation = \
            RecommendationController \
            .get_by_session(

                id_session
            )

        if not recommandation:

            return jsonify({

                "success":
                    False,

                "message":
                    "Recommandation introuvable"

            }), 404

        return jsonify({

            "success":
                True,

            "data": {

                "id_recommandation":
                    recommandation.id_recommandation,

                "score":
                    recommandation.score,

                "profil_detecte":
                    recommandation.profil_detecte,

                "commentaire":
                    recommandation.commentaire,

                "id_session":
                    recommandation.id_session,

                "id_parcours":
                    recommandation.id_parcours
            }

        }), 200

    except Exception as e:

        return jsonify({

            "success":
                False,

            "message":
                str(e)

        }), 400


# ==========================================
# LISTE COMPLETE
# GET /api/recommandations
# ==========================================

@recommandation_bp.route(

    "/recommandations",

    methods=["GET"]
)
def get_all_recommandations():

    try:

        recommandations = \
            RecommendationController \
            .get_all()

        return jsonify({

            "success":
                True,

            "total":
                len(recommandations),

            "data":

                [

                    {

                        "id":
                            r.id_recommandation,

                        "score":
                            r.score,

                        "profil":
                            r.profil_detecte,

                        "session":
                            r.id_session

                    }

                    for r in recommandations
                ]

        }), 200

    except Exception as e:

        return jsonify({

            "success":
                False,

            "message":
                str(e)

        }), 400
