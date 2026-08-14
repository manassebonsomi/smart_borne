# tests/unit/test_recommendation.py

import pytest

from services.recommendation_engine import RecommendationEngine


# ==========================================================
# OUTIL
# ==========================================================

def generate(age, niveau_scolaire, reponses):
    return RecommendationEngine.generate(
        age,
        niveau_scolaire,
        reponses
    )


# ==========================================================
# STRUCTURE DU RÉSULTAT
# ==========================================================

def test_resultat_structure():

    result = generate(
        11,
        "6eme",
        [
            "J'aime les jeux",
            "J'aime l'animation"
        ]
    )

    assert isinstance(result, dict)

    assert "parcours" in result
    assert "scores" in result
    assert "score_final" in result

    assert isinstance(
        result["scores"],
        dict
    )

    assert isinstance(
        result["score_final"],
        (int, float)
    )


# ==========================================================
# LES 5 PARCOURS DOIVENT ÊTRE PRÉSENTS
# ==========================================================

def test_cinq_parcours():

    result = generate(
        20,
        "universite",
        []
    )

    scores = result["scores"]

    parcours = [
        "Découverte Numérique",
        "Scratch Junior",
        "Scratch Avancé",
        "Python Débutant",
        "Mentor Junior"
    ]

    for parcours_name in parcours:

        assert parcours_name in scores


# ==========================================================
# RÈGLES D'ÂGE
# ==========================================================

@pytest.mark.parametrize(
    "age, parcours_attendu",
    [
        (7, "Découverte Numérique"),
        (8, "Scratch Junior"),
        (10, "Scratch Junior"),
        (11, "Scratch Avancé"),
        (13, "Scratch Avancé"),
        (14, "Python Débutant"),
        (16, "Python Débutant"),
        (17, "Mentor Junior"),
        (25, "Mentor Junior"),
    ]
)
def test_regle_age(age, parcours_attendu):

    result = generate(
        age,
        "universite",
        []
    )

    assert (
        result["parcours"]
        ==
        parcours_attendu
    )


# ==========================================================
# ÂGE — POIDS +40
# ==========================================================

@pytest.mark.parametrize(
    "age, parcours_attendu",
    [
        (7, "Découverte Numérique"),
        (8, "Scratch Junior"),
        (11, "Scratch Avancé"),
        (14, "Python Débutant"),
        (17, "Mentor Junior"),
    ]
)
def test_score_age(age, parcours_attendu):

    result = generate(
        age,
        "universite",
        []
    )

    assert (
        result["scores"][parcours_attendu]
        >=
        40
    )


# ==========================================================
# NIVEAU SCOLAIRE — DÉCOUVERTE
# ==========================================================

@pytest.mark.parametrize(
    "niveau",
    [
        "1ere",
        "2eme",
        "3eme",
    ]
)
def test_niveau_decouverte(niveau):

    result = generate(
        20,
        niveau,
        []
    )

    assert (
        result["scores"]["Découverte Numérique"]
        >=
        20
    )


# ==========================================================
# NIVEAU SCOLAIRE — SCRATCH JUNIOR
# ==========================================================

@pytest.mark.parametrize(
    "niveau",
    [
        "4eme",
        "5eme",
        "6eme",
    ]
)
def test_niveau_scratch_junior(niveau):

    result = generate(
        20,
        niveau,
        []
    )

    assert (
        result["scores"]["Scratch Junior"]
        >=
        20
    )


# ==========================================================
# NIVEAU SCOLAIRE — SCRATCH AVANCÉ
# ==========================================================

@pytest.mark.parametrize(
    "niveau",
    [
        "7eme",
        "8eme",
    ]
)
def test_niveau_scratch_avance(niveau):

    result = generate(
        20,
        niveau,
        []
    )

    assert (
        result["scores"]["Scratch Avancé"]
        >=
        20
    )


# ==========================================================
# NIVEAU SCOLAIRE — PYTHON
# ==========================================================

@pytest.mark.parametrize(
    "niveau",
    [
        "1ere secondaire",
        "2eme secondaire",
    ]
)
def test_niveau_python(niveau):

    result = generate(
        20,
        niveau,
        []
    )

    assert (
        result["scores"]["Python Débutant"]
        >=
        20
    )


# ==========================================================
# NIVEAU SCOLAIRE — MENTOR
# ==========================================================

def test_niveau_mentor():

    result = generate(
        20,
        "universite",
        []
    )

    assert (
        result["scores"]["Mentor Junior"]
        >=
        20
    )


# ==========================================================
# MOT-CLÉ : JEU
# ==========================================================

