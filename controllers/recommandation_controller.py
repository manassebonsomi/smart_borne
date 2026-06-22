from models.session import SessionUtilisateur
from models.reponse import Reponse
from models.recommandation import Recommandation
from services.recommendation_service import RecommendationService


class RecommendationController:

    @staticmethod
    def generate(id_session):
        session = SessionUtilisateur.query.get(id_session)
        if not session:
            raise Exception("Session introuvable")

        utilisateur = session.utilisateur
        reponses = Reponse.query.filter_by(id_session=id_session).all()

        donnees_reponses = []

        for reponse in reponses:
            donnees_reponses.append({
                "categorie": reponse.question.id_categorie,
                "valeur": reponse.valeur_reponse
            })

        return RecommendationService.generate_and_save(
                session,
                utilisateur,
                donnees_reponses
            )

    @staticmethod
    def get_by_session(id_session):
        return Recommandation.query.filter_by(id_session=id_session).first()

    @staticmethod
    def get_all():
        return Recommandation.query.all()