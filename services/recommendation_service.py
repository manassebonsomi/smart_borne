from config.database import db
from models.parcours import Parcours
from models.recommandation import Recommandation
from services.recommendation_engine import RecommendationEngine
from services.audit_service import AuditService


class RecommendationService:

    @staticmethod
    def generate_and_save(session, utilisateur, reponses):

        resultat = RecommendationEngine.generate(
                age= utilisateur.age,
                niveau_scolaire= utilisateur.niveau_scolaire,
                reponses=reponses
            )

        parcours = Parcours.query.filter_by(
                nom_parcours= resultat["parcours"]).first()

        if not parcours:
            raise Exception(
                "Parcours introuvable : "
                + resultat["parcours"]
            )

        ancienne = Recommandation.query.filter_by(id_session=session.id_session).first()

        if ancienne:
            db.session.delete(ancienne )
            db.session.commit()

        recommandation = Recommandation(
                score=resultat["score"],
                profil_detecte=resultat["parcours"],
                commentaire="Recommandation générée automatiquement",
                id_session=session.id_session,
                id_parcours=parcours.id_parcours
            )

        db.session.add(recommandation)
        db.session.commit()

        AuditService.log(
            action="RECOMMANDATION",
            objet=resultat["parcours"],
            resultat="SUCCES",
            details=str(resultat)
        )

        return {
            "recommandation_id":recommandation.id_recommandation,
            **resultat
        }