def test_reponse_jeu():

    result = generate(
        20,
        "universite",
        [
            "J'aime les jeux"
        ]
    )

    assert (
        result["scores"]["Scratch Junior"]
        >=
        15
    )

    assert (
        result["scores"]["Scratch Avancé"]
        >=
        10
    )


# ==========================================================
# MOT-CLÉ : ANIMATION
# ==========================================================

def test_reponse_animation():

    result = generate(
        20,
        "universite",
        [
            "J'aime l'animation"
        ]
    )

    assert (
        result["scores"]["Scratch Junior"]
        >=
        15
    )

    assert (
        result["scores"]["Scratch Avancé"]
        >=
        10
    )


# ==========================================================
# MOT-CLÉ : PROGRAMMER
# ==========================================================

def test_reponse_programmer():

    result = generate(
        20,
        "universite",
        [
            "Je veux programmer"
        ]
    )

    assert (
        result["scores"]["Python Débutant"]
        >=
        20
    )


# ==========================================================
# MOT-CLÉ : PROBLÈME
# ==========================================================

def test_reponse_probleme():

    result = generate(
        20,
        "universite",
        [
            "J'aime résoudre des problèmes"
        ]
    )

    assert (
        result["scores"]["Python Débutant"]
        >=
        15
    )

    assert (
        result["scores"]["Mentor Junior"]
        >=
        10
    )


# ==========================================================
# MOT-CLÉ : ENSEIGNER
# ==========================================================

def test_reponse_enseigner():

    result = generate(
        20,
        "universite",
        [
            "J'aimerais enseigner"
        ]
    )

    assert (
        result["scores"]["Mentor Junior"]
        >=
        20
    )


# ==========================================================
# MOT-CLÉ : CRÉER
# ==========================================================

def test_reponse_creer():

    result = generate(
        20,
        "universite",
        [
            "J'aime créer"
        ]
    )

    assert (
        result["scores"]["Scratch Avancé"]
        >=
        15
    )


# ==========================================================
# COMBINAISON ÂGE + NIVEAU + RÉPONSES
# ==========================================================

def test_combinaison_complete():

    result = generate(
        11,
        "6eme",
        [
            "J'aime les jeux",
            "J'aime créer",
            "J'aime l'animation"
        ]
    )

    assert result["parcours"] == (
        "Scratch Avancé"
    )

    assert (
        result["scores"]["Scratch Avancé"]
        >=
        40
    )


# ==========================================================
# SCORE FINAL
# ==========================================================

def test_score_final():

    result = generate(
        11,
        "6eme",
        [
            "J'aime les jeux"
        ]
    )

    assert (
        result["score_final"]
        ==
        result["scores"][result["parcours"]]
    )


# ==========================================================
# RÉPONSES VIDES
# ==========================================================

def test_reponses_vides():

    result = generate(
        11,
        "6eme",
        []
    )

    assert result["parcours"] is not None

    assert isinstance(
        result["scores"],
        dict
    )

    assert (
        result["score_final"]
        >=
        0
    )


# ==========================================================
# UNE SEULE RÉPONSE
# ==========================================================

def test_une_reponse():

    result = generate(
        14,
        "1ere secondaire",
        [
            "Je veux programmer"
        ]
    )

    assert result["parcours"] == (
        "Python Débutant"
    )


# ==========================================================
# PLUSIEURS RÉPONSES
# ==========================================================

def test_plusieurs_reponses():

    result = generate(
        17,
        "universite",
        [
            "Je veux programmer",
            "J'aime résoudre des problèmes",
            "J'aimerais enseigner"
        ]
    )

    assert result["parcours"] == (
        "Mentor Junior"
    )

    assert (
        result["scores"]["Python Débutant"]
        >=
        20
    )

    assert (
        result["scores"]["Mentor Junior"]
        >=
        30
    )


# ==========================================================
# STABILITÉ
# ==========================================================

def test_recommandation_stable():

    arguments = (
        11,
        "6eme",
        [
            "J'aime les jeux",
            "J'aime créer"
        ]
    )

    result1 = generate(*arguments)
    result2 = generate(*arguments)

    assert result1 == result2


# ==========================================================
# TYPE DU PARCOURS
# ==========================================================

def test_parcours_string():

    result = generate(
        11,
        "6eme",
        []
    )

    assert isinstance(
        result["parcours"],
        str
    )


# ==========================================================
# SCORES NUMÉRIQUES
# ==========================================================

def test_scores_numeriques():

    result = generate(
        11,
        "6eme",
        [
            "J'aime les jeux"
        ]
    )

    for score in result["scores"].values():

        assert isinstance(
            score,
            (int, float)
        )