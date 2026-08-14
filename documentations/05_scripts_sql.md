# Scripts SQL et contraintes — CCC Orientation System

## 1. Présentation

La base de données du **CCC Orientation System** est basée sur **MySQL** et est manipulée par l'application à travers **SQLAlchemy / Flask-SQLAlchemy**.

Au-delà de la définition des tables et des relations, l'intégrité des données est renforcée directement au niveau du SGBD grâce à plusieurs types de contraintes.

L'objectif est de garantir qu'une donnée incorrecte ne puisse pas être enregistrée simplement parce qu'une validation applicative aurait été oubliée.

---

## 2. Types de contraintes utilisés

La base de données repose notamment sur les contraintes suivantes :

```text
PRIMARY KEY
FOREIGN KEY
NOT NULL
UNIQUE
CHECK
DEFAULT
INDEX
```

Chaque type de contrainte répond à un objectif précis dans le modèle relationnel.

---

## 3. PRIMARY KEY

La contrainte `PRIMARY KEY` permet d'identifier de manière unique chaque enregistrement d'une table.

Exemple :

```sql
CREATE TABLE utilisateur (
    id_utilisateur INT AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,

    PRIMARY KEY (id_utilisateur)
);
```

Dans le projet, les principales clés primaires sont notamment :

```text
id_utilisateur
id_ville
id_session
id_campagne
id_question
id_categorie
id_reponse
id_recommandation
id_parcours
id_formateur
id_commande
id_erreur
id_audit
id_evenement
```

---

## 4. FOREIGN KEY

Les clés étrangères assurent les relations entre les différentes tables et garantissent l'intégrité référentielle.

Exemples :

```sql
FOREIGN KEY (id_ville)
    REFERENCES ville(id_ville)
```

```sql
FOREIGN KEY (id_utilisateur)
    REFERENCES utilisateur(id_utilisateur)
```

```sql
FOREIGN KEY (id_campagne)
    REFERENCES campagne(id_campagne)
```

```sql
FOREIGN KEY (id_categorie)
    REFERENCES categorie_question(id_categorie)
```

```sql
FOREIGN KEY (id_session)
    REFERENCES session_utilisateur(id_session)
```

```sql
FOREIGN KEY (id_question)
    REFERENCES question(id_question)
```

```sql
FOREIGN KEY (id_parcours)
    REFERENCES parcours(id_parcours)
```

```sql
FOREIGN KEY (id_formateur)
    REFERENCES formateur(id_formateur)
```

Ces contraintes empêchent notamment de créer des références vers des enregistrements inexistants.

---

## 5. NOT NULL

La contrainte `NOT NULL` permet de rendre certaines informations obligatoires.

Exemples :

```sql
nom VARCHAR(100) NOT NULL
```

```sql
prenom VARCHAR(100) NOT NULL
```

```sql
age INT NOT NULL
```

```sql
texte_question TEXT NOT NULL
```

```sql
ordre_question INT NOT NULL
```

```sql
email VARCHAR(150) NOT NULL
```

Une tentative d'insertion avec une valeur `NULL` sur une colonne obligatoire est alors refusée par le SGBD.

---

## 6. UNIQUE

La contrainte `UNIQUE` empêche l'enregistrement de doublons lorsqu'une valeur doit être unique.

### Ville

```sql
UNIQUE (nom_ville)
```

Le nom d'une ville ne doit pas être dupliqué.

### Email du formateur

```sql
UNIQUE (email)
```

Deux formateurs ne peuvent pas utiliser la même adresse email.

### Recommandation

Le modèle prévoit également une unicité sur :

```sql
UNIQUE (id_session)
```

pour éviter plusieurs recommandations associées à une même session lorsque le modèle métier impose une recommandation unique par session.

---

## 7. CHECK

Les contraintes `CHECK` permettent d'imposer directement certaines règles de validité au niveau de MySQL.

Elles sont particulièrement importantes dans le CCC Orientation System car elles permettent à la base de données de refuser elle-même certaines valeurs incorrectes.

---

### 7.1. Contrôle de l'âge

L'âge d'un utilisateur doit être supérieur ou égal à zéro.

