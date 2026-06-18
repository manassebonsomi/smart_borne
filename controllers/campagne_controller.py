from config.database import db

from models.campagne import \
    Campagne

from services.audit_service import \
    AuditService


class CampagneController:

    @staticmethod
    def create(
            nom_campagne,
            description,
            date_debut,
            date_fin
    ):

        try:

            campagne = Campagne(

                nom_campagne=
                nom_campagne,

                description=
                description,

                date_debut=
                date_debut,

                date_fin=
                date_fin,

                active=True
            )

            db.session.add(
                campagne
            )

            db.session.commit()

            return campagne

        except Exception:

            db.session.rollback()

            return None

    @staticmethod
    def get_all():

        return Campagne.query.all()

    @staticmethod
    def get_by_id(
            id_campagne
    ):

        return Campagne.query.get(
            id_campagne
        )

    @staticmethod
    def activate(
            id_campagne
    ):

        campagne = Campagne.query.get(
            id_campagne
        )

        if campagne:

            campagne.active = True

            db.session.commit()

        return campagne

    @staticmethod
    def deactivate(
            id_campagne
    ):

        campagne = Campagne.query.get(
            id_campagne
        )

        if campagne:

            campagne.active = False

            db.session.commit()

        return campagne