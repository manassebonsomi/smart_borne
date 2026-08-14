# Guide utilisateur — CCC Orientation System

## 1. Présentation

Le **CCC Orientation System** fournit une interface permettant à l'utilisateur d'interagir avec le système à travers des commandes textuelles.

L'utilisateur peut saisir une commande, l'envoyer au système et consulter immédiatement le résultat du traitement.

Le système analyse la commande, vérifie sa validité et, lorsque cela est nécessaire, propose automatiquement une correction, une suggestion ou une reformulation.

L'objectif de ce guide est de présenter de manière simple les principales possibilités offertes à l'utilisateur et la manière d'interagir avec le système.

---

## 2. Accès à l'interface

L'utilisateur accède à l'interface de commande depuis la borne ou l'interface web prévue à cet effet.

L'interface contient principalement :

- un champ de saisie de commande ;
- un bouton d'exécution ;
- une zone d'affichage de la réponse ;
- une zone permettant d'afficher les formulaires dynamiques ;
- un historique des commandes exécutées.

---

## 3. Saisie d'une commande

L'utilisateur saisit une commande dans le champ prévu à cet effet.

Exemple :

```text
AFFICHER STATISTIQUES
```

Après l'envoi, le système transmet la commande au backend.

Le traitement général est :

```text
Commande saisie
      ↓
Analyse / correction
      ↓
Analyse lexicale
      ↓
Analyse syntaxique
      ↓
Construction
      ↓
Exécution
      ↓
Réponse utilisateur
```

---

## 4. Commande valide

Une commande correcte est traitée directement.

Exemple :

```text
AFFICHER STATISTIQUES
```

Lorsque la commande est reconnue, le système :

1. vérifie sa structure ;
2. vérifie sa syntaxe ;
3. identifie l'action correspondante ;
4. exécute le traitement ;
5. retourne le résultat.

Une commande valide est généralement associée au mode :

```text
VALID
```

---

## 5. Correction automatique

Le système peut corriger automatiquement certaines fautes lorsqu'il estime que la correction est suffisamment fiable.

Exemple :

```text
AFFICHER STATISTIQUESS
```

Le système peut proposer ou appliquer automatiquement :

```text
AFFICHER STATISTIQUES
```

Ce fonctionnement correspond au mode :

```text
AUTO_CORRECT
```

Lorsque la correction est automatique, l'utilisateur peut poursuivre son utilisation sans avoir à ressaisir la commande.

---

## 6. Suggestion de correction

Lorsqu'une commande est suffisamment proche d'une commande connue mais nécessite une confirmation, le système utilise le mode :

```text
SUGGEST
```

Exemple :

```text
AFFICHER STATISTIQ
```

L'interface peut alors afficher :

```text
Voulez-vous dire :

AFFICHER STATISTIQUES ?

[ OUI ] [ NON ]
```

### 6.1. Bouton OUI

En sélectionnant :

```text
[ OUI ]
```

l'utilisateur confirme la proposition.

La commande proposée peut alors continuer son traitement normal.

```text
Suggestion confirmée
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
Résultat
```

### 6.2. Bouton NON

En sélectionnant :

```text
[ NON ]
```

la suggestion n'est pas exécutée.

L'utilisateur peut alors saisir une nouvelle commande.

---

## 7. Reformulation d'une commande

Lorsque le système ne peut pas déterminer avec suffisamment de précision l'intention de l'utilisateur, il peut demander une reformulation.

Le mode utilisé est alors :

```text
REFORMULATE
```

L'utilisateur doit saisir une nouvelle commande plus claire.

La commande concernée n'est pas exécutée tant qu'une formulation exploitable n'a pas été fournie.

---

## 8. Commande `AFFICHER STATISTIQUES`

L'utilisateur peut saisir :

```text
AFFICHER STATISTIQUES
```

Cette commande permet de demander les statistiques disponibles dans le système.

Le système analyse la commande puis transmet la demande au module statistique.

Le résultat est ensuite affiché dans l'interface.

---

## 9. Commande `AFFICHER ERREURS`

L'utilisateur peut saisir :

```text
AFFICHER ERREURS
```

Cette commande permet de consulter les erreurs enregistrées par le système.

Les informations peuvent notamment concerner :

- le type d'erreur ;
- le message ;
- le statut de correction ;
- la date d'enregistrement.

---

## 10. Commande `LANCER ENQUETE CYBERSECURITE`

La commande :

```text
LANCER ENQUETE CYBERSECURITE
```

permet de lancer l'opération correspondant à l'enquête de cybersécurité.

Le système valide la commande avant d'effectuer le traitement métier.

---

## 11. Commande `LANCER CAMPAGNE ECOLE`

La commande :

```text
LANCER CAMPAGNE ECOLE
```

