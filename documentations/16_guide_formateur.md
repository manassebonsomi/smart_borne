# Guide formateur — CCC Orientation System

## 1. Présentation

Le **CCC Orientation System** met à la disposition du formateur une interface de supervision et de gestion permettant d'interagir avec les principaux modules du système à travers un ensemble de commandes contrôlées.

Le formateur peut notamment :

- consulter les statistiques ;
- consulter les erreurs ;
- gérer les questions ;
- lancer des enquêtes ;
- lancer des campagnes ;
- effectuer certaines recherches ;
- exporter des rapports ;
- gérer les sessions.

Les commandes de gestion suivent obligatoirement le pipeline de validation du système avant toute exécution métier.

---

## 2. Rôle du formateur

Le formateur constitue un utilisateur habilité à superviser et à administrer certaines opérations du système.

Ses principales responsabilités peuvent notamment concerner :

```text
Supervision
    ↓
Consultation
    ↓
Gestion des contenus
    ↓
Lancement des opérations
    ↓
Recherche
    ↓
Production de rapports
    ↓
Gestion des sessions
```

Les opérations disponibles dépendent des commandes définies et implémentées dans le système.

---

## 3. Principe de fonctionnement des commandes

Une commande saisie par le formateur ne doit pas être exécutée directement.

Elle passe par le pipeline :

```text
Commande du formateur
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
Base de données / service
```

Cette architecture permet de contrôler la syntaxe et la structure de la commande avant son exécution.

---

## 4. Validation syntaxique obligatoire

Toutes les commandes de gestion doivent respecter la grammaire définie par le système.

Le processus est :

```text
Saisie
  ↓
Correction éventuelle
  ↓
Analyse lexicale
  ↓
Validation syntaxique LL(1)
  ↓
Construction de la commande
  ↓
Exécution
```

Une commande syntaxiquement invalide est arrêtée avant l'exécution métier.

Exemple :

```text
AFFICHER
```

n'est pas une commande complète, car le système attend un sujet après `AFFICHER`.

---

## 5. Consulter les statistiques

Le formateur peut utiliser :

```text
AFFICHER STATISTIQUES
```

Cette commande permet d'accéder aux statistiques fournies par le module de statistiques.

Le traitement suit :

```text
AFFICHER STATISTIQUES
        ↓
Validation
        ↓
DashboardController
        ↓
Statistiques
```

Les résultats retournés peuvent notamment être utilisés pour suivre l'activité du système.

---

## 6. Consulter les erreurs

Le formateur peut consulter les erreurs avec :

```text
AFFICHER ERREURS
```

Cette commande permet d'accéder aux erreurs enregistrées par le système.

Les informations peuvent notamment comprendre :

- identifiant ;
- type d'erreur ;
- message ;
- état de correction ;
- date d'enregistrement.

Cette fonctionnalité est particulièrement utile pour le suivi et le diagnostic.

---

## 7. Gestion des questions

Le formateur peut gérer les questions du questionnaire.

Les principales opérations sont :

```text
AJOUTER QUESTION
MODIFIER QUESTION 3
SUPPRIMER QUESTION 25
```

Les numéros utilisés dans les exemples sont indicatifs.

---

## 8. Ajouter une question

Pour démarrer l'ajout d'une question :

```text
AJOUTER QUESTION
```

La commande est d'abord validée par le pipeline.

Après validation, le système peut demander les informations complémentaires nécessaires.

Le frontend peut afficher un formulaire dynamique comprenant notamment :

```text
Texte de la question
Ordre de la question
Catégorie
```

Le formateur complète ensuite les informations et valide l'enregistrement.

---

## 9. Modifier une question

Pour modifier une question :

```text
MODIFIER QUESTION 3
```

Le nombre :

```text
3
```

désigne la question concernée.

Après validation de la commande, le système peut présenter un formulaire de modification permettant notamment de renseigner :

```text
Nouveau texte
Nouvel ordre
Statut actif
```

Le formateur valide ensuite la modification.

---

## 10. Supprimer une question

Pour supprimer une question :

```text
SUPPRIMER QUESTION 25
```

Le système identifie la question numéro `25`.

Selon l'interface et le comportement applicatif prévu, une confirmation supplémentaire peut être demandée avant l'exécution de l'opération.

