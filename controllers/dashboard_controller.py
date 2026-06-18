from models import Ville, SessionUtilisateur, Reponse, Campagne, Evenement
from models.utilisateur import Utilisateur
from models.recommandation import Recommandation
from models.erreur import Erreur
from models.commande import Commande


class DashboardController:

    @staticmethod
    def statistics():

        return {

            "villes":
                Ville.query.count(),

            "utilisateurs":
                Utilisateur.query.count(),

            "sessions":
                SessionUtilisateur
                .query.count(),

            "reponses":
                Reponse.query.count(),

            "recommandations":
                Recommandation
                .query.count(),

            "commandes":
                Commande.query.count(),

            "erreurs":
                Erreur.query.count(),

            "campagnes":
                Campagne.query.count(),

            "evenements":
                Evenement.query.count()
        }