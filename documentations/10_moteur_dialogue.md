# Moteur de dialogue / commandes — CCC Orientation System

Le **moteur de dialogue et de commandes** permet à l'utilisateur d'interagir avec le système à travers un langage de commandes contrôlé.

## 1. Pipeline de traitement

Chaque commande suit le pipeline principal :

```text
Corrector
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
```

Chaque composant possède une responsabilité précise :

| Composant | Rôle |
|---|---|
| `Corrector` | Analyse, correction et suggestion |
| `Lexer` | Transformation du texte en tokens |
| `Parser` | Validation syntaxique LL(1) |
| `Builder` | Construction de la commande structurée |
| `Dispatcher` | Identification de l'action |
| `Handler` | Exécution métier |

---

## 2. Modes du correcteur

Le `CommandCorrector` utilise quatre modes principaux :

```text
VALID
AUTO_CORRECT
SUGGEST
REFORMULATE
```

### `VALID`

La commande est reconnue correctement et peut poursuivre le pipeline.

```text
AFFICHER STATISTIQUES
```

### `AUTO_CORRECT`

Une faute est corrigée automatiquement lorsque la correction est suffisamment fiable.

```text
AFFICHER STATISTIQUESS
        ↓
AFFICHER STATISTIQUES
```

### `SUGGEST`

Une correction est proposée à l'utilisateur et nécessite une confirmation avant de poursuivre.

Exemple :

```text
AFFICHER STATISTIQ
```

Réponse :

```text
Voulez-vous dire :

AFFICHER STATISTIQUES ?

[ OUI ] [ NON ]
```

Tant que la confirmation n'est pas fournie, le pipeline s'arrête avant le Lexer.

### `REFORMULATE`

Lorsque la commande ne peut pas être interprétée suffisamment clairement, le système demande à l'utilisateur de la reformuler.

---

## 3. Fonctionnement du pipeline

### Commande valide

```text
Commande
   ↓
VALID
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
```

### Correction automatique

```text
Commande incorrecte
   ↓
AUTO_CORRECT
   ↓
Commande corrigée
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
```

### Suggestion

```text
Commande
   ↓
SUGGEST
   ↓
Confirmation utilisateur
   ↓
OUI → reprise du pipeline
NON → nouvelle saisie
```

### Reformulation

```text
Commande
   ↓
REFORMULATE
   ↓
Nouvelle saisie
```

---

## 4. Réponse du contrôleur

Pour le mode `SUGGEST`, le contrôleur retourne une réponse structurée contenant notamment :

```text
success = false
mode = SUGGEST
suggestion
suggestions
score
requires_confirmation = true
trace
```

Cette structure permet au frontend de déterminer qu'une interaction utilisateur est nécessaire.

---

## 5. Exemple complet

Pour la saisie :

```text
AFFICHER STATISTIQ
```

le système peut produire :

```text
mode = SUGGEST
suggestion = AFFICHER STATISTIQUES
requires_confirmation = true
```

L'interface affiche alors :

```text
Voulez-vous dire :

AFFICHER STATISTIQUES ?

[ OUI ] [ NON ]
```

Après confirmation, la commande corrigée peut poursuivre son traitement normal.

---

## 6. Traçabilité

Le moteur conserve une trace des principales étapes :

```text
Commande reçue
Commande normalisée
Analyse lexicale
Correction éventuelle
Décision du Corrector
Analyse syntaxique
Construction
Dispatching
Exécution
```

Cette trace facilite le diagnostic, les tests et la démonstration du fonctionnement du moteur de commandes.

---

## 7. Intégration globale

Le moteur de dialogue s'intègre dans l'architecture générale :

```text
Interface utilisateur
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
Contrôleurs métier
        ↓
SQLAlchemy / MySQL
```

Le moteur constitue ainsi l'interface entre la saisie utilisateur et l'exécution contrôlée des opérations métier du **CCC Orientation System**.