Le formateur doit vérifier le numéro avant de confirmer une suppression.

---

## 11. Lancer une enquête

Le formateur peut lancer une enquête à l'aide de :

```text
LANCER ENQUETE CYBERSECURITE
```

Le système :

1. vérifie la commande ;
2. analyse sa syntaxe ;
3. construit la commande ;
4. identifie l'action correspondante ;
5. exécute le traitement métier.

---

## 12. Lancer une campagne scolaire

La commande :

```text
LANCER CAMPAGNE ECOLE
```

permet de déclencher l'opération associée à une campagne scolaire.

Le système peut retourner les informations relatives à la campagne créée ou à son état d'exécution.

---

## 13. Effectuer des recherches

Le formateur peut utiliser les recherches prévues par le système.

### Recherche des enfants à Kinshasa

```text
CHERCHER ENFANTS KINSHASA
```

### Recherche des adolescents intéressés par Python

```text
CHERCHER ADOLESCENTS INTERESSES PAR PYTHON
```

Ces commandes sont traitées par le système selon les critères métier associés.

---

## 14. Exporter un rapport

Le formateur peut générer un rapport avec :

```text
EXPORTER RAPPORT
```

Le système valide la commande puis appelle le traitement d'export correspondant.

Lorsque l'opération réussit, les informations relatives au rapport généré peuvent être retournées au formateur.

---

## 15. Gestion des sessions

Le formateur peut également intervenir sur les commandes de session prévues par le système.

La commande actuellement couverte par le langage de commandes est notamment :

```text
RECOMMENCER SESSION
```

Cette opération permet de réinitialiser une session conformément aux règles de gestion du `SessionManager`.

---

## 16. Terminer une session

La commande :

```text
QUITTER
```

permet de terminer la session courante.

Le système peut alors enregistrer la fin de la session et positionner son état sur :

```text
FIN_SESSION
```

---

## 17. Correction automatique des commandes

Le système peut détecter certaines erreurs de saisie et appliquer automatiquement une correction.

Exemple :

```text
AFFICHER STATISTIQUESS
```

peut être corrigé vers :

```text
AFFICHER STATISTIQUES
```

Le mode correspondant est :

```text
AUTO_CORRECT
```

Lorsque la correction est suffisamment fiable, le traitement peut se poursuivre automatiquement.

---

## 18. Suggestion de commande

Lorsque le système identifie une correction possible mais demande l'accord du formateur, il utilise le mode :

```text
SUGGEST
```

Exemple :

```text
AFFICHER STATISTIQ
```

L'interface peut afficher :

```text
Voulez-vous dire :

AFFICHER STATISTIQUES ?

[ OUI ] [ NON ]
```

### Si le formateur choisit OUI

La commande proposée est confirmée et poursuit le pipeline.

### Si le formateur choisit NON

La suggestion est rejetée et le formateur peut saisir une nouvelle commande.

---

## 19. Reformulation

Lorsque le système ne peut pas déterminer suffisamment clairement l'intention du formateur, il peut demander une reformulation.

Le mode est alors :

```text
REFORMULATE
```

Le formateur doit saisir une commande plus claire.

La commande concernée n'est pas exécutée tant qu'elle n'a pas été correctement comprise.

---

## 20. Gestion des erreurs

Le système peut retourner différents types d'erreurs :

```text
LEXICAL_ERROR
SYNTAX_ERROR
BUILD_ERROR
EXECUTION_ERROR
DATABASE_ERROR
```

Le formateur doit consulter le message retourné afin de déterminer l'action à entreprendre.

### Exemple

Une commande incomplète :

```text
MODIFIER QUESTION
```

peut être rejetée car le numéro de la question est absent.

---

## 21. Consultation de l'historique

Les commandes peuvent être conservées dans l'historique du système.

L'historique peut notamment présenter :

```text
ID
Texte de la commande
Tokens
Résultat
Validité
Date d'exécution
```

Cela permet au formateur de suivre les opérations précédemment effectuées.

---

## 22. Traçabilité

Le système produit des informations de trace lors du traitement des commandes.

Ces traces permettent notamment de suivre :

```text
Commande reçue
      ↓
Normalisation
      ↓
Correction
      ↓
Tokenisation
      ↓
Parsing
      ↓
Construction
      ↓
Dispatching
      ↓
Exécution
```

