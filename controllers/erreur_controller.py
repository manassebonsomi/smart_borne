from config.database import db

from models.erreur import Erreur

from services.audit_service import \
    AuditService


class ErreurController:

    @staticmethod
    def create(
            type_erreur,
            message
    ):

        erreur = Erreur(

            type_erreur=
            type_erreur,

            message=
            message
        )

        db.session.add(
            erreur
        )

        db.session.commit()

        return erreur

    @staticmethod
    def get_all():

        return Erreur.query.order_by(

            Erreur.date_erreur.desc()

        ).all()

    @staticmethod
    def get_by_id(
            id_erreur
    ):

        return Erreur.query.get(
            id_erreur
        )

    @staticmethod
    def mark_corrected(
            id_erreur
    ):

        erreur = Erreur.query.get(
            id_erreur
        )

        if erreur:

            erreur.corrigee = True

            db.session.commit()

        return erreur