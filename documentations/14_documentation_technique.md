# Documentation technique — CCC Orientation System

## 1. Présentation

Le **CCC Orientation System** est une application backend développée en Python et organisée selon une architecture modulaire séparant les modèles de données, la logique métier, les contrôleurs, les routes API, les services, la configuration et les tests.

L'application utilise **Flask** pour exposer les services HTTP, **SQLAlchemy** pour l'accès aux données et **MySQL** pour la persistance.

Le système intègre également un moteur de traitement des commandes basé sur un **correcteur de commandes**, un **analyseur lexical**, une **grammaire LL(1)**, une **table d'analyse syntaxique**, un **constructeur de commandes**, un **dispatcher** et des **handlers métier**.

---

## 2. Stack technique

La stack principale du projet est :

```text
Python 3.12
Flask
Flask-SQLAlchemy
PyMySQL
MySQL
pytest
```

### Python

Python constitue le langage principal de développement.

Il est utilisé pour :

- la logique métier ;
- l'API ;
- l'analyse des commandes ;
- le moteur de recommandation ;
- la gestion des sessions ;
- l'accès aux données ;
- les tests automatisés.

### Flask

Flask constitue le framework web principal.

Il assure notamment :

- la création de l'application ;
- le routage HTTP ;
- l'exposition des API ;
- la gestion des requêtes JSON ;
- la génération des réponses JSON ;
- l'enregistrement des blueprints.

### Flask-SQLAlchemy

Flask-SQLAlchemy assure l'intégration entre Flask et SQLAlchemy.

L'application initialise SQLAlchemy à l'aide de :

```python
db.init_app(app)
```

### PyMySQL

PyMySQL est utilisé comme connecteur Python vers MySQL.

### MySQL

MySQL constitue le système de gestion de base de données relationnelle utilisé pour la persistance des données du projet.

### pytest

`pytest` est utilisé pour les tests unitaires et les tests d'intégration.

---

## 3. Architecture applicative

L'application est organisée principalement autour des répertoires suivants :

```text
models/
controllers/
routes/
services/
config/
tests/
docs/
```

La séparation générale peut être représentée comme suit :

```text
Interface utilisateur
        ↓
Routes Flask
        ↓
Controllers
        ↓
Services
        ↓
SQLAlchemy
        ↓
MySQL
```

Cette organisation permet de séparer les responsabilités et de limiter le couplage entre les différentes couches.

---

## 4. Répertoire `models/`

Le répertoire `models/` contient les modèles SQLAlchemy représentant les principales tables de la base de données.

Les principales entités du projet sont :

```text
Utilisateur
Ville
Formateur
Campagne
SessionUtilisateur
Question
CategorieQuestion
Reponse
Recommandation
Parcours
Commande
Erreur
AuditLog
Evenement
```

Chaque modèle peut définir notamment :

- le nom de la table ;
- les colonnes ;
- la clé primaire ;
- les clés étrangères ;
- les contraintes ;
- les relations SQLAlchemy.

Exemple :

```python
class Utilisateur(db.Model):
    __tablename__ = "utilisateur"
```

---

## 5. Répertoire `controllers/`

Les contrôleurs centralisent les opérations métier et assurent l'orchestration entre les routes, les services et les modèles.

Les principaux contrôleurs comprennent notamment :

```text
CommandController
QuestionController
UtilisateurController
CampagneController
ErreurController
ReportController
DashboardController
SessionController
```

Le `CommandController` orchestre le traitement des commandes en faisant intervenir les différentes couches du pipeline.

---

## 6. Répertoire `routes/`

Le répertoire `routes/` contient les blueprints Flask exposant les fonctionnalités du backend.

Les blueprints sont enregistrés avec le préfixe :

```text
/api
```

Le système expose notamment des routes relatives à :

```text
/commands
/questions
/utilisateurs
/campagnes
/erreurs
/reports
/sessions
```

