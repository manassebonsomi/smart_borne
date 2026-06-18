from flask import Blueprint
from flask import jsonify

from controllers.erreur_controller \
    import ErreurController

erreur_bp = Blueprint(
    "erreur",
    __name__
)


@erreur_bp.route(
    "/erreurs",
    methods=["GET"]
)
def get_erreurs():

    erreurs = \
        ErreurController.get_all()

    return jsonify([

        {

            "id":
                e.id_erreur,

            "type":
                e.type_erreur,

            "message":
                e.message,

            "corrigee":
                e.corrigee

        }

        for e in erreurs
    ])