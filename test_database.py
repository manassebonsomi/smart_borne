from app import app
from config.database import db
from models.ville import Ville

with app.app_context():

    ville = Ville(
        nom_ville="Kinshasa"
    )

    db.session.add(ville)
    db.session.commit()

    print("Ville créée avec succès")