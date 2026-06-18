from models.formateur import Formateur


class AuthController:

    @staticmethod
    def login(email, password):
        user = Formateur.query.filter_by(email=email).first()

        if user and user.password == password:
            return user

        return None