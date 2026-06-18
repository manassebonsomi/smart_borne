from config.database import db

from models.utilisateur import \
    Utilisateur

from services.audit_service import \
    AuditService


class UtilisateurController:

    @staticmethod
    def get_all():

        return Utilisateur.query.all()

    @staticmethod
    def get_by_id(
            id_utilisateur
    ):

        return Utilisateur.query.get(
            id_utilisateur
        )

    @staticmethod
    def search_children():

        return Utilisateur.query.filter_by(

            type_profil="ENFANT"

        ).all()

    @staticmethod
    def search_adolescents():

        return Utilisateur.query.filter_by(

            type_profil=
            "ADOLESCENT"

        ).all()

    @staticmethod
    def search_by_city(
            id_ville
    ):

        return Utilisateur.query.filter_by(

            id_ville=id_ville

        ).all()