from app import app
from config.database import db
from models.formateur import Formateur
from services.auth_service import AuthService


with app.app_context():
    admin = Formateur(
        nom="Norman",
        email="norman@ccc.cd",
        mot_de_passe=
        AuthService.hash_password(
            "123456"
        )
    )

    db.session.add(admin)
    db.session.commit()
    print("Formateur créé")