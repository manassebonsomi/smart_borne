from config.database import db
from models.audit_log import AuditLog
from models.erreur import Erreur


class AuditService:

    @staticmethod
    def log(
            action,
            objet,
            resultat,
            details
    ):

        audit = AuditLog(

            action=action,

            objet=objet,

            resultat=resultat,

            details=details
        )

        db.session.add(audit)

        db.session.commit()

        return audit

    @staticmethod
    def log_error(message):

        return AuditService.log(
            action="ERREUR",
            objet="SYSTEME",
            resultat="ECHEC",
            details=message
        )

    @staticmethod
    def log_command(
            commande
    ):

        return AuditService.log(
            action="COMMANDE",
            objet=commande,
            resultat="EXECUTEE",
            details=""
        )

    @staticmethod
    def log_recommendation(
            parcours
    ):

        return AuditService.log(
            action="RECOMMANDATION",
            objet=parcours,
            resultat="GENEREE",
            details=""
        )

    @staticmethod
    def log_login(email):

        AuditService.log(
            "LOGIN",
            email,
            "SUCCES",
            "Connexion formateur"
        )

    @staticmethod
    def log_recommendation(
            profil
    ):
        AuditService.log(
            action="RECOMMANDATION",
            objet=profil,
            resultat="GENEREE",
            details="Parcours proposé"
        )