```sql
CONSTRAINT ck_utilisateur_age_positif
    CHECK (age >= 0)
```

Ainsi, une valeur telle que :

```text
-5
```

doit être refusée directement par MySQL.

---

### 7.2. Contrôle de l'ordre d'une question

L'ordre d'une question doit être positif.

```sql
CONSTRAINT ck_question_ordre_positif
    CHECK (ordre_question > 0)
```

Une valeur telle que :

```text
-1
```

doit donc être rejetée.

---

### 7.3. Contrôle de la question actuelle d'une session

La position courante dans le questionnaire ne doit pas être négative.

```sql
CONSTRAINT ck_session_question_positive
    CHECK (question_actuelle >= 0)
```

---

### 7.4. Contrôle du temps d'inactivité

Le temps d'inactivité ne peut pas être négatif.

```sql
CONSTRAINT ck_session_inactivite_positive
    CHECK (temps_inactivite >= 0)
```

---

### 7.5. Contrôle du score

Le score d'une recommandation doit rester supérieur ou égal à zéro.

```sql
CONSTRAINT ck_recommandation_score_positif
    CHECK (score >= 0)
```

---

## 8. DEFAULT

La contrainte `DEFAULT` permet d'attribuer automatiquement une valeur lorsqu'aucune valeur explicite n'est fournie.

Exemples :

```sql
date_creation DATETIME DEFAULT CURRENT_TIMESTAMP
```

```sql
date_execution DATETIME DEFAULT CURRENT_TIMESTAMP
```

```sql
sauvegardee BOOLEAN DEFAULT FALSE
```

```sql
question_actuelle INT DEFAULT 0
```

```sql
temps_inactivite INT DEFAULT 0
```

```sql
active BOOLEAN DEFAULT TRUE
```

Ces valeurs permettent d'initialiser automatiquement certains champs.

---

## 9. INDEX

Les index permettent d'améliorer les performances des recherches et des jointures fréquemment utilisées.

Exemples :

```sql
INDEX idx_utilisateur_ville (id_ville)
```

```sql
INDEX idx_session_utilisateur (id_utilisateur)
```

```sql
INDEX idx_session_campagne (id_campagne)
```

```sql
INDEX idx_question_categorie (id_categorie)
```

```sql
INDEX idx_recommandation_parcours (id_parcours)
```

L'indexation doit rester adaptée aux besoins réels d'accès aux données.

---

# 10. Exemple de définition SQL — Utilisateur

Voici un exemple de définition SQL correspondant à l'entité `Utilisateur` :

```sql
CREATE TABLE utilisateur (
    id_utilisateur INT AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    niveau_scolaire VARCHAR(30) NOT NULL,
    type_profil VARCHAR(30) NOT NULL,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_ville INT,

    PRIMARY KEY (id_utilisateur),

    FOREIGN KEY (id_ville)
        REFERENCES ville(id_ville),

    CONSTRAINT ck_utilisateur_age_positif
        CHECK (age >= 0),

    INDEX idx_utilisateur_ville (id_ville)
);
```

Cette définition met en œuvre :

```text
PRIMARY KEY
FOREIGN KEY
NOT NULL
CHECK
DEFAULT
INDEX
```

---

# 11. Exemple de définition SQL — Question

La table `question` peut être définie comme suit :

```sql
CREATE TABLE question (
    id_question INT AUTO_INCREMENT,
    texte_question TEXT NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    ordre_question INT NOT NULL,
    id_categorie INT,

    PRIMARY KEY (id_question),

    FOREIGN KEY (id_categorie)
        REFERENCES categorie_question(id_categorie),

    CONSTRAINT ck_question_ordre_positif
        CHECK (ordre_question > 0),

    INDEX idx_question_categorie (id_categorie)
);
```

Cette définition permet notamment de garantir :

```text
texte_question obligatoire
ordre_question positif
categorie valide
id_question unique
```

---

# 12. Exemple de définition SQL — SessionUtilisateur

La table `session_utilisateur` peut être définie comme suit :

