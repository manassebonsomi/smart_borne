from models.utilisateur import Utilisateur
from models.session import SessionUtilisateur
from models.recommandation import Recommandation
from models.question import Question
from models.campagne import Campagne
from models.erreur import Erreur
from models.audit_log import AuditLog
from models.parcours import Parcours
from models.commande import Commande


class DashboardController:
    @staticmethod
    def statistics():
        return {
            "utilisateurs": Utilisateur.query.count(),
            "sessions": SessionUtilisateur.query.count(),
            "recommandations": Recommandation.query.count(),
            "questions": Question.query.count(),
            "commandes": Commande.query.count(),
            "campagnes": Campagne.query.count(),
            "erreurs": Erreur.query.count(),
            "audits": AuditLog.query.count()
        }

    @staticmethod
    def parcours_statistics():
        resultats = []
        parcours = Parcours.query.order_by(Parcours.nom_parcours.all())

        for p in parcours:
            total = Recommandation.query.filter_by(id_parcours=p.id_parcours).count()
            resultats.append({
                "parcours": p.nom_parcours,
                "nombre": total
            })
        return resultats

    @staticmethod
    def session_statistics():
        return {
            "actives": SessionUtilisateur.query.filter_by(etat="QUESTIONNAIRE").count(),
            "interrompues": SessionUtilisateur.query.filter_by(etat="SESSION_INTERRUPTION").count(),
            "terminees":SessionUtilisateur.query.filter_by(etat="FIN_SESSION").count()
        }

    @staticmethod
    def user_statistics():
        return {
            "enfants": Utilisateur.query.filter_by(type_profil="ENFANT").count(),
            "adolescents": Utilisateur.query.filter_by(type_profil="ADOLESCENT").count(),
            "parents": Utilisateur.query.filter_by(type_profil="PARENT").count()
        }

    @staticmethod
    def recommendations():
        recommandations = Recommandation.query.all()
        return [
            {
                "id": r.id_recommandation,
                "profil": r.profil_detecte,
                "score": r.score,
                "session": r.id_session
            }
            for r in recommandations
        ]

    @staticmethod
    def errors():
        erreurs = Erreur.query.order_by(Erreur.id_erreur.desc()).all()
        return [
            {
                "id": e.id_erreur,
                "type": e.type_erreur,
                "message": e.message,
                "corrigee": e.corrigee,
                "date":str(e.date_erreur)
            }
            for e in erreurs
        ]

    @staticmethod
    def audit_logs():
        logs = AuditLog.query.order_by(AuditLog.id_audit.desc()).all()
        return [
            {
                "id": log.id_audit,
                "date": str(log.date_action),
                "action": log.action,
                "objet": log.objet,
                "resultat": log.resultat,
                "details": log.details
            }
            for log in logs
        ]

    @staticmethod
    def campaigns():
        campagnes = Campagne.query.all()
        return [
            {
                "id": c.id_campagne,
                "nom": c.nom_campagne,
                "description": c.description,
                "date_debut": str(c.date_debut),
                "date_fin": str(c.date_fin),
                "active": c.active
            }
            for c in campagnes
        ]

    @staticmethod
    def questions():
        questions = Question.query.order_by(Question.ordre_question).all()
        return [
            {
                "id": q.id_question,
                "question": q.texte_question,
                "ordre": q.ordre_question,
                "active": q.active,
                "categorie": q.id_categorie
            }
            for q in questions
        ]