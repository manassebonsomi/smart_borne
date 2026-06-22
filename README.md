# CCC ORIENTATION SYSTEM

## Présentation

CCC Orientation System est une plateforme intelligente d'orientation numérique destinée aux enfants et adolescents.

Le système fonctionne sous forme de borne interactive permettant :

* l'identification des utilisateurs ;
* le lancement automatique de questionnaires ;
* l'analyse des réponses ;
* la génération d'un parcours recommandé ;
* la gestion des statistiques ;
* l'exécution de commandes intelligentes par les formateurs ;
* le suivi complet des sessions utilisateurs.

Le projet intègre un analyseur lexical, un parser LL(1), un moteur de recommandation, un système d'audit et une gestion avancée des erreurs.

---

# Fonctionnalités principales

## Côté Élève

* Création de profil
* Reprise de session interrompue
* Questionnaire interactif
* Sauvegarde automatique
* Détection d'inactivité
* Génération automatique d'un parcours
* Affichage des résultats

### Parcours disponibles

* Découverte Numérique
* Scratch Junior
* Scratch Avancé
* Python Débutant
* Mentor Junior

---

## Côté Formateur

### Dashboard

* Nombre total d'utilisateurs
* Nombre de questionnaires terminés
* Nombre de recommandations générées
* Statistiques générales

### Gestion des Questions

* Ajouter une question
* Modifier une question
* Supprimer une question
* Activer / désactiver une question

### Gestion des Commandes IA

Exemples :

AFFICHER STATISTIQUES

AFFICHER ERREURS

LANCER ENQUETE CYBERSECURITE

LANCER CAMPAGNE ECOLE

CHERCHER ENFANTS KINSHASA

CHERCHER ADOLESCENTS INTERESSES PAR PYTHON

AJOUTER QUESTION

MODIFIER QUESTION 3

SUPPRIMER QUESTION 5

EXPORTER RAPPORT

RECOMMENCER SESSION

QUITTER

### Historique

* Historique des commandes
* Historique des audits
* Historique des erreurs

---

# Architecture du Projet

backend/

config/

controllers/

models/

routes/

services/

frontend/

admin/

borne/

assets/

database/

migrations/

rapport_ccc/

---

# Technologies Utilisées

## Backend

* Python 3
* Flask
* Flask SQLAlchemy
* Flask JWT Extended
* Flask CORS

## Base de données

* MySQL

ou

* SQLite (mode hors ligne)

## Frontend

* HTML5
* CSS3
* JavaScript Vanilla

---

# Installation

## 1. Cloner le projet

git clone https://github.com/manassebonsomi/smart_borne.git

cd smart_borne

---

## 2. Créer un environnement virtuel

Windows

python -m venv .venv

.venv\Scripts\activate

Linux / Mac

python3 -m venv .venv

source .venv/bin/activate

---

## 3. Installer les dépendances

pip install -r requirements.txt

---

# Configuration Base de Données

Modifier :

avec password = "Votre_mot_de_passe_mysql"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:'+password+'@localhost/db_ccc_orientation_system'

---

# Création des Tables

Exécuter :

python create_tables.py

---

# Lancement du Serveur

Depuis la racine du projet :

python app.py

Le serveur démarre sur :

http://127.0.0.1:5000

---

# Utilisation

## Interface Formateur

Ouvrir le fich :

ccc_orientation_system/frontend/admin/dashboard.html

---

## Interface Borne

Ouvrir le fichier d'accueil :

ccc_orientation_system/frontend/index.html


Toujours utiliser le serveur Flask.

---

# Flux Utilisateur

1. Création du profil
2. Démarrage de session
3. Questionnaire
4. Sauvegarde automatique
5. Analyse
6. Génération de recommandation
7. Affichage du résultat
8. Fin de session

---

# Moteur de Recommandation

Le système attribue des points selon :

## Âge

* 0 à 7 ans → Découverte Numérique
* 8 à 10 ans → Scratch Junior
* 11 à 13 ans → Scratch Avancé
* 14 à 16 ans → Python Débutant
* 17+ ans → Mentor Junior

## Niveau scolaire

Le niveau scolaire ajoute un bonus.

## Réponses

Réponse | Points

NON | 0

UN PEU | 2

MOYEN | 3

BEAUCOUP | 5

OUI | 5

Chaque question appartient à une catégorie reliée à un parcours.

Le parcours ayant le score total le plus élevé est recommandé.

---

# Analyseur Lexical

Le système transforme les commandes du formateur en tokens.

Exemple :

AFFICHER STATISTIQUES

devient :

[AFFICHER]
[STATISTIQUES]

---

# Analyseur Syntaxique LL(1)

Validation des commandes selon une grammaire formelle.

Exemple :

AFFICHER STATISTIQUES

✔ valide

AFFICHER STATISTIQ

✘ invalide

Suggestion :

"Voulez-vous dire : AFFICHER STATISTIQUES ?"

---

# Gestion des Erreurs

Le système enregistre :

* erreurs applicatives
* erreurs SQL
* erreurs d'analyse lexicale
* erreurs syntaxiques
* erreurs d'exécution

Toutes les erreurs sont visibles dans :

Menu Erreurs

---

# Audit

Chaque action importante est enregistrée :

* connexion
* création
* modification
* suppression
* commandes
* recommandations

---

# Sécurité

* JWT Authentication
* Validation des entrées
* Gestion des exceptions
* Journalisation des événements

---

# Développement

Pour lancer en mode debug :

flask --app app.py --debug run

ou

python app.py

---

# Auteur

Manassé Bonsomi - Formateur (CCC)

Projet d'orientation intelligente basé sur les automates, les compilateurs et les systèmes experts.

---

# Version

1.0 

Statut : Fonctionnel
