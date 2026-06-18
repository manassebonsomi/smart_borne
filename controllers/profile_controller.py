from config.database import db
from models.utilisateur import Utilisateur


class ProfileController:

    @staticmethod
    def create(data):

        utilisateur = Utilisateur(
            nom=data.get("nom"),
            prenom=data.get("prenom"),
            age=data.get("age"),
            type_profil=data.get("type_profil"),
            id_ville=data.get("id_ville")
        )

        db.session.add(utilisateur)
        db.session.commit()

        return utilisateur

    @staticmethod
    def update(id_utilisateur, data):

        utilisateur = Utilisateur.query.get(id_utilisateur)

        if not utilisateur:
            return None

        for key, value in data.items():
            setattr(utilisateur, key, value)

        db.session.commit()
        return utilisateur

    @staticmethod
    def get_all():

        return Utilisateur.query.all()

    @staticmethod
    def get_by_id(id_utilisateur):

        return Utilisateur.query.get(id_utilisateur)

    @staticmethod
    def delete(id_utilisateur):

        utilisateur = Utilisateur.query.get(id_utilisateur)

        if utilisateur:

            db.session.delete(utilisateur)
            db.session.commit()

            return True

        return False