```sql
CREATE TABLE session_utilisateur (
    id_session INT AUTO_INCREMENT,
    date_debut DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_fin DATETIME,
    etat VARCHAR(50),
    sauvegardee BOOLEAN DEFAULT FALSE,
    question_actuelle INT DEFAULT 0,
    temps_inactivite INT DEFAULT 0,
    id_utilisateur INT,
    id_campagne INT,

    PRIMARY KEY (id_session),

    FOREIGN KEY (id_utilisateur)
        REFERENCES utilisateur(id_utilisateur),

    FOREIGN KEY (id_campagne)
        REFERENCES campagne(id_campagne),

    CONSTRAINT ck_session_question_positive
        CHECK (question_actuelle >= 0),

    CONSTRAINT ck_session_inactivite_positive
        CHECK (temps_inactivite >= 0),

    INDEX idx_session_utilisateur (id_utilisateur),
    INDEX idx_session_campagne (id_campagne)
);
```

Les principales protections sont :

```text
PRIMARY KEY
FOREIGN KEY
CHECK
DEFAULT
INDEX
```

---

# 13. Exemple de définition SQL — Recommandation

La table `recommandation` peut être définie comme suit :

```sql
CREATE TABLE recommandation (
    id_recommandation INT AUTO_INCREMENT,
    score FLOAT,
    profil_detecte VARCHAR(100),
    commentaire TEXT,
    date_generation DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_session INT UNIQUE,
    id_parcours INT,

    PRIMARY KEY (id_recommandation),

    FOREIGN KEY (id_session)
        REFERENCES session_utilisateur(id_session),

    FOREIGN KEY (id_parcours)
        REFERENCES parcours(id_parcours),

    CONSTRAINT ck_recommandation_score_positif
        CHECK (score >= 0),

    INDEX idx_recommandation_parcours (id_parcours)
);
```

La contrainte :

```sql
UNIQUE (id_session)
```

permet notamment d'assurer qu'une session ne possède qu'une recommandation lorsque cette règle est requise par le modèle.

---

# 14. Test volontaire des contraintes

Une partie importante de la validation consiste à tenter volontairement d'enregistrer des données invalides.

L'objectif est de vérifier que les contraintes sont réellement appliquées par MySQL.

---

## 14.1. Test : âge négatif

Exemple :

```sql
INSERT INTO utilisateur (
    nom,
    prenom,
    age,
    niveau_scolaire,
    type_profil
)
VALUES (
    'TEST',
    'AGE',
    -5,
    'TEST',
    'TEST'
);
```

Résultat attendu :

```text
INSERTION REFUSÉE
```

La contrainte concernée est :

```text
ck_utilisateur_age_positif
```

---

## 14.2. Test : ordre de question invalide

Exemple :

```sql
INSERT INTO question (
    texte_question,
    ordre_question
)
VALUES (
    'Question invalide',
    -1
);
```

Résultat attendu :

```text
INSERTION REFUSÉE
```

La contrainte concernée est :

```text
ck_question_ordre_positif
```

---

## 14.3. Test : question actuelle négative

Exemple :

```sql
UPDATE session_utilisateur
SET question_actuelle = -1
WHERE id_session = 1;
```

Résultat attendu :

```text
MISE À JOUR REFUSÉE
```

La contrainte concernée est :

```text
ck_session_question_positive
```

---

## 14.4. Test : temps d'inactivité négatif

Exemple :

```sql
UPDATE session_utilisateur
SET temps_inactivite = -20
WHERE id_session = 1;
```

Résultat attendu :

```text
MISE À JOUR REFUSÉE
```

La contrainte concernée est :

```text
ck_session_inactivite_positive
```

---

## 14.5. Test : catégorie inexistante

Exemple :

```sql
INSERT INTO question (
    texte_question,
    ordre_question,
    id_categorie
)
VALUES (
    'Question test',
    1,
    999999
);
```

Si la catégorie `999999` n'existe pas, la clé étrangère doit empêcher l'insertion.

Résultat attendu :

```text
INSERTION REFUSÉE
```

---

## 14.6. Test : doublon de ville

Exemple :

```sql
INSERT INTO ville (
    nom_ville
)
VALUES (
    'Kinshasa'
);
```

