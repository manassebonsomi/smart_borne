from flask_jwt_extended import create_access_token
from models.formateur import Formateur
from services.auth_service import AuthService


class AuthController:

    @staticmethod
    def login(email, mot_de_passe):

        formateur = Formateur.query.filter_by(email=email).first()

        if not formateur:
            return None

        if not AuthService.verify_password(mot_de_passe, formateur.mot_de_passe):
            return None

        token = create_access_token(identity=str(formateur.id_formateur))

        return {

            "token": token,
            "id_formateur": formateur.id_formateur,
            "nom": formateur.nom,
            "email": formateur.email
        }

    @staticmethod
    def get_by_id(id_formateur):
        return Formateur.query.get(id_formateur)


