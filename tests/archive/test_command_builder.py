from services.lexer import Lexer
from services.ll1_parser import LL1Parser
from services.command_builder import CommandBuilder


def parse_and_build(command):

    tokens = Lexer.tokenize(
        command
    )

    result = LL1Parser.parse(
        tokens,
        return_trace=True
    )

    assert result["success"] is True

    return CommandBuilder.build(
        tokens
    )


# ==========================================================
# AFFICHER
# ==========================================================

def test_afficher():

    command = parse_and_build(
        "AFFICHER STATISTIQUES"
    )

    assert command.action == "AFFICHER"

    assert command.subject == "STATISTIQUES"

    assert command.arguments == {}

    print(
        "PASS : AFFICHER STATISTIQUES"
    )


# ==========================================================
# MODIFIER
# ==========================================================

def test_modifier():

    command = parse_and_build(
        "MODIFIER QUESTION 3"
    )

    assert command.action == "MODIFIER"

    assert command.subject == "QUESTION"

    assert (
        command.arguments["numero"]
        == 3
    )

    print(
        "PASS : MODIFIER QUESTION 3"
    )


# ==========================================================
# SUPPRIMER
# ==========================================================

def test_supprimer():

    command = parse_and_build(
        "SUPPRIMER QUESTION 25"
    )

    assert command.action == "SUPPRIMER"

    assert command.subject == "QUESTION"

    assert (
        command.arguments["numero"]
        == 25
    )

    print(
        "PASS : SUPPRIMER QUESTION 25"
    )


# ==========================================================
# LANCER
# ==========================================================

def test_lancer():

    command = parse_and_build(
        "LANCER ENQUETE CYBERSECURITE"
    )

    assert command.action == "LANCER"

    assert command.subject == "ENQUETE"

    assert (
        command.arguments["nom"]
        == "CYBERSECURITE"
    )

    print(
        "PASS : LANCER ENQUETE CYBERSECURITE"
    )


# ==========================================================
# EXPORTER
# ==========================================================

def test_exporter():

    command = parse_and_build(
        "EXPORTER RAPPORT"
    )

    assert command.action == "EXPORTER"

    assert command.subject == "RAPPORT"

    print(
        "PASS : EXPORTER RAPPORT"
    )


# ==========================================================
# RECOMMENCER
# ==========================================================

def test_recommencer():

    command = parse_and_build(
        "RECOMMENCER SESSION"
    )

    assert command.action == "RECOMMENCER"

    assert command.subject == "SESSION"

    print(
        "PASS : RECOMMENCER SESSION"
    )


# ==========================================================
# QUITTER
# ==========================================================

def test_quitter():

    command = parse_and_build(
        "QUITTER"
    )

    assert command.action == "QUITTER"

    assert command.subject is None

    print(
        "PASS : QUITTER"
    )


# ==========================================================
# RAW
# ==========================================================

def test_raw():

    command = parse_and_build(
        "AFFICHER STATISTIQUES"
    )

    assert (
        command.raw
        ==
        "AFFICHER STATISTIQUES"
    )

    print(
        "PASS : RAW"
    )


# ==========================================================
# DICTIONNAIRE
# ==========================================================

def test_to_dict():

    command = parse_and_build(
        "MODIFIER QUESTION 3"
    )

    data = command.to_dict()

    assert data["action"] == "MODIFIER"

    assert data["subject"] == "QUESTION"

    assert (
        data["arguments"]["numero"]
        == 3
    )

    print(
        "PASS : TO_DICT"
    )


# ==========================================================
# EXÉCUTION
# ==========================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("TEST COMMAND BUILDER")
    print("=" * 70)
    print()

    test_afficher()
    test_modifier()
    test_supprimer()
    test_lancer()
    test_exporter()
    test_recommencer()
    test_quitter()
    test_raw()
    test_to_dict()

    print()
    print("=" * 70)
    print(
        "TOUS LES TESTS COMMAND BUILDER "
        "SONT PASSÉS"
    )
    print("=" * 70)