from app import app
from config.database import db

from models.ville import Ville
from models.utilisateur import Utilisateur

with app.app_context():

    ville = Ville(
        nom_ville="Royaume de Dieu"
    )

    db.session.add(ville)
    db.session.commit()

    utilisateur = Utilisateur(
        nom="Bonsomi",
        prenom="Manassé",
        age=26,
        type_profil="DEVELOPPEUR",
        id_ville=ville.id_ville
    )

    db.session.add(utilisateur)
    db.session.commit()

    print(ville.utilisateurs)
    print("Ville créée :", ville.nom_ville)
    print("Utilisateur créé :", utilisateur.nom)