Si `Kinshasa` existe déjà et que `nom_ville` est défini comme `UNIQUE`, une nouvelle insertion identique doit être refusée.

Résultat attendu :

```text
INSERTION REFUSÉE
```

---

## 14.7. Test : doublon d'email

Exemple :

```sql
INSERT INTO formateur (
    nom,
    email,
    mot_de_passe
)
VALUES (
    'Formateur Test',
    'test@example.com',
    'password'
);
```

Une deuxième insertion avec le même email doit être refusée.

Résultat attendu :

```text
INSERTION REFUSÉE
```

---

# 15. Tests automatisés des contraintes

Les contraintes de la base ont été vérifiées avec des tests automatisés.

Les scénarios validés comprennent notamment :

```text
PASS : CHECK AGE >= 0
PASS : CHECK ORDRE QUESTION
PASS : CHECK SESSION QUESTION
PASS : CHECK TEMPS INACTIVITE
PASS : NOT NULL QUESTION
PASS : UNIQUE VILLE
PASS : UNIQUE FORMATEUR EMAIL
PASS : FOREIGN KEY QUESTION → CATEGORIE
```

Ces tests vérifient que les violations sont bien rejetées par le SGBD.

---

# 16. Validation au niveau de l'application et de la base

Le système applique une stratégie de défense en profondeur.

La validation applicative peut intervenir avant l'accès à la base :

```text
Donnée saisie
     ↓
Validation Python
     ↓
SQLAlchemy
     ↓
MySQL
```

Mais MySQL constitue également une barrière indépendante :

```text
Application
     ↓
SQLAlchemy
     ↓
Contraintes MySQL
     ↓
Donnée acceptée ou refusée
```

Ainsi, une donnée incorrecte ne dépend pas uniquement du comportement du code Python pour être rejetée.

---

# 17. Résumé des contraintes

| Contrainte | Exemple | Fonction |
|---|---|---|
| `PRIMARY KEY` | `id_utilisateur` | Identifie chaque enregistrement |
| `FOREIGN KEY` | `id_categorie` | Garantit l'intégrité référentielle |
| `NOT NULL` | `texte_question` | Rend une valeur obligatoire |
| `UNIQUE` | `email` | Empêche les doublons |
| `CHECK` | `age >= 0` | Impose une règle de validité |
| `DEFAULT` | `question_actuelle = 0` | Définit une valeur initiale |
| `INDEX` | `id_utilisateur` | Optimise les recherches |

---

# 18. Correspondance avec SQLAlchemy

Les contraintes sont également représentées dans les modèles SQLAlchemy.

Exemple :

```python
age = db.Column(
    db.Integer,
    nullable=False
)
```

Une contrainte peut également être explicitement déclarée dans un modèle avec `CheckConstraint`.

Exemple :

```python
__table_args__ = (
    db.CheckConstraint(
        "age >= 0",
        name="ck_utilisateur_age_positif"
    ),
)
```

La définition dans le modèle doit rester cohérente avec la structure effective de la base MySQL.

---

# 19. Principe de défense en profondeur

La stratégie retenue est :

```text
┌─────────────────────────────┐
│ Validation frontend         │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ Validation applicative      │
│ Python / Flask              │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ SQLAlchemy                  │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ Contraintes MySQL           │
└──────────────┬──────────────┘
               ↓
        Donnée persistée
```

Chaque niveau constitue une protection supplémentaire.

---

# 20. Conclusion

Le renforcement SQL du **CCC Orientation System** permet de déplacer une partie importante des garanties d'intégrité directement au niveau de la base de données.

Les contraintes utilisées sont :

```text
PRIMARY KEY
FOREIGN KEY
NOT NULL
UNIQUE
CHECK
DEFAULT
INDEX
```

Les règles critiques telles que :

```text
age >= 0
ordre_question > 0
question_actuelle >= 0
temps_inactivite >= 0
score >= 0
```

sont ainsi protégées au niveau du SGBD.

Les violations ont été testées volontairement et refusées par MySQL.

Cette approche garantit que l'intégrité des données ne dépend pas uniquement de la validation effectuée dans le code Python et constitue une composante essentielle de la robustesse du **CCC Orientation System**.