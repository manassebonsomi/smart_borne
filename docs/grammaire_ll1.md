# Grammaire LL(1) du système CCC Orientation

## 1. Présentation

Le système CCC Orientation utilise un langage de commande en mini-français permettant au formateur d'interagir avec la plateforme à travers des commandes textuelles.

Le traitement d'une commande suit la chaîne :

```text
Commande utilisateur
        ↓
Analyse lexicale
        ↓
Séquence de tokens
        ↓
Analyse syntaxique LL(1)
        ↓
Table LL(1)
        ↓
Pile d'analyse
        ↓
Acceptation / erreur
        ↓
Moteur de dialogue
        ↓
Exécution de l'action
```

L'analyse syntaxique est réalisée par un parseur LL(1) piloté par :

* une pile ;
* une séquence de tokens ;
* une table d'analyse LL(1) ;
* un ensemble de productions ;
* un symbole de fin `EOF`.

---

# 2. Axiome

L'axiome de la grammaire est :

```text
COMMANDE
```

Toute commande utilisateur doit pouvoir être dérivée à partir de cet axiome.

---

# 3. Terminaux

Les terminaux utilisés par la grammaire sont :

```text
AFFICHER
STATISTIQUES
ERREURS

LANCER
ENQUETE
CYBERSECURITE
CAMPAGNE
ECOLE

CHERCHER
ENFANTS
KINSHASA
ADOLESCENTS
INTERESSES
PAR
PYTHON

AJOUTER
QUESTION

MODIFIER
NUMERO

SUPPRIMER

EXPORTER
RAPPORT

RECOMMENCER
SESSION

QUITTER

EOF
```

`NUMERO` est un terminal produit par l'analyseur lexical lorsqu'un nombre entier est rencontré dans la commande.

Exemple :

```text
MODIFIER QUESTION 3
```

est transformé lexicalement en :

```text
MODIFIER QUESTION NUMERO EOF
```

avec :

```text
NUMERO.value = 3
```

---

# 4. Non-terminaux

Les non-terminaux de la grammaire sont :

```text
COMMANDE

CMD_AFFICHER
SUJET_AFFICHAGE

CMD_LANCER
SUJET_LANCER

CMD_CHERCHER
SUJET_RECHERCHE

CMD_AJOUTER
SUJET_AJOUTER

CMD_MODIFIER
SUJET_MODIFIER

CMD_SUPPRIMER
SUJET_SUPPRIMER

CMD_EXPORTER
SUJET_EXPORTER

CMD_RECOMMENCER
SUJET_RECOMMENCER

CMD_QUITTER
```

---

# 5. Productions

## 5.1 Commande principale

```text
COMMANDE → CMD_AFFICHER
         | CMD_LANCER
         | CMD_CHERCHER
         | CMD_AJOUTER
         | CMD_MODIFIER
         | CMD_SUPPRIMER
         | CMD_EXPORTER
         | CMD_RECOMMENCER
         | CMD_QUITTER
```

---

## 5.2 Affichage

```text
CMD_AFFICHER → AFFICHER SUJET_AFFICHAGE
```

```text
SUJET_AFFICHAGE → STATISTIQUES
                | ERREURS
```

Commandes valides :

```text
AFFICHER STATISTIQUES
AFFICHER ERREURS
```

---

## 5.3 Lancement

```text
CMD_LANCER → LANCER SUJET_LANCER
```

```text
SUJET_LANCER → ENQUETE CYBERSECURITE
             | CAMPAGNE ECOLE
```

Commandes valides :

```text
LANCER ENQUETE CYBERSECURITE
LANCER CAMPAGNE ECOLE
```

---

## 5.4 Recherche

```text
CMD_CHERCHER → CHERCHER SUJET_RECHERCHE
```

```text
SUJET_RECHERCHE → ENFANTS KINSHASA
                 | ADOLESCENTS INTERESSES PAR PYTHON
```

Commandes valides :

```text
CHERCHER ENFANTS KINSHASA

CHERCHER ADOLESCENTS INTERESSES PAR PYTHON
```

---

## 5.5 Ajout d'une question

```text
CMD_AJOUTER → AJOUTER SUJET_AJOUTER
```

```text
SUJET_AJOUTER → QUESTION
```

Commande syntaxiquement valide :

```text
AJOUTER QUESTION
```

Cette commande déclenche ensuite le formulaire d'ajout de question dans le moteur de dialogue.

---

## 5.6 Modification d'une question

```text
CMD_MODIFIER → MODIFIER SUJET_MODIFIER
```

```text
SUJET_MODIFIER → QUESTION NUMERO
```

Exemple :

```text
MODIFIER QUESTION 3
```

Le parseur valide la structure :

```text
MODIFIER QUESTION NUMERO
```

et la valeur numérique `3` est conservée dans le token :

```text
NUMERO.value = 3
```

Le moteur de dialogue peut ensuite utiliser cette valeur pour rechercher la question correspondante.

---

## 5.7 Suppression

```text
CMD_SUPPRIMER → SUPPRIMER SUJET_SUPPRIMER
```

```text
SUJET_SUPPRIMER → QUESTION NUMERO
```

Exemple :

```text
SUPPRIMER QUESTION 2
```

---

## 5.8 Exportation

```text
CMD_EXPORTER → EXPORTER SUJET_EXPORTER
```

```text
SUJET_EXPORTER → RAPPORT
```

Commande :

```text
EXPORTER RAPPORT
```

---

## 5.9 Reprise

```text
CMD_RECOMMENCER → RECOMMENCER SUJET_RECOMMENCER
```

```text
SUJET_RECOMMENCER → SESSION
```

Commande :

```text
RECOMMENCER SESSION
```

---

## 5.10 Quitter

```text
CMD_QUITTER → QUITTER
```

Commande :

```text
QUITTER
```

---

# 6. Propriété LL(1)

La grammaire est construite de manière à ce que le premier token permette de déterminer la famille de commande.

Le non-terminal :

```text
COMMANDE
```

possède les alternatives suivantes :

```text
COMMANDE → CMD_AFFICHER
         | CMD_LANCER
         | CMD_CHERCHER
         | CMD_AJOUTER
         | CMD_MODIFIER
         | CMD_SUPPRIMER
         | CMD_EXPORTER
         | CMD_RECOMMENCER
         | CMD_QUITTER
```

Les ensembles FIRST sont disjoints :

```text
FIRST(CMD_AFFICHER)    = {AFFICHER}
FIRST(CMD_LANCER)      = {LANCER}
FIRST(CMD_CHERCHER)    = {CHERCHER}
FIRST(CMD_AJOUTER)     = {AJOUTER}
FIRST(CMD_MODIFIER)    = {MODIFIER}
FIRST(CMD_SUPPRIMER)   = {SUPPRIMER}
FIRST(CMD_EXPORTER)    = {EXPORTER}
FIRST(CMD_RECOMMENCER) = {RECOMMENCER}
FIRST(CMD_QUITTER)     = {QUITTER}
```

Il n'existe donc pas de conflit pour `COMMANDE`.

---

# 7. Ensembles FIRST

Les ensembles FIRST calculés par le système sont :

```text
FIRST(CMD_AFFICHER)    = {AFFICHER}
FIRST(CMD_AJOUTER)     = {AJOUTER}
FIRST(CMD_CHERCHER)    = {CHERCHER}
FIRST(CMD_EXPORTER)    = {EXPORTER}
FIRST(CMD_LANCER)      = {LANCER}
FIRST(CMD_MODIFIER)    = {MODIFIER}
FIRST(CMD_QUITTER)     = {QUITTER}
FIRST(CMD_RECOMMENCER) = {RECOMMENCER}
FIRST(CMD_SUPPRIMER)   = {SUPPRIMER}
```

Pour les sujets :

```text
FIRST(SUJET_AFFICHAGE)
= {STATISTIQUES, ERREURS}

FIRST(SUJET_AJOUTER)
= {QUESTION}

FIRST(SUJET_EXPORTER)
= {RAPPORT}

FIRST(SUJET_LANCER)
= {ENQUETE, CAMPAGNE}

FIRST(SUJET_MODIFIER)
= {QUESTION}

FIRST(SUJET_RECHERCHE)
= {ENFANTS, ADOLESCENTS}

FIRST(SUJET_RECOMMENCER)
= {SESSION}

FIRST(SUJET_SUPPRIMER)
= {QUESTION}
```

Enfin :

```text
FIRST(COMMANDE)
=
{
    AFFICHER,
    AJOUTER,
    CHERCHER,
    EXPORTER,
    LANCER,
    MODIFIER,
    QUITTER,
    RECOMMENCER,
    SUPPRIMER
}
```

Aucune production de la grammaire actuelle ne produit `ε`.

---

# 8. Ensembles FOLLOW

L'axiome :

```text
COMMANDE
```

est suivi par :

```text
EOF
```

Par propagation dans les productions, les non-terminaux terminaux de niveau commande possèdent également :

```text
FOLLOW(CMD_AFFICHER)    = {EOF}
FOLLOW(CMD_AJOUTER)     = {EOF}
FOLLOW(CMD_CHERCHER)    = {EOF}
FOLLOW(CMD_EXPORTER)    = {EOF}
FOLLOW(CMD_LANCER)      = {EOF}
FOLLOW(CMD_MODIFIER)    = {EOF}
FOLLOW(CMD_QUITTER)     = {EOF}
FOLLOW(CMD_RECOMMENCER) = {EOF}
FOLLOW(CMD_SUPPRIMER)   = {EOF}
FOLLOW(COMMANDE)        = {EOF}
```

Les sujets sont également suivis par `EOF` :

```text
FOLLOW(SUJET_AFFICHAGE)    = {EOF}
FOLLOW(SUJET_AJOUTER)      = {EOF}
FOLLOW(SUJET_EXPORTER)     = {EOF}
FOLLOW(SUJET_LANCER)       = {EOF}
FOLLOW(SUJET_MODIFIER)     = {EOF}
FOLLOW(SUJET_RECHERCHE)    = {EOF}
FOLLOW(SUJET_RECOMMENCER)  = {EOF}
FOLLOW(SUJET_SUPPRIMER)    = {EOF}
```

---

# 9. Table LL(1)

La table est construite automatiquement à partir de :

```text
FIRST
FOLLOW
Productions
```

Pour une production :

```text
A → α
```

le constructeur de table applique :

```text
Pour chaque terminal a ∈ FIRST(α) :
    M[A,a] = A → α
```

Si `ε ∈ FIRST(α)`, alors :

```text
Pour chaque b ∈ FOLLOW(A) :
    M[A,b] = A → ε
```

La construction vérifie également les conflits.

Si une cellule contient déjà une production différente, le système déclenche :

```text
GrammarConflictError
```

---

# 10. Validation de la table

La table actuelle est validée sans conflit.

Le système retourne :

```text
Validation : Aucun conflit LL(1) détecté.
```

La validation est effectuée par :

```python
LL1Table.validate()
```

et permet de vérifier automatiquement que deux productions différentes ne sont pas placées dans une même cellule.

---

# 11. Analyseur LL(1)

Le parseur utilise :

```text
Pile
Tokens
Table LL(1)
Lookahead
Productions
EOF
```

La pile initiale est :

```text
EOF COMMANDE
```

Le premier token constitue le lookahead.

Pour :

```text
AFFICHER STATISTIQUES
```

les tokens sont :

```text
AFFICHER
STATISTIQUES
EOF
```

La table donne :

```text
M[COMMANDE, AFFICHER]
```

qui contient :

```text
COMMANDE → CMD_AFFICHER
```

Le parseur remplace alors le non-terminal par la production correspondante.

---

# 12. Trace d'une commande valide

Commande :

```text
AFFICHER STATISTIQUES
```

Tokens :

```text
AFFICHER
STATISTIQUES
EOF
```

Trace :

```text
Étape 1
Pile : EOF COMMANDE
Lookahead : AFFICHER
Action : COMMANDE → CMD_AFFICHER

Étape 2
Pile : EOF CMD_AFFICHER
Lookahead : AFFICHER
Action : CMD_AFFICHER → AFFICHER SUJET_AFFICHAGE

Étape 3
Lookahead : AFFICHER
Action : Correspondance : AFFICHER

Étape 4
Lookahead : STATISTIQUES
Action : SUJET_AFFICHAGE → STATISTIQUES

Étape 5
Lookahead : STATISTIQUES
Action : Correspondance : STATISTIQUES

Étape 6
Lookahead : EOF
Action : ACCEPT
```

Résultat :

```text
ACCEPTATION
```

---

# 13. Trace d'une commande invalide

Commande :

```text
AFFICHER QUESTION
```

Tokens :

```text
AFFICHER
QUESTION
EOF
```

Le parseur reconnaît :

```text
COMMANDE → CMD_AFFICHER
```

puis :

```text
CMD_AFFICHER → AFFICHER SUJET_AFFICHAGE
```

Après consommation de `AFFICHER`, le lookahead devient :

```text
QUESTION
```

Or :

```text
M[SUJET_AFFICHAGE, QUESTION]
```

n'existe pas.

Le parseur produit donc :

```text
Aucune production pour SUJET_AFFICHAGE
avec le lookahead QUESTION.
```

Résultat :

```text
ERREUR
```

---

# 14. Exemple d'erreur syntaxique en fin de commande

Commande :

```text
QUITTER QUESTION
```

Le parseur reconnaît :

```text
QUITTER
```

mais après cette correspondance il attend :

```text
EOF
```

alors que le lookahead est :

```text
QUESTION
```

Le résultat est :

```text
Erreur syntaxique :
attendu EOF,
reçu QUESTION.
```

---

# 15. Erreurs lexicales

L'analyseur lexical intervient avant le parseur.

Lorsqu'un mot inconnu est rencontré, le système tente d'identifier une commande proche grâce au module :

```text
CommandSuggester
```

Exemple :

```text
AFFICHER STATISTIQES
```

peut produire une suggestion proche de :

```text
STATISTIQUES
```

La correction lexicale et la correction syntaxique sont ainsi séparées.

---

# 16. Séparation des responsabilités

Le système respecte la séparation suivante :

```text
LexicalAnalyzer
    ↓
Tokenisation
    ↓
LL1Parser
    ↓
Analyse syntaxique
    ↓
Moteur de dialogue
    ↓
Exécution
```

L'analyseur lexical ne décide pas si une phrase est syntaxiquement valide.

Le parseur ne réalise pas directement les opérations métier.

Le moteur de dialogue exploite le résultat du parseur pour déclencher l'action correspondante.

---

# 17. Commandes valides de référence

Les commandes actuellement reconnues sont :

```text
AFFICHER STATISTIQUES
AFFICHER ERREURS

LANCER ENQUETE CYBERSECURITE
LANCER CAMPAGNE ECOLE

CHERCHER ENFANTS KINSHASA
CHERCHER ADOLESCENTS INTERESSES PAR PYTHON

AJOUTER QUESTION

MODIFIER QUESTION 3
MODIFIER QUESTION 10

SUPPRIMER QUESTION 2
SUPPRIMER QUESTION 10

EXPORTER RAPPORT

RECOMMENCER SESSION

QUITTER
```

---

# 18. Commandes invalides de référence

Les commandes suivantes doivent être rejetées :

```text
AFFICHER QUESTION

MODIFIER STATISTIQUES

LANCER QUESTION

AJOUTER STATISTIQUES

SUPPRIMER RAPPORT

QUITTER QUESTION
```

Elles permettent de vérifier le comportement du parseur face aux erreurs syntaxiques.

---

# 19. Conclusion

La chaîne d'analyse LL(1) du système est :

```text
Grammaire
    ↓
FIRST
    ↓
FOLLOW
    ↓
Table LL(1)
    ↓
Tokens
    ↓
Pile
    ↓
Lookahead
    ↓
Production
    ↓
Correspondance
    ↓
ACCEPT / ERREUR
```

Cette architecture permet de démontrer que l'analyse syntaxique n'est pas basée sur une simple succession de conditions ou de comparaisons de chaînes.

Le parseur utilise effectivement une table LL(1), une pile et des productions issues de la grammaire.

La prochaine étape consiste à renforcer les tests automatisés afin de démontrer la stabilité de cette chaîne dans différents scénarios.