Les routes servent notamment à :

1. recevoir les requêtes du frontend ;
2. récupérer les données JSON ;
3. appeler les contrôleurs ;
4. retourner les résultats au format JSON.

---

## 7. Répertoire `services/`

Le répertoire `services/` contient les composants responsables de la logique applicative et technique.

Les principaux services comprennent notamment :

```text
CommandCorrector
Lexer
LL1Parser
CommandBuilder
CommandDispatcher
CommandHandler
RecommendationEngine
SessionManager
```

Cette organisation permet de séparer les services génériques ou métier des contrôleurs HTTP.

---

## 8. Configuration de l'application

Le point d'entrée principal est :

```text
app.py
```

L'application Flask est créée avec :

```python
app = Flask(__name__)
```

La configuration initialise notamment :

- JWT ;
- CORS ;
- SQLAlchemy ;
- les blueprints Flask.

SQLAlchemy est initialisé avec :

```python
db.init_app(app)
```

Les différentes routes sont ensuite enregistrées sous :

```text
/api
```

Exemple :

```python
app.register_blueprint(
    command_bp,
    url_prefix="/api"
)
```

Le projet utilise également :

```python
CORS(app)
```

afin de permettre les communications nécessaires entre le frontend et le backend.

---

## 9. Gestion de l'authentification

L'application utilise :

```text
Flask-JWT-Extended
```

pour la gestion des tokens JWT.

L'application initialise :

```python
jwt = JWTManager(app)
```

La configuration de sécurité est centralisée dans :

```text
config/security.py
```

La configuration comprend notamment la clé secrète JWT et la durée de validité des tokens.

---

## 10. Pipeline de traitement des commandes

Le moteur de commandes constitue un des composants techniques majeurs du système.

Le traitement suit le pipeline :

```text
Commande utilisateur
        ↓
CommandCorrector
        ↓
Lexer
        ↓
Parser LL(1)
        ↓
CommandBuilder
        ↓
CommandDispatcher
        ↓
CommandHandler
        ↓
Action métier
```

Chaque composant possède une responsabilité spécifique.

---

## 11. CommandCorrector

Le `CommandCorrector` analyse la commande avant son passage au Lexer.

Les principaux modes utilisés sont :

```text
VALID
AUTO_CORRECT
SUGGEST
REFORMULATE
```

### VALID

La commande est reconnue telle qu'elle a été saisie.

Exemple :

```text
AFFICHER STATISTIQUES
```

### AUTO_CORRECT

Une correction est appliquée automatiquement lorsque le niveau de confiance est suffisant.

Exemple :

```text
AFFICHER STATISTIQUESS
```

peut devenir :

```text
AFFICHER STATISTIQUES
```

### SUGGEST

Une correction est proposée à l'utilisateur avant la poursuite du traitement.

Exemple :

```text
AFFICHER STATISTIQ
```

peut produire :

```text
Voulez-vous dire :

AFFICHER STATISTIQUES ?

[ OUI ] [ NON ]
```

### REFORMULATE

Le système demande à l'utilisateur de reformuler la commande lorsque la correction automatique n'est pas suffisamment fiable.

---

## 12. Analyse lexicale

Le Lexer transforme le texte en tokens.

Il gère notamment :

- les mots réservés ;
- les numéros ;
- les espaces ;
- la casse ;
- `EOF` ;
- les mots inconnus ;
- les caractères invalides.

Exemple :

```text
MODIFIER QUESTION 25
```

est transformé conceptuellement en :

```text
MODIFIER
QUESTION
NUMERO
EOF
```

Le Lexer constitue la première étape de validation technique de la commande.

---

## 13. Analyse syntaxique LL(1)

Le Parser LL(1) vérifie que les tokens respectent la grammaire du système.

Le mécanisme s'appuie sur :

```text
Grammaire
FIRST
FOLLOW
EPSILON
EOF
Table LL(1)
Pile d'analyse
```