La traçabilité facilite le diagnostic en cas de problème.

---

## 23. Bonnes pratiques pour le formateur

Le formateur doit notamment :

- vérifier la commande avant son exécution ;
- vérifier les numéros de questions ;
- lire les suggestions proposées ;
- confirmer uniquement les suggestions correspondant à son intention ;
- vérifier les résultats après les opérations importantes ;
- utiliser les fonctions de consultation des erreurs en cas de problème ;
- éviter d'utiliser une commande non prévue par la grammaire.

---

## 24. Commandes principales du formateur

Les commandes actuellement couvertes par le système comprennent :

```text
AFFICHER STATISTIQUES
AFFICHER ERREURS

LANCER ENQUETE CYBERSECURITE
LANCER CAMPAGNE ECOLE

CHERCHER ENFANTS KINSHASA
CHERCHER ADOLESCENTS INTERESSES PAR PYTHON

AJOUTER QUESTION
MODIFIER QUESTION 3
SUPPRIMER QUESTION 25

EXPORTER RAPPORT

RECOMMENCER SESSION
QUITTER
```

Le numéro utilisé dans `MODIFIER QUESTION` et `SUPPRIMER QUESTION` doit être remplacé par le numéro réel concerné.

---

## 25. Exemple de séance de supervision

Une séance de travail du formateur peut suivre le scénario :

### Étape 1 — consulter les statistiques

```text
AFFICHER STATISTIQUES
```

### Étape 2 — consulter les erreurs

```text
AFFICHER ERREURS
```

### Étape 3 — rechercher un groupe

```text
CHERCHER ENFANTS KINSHASA
```

ou :

```text
CHERCHER ADOLESCENTS INTERESSES PAR PYTHON
```

### Étape 4 — gérer les questions

```text
MODIFIER QUESTION 3
```

ou :

```text
AJOUTER QUESTION
```

### Étape 5 — produire un rapport

```text
EXPORTER RAPPORT
```

### Étape 6 — terminer

```text
QUITTER
```

---

## 26. Relation avec les composants techniques

Les commandes du formateur sont prises en charge par plusieurs couches techniques :

```text
Formateur
    ↓
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
Contrôleur métier
    ↓
SQLAlchemy / MySQL
```

Chaque commande est donc soumise au même mécanisme de contrôle avant d'atteindre la logique métier.

---

## 27. Sécurité et contrôle

La validation syntaxique constitue une première barrière de contrôle.

Le système ne doit pas passer directement d'une saisie utilisateur à une opération métier.

Le traitement respecte :

```text
Saisie
  ↓
Validation
  ↓
Interprétation
  ↓
Exécution
```

Cette organisation réduit les risques d'exécuter une commande dont la structure n'est pas reconnue par la grammaire.

Les mécanismes d'authentification et d'autorisation du backend complètent ce contrôle.

---

## 28. Tests associés

Les fonctionnalités de commandes sont couvertes par des tests automatisés.

La suite officielle vérifie notamment :

- commandes valides ;
- correction automatique ;
- suggestions ;
- reformulations ;
- construction ;
- dispatching ;
- handlers ;
- numéros de questions ;
- casse ;
- traces ;
- intégration complète.

La dernière suite globale validée a produit :

```text
224 passed
0 failed
0 errors
```

---

## 29. Résumé

Le **Guide formateur** repose sur le principe suivant :

```text
Le formateur saisit une commande
        ↓
Le système la corrige si nécessaire
        ↓
Le Lexer analyse les tokens
        ↓
Le Parser LL(1) vérifie la syntaxe
        ↓
Le Builder construit la commande
        ↓
Le Dispatcher sélectionne l'action
        ↓
Le Handler exécute l'opération
        ↓
Le résultat est retourné au formateur
```

Le formateur dispose ainsi d'un ensemble de commandes permettant la supervision et la gestion du système :

```text
Statistiques
Erreurs
Questions
Enquêtes
Campagnes
Recherches
Rapports
Sessions
```

Les commandes de gestion passent obligatoirement par le mécanisme de validation du système avant toute exécution métier, ce qui garantit une interaction structurée et cohérente avec le **CCC Orientation System**.