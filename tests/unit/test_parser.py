import pytest

from services.lexer import Lexer
from services.ll1_parser import LL1Parser


# ==========================================================
# OUTIL
# ==========================================================

def parse(command):

    tokens = Lexer.tokenize(command)

    return LL1Parser.parse(
        tokens,
        return_trace=True
    )


# ==========================================================
# COMMANDES VALIDES
# ==========================================================

@pytest.mark.parametrize(
    "command",
    [
        "AFFICHER STATISTIQUES",
        "AFFICHER ERREURS",
        "LANCER ENQUETE CYBERSECURITE",
        "LANCER CAMPAGNE ECOLE",
        "CHERCHER ENFANTS KINSHASA",
        "CHERCHER ADOLESCENTS INTERESSES PAR PYTHON",
        "AJOUTER QUESTION",
        "MODIFIER QUESTION 3",
        "SUPPRIMER QUESTION 25",
        "EXPORTER RAPPORT",
        "RECOMMENCER SESSION",
        "QUITTER",
    ]
)
def test_valid_commands(command):

    result = parse(command)

    assert result["success"] is True
    assert result["errors"] == []


# ==========================================================
# NUMERO
# ==========================================================

def test_modifier_question_numero():

    result = parse(
        "MODIFIER QUESTION 3"
    )

    assert result["success"] is True


def test_supprimer_question_numero():

    result = parse(
        "SUPPRIMER QUESTION 25"
    )

    assert result["success"] is True


# ==========================================================
# COMMANDE INCOMPLETE
# ==========================================================

def test_incomplete_afficher():

    result = parse(
        "AFFICHER"
    )

    assert result["success"] is False
    assert result["error"] == "SYNTAX_ERROR"


def test_incomplete_modifier():

    result = parse(
        "MODIFIER QUESTION"
    )

    assert result["success"] is False
    assert result["error"] == "SYNTAX_ERROR"


def test_incomplete_lancer():

    result = parse(
        "LANCER"
    )

    assert result["success"] is False
    assert result["error"] == "SYNTAX_ERROR"


# ==========================================================
# ORDRE INCORRECT
# ==========================================================

def test_wrong_order():

    result = parse(
        "STATISTIQUES AFFICHER"
    )

    assert result["success"] is False
    assert result["error"] == "SYNTAX_ERROR"


# ==========================================================
# TOKEN INATTENDU
# ==========================================================

def test_unexpected_token():

    result = parse(
        "AFFICHER STATISTIQUES QUESTION"
    )

    assert result["success"] is False
    assert result["error"] == "SYNTAX_ERROR"


# ==========================================================
# MAUVAIS NUMERO
# ==========================================================

def test_modifier_question_without_number():

    tokens = Lexer.tokenize(
        "MODIFIER QUESTION"
    )

    result = LL1Parser.parse(
        tokens,
        return_trace=True
    )

    assert result["success"] is False
    assert result["error"] == "SYNTAX_ERROR"


# ==========================================================
# TRACE
# ==========================================================

def test_parser_trace():

    result = parse(
        "AFFICHER STATISTIQUES"
    )

    assert result["success"] is True
    assert "trace" in result
    assert isinstance(
        result["trace"],
        list
    )

    assert len(
        result["trace"]
    ) > 0


# ==========================================================
# EMPTY INPUT
# ==========================================================

def test_empty_tokens():

    result = LL1Parser.parse(
        [],
        return_trace=True
    )

    assert result["success"] is False
    assert result["error"] == "EMPTY_INPUT"


# ==========================================================
# CASE INSENSITIVE
# ==========================================================

def test_parser_case_insensitive():

    result = parse(
        "afficher statistiques"
    )

    assert result["success"] is True