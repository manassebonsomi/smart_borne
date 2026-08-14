from unittest.mock import patch

from services.command_interaction import (
    CommandInteraction
)


# ==========================================================
# VALID
# ==========================================================

def test_valid():

    result = {
        "mode": "VALID",
        "corrected": "AFFICHER STATISTIQUES",
        "suggestion": None,
        "trace": []
    }

    response = CommandInteraction.handle(
        result
    )

    assert response["success"] is True
    assert response["accepted"] is True
    assert response["mode"] == "VALID"

    assert (
        response["command"]
        == "AFFICHER STATISTIQUES"
    )

    print(
        "PASS : VALID"
    )


# ==========================================================
# AUTO CORRECT
# ==========================================================

def test_auto_correct():

    result = {
        "mode": "AUTO_CORRECT",
        "corrected": "AFFICHER STATISTIQUES",
        "suggestion": "AFFICHER STATISTIQUES",
        "trace": []
    }

    response = CommandInteraction.handle(
        result
    )

    assert response["success"] is True
    assert response["accepted"] is True
    assert response["mode"] == "AUTO_CORRECT"

    assert (
        response["command"]
        == "AFFICHER STATISTIQUES"
    )

    print(
        "PASS : AUTO_CORRECT"
    )


# ==========================================================
# SUGGEST → OUI
# ==========================================================

@patch(
    "services.command_interaction.input",
    return_value="Oui"
)
def test_suggest_yes(mock_input):

    result = {
        "mode": "SUGGEST",
        "corrected": "AFFICHER STATISTIQ",
        "suggestion": "AFFICHER STATISTIQUES",
        "trace": []
    }

    response = CommandInteraction.handle(
        result
    )

    assert response["success"] is True
    assert response["accepted"] is True

    assert (
        response["mode"]
        == "SUGGEST_ACCEPTED"
    )

    assert (
        response["command"]
        == "AFFICHER STATISTIQUES"
    )

    print(
        "PASS : SUGGEST → OUI"
    )


# ==========================================================
# SUGGEST → NON
# ==========================================================

@patch(
    "services.command_interaction.input",
    return_value="Non"
)
def test_suggest_no(mock_input):

    result = {
        "mode": "SUGGEST",
        "corrected": "AFFICHER STATISTIQ",
        "suggestion": "AFFICHER STATISTIQUES",
        "trace": []
    }

    response = CommandInteraction.handle(
        result
    )

    assert response["success"] is False
    assert response["accepted"] is False

    assert (
        response["mode"]
        == "REFORMULATE"
    )

    assert (
        response["command"]
        is None
    )

    print(
        "PASS : SUGGEST → NON"
    )


# ==========================================================
# REFORMULATE
# ==========================================================

def test_reformulate():

    result = {
        "mode": "REFORMULATE",
        "corrected": None,
        "suggestion": None,
        "trace": []
    }

    response = CommandInteraction.handle(
        result
    )

    assert response["success"] is False
    assert response["accepted"] is False

    assert (
        response["mode"]
        == "REFORMULATE"
    )

    print(
        "PASS : REFORMULATE"
    )


# ==========================================================
# TRACE
# ==========================================================

def test_trace():

    result = {
        "mode": "SUGGEST_ACCEPTED",
        "success": True,
        "accepted": True,
        "command": "AFFICHER STATISTIQUES",
        "trace": [
            "Suggestion acceptée."
        ]
    }

    trace = CommandInteraction.trace(
        result
    )

    assert (
        trace["component"]
        == "CommandInteraction"
    )

    assert (
        trace["mode"]
        == "SUGGEST_ACCEPTED"
    )

    assert (
        trace["accepted"]
        is True
    )

    assert (
        trace["command"]
        == "AFFICHER STATISTIQUES"
    )

    print(
        "PASS : TRACE"
    )


# ==========================================================
# EXECUTION
# ==========================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print(
        "TEST COMMAND INTERACTION"
    )
    print("=" * 70)
    print()

    test_valid()
    test_auto_correct()
    test_suggest_yes()
    test_suggest_no()
    test_reformulate()
    test_trace()

    print()
    print("=" * 70)
    print(
        "TOUS LES TESTS COMMAND INTERACTION "
        "SONT PASSÉS"
    )
    print("=" * 70)