permet d'initialiser l'opération liée à une campagne scolaire.

Le système retourne le résultat de l'opération et, lorsque cela est applicable, les informations relatives à la campagne créée.

---

## 12. Commande `CHERCHER ENFANTS KINSHASA`

La commande :

```text
CHERCHER ENFANTS KINSHASA
```

permet d'effectuer une recherche correspondant au critère prévu par le système.

Les résultats peuvent être retournés sous forme d'une liste accompagnée du nombre d'éléments trouvés.

---

## 13. Commande `CHERCHER ADOLESCENTS INTERESSES PAR PYTHON`

La commande :

```text
CHERCHER ADOLESCENTS INTERESSES PAR PYTHON
```

permet d'effectuer une recherche ciblée sur les adolescents intéressés par Python selon les critères définis dans le système.

---

## 14. Ajouter une question

L'utilisateur peut saisir :

```text
AJOUTER QUESTION
```

Cette commande peut entraîner l'affichage d'un formulaire dynamique.

Le formulaire permet notamment de renseigner :

```text
Texte de la question
Ordre de la question
Catégorie
```

Exemple d'interface :

```text
┌─────────────────────────────────┐
│ Ajouter une question            │
│                                 │
│ Texte de la question            │
│ [_____________________________] │
│                                 │
│ Ordre                           │
│ [_____________________________] │
│                                 │
│ Catégorie                       │
│ [_____________________________] │
│                                 │
│        [ Enregistrer ]          │
└─────────────────────────────────┘
```

Après validation, le système transmet les données nécessaires au backend.

---

## 15. Modifier une question

L'utilisateur peut modifier une question existante avec une commande telle que :

```text
MODIFIER QUESTION 3
```

Le numéro :

```text
3
```

identifie la question concernée.

Le système peut alors afficher un formulaire de modification.

Les informations pouvant être modifiées comprennent notamment :

- le texte de la question ;
- l'ordre ;
- le statut actif.

Exemple :

```text
┌─────────────────────────────────┐
│ Modification de la question 3  │
│                                 │
│ Nouvelle question               │
│ [_____________________________] │
│                                 │
│ Nouvel ordre                    │
│ [_____________________________] │
│                                 │
│          [ Modifier ]           │
└─────────────────────────────────┘
```

---

## 16. Supprimer une question

Pour supprimer une question, l'utilisateur peut saisir :

```text
SUPPRIMER QUESTION 25
```

Le système identifie la question numéro `25` puis exécute l'opération prévue par le backend.

Selon l'interface utilisée, une confirmation supplémentaire peut être demandée avant la suppression.

---

## 17. Exporter un rapport

La commande :

```text
EXPORTER RAPPORT
```

permet de déclencher l'opération d'exportation d'un rapport.

Le système retourne le résultat de l'opération et, lorsqu'un fichier est produit, les informations nécessaires relatives à cet export.

---

## 18. Recommencer une session

Pour recommencer une session, l'utilisateur peut utiliser :

```text
RECOMMENCER SESSION
```

Cette opération réinitialise la progression de la session selon les règles du système.

Les informations de progression peuvent notamment être remises à leur état initial.

---

## 19. Quitter

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

## 20. Gestion des sessions

Le système conserve les informations nécessaires à la gestion du parcours utilisateur.

Une session peut notamment conserver :

```text
Identifiant de session
Date de début
Date de fin
État
Question actuelle
Temps d'inactivité
Indicateur de sauvegarde
Utilisateur associé
Campagne associée
```

Les principaux états rencontrés sont :

```text
ACCUEIL
QUESTIONNAIRE
SESSION_INTERRUPTION
REPRISE_SESSION
FIN_SESSION
```

---

## 21. Reprise d'une session interrompue

Lorsque la progression d'une session a été sauvegardée avant une interruption, le système peut identifier l'existence d'une session interrompue.

La logique générale est :

```text
Session active
      ↓
Interruption
      ↓
SESSION_INTERRUPTION
      ↓
Restauration
      ↓
REPRISE_SESSION
      ↓
QUESTIONNAIRE
```

L'objectif est de permettre à l'utilisateur de continuer son parcours sans recommencer inutilement l'ensemble du questionnaire.

---

## 22. Gestion du temps d'inactivité

Le système suit le temps d'inactivité de la session.

Lorsque la limite configurée est atteinte, la session peut être automatiquement terminée.

Le mécanisme peut être représenté ainsi :

```text
QUESTIONNAIRE
      ↓
Temps d'inactivité
      ↓
Limite atteinte
      ↓
FIN_SESSION
```

---

## 23. Affichage des erreurs

Lorsqu'une erreur se produit, le système peut afficher un message permettant à l'utilisateur de comprendre la situation.

Les erreurs peuvent notamment concerner :

```text
Erreur lexicale
Erreur syntaxique
Commande inconnue
Commande incomplète
Erreur d'exécution
Erreur de données
```

L'objectif est d'éviter une exécution silencieuse d'une commande incorrecte.

---

## 24. Exemples de commandes incorrectes

### Commande incomplète

```text
AFFICHER
```

### Numéro absent

```text
MODIFIER QUESTION
```

### Mauvais ordre

```text
QUESTION MODIFIER 3
```

### Argument inattendu

```text
QUITTER RAPPORT
```

Dans ces situations, le système doit détecter l'erreur ou demander une reformulation.

---

## 25. Casse des commandes

Le système est conçu pour gérer les commandes sans dépendre strictement de la casse.

Exemple :

```text
AFFICHER STATISTIQUES
```

et :

```text
afficher statistiques
```

peuvent être interprétés de manière équivalente après normalisation.

---

## 26. Historique des commandes

Le système conserve un historique des commandes exécutées.

L'interface peut afficher notamment :

```text
ID
Commande
Tokens
Résultat
Valide
Date d'exécution
```

Cet historique permet notamment de suivre les opérations déjà effectuées.

---

## 27. Comprendre la réponse du système

Le backend retourne une réponse JSON structurée.

Selon le traitement, elle peut contenir notamment :

```text
success
mode
original
corrected
suggestion
suggestions
execution
resultat
trace
```

### Exemple de commande valide

```json
{
    "success": true,
    "mode": "VALID",
    "original": "AFFICHER STATISTIQUES",
    "corrected": "AFFICHER STATISTIQUES"
}
```

### Exemple de suggestion

```json
{
    "success": false,
    "mode": "SUGGEST",
    "original": "AFFICHER STATISTIQ",
    "suggestion": "AFFICHER STATISTIQUES",
    "requires_confirmation": true
}
```

Le frontend utilise ces informations pour adapter l'expérience utilisateur.

---

## 28. Cycle d'utilisation recommandé

L'utilisation normale du système suit le cycle :

```text
1. Saisir une commande
        ↓
2. Envoyer la commande
        ↓
3. Consulter la réponse
        ↓
4. Si suggestion → choisir OUI ou NON
        ↓
5. Si formulaire → compléter les données
        ↓
6. Valider
        ↓
7. Consulter le résultat
```

---

## 29. Liste des commandes principales

Les commandes actuellement couvertes comprennent :

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

Le numéro dans les commandes `MODIFIER QUESTION` et `SUPPRIMER QUESTION` est un exemple et doit être remplacé par le numéro réel de la question concernée.

---

## 30. Conseils d'utilisation

Pour faciliter l'utilisation du système :

- saisir des commandes correspondant aux fonctionnalités disponibles ;
- lire attentivement les suggestions proposées ;
- confirmer une suggestion uniquement lorsqu'elle correspond à l'intention ;
- utiliser les formulaires dynamiques lorsqu'ils sont proposés ;
- vérifier les numéros de questions avant une modification ou une suppression ;
- reformuler une commande lorsqu'elle n'est pas comprise.

---

## 31. Exemple d'utilisation complète

### Étape 1 — consulter les statistiques

```text
AFFICHER STATISTIQUES
```

### Étape 2 — saisir une commande avec une faute

```text
AFFICHER STATISTIQ
```

Le système propose :

```text
Voulez-vous dire :

AFFICHER STATISTIQUES ?

[ OUI ] [ NON ]
```

### Étape 3 — confirmer

L'utilisateur choisit :

```text
[ OUI ]
```

La commande est alors poursuivie dans le pipeline normal.

### Étape 4 — modifier une question

```text
MODIFIER QUESTION 3
```

Le système peut afficher le formulaire correspondant.

### Étape 5 — exporter un rapport

```text
EXPORTER RAPPORT
```

### Étape 6 — terminer

```text
QUITTER
```

La session peut alors être clôturée.

---

## 32. Résumé

Le **CCC Orientation System** permet à l'utilisateur d'interagir avec une interface de commandes textuelles tout en bénéficiant d'un mécanisme de correction et d'assistance.

Le parcours général est :

```text
Saisie
   ↓
Correction intelligente
   ↓
Suggestion / reformulation si nécessaire
   ↓
Validation syntaxique
   ↓
Exécution métier
   ↓
Résultat
```

Les fonctions principales accessibles à l'utilisateur concernent notamment :

```text
Statistiques
Erreurs
Enquêtes
Campagnes
Recherches
Questions
Rapports
Sessions
```

Le système associe ainsi une interface simple à un moteur backend structuré permettant de contrôler, corriger, interpréter et exécuter les commandes de manière cohérente.