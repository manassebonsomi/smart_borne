import pytest

from services.lexer import Lexer, LexerError
from services.grammar import EOF


def test_tokenize_afficher_statistiques():

    tokens = Lexer.tokenize(
        "AFFICHER STATISTIQUES"
    )

    assert tokens[0].type == "AFFICHER"
    assert tokens[1].type == "STATISTIQUES"
    assert tokens[-1].type == EOF


def test_tokenize_numero():

    tokens = Lexer.tokenize(
        "MODIFIER QUESTION 25"
    )

    assert tokens[0].type == "MODIFIER"
    assert tokens[1].type == "QUESTION"
    assert tokens[2].type == "NUMERO"
    assert tokens[2].value == "25"
    assert tokens[-1].type == EOF

def test_tokenize_lancer_enquete():

    tokens = Lexer.tokenize(
        "LANCER ENQUETE CYBERSECURITE"
    )

    types = [
        token.type
        for token in tokens
    ]

    assert types == [
        "LANCER",
        "ENQUETE",
        "CYBERSECURITE",
        EOF
    ]


def test_tokenize_ignore_spaces():

    tokens = Lexer.tokenize(
        "   AFFICHER     STATISTIQUES   "
    )

    types = [
        token.type
        for token in tokens
    ]

    assert types == [
        "AFFICHER",
        "STATISTIQUES",
        EOF
    ]


def test_tokenize_case_insensitive():

    tokens = Lexer.tokenize(
        "afficher statistiques"
    )

    assert tokens[0].type == "AFFICHER"
    assert tokens[1].type == "STATISTIQUES"


def test_tokenize_empty():

    tokens = Lexer.tokenize("")

    assert len(tokens) == 1
    assert tokens[0].type == EOF


def test_tokenize_none():

    with pytest.raises(LexerError):

        Lexer.tokenize(None)


def test_unknown_word():

    with pytest.raises(LexerError):

        Lexer.tokenize(
            "AFFICHER INCONNU"
        )


def test_invalid_character():

    with pytest.raises(LexerError):

        Lexer.tokenize(
            "AFFICHER @"
        )


def test_word_with_number():

    with pytest.raises(LexerError):

        Lexer.tokenize(
            "AFFICHER STATISTIQUES123"
        )