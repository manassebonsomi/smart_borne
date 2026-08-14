# Analyse syntaxique : Ensembles FIRST et FOLLOW — CCC Orientation System

## 1. Présentation

Les ensembles **FIRST** et **FOLLOW** sont utilisés par le mécanisme d'analyse syntaxique **LL(1)** du **CCC Orientation System**.

Ils permettent de construire la table LL(1) et d'aider le Parser à sélectionner la bonne production avec un seul token de lookahead.

Le processus est :

```text
Grammaire
    ↓
GrammarAnalyzer
    ↓
FIRST + FOLLOW
    ↓
Table LL(1)
    ↓
Parser LL(1)
```

---

## 2. Composant `GrammarAnalyzer`

Le `GrammarAnalyzer` analyse les productions de la grammaire afin de calculer automatiquement :

```text
FIRST
FOLLOW
```

Il constitue ainsi l'intermédiaire entre :

```text
grammar.py
     ↓
GrammarAnalyzer
     ↓
LL1Table
```

---

## 3. Ensemble FIRST

`FIRST(X)` contient les terminaux pouvant apparaître au début d'une dérivation de `X`.

Exemple :

```text
<A> ::= AFFICHER
```

donne :

```text
FIRST(<A>) = { AFFICHER }
```

Pour :

```text
<CIBLE_AFFICHER> ::= STATISTIQUES
                   | ERREURS
```

on obtient :

```text
FIRST(<CIBLE_AFFICHER>) =
{
    STATISTIQUES,
    ERREURS
}
```

---

## 4. Ensemble FOLLOW

`FOLLOW(X)` contient les terminaux pouvant apparaître après le non-terminal `X`.

Il est notamment utilisé pour les productions pouvant générer `EPSILON`.

Pour le symbole de départ :

```text
<COMMANDE>
```

le système utilise notamment :

```text
EOF ∈ FOLLOW(<COMMANDE>)
```

Cela permet au Parser de reconnaître correctement la fin d'une commande.

---

## 5. FIRST de la commande principale

La grammaire du système contient les principales familles :

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

Ainsi, conceptuellement :

```text
FIRST(<COMMANDE>) =
{
    AFFICHER,
    LANCER,
    CHERCHER,
    AJOUTER,
    MODIFIER,
    SUPPRIMER,
    EXPORTER,
    RECOMMENCER,
    QUITTER
}
```

Le premier token permet donc généralement de sélectionner directement la famille de commande.

---

## 6. Exemple avec `AFFICHER`

Production :

```text
<ACTION_AFFICHER> ::= AFFICHER <CIBLE_AFFICHER>
```

On obtient :

```text
FIRST(<ACTION_AFFICHER>) =
{
    AFFICHER
}
```

et :

```text
FIRST(<CIBLE_AFFICHER>) =
{
    STATISTIQUES,
    ERREURS
}
```

Cela permet d'analyser :

```text
AFFICHER STATISTIQUES
```

ou :

```text
AFFICHER ERREURS
```

---

## 7. Exemple avec `LANCER`

Production :

```text
<ACTION_LANCER> ::= LANCER <CIBLE_LANCER>
```

donne :

```text
FIRST(<ACTION_LANCER>) =
{
    LANCER
}
```

et :

```text
FIRST(<CIBLE_LANCER>) =
{
    ENQUETE,
    CAMPAGNE
}
```

Les deux commandes suivantes sont ainsi distinguées :

```text
LANCER ENQUETE CYBERSECURITE
LANCER CAMPAGNE ECOLE
```

---

## 8. Exemple avec `CHERCHER`

Production :

```text
<ACTION_CHERCHER> ::= CHERCHER <CIBLE_RECHERCHE>
```

donne :

```text
FIRST(<ACTION_CHERCHER>) =
{
    CHERCHER
}
```

et :

```text
FIRST(<CIBLE_RECHERCHE>) =
{
    ENFANTS,
    ADOLESCENTS
}
```

Cela permet de distinguer :

```text
CHERCHER ENFANTS KINSHASA
```

et :

```text
CHERCHER ADOLESCENTS INTERESSES PAR PYTHON
```

---

## 9. Exemple avec la gestion des questions

La production :

```text
<ACTION_GESTION_QUESTION> ::= AJOUTER QUESTION
                             | MODIFIER QUESTION NUMERO
                             | SUPPRIMER QUESTION NUMERO
```

donne :

```text
FIRST(<ACTION_GESTION_QUESTION>) =
{
    AJOUTER,
    MODIFIER,
    SUPPRIMER
}
```

Le Parser peut donc sélectionner la bonne branche dès le premier token.

---

## 10. FIRST et `EPSILON`

Lorsqu'une production contient plusieurs symboles, le calcul de FIRST tient compte des symboles pouvant produire `EPSILON`.

Exemple :

```text
<A> ::= <B> <C>
```

Si :

```text
EPSILON ∈ FIRST(<B>)
```

alors les éléments de :

```text
FIRST(<C>)
```

peuvent également être intégrés à :

```text
FIRST(<A>)
```

---

## 11. FOLLOW et `EPSILON`

Pour une production :

```text
<A> ::= EPSILON
```

les éléments de :

```text
FOLLOW(<A>)
```

permettent de déterminer dans quels contextes la production vide peut être sélectionnée dans la table LL(1).

---

## 12. Construction de la table LL(1)

FIRST et FOLLOW servent directement à construire la table :

```text
M[Non-terminal, Lookahead]
```

Le processus est :

```text
Grammaire
    ↓
GrammarAnalyzer
    ↓
FIRST / FOLLOW
    ↓
LL1Table
    ↓
Validation
    ↓
Parser LL(1)
```

---

## 13. Détection des conflits

Une table LL(1) doit permettre une décision unique pour chaque couple :

```text
(Non-terminal, Lookahead)
```

Une situation telle que :

```text
M[A, token]
    → Production 1
    → Production 2
```

constituerait un conflit LL(1).

FIRST et FOLLOW participent donc à la vérification de l'absence de ces ambiguïtés.

---

## 14. Récupération syntaxique

FOLLOW est également utilisé pour faciliter la récupération après une erreur syntaxique.

Le principe est :

```text
Erreur
   ↓
Recherche d'un token de synchronisation
   ↓
FOLLOW
   ↓
Avancement contrôlé
   ↓
Reprise de l'analyse
```

Exemple :

```text
MODIFIER QUESTION
```

Le Parser attend :

```text
NUMERO
```

mais peut rencontrer :

```text
EOF
```

Il signale alors l'erreur et applique sa stratégie de récupération.

---

## 15. Relation avec le Lexer

Le flux d'analyse est :

```text
Texte utilisateur
        ↓
Lexer
        ↓
Tokens
        ↓
Table LL(1)
        ↓
Parser
```

Le Lexer produit notamment :

```text
AFFICHER
STATISTIQUES
QUESTION
NUMERO
QUITTER
EOF
```

Le Parser utilise ensuite ces tokens pour valider la structure de la commande.

---

## 16. Relation entre les composants

| Composant | Responsabilité |
|---|---|
| `grammar.py` | Définit les productions |
| `GrammarAnalyzer` | Calcule FIRST et FOLLOW |
| `LL1Table` | Construit et valide la table |
| `LL1Parser` | Effectue l'analyse syntaxique |

Chaîne complète :

```text
grammar.py
     ↓
GrammarAnalyzer
     ↓
FIRST / FOLLOW
     ↓
LL1Table
     ↓
LL1Parser
```

---

## 17. Trace du traitement

Le Parser peut produire une trace comprenant notamment :

```text
Commande reçue
Token courant
Sommet de la pile
Production sélectionnée
Terminal reconnu
Erreur détectée
Action de récupération
Fin de l'analyse
```

Cette trace facilite le débogage et la démonstration du fonctionnement LL(1).

---

## 18. Exemple complet

Pour :

```text
AFFICHER STATISTIQUES
```

le traitement est conceptuellement :

```text
Texte
  ↓
Lexer
  ↓
AFFICHER STATISTIQUES EOF
  ↓
Lookahead = AFFICHER
  ↓
<ACTION_AFFICHER>
  ↓
Lookahead = STATISTIQUES
  ↓
<CIBLE_AFFICHER>
  ↓
STATISTIQUES
  ↓
EOF
  ↓
Analyse réussie
```

---

## 19. Tests automatisés

Les mécanismes FIRST/FOLLOW et LL(1) sont couverts par les tests automatisés.

Résultats validés :

```text
Table LL(1) : 7 passed
Parser LL(1) : 23 passed
```

La suite globale officielle du projet a également été validée avec :

```text
224 passed
0 failed
0 errors
```

---

## 20. Résumé

Le mécanisme peut être résumé ainsi :

```text
              Grammaire
                   ↓
           GrammarAnalyzer
              /         \
             ↓           ↓
          FIRST         FOLLOW
             \           /
              ↓         ↓
               LL1Table
                   ↓
               LL1Parser
                   ↓
          Validation syntaxique
```

FIRST et FOLLOW permettent notamment :

- de déterminer les terminaux possibles au début des dérivations ;
- d'identifier les terminaux pouvant suivre un non-terminal ;
- de construire la table LL(1) ;
- de sélectionner les productions avec un seul lookahead ;
- de gérer `EPSILON` et `EOF` ;
- de faciliter la récupération syntaxique.

Ils constituent ainsi une partie essentielle du moteur de commandes LL(1) du **CCC Orientation System**.