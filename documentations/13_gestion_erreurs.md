# Gestion des erreurs — CCC Orientation System

Le **CCC Orientation System** dispose d'un mécanisme de gestion des erreurs réparti sur les différentes couches du système.

## 1. Catégories d'erreurs

Les principales catégories couvertes sont :

```text
Erreur lexicale
Erreur syntaxique
Suggestion / reformulation
Erreur de construction
Erreur d'exécution
Erreur base de données
Commande inconnue
Données manquantes
```

---

## 2. Gestion par couche

Les erreurs peuvent être détectées à différents niveaux :

```text
Corrector
   ↓
Lexer
   ↓
Parser
   ↓
Builder
   ↓
Dispatcher
   ↓
Handler
   ↓
Controller / Database
```

Chaque couche est responsable des erreurs relevant de son propre traitement.

---

## 3. Erreur lexicale

Une erreur lexicale apparaît lorsqu'un caractère ou un mot ne peut pas être reconnu par le Lexer.

Exemple :

```text
AFFICHER @
```

Le système peut retourner :

```text
mode = LEXICAL_ERROR
```

avec un message et une trace associés.

---

## 4. Erreur syntaxique

Une erreur syntaxique apparaît lorsque les tokens ne respectent pas la grammaire.

Exemples :

```text
AFFICHER
MODIFIER QUESTION
```

Le Parser retourne alors une erreur structurée, avec notamment :

```text
success
message
errors
trace
```

---

## 5. Suggestion et reformulation

Le correcteur peut interrompre le pipeline lorsqu'une interaction utilisateur est nécessaire.

### Suggestion

```text
AFFICHER STATISTIQ
```

peut produire :

```text
SUGGEST
```

avec une proposition :

```text
AFFICHER STATISTIQUES
```

### Reformulation

Lorsque la commande ne peut pas être interprétée correctement :

```text
REFORMULATE
```

Le système demande alors une nouvelle saisie.

---

## 6. Erreur de construction

Une `BUILD_ERROR` apparaît lorsqu'une commande valide syntaxiquement ne peut pas être transformée correctement en objet `Command`.

Le contrôleur retourne alors un résultat structuré contenant notamment :

```text
success = false
mode = BUILD_ERROR
error = BUILD_ERROR
message
trace
```

---

## 7. Erreur d'exécution

Une `EXECUTION_ERROR` apparaît lorsqu'une erreur survient pendant l'exécution métier de la commande.

Le système effectue notamment les opérations nécessaires pour éviter de laisser une transaction incohérente.

La réponse peut contenir :

```text
success = false
mode = EXECUTION_ERROR
error = EXECUTION_ERROR
message
trace
```

---

## 8. Erreur de base de données

Une `DATABASE_ERROR` correspond à une erreur survenue lors de la sauvegarde ou d'une opération de persistance.

Le système effectue alors un :

```python
db.session.rollback()
```

afin d'annuler la transaction concernée.

---

## 9. Commande inconnue

Une commande ou une action inconnue peut être détectée au niveau du Dispatcher ou du Handler.

Exemple conceptuel :

```text
ACTION_INEXISTANTE
```

Le système retourne un résultat indiquant que l'action n'est pas reconnue.

---

## 10. Données manquantes

Certaines commandes nécessitent des informations supplémentaires.

Exemple :

```text
AJOUTER QUESTION
```

peut être syntaxiquement valide mais nécessiter des données complémentaires pour poursuivre.

Dans ce cas, le Handler peut retourner un état indiquant qu'il attend les données nécessaires et permettre au frontend d'afficher un formulaire dynamique.

---

## 11. Trace des erreurs

Lorsqu'elle est pertinente, chaque couche contribue à la trace du traitement.

Une trace peut notamment contenir :

```text
Commande reçue
Commande normalisée
Correction
Tokenisation
Production Parser
Erreur détectée
Action de récupération
Construction
Exécution
```

Cette traçabilité facilite le diagnostic et la démonstration du fonctionnement du système.

---

## 12. Structure générale

Le principe global est :

```text
Erreur détectée
      ↓
Classification
      ↓
Message structuré
      ↓
Trace
      ↓
Réponse JSON
      ↓
Frontend
```

La gestion des erreurs permet ainsi de conserver une réponse cohérente entre les différentes couches du **CCC Orientation System**.