# Soutenance — CCC Orientation System

## 1. Objectif de la démonstration

La soutenance doit montrer que le **CCC Orientation System** fonctionne comme un système complet, depuis la saisie d'une commande jusqu'à son traitement métier, sa persistance et sa validation par les tests.

Les principaux points à démontrer sont :

```text
Architecture générale
Analyse lexicale
Grammaire et Parser LL(1)
Correction automatique
Suggestion / confirmation
Exécution des commandes
Moteur de recommandation
Gestion des sessions
Contraintes MySQL
Tests automatisés
```

---

## 2. Ordre recommandé de la démonstration

### 1. Présentation rapide

Présenter en quelques phrases :

- l'objectif du système ;
- le problème traité ;
- les principales technologies ;
- l'architecture générale.

Architecture à rappeler :

```text
Interface
   ↓
API Flask
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
Services / Controllers
   ↓
SQLAlchemy / MySQL
```

---

### 2. Démonstration d'une commande valide

Saisir :

```text
AFFICHER STATISTIQUES
```

Montrer que :

```text
Commande
   ↓
VALID
   ↓
Lexer
   ↓
Parser LL(1)
   ↓
Builder
   ↓
Dispatcher
   ↓
Handler
   ↓
Résultat
```

Présenter la réponse retournée par l'API et, si pertinent, la trace du traitement.

---

### 3. Démonstration `AUTO_CORRECT`

Saisir volontairement une faute proche d'une commande valide :

```text
AFFICHER STATISTIQUESS
```

Montrer que le système détecte et corrige la commande :

```text
AFFICHER STATISTIQUESS
        ↓
AUTO_CORRECT
        ↓
AFFICHER STATISTIQUES
```

Puis montrer que la commande corrigée poursuit le pipeline normal.

---

### 4. Démonstration `SUGGEST`

Saisir :

```text
AFFICHER STATISTIQ
```

Le système doit proposer :

```text
Voulez-vous dire :

AFFICHER STATISTIQUES ?

[ OUI ] [ NON ]
```

Montrer ensuite le comportement des deux choix :

```text
OUI
→ confirmation
→ poursuite du traitement
```

```text
NON
→ suggestion refusée
→ nouvelle saisie
```

Insister sur le fait qu'une suggestion n'est pas exécutée automatiquement.

---

### 5. Démonstration `MODIFIER` / `SUPPRIMER`

Tester :

```text
MODIFIER QUESTION 3
```

Montrer :

```text
Commande
   ↓
Parsing
   ↓
Identification du numéro
   ↓
Handler
   ↓
Formulaire / traitement métier
```

Puis :

```text
SUPPRIMER QUESTION 25
```

Montrer que le numéro est correctement identifié et que l'opération correspondante est déclenchée.

---

### 6. Démonstration du moteur de recommandation

Présenter le fonctionnement de :

```python
RecommendationEngine.generate(
    age,
    niveau_scolaire,
    reponses
)
```

Montrer que les scores sont calculés pour :

```text
Découverte Numérique
Scratch Junior
Scratch Avancé
Python Débutant
Mentor Junior
```

Puis présenter :

```text
parcours
scores
score_final
```

Expliquer brièvement que les scores combinent :

```text
Âge
+
Niveau scolaire
+
Réponses
```

---

### 7. Démonstration de la gestion des sessions

Présenter le cycle :

```text
ACCUEIL
   ↓
QUESTIONNAIRE
   ↓
SESSION_INTERRUPTION
   ↓
REPRISE_SESSION
   ↓
QUESTIONNAIRE
   ↓
FIN_SESSION
```

Montrer notamment :

```text
sauvegarde de progression
question actuelle
temps d'inactivité
reprise
redémarrage
fermeture
```

La commande :

```text
RECOMMENCER SESSION
```

peut servir de démonstration du redémarrage.

---

### 8. Démonstration des contraintes de base de données

Présenter une violation volontaire.

Exemple :

```text
age = -5
```

Montrer que l'insertion est refusée directement par MySQL grâce à :

```sql
CHECK (age >= 0)
```

Présenter également quelques contraintes importantes :

```text
PRIMARY KEY
FOREIGN KEY
NOT NULL
UNIQUE
CHECK
DEFAULT
INDEX
```

Exemples de contrôles déjà validés :

```text
age >= 0
ordre_question > 0
question_actuelle >= 0
temps_inactivite >= 0
```

L'objectif est de montrer que l'intégrité ne dépend pas uniquement de Python.

---

### 9. Lancement de la suite de tests

Terminer la démonstration par :

```bash
pytest -v
```

Présenter le résultat final :

```text
224 passed
0 failed
0 errors
64 warnings
```

Expliquer que les tests couvrent notamment :

```text
Lexer
Parser
Table LL(1)
Commandes
Pipeline
Erreurs
Recommandation
Sessions
Intégration
Base de données
```

---

## 3. Scénario de démonstration complet

Le scénario recommandé devant le jury peut être :

```text
1. Présentation du système
        ↓
2. AFFICHER STATISTIQUES
        ↓
3. AFFICHER STATISTIQUESS
        ↓
4. AFFICHER STATISTIQ
        ↓
5. MODIFIER QUESTION 3
        ↓
6. SUPPRIMER QUESTION 25
        ↓
7. Démonstration recommandation
        ↓
8. Démonstration session
        ↓
9. Violation SQL
        ↓
10. pytest -v
```

---

## 4. Points techniques à expliquer au jury

### Architecture

Chaque couche possède une responsabilité distincte.

### Lexer

Il transforme le texte en tokens et détecte les erreurs lexicales.

### Parser LL(1)

Il vérifie la structure selon la grammaire et utilise la table LL(1).

### Correcteur

Il distingue :

```text
VALID
AUTO_CORRECT
SUGGEST
REFORMULATE
```

### Dispatcher / Handler

Ils assurent l'association entre une commande reconnue et son traitement métier.

### Base de données

MySQL assure une dernière couche d'intégrité grâce aux contraintes SQL.

### Tests

Les tests automatisés vérifient séparément les composants et leur intégration.

---

## 5. Réponses courtes aux questions probables du jury

### Pourquoi utiliser un Parser LL(1) ?

Pour analyser les commandes de manière déterministe avec un seul token de lookahead.

### Pourquoi FIRST et FOLLOW ?

Ils permettent notamment de construire la table LL(1) et de déterminer les productions utilisables.

### Pourquoi un Lexer séparé ?

Pour isoler la reconnaissance des tokens de l'analyse syntaxique.

### Pourquoi un Corrector avant le Lexer ?

Pour corriger ou proposer une interprétation avant l'analyse syntaxique lorsque la saisie comporte une faute.

### Pourquoi MySQL impose-t-il aussi des contraintes ?

Pour garantir l'intégrité des données même si une validation applicative est contournée ou oubliée.

### Pourquoi automatiser les tests ?

Pour vérifier de manière reproductible les composants et prévenir les régressions.

---

## 6. Résultat attendu de la soutenance

À la fin de la démonstration, le jury doit pouvoir constater que le système possède :

```text
Une architecture structurée
Un langage de commandes formalisé
Un Lexer fonctionnel
Un Parser LL(1)
Une correction intelligente
Une interaction SUGGEST OUI/NON
Un moteur de recommandation
Une gestion des sessions
Une base MySQL protégée
Une suite de tests automatisés
```

Le résultat de référence est :

```text
224 tests passés
0 échec
0 erreur
```

Le **CCC Orientation System** peut ainsi être présenté comme une solution complète, testée et structurée, combinant traitement du langage de commandes, logique métier, gestion des sessions, recommandation et persistance sécurisée.