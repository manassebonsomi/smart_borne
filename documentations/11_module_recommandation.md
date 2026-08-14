# Module recommandation — CCC Orientation System

Le **RecommendationEngine** permet de déterminer le parcours le plus adapté au profil du bénéficiaire à partir de son âge, de son niveau scolaire et de ses réponses au questionnaire.

## 1. Fonction principale

La méthode principale est :

```python
RecommendationEngine.generate(
    age,
    niveau_scolaire,
    reponses
)
```

Elle prend en entrée :

```text
âge
niveau scolaire
réponses
```

et calcule les scores des parcours disponibles.

---

## 2. Parcours évalués

Le moteur calcule un score pour les cinq parcours suivants :

```text
Découverte Numérique
Scratch Junior
Scratch Avancé
Python Débutant
Mentor Junior
```

---

## 3. Calcul des scores

Les scores combinent trois éléments principaux :

```text
Âge
   +
Niveau scolaire
   +
Réponses au questionnaire
```

Les réponses textuelles peuvent notamment influencer le score selon les intérêts exprimés par le bénéficiaire.

Le moteur utilise donc les informations du profil et du questionnaire pour déterminer le parcours présentant le meilleur score.

---

## 4. Résultat

La méthode `generate()` retourne une structure contenant notamment :

```text
parcours
scores
score_final
```

Exemple conceptuel :

```json
{
    "parcours": "Scratch Avancé",
    "scores": {
        "Découverte Numérique": 20,
        "Scratch Junior": 35,
        "Scratch Avancé": 50,
        "Python Débutant": 30,
        "Mentor Junior": 25
    },
    "score_final": 50
}
```

`parcours` correspond au parcours recommandé et `score_final` correspond au score obtenu par ce parcours.

---

## 5. Exemple d'utilisation

```python
result = RecommendationEngine.generate(
    11,
    "6eme",
    [
        "J'aime les jeux",
        "J'aime créer"
    ]
)
```

Le résultat permet ensuite d'obtenir :

```python
result["parcours"]
result["scores"]
result["score_final"]
```

---

## 6. Validation du module

Le moteur de recommandation dispose d'une suite de tests dédiée :

```text
tests/unit/test_recommendation.py
```

La dernière exécution validée donne :

```text
41 tests passés
0 échec
```

Le module de recommandation est ainsi couvert par des tests portant notamment sur :

- la structure du résultat ;
- les cinq parcours ;
- les règles liées à l'âge ;
- le niveau scolaire ;
- les réponses textuelles ;
- les combinaisons de critères ;
- le score final ;
- la stabilité des recommandations.

---

## 7. Intégration dans le système

Le moteur de recommandation s'intègre au processus général d'orientation :

```text
Utilisateur
    ↓
Questionnaire
    ↓
Réponses
    ↓
RecommendationEngine
    ↓
Calcul des scores
    ↓
Parcours recommandé
```

Le module constitue donc le composant chargé de transformer les informations collectées pendant le questionnaire en une recommandation de parcours.