Le Parser :

- vérifie la table LL(1) ;
- utilise un token de lookahead ;
- sélectionne les productions ;
- détecte les erreurs syntaxiques ;
- utilise `FOLLOW` pour la récupération ;
- produit une trace détaillée.

---

## 14. CommandBuilder

Le `CommandBuilder` transforme les tokens validés en un objet `Command`.

Une commande structurée contient notamment :

```text
action
subject
arguments
tokens
raw
```

Exemple :

```text
MODIFIER QUESTION 3
```

est représenté conceptuellement par :

```text
action = MODIFIER
subject = QUESTION
arguments = {
    numero: 3
}
```

Le Builder ne réalise pas directement l'opération métier.

---

## 15. CommandDispatcher

Le `CommandDispatcher` détermine l'action métier correspondant à la commande.

Exemple :

```text
AFFICHER STATISTIQUES
```

est associé à :

```text
AFFICHER_STATISTIQUES
```

Le Dispatcher :

- récupère l'action ;
- cherche le handler correspondant ;
- gère les actions inconnues ;
- déclenche le handler approprié.

---

## 16. CommandHandler

Le `CommandHandler` réalise les traitements métier associés aux commandes.

Il peut notamment intervenir pour :

```text
AFFICHER STATISTIQUES
AFFICHER ERREURS
LANCER ENQUETE CYBERSECURITE
LANCER CAMPAGNE ECOLE
CHERCHER ENFANTS KINSHASA
CHERCHER ADOLESCENTS INTERESSES PAR PYTHON
AJOUTER QUESTION
MODIFIER QUESTION
SUPPRIMER QUESTION
EXPORTER RAPPORT
RECOMMENCER SESSION
QUITTER
```

Il s'appuie sur les contrôleurs ou services métier appropriés.

---

## 17. Moteur de recommandation

Le moteur de recommandation est implémenté dans :

```text
services/recommendation_engine.py
```

Son point d'entrée principal est :

```python
RecommendationEngine.generate(
    age,
    niveau_scolaire,
    reponses
)
```

Le moteur calcule les scores de cinq parcours :

```text
Découverte Numérique
Scratch Junior
Scratch Avancé
Python Débutant
Mentor Junior
```

Le résultat contient notamment :

```text
parcours
scores
score_final
```

Le moteur est déterministe et fait l'objet de tests automatisés.

---

## 18. Gestion des sessions

La gestion des sessions est centralisée dans :

```text
services/session_manager.py
```

Les principales opérations sont :

```text
create_session()
save_progress()
pause_session()
is_interrupted()
set_state()
resume_session()
update_inactivity()
get_session()
get_last_session()
restart_session()
get_interrupted_session()
can_resume()
restore_session()
finish_if_inactive()
close_session()
get_state()
```

Les états principaux utilisés sont :

```text
ACCUEIL
QUESTIONNAIRE
SESSION_INTERRUPTION
REPRISE_SESSION
FIN_SESSION
```

---

## 19. Gestion des erreurs

Le système prévoit plusieurs niveaux de gestion des erreurs :

```text
Erreur lexicale
Erreur syntaxique
Erreur de construction
Erreur d'exécution
Erreur de base de données
Commande inconnue
Données manquantes
```

Les résultats retournés par les couches concernées restent structurés afin de faciliter l'exploitation par le frontend et le diagnostic technique.

Les principales catégories d'erreurs utilisées dans le contrôleur de commandes sont notamment :

```text
LEXICAL_ERROR
SYNTAX_ERROR
BUILD_ERROR
EXECUTION_ERROR
DATABASE_ERROR
```

---

## 20. Persistance et transactions

Les opérations de persistance passent par :

```python
db.session
```

Une opération d'écriture suit généralement le principe :

```text
Création / modification
        ↓
db.session.add()
        ↓
db.session.commit()
```

En cas d'erreur :

```python
db.session.rollback()
```

peut être utilisé afin d'annuler la transaction en cours.

Cette approche permet de limiter les incohérences transactionnelles.

---

## 21. Contraintes de base de données

La base MySQL utilise plusieurs catégories de contraintes :

```text
PRIMARY KEY
FOREIGN KEY
NOT NULL
UNIQUE
CHECK
DEFAULT
INDEX
```

Des règles importantes sont appliquées directement au niveau de la base.

Exemples :

```text
age >= 0
ordre_question > 0
question_actuelle >= 0
temps_inactivite >= 0
score >= 0
```

Les violations de ces contraintes ont été testées volontairement et refusées par MySQL.

---

## 22. API principale de traitement des commandes

La route principale permettant d'exécuter une commande est :

```http
POST /api/commands/execute
```

Exemple de requête :

```json
{
    "command": "AFFICHER STATISTIQUES"
}
```

Le contrôleur reçoit ensuite la commande et orchestre le traitement complet.

La réponse JSON peut notamment contenir :

```text
success
mode
commande_id
original
corrected
suggestion
suggestions
execution
resultat
trace
```

Les champs présents dépendent du mode de traitement et du résultat de l'opération.

---

## 23. Interaction frontend / backend

Le frontend communique avec l'API Flask en utilisant des requêtes HTTP JSON.

Exemple :

```text
Frontend
   ↓
POST /api/commands/execute
   ↓
CommandController
   ↓
Traitement
   ↓
Réponse JSON
   ↓
Frontend
```

Le frontend exploite notamment le champ :

```text
mode
```

pour adapter l'interface.

Pour une suggestion, il peut afficher :

```text
Voulez-vous dire :

AFFICHER STATISTIQUES ?

[ OUI ] [ NON ]
```

Pour certaines commandes de gestion, la réponse du handler peut également déclencher un formulaire dynamique.

---

## 24. Structure générale du projet

La structure générale peut être représentée comme suit :

```text
ccc_orientation_system/
│
├── app.py
│
├── config/
│   ├── database.py
│   └── security.py
│
├── models/
│
├── controllers/
│
├── routes/
│
├── services/
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── docs/
│
├── pytest.ini
│
└── ...
```

### Responsabilités

| Répertoire | Responsabilité |
|---|---|
| `config/` | Configuration de l'application et sécurité |
| `models/` | Modèles SQLAlchemy |
| `controllers/` | Orchestration métier |
| `routes/` | API HTTP Flask |
| `services/` | Logique applicative et technique |
| `tests/` | Tests unitaires et d'intégration |
| `docs/` | Documentation du projet |

---

## 25. Organisation des tests

La suite officielle est organisée dans :

```text
tests/
├── unit/
│   ├── test_command_pipeline.py
│   ├── test_commands.py
│   ├── test_errors.py
│   ├── test_lexer.py
│   ├── test_ll1_table.py
│   ├── test_parser.py
│   ├── test_recommendation.py
│   └── test_sessions.py
│
└── integration/
    └── test_integration.py
```

La collecte officielle est configurée dans :

```text
pytest.ini
```

avec :

```ini
[pytest]
testpaths =
    tests/unit
    tests/integration

python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

Les anciens tests conservés dans les archives ne sont donc pas inclus dans la suite officielle.

---

## 26. Exécution de l'application

L'application peut être démarrée depuis :

```text
app.py
```

Commande typique :

```bash
python app.py
```

Dans le contexte de développement local, le backend Flask est alors accessible via l'adresse configurée par l'application.

---

## 27. Exécution des tests

### Suite complète

```bash
pytest -v
```

### Tests unitaires

```bash
pytest tests/unit -v
```

### Tests d'intégration

```bash
pytest tests/integration -v
```

La dernière exécution globale validée de la suite officielle a produit :

```text
224 passed
0 failed
0 errors
```

---

## 28. Environnement virtuel

Le projet est développé dans un environnement virtuel Python :

```text
.venv/
```

Sous Windows, l'activation peut être réalisée avec :

```bash
.venv\Scripts\activate
```

Les dépendances du projet doivent être installées dans cet environnement.

---

## 29. Maintenance technique

La suite de tests actuelle est fonctionnelle et entièrement validée, mais certaines bibliothèques signalent des API faisant l'objet de dépréciations futures.

Les principaux avertissements observés concernent notamment :

```text
Query.get()
datetime.utcnow()
```

Ces éléments pourront être modernisés progressivement.

Exemple de modernisation future de :

```python
SessionUtilisateur.query.get(session_id)
```

vers une API SQLAlchemy moderne basée sur :

```python
db.session.get(SessionUtilisateur, session_id)
```

Ces avertissements n'empêchent pas la suite officielle de réussir :

```text
224 passed
0 failed
0 errors
```

---

## 30. Principes de conception

L'architecture technique repose sur plusieurs principes.

### Séparation des responsabilités

Chaque couche possède un rôle distinct :

```text
Routes
   ↓
Controllers
   ↓
Services
   ↓
Models / Database
```

### Testabilité

Les composants peuvent être testés individuellement.

### Maintenabilité

La séparation entre les domaines facilite la modification du système.

### Traçabilité

Les commandes, erreurs et opérations importantes peuvent être suivies à travers les résultats et les traces.

### Évolutivité

L'architecture permet d'ajouter de nouveaux parcours, de nouvelles commandes et de nouvelles fonctionnalités avec un impact limité sur les autres composants.

---

## 31. Flux technique général

Pour une opération standard :

```text
Utilisateur
    ↓
Frontend / borne
    ↓
Requête HTTP JSON
    ↓
Route Flask
    ↓
Controller
    ↓
Service
    ↓
Model SQLAlchemy
    ↓
MySQL
    ↓
Résultat
    ↓
Controller
    ↓
Réponse JSON
    ↓
Frontend
```

Pour une commande :

```text
Utilisateur
    ↓
Frontend
    ↓
POST /api/commands/execute
    ↓
CommandController
    ↓
CommandCorrector
    ↓
Lexer
    ↓
Parser LL(1)
    ↓
CommandBuilder
    ↓
CommandDispatcher
    ↓
CommandHandler
    ↓
Contrôleur métier
    ↓
SQLAlchemy
    ↓
MySQL
    ↓
Réponse JSON
    ↓
Frontend
```

---

## 32. Validation technique finale

La validation automatisée du projet couvre actuellement :

```text
Analyse lexicale
Analyse syntaxique
Table LL(1)
Gestion des commandes
Pipeline de commandes
Moteur de recommandation
Gestion des sessions
Gestion des erreurs
Intégration API
Contraintes de base de données
```

La suite officielle a été exécutée avec succès :

```text
224 passed
0 failed
0 errors
```

Cette validation confirme que les principales couches techniques et leur intégration fonctionnent conformément aux tests définis dans le projet.

---

## 33. Conclusion

Le **CCC Orientation System** repose sur une architecture modulaire combinant :

```text
Python 3.12
+
Flask
+
Flask-SQLAlchemy
+
PyMySQL
+
MySQL
+
pytest
```

L'organisation en :

```text
models
controllers
routes
services
config
tests
docs
```

permet de séparer les responsabilités tout en conservant une communication structurée entre les différentes couches.

Le moteur de commandes ajoute une chaîne de traitement complète :

```text
Correction
    ↓
Analyse lexicale
    ↓
Analyse syntaxique LL(1)
    ↓
Construction
    ↓
Dispatching
    ↓
Exécution métier
```

L'ensemble est accompagné de tests automatisés et d'une documentation destinée à faciliter la maintenance, l'évolution du projet et sa présentation lors de la soutenance.