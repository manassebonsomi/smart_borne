# Parseur LL(1) — CCC Orientation System

Le **Parser LL(1)** est chargé de vérifier la conformité syntaxique des commandes à partir de la grammaire et de la table LL(1).

---

## 1. Fonctionnement

Le parseur :

- vérifie la validité de la table LL(1) ;
- ajoute `EOF` lorsqu'il est absent ;
- utilise une pile d'analyse LL(1) ;
- exploite un token de lookahead ;
- sélectionne les productions à partir de la table LL(1) ;
- produit une trace détaillée ;
- détecte les erreurs terminales et les erreurs de production ;
- utilise `FOLLOW` pour la récupération syntaxique ;
- se synchronise sur des tokens pertinents.

Le processus général est :

```text
Tokens
   ↓
Pile LL(1)
   ↓
Lookahead
   ↓
Table LL(1)
   ↓
Production
   ↓
Validation syntaxique
```

---

## 2. Gestion des erreurs

En cas d'erreur syntaxique, le Parser peut produire une structure indiquant notamment :

```text
success
message
errors
trace
```

La récupération syntaxique permet, lorsque cela est possible, de poursuivre l'analyse de manière contrôlée.

---

## 3. Trace

La trace permet notamment de suivre :

```text
Token courant
Sommet de la pile
Production sélectionnée
Terminal reconnu
Erreur détectée
Action de récupération
```

Elle facilite le débogage, la maintenance et la démonstration du fonctionnement du Parser.

---

## 4. Intégration dans le pipeline

Le Parser intervient entre le Lexer et le Builder :

```text
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
```

Une commande syntaxiquement invalide est arrêtée avant sa construction et son exécution métier.

---

## 5. Exemple

Pour :

```text
AFFICHER STATISTIQUES
```

le Parser vérifie conceptuellement :

```text
COMMANDE
   ↓
ACTION_AFFICHER
   ↓
AFFICHER STATISTIQUES
   ↓
EOF
   ↓
Analyse réussie
```

---

## 6. Tests

Le Parser dispose d'une suite dédiée :

```text
tests/unit/test_parser.py
```

Résultat validé :

```text
23 tests passés
0 échec
```

Le Parser LL(1) constitue ainsi la couche de validation syntaxique entre l'analyse lexicale et la construction des commandes.