from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


class AuthService:

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def verify_password(password, hashed_password):
        return check_password_hash(hashed_password, password)