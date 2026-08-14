# Grammaire complète du Parser LL(1) — CCC Orientation System

## 1. Présentation

Cette grammaire hors-contexte définit les commandes reconnues par le **Parser LL(1)** du **CCC Orientation System**.

Le symbole initial est :

```text
<COMMANDE>
```

Elle permet de valider la structure des commandes avant leur construction et leur exécution.

---

## 2. Commandes supportées

| Catégorie | Commandes |
|---|---|
| Affichage | `AFFICHER STATISTIQUES` · `AFFICHER ERREURS` |
| Lancement | `LANCER ENQUETE CYBERSECURITE` · `LANCER CAMPAGNE ECOLE` |
| Recherche | `CHERCHER ENFANTS KINSHASA` · `CHERCHER ADOLESCENTS INTERESSES PAR PYTHON` |
| Questions | `AJOUTER QUESTION` · `MODIFIER QUESTION NUMERO` · `SUPPRIMER QUESTION NUMERO` |
| Session / Rapport | `EXPORTER RAPPORT` · `RECOMMENCER SESSION` · `QUITTER` |

---

## 3. Non-terminaux principaux

```text
<COMMANDE>
<ACTION_AFFICHER>
<CIBLE_AFFICHER>
<ACTION_LANCER>
<CIBLE_LANCER>
<ACTION_CHERCHER>
<CIBLE_RECHERCHE>
<ACTION_GESTION_QUESTION>
<ACTION_SESSION>
```

Les terminaux principaux sont les mots réservés du langage ainsi que :

```text
NUMERO
EOF
```

`NUMERO` représente un numéro de question et `EOF` la fin de l'entrée.

---

## 4. Règles de production

```text
<COMMANDE>                ::= <ACTION_AFFICHER>
                            | <ACTION_LANCER>
                            | <ACTION_CHERCHER>
                            | <ACTION_GESTION_QUESTION>
                            | <ACTION_SESSION>

<ACTION_AFFICHER>         ::= AFFICHER <CIBLE_AFFICHER>

<CIBLE_AFFICHER>          ::= STATISTIQUES
                            | ERREURS

<ACTION_LANCER>           ::= LANCER <CIBLE_LANCER>

<CIBLE_LANCER>            ::= ENQUETE CYBERSECURITE
                            | CAMPAGNE ECOLE

<ACTION_CHERCHER>         ::= CHERCHER <CIBLE_RECHERCHE>

<CIBLE_RECHERCHE>         ::= ENFANTS KINSHASA
                            | ADOLESCENTS INTERESSES PAR PYTHON

<ACTION_GESTION_QUESTION> ::= AJOUTER QUESTION
                            | MODIFIER QUESTION NUMERO
                            | SUPPRIMER QUESTION NUMERO

<ACTION_SESSION>          ::= EXPORTER RAPPORT
                            | RECOMMENCER SESSION
                            | QUITTER
```

---

## 5. Exemples de commandes valides

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

---

## 6. Exemples de commandes invalides

```text
AFFICHER
MODIFIER QUESTION
SUPPRIMER QUESTION
LANCER
QUESTION MODIFIER 3
QUITTER RAPPORT
```

Le Parser doit rejeter ces structures lorsqu'elles ne correspondent à aucune production valide.

---

## 7. Exemple de dérivation

Pour :

```text
AFFICHER STATISTIQUES
```

on obtient :

```text
<COMMANDE>
    ↓
<ACTION_AFFICHER>
    ↓
AFFICHER <CIBLE_AFFICHER>
    ↓
AFFICHER STATISTIQUES
```

Pour :

```text
MODIFIER QUESTION 3
```

on obtient :

```text
<COMMANDE>
    ↓
<ACTION_GESTION_QUESTION>
    ↓
MODIFIER QUESTION NUMERO
    ↓
MODIFIER QUESTION 3
```

---

## 8. Principes LL(1)

Le Parser utilise :

```text
FIRST
FOLLOW
Table LL(1)
Lookahead
Pile d'analyse
```

Les premiers terminaux de `<COMMANDE>` sont notamment :

```text
AFFICHER
LANCER
CHERCHER
AJOUTER
MODIFIER
SUPPRIMER
EXPORTER
RECOMMENCER
QUITTER
```

Ils permettent de sélectionner la branche syntaxique à partir du premier token.

---

## 9. `NUMERO` et `EOF`

Pour :

```text
MODIFIER QUESTION 3
```

le Lexer produit conceptuellement :

```text
MODIFIER
QUESTION
NUMERO("3")
EOF
```

Le Parser vérifie ensuite que cette séquence respecte la production correspondante.

`EOF` permet de confirmer que toute la commande a été consommée.

---

## 10. Intégration dans le pipeline

La grammaire s'intègre au pipeline :

```text
Commande utilisateur
        ↓
CommandCorrector
        ↓
Lexer
        ↓
Grammaire / FIRST / FOLLOW
        ↓
Table LL(1)
        ↓
Parser LL(1)
        ↓
CommandBuilder
        ↓
CommandDispatcher
        ↓
CommandHandler
```

La grammaire définit la syntaxe ; l'exécution métier est assurée par les couches suivantes.

---

## 11. Extension de la grammaire

L'ajout d'une nouvelle commande nécessite généralement :

```text
grammar.py
    ↓
FIRST / FOLLOW
    ↓
Table LL(1)
    ↓
Parser
    ↓
CommandBuilder
    ↓
Dispatcher
    ↓
Handler
    ↓
Tests
```

Une nouvelle commande ne doit donc pas être ajoutée uniquement au frontend.

---

## 12. Validation

La grammaire est couverte par les tests du Parser et de la table LL(1).

Résultats validés :

```text
Parser LL(1) : 23 passed
Table LL(1)  : 7 passed
```

Suite globale :

```text
224 passed
0 failed
0 errors
```

---

## 13. Résumé

La grammaire définit cinq branches principales :

```text
<COMMANDE>
├── <ACTION_AFFICHER>
├── <ACTION_LANCER>
├── <ACTION_CHERCHER>
├── <ACTION_GESTION_QUESTION>
└── <ACTION_SESSION>
```

Elle constitue la base formelle du langage de commandes du **CCC Orientation System** et permet au Parser LL(1) de valider les commandes avant leur construction et leur exécution.