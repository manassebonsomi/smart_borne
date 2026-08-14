from unittest.mock import patch
from app import app

def get_client():

    app.config["TESTING"] = True

    return app.test_client()


def test_valid():

    client = get_client()

    expected = {
        "success": True,
        "mode": "VALID",
        "commande_id": 1,
        "execution": {
            "action": "AFFICHER_STATISTIQUES",
            "success": True,
            "data": {
                "utilisateurs": 10,
                "questions": 5,
                "sessions": 3
            }
        },
        "resultat": "AFFICHER_STATISTIQUES"
    }

    with patch(
        "routes.command_routes.CommandController.execute",
        return_value=expected
    ) as mock_execute:

        response = client.post(
            "/api/commands/execute",
            json={
                "command":
                    "AFFICHER STATISTIQUES"
            }
        )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True

    assert (
        data["mode"]
        ==
        "VALID"
    )

    assert (
        data["execution"]["action"]
        ==
        "AFFICHER_STATISTIQUES"
    )

    mock_execute.assert_called_once_with(
        texte_commande="AFFICHER STATISTIQUES",
        id_formateur=None,
        data=None
    )

    print(
        "PASS : ROUTE VALID"
    )


def test_auto_correct():

    client = get_client()

    expected = {
        "success": True,
        "mode": "AUTO_CORRECT",
        "commande_id": 2,
        "original":
            "AFFICHER STATISTIQUESS",
        "corrected":
            "AFFICHER STATISTIQUES",
        "execution": {
            "action":
                "AFFICHER_STATISTIQUES",
            "success": True
        },
        "resultat":
            "AFFICHER_STATISTIQUES"
    }

    with patch(
        "routes.command_routes.CommandController.execute",
        return_value=expected
    ) as mock_execute:

        response = client.post(
            "/api/commands/execute",
            json={
                "command":
                    "AFFICHER STATISTIQUESS"
            }
        )

    assert response.status_code == 200

    data = response.get_json()

    assert (
        data["mode"]
        ==
        "AUTO_CORRECT"
    )

    assert (
        data["corrected"]
        ==
        "AFFICHER STATISTIQUES"
    )

    assert (
        data["execution"]["action"]
        ==
        "AFFICHER_STATISTIQUES"
    )

    mock_execute.assert_called_once_with(
        texte_commande="AFFICHER STATISTIQUESS",
        id_formateur=None,
        data=None
    )

    print(
        "PASS : ROUTE AUTO_CORRECT"
    )


def test_suggest():

    client = get_client()

    expected = {
        "success": False,
        "mode": "SUGGEST",
        "original":
            "AFFICHER STATISTIQ",
        "suggestion":
            "AFFICHER STATISTIQUES",
        "requires_confirmation":
            True
    }

    with patch(
        "routes.command_routes.CommandController.execute",
        return_value=expected
    ) as mock_execute:

        response = client.post(
            "/api/commands/execute",
            json={
                "command":
                    "AFFICHER STATISTIQ"
            }
        )

    assert response.status_code == 200

    data = response.get_json()

    assert (
        data["success"]
        is False
    )

    assert (
        data["mode"]
        ==
        "SUGGEST"
    )

    assert (
        data["requires_confirmation"]
        is True
    )

    assert (
        "STATISTIQUES"
        in
        data["suggestion"]
    )

    mock_execute.assert_called_once_with(
        texte_commande="AFFICHER STATISTIQ",
        id_formateur=None,
        data=None
    )

    print(
        "PASS : ROUTE SUGGEST"
    )


def test_reformulate():

    client = get_client()

    expected = {
        "success": False,
        "mode": "REFORMULATE",
        "original": "BONJOUR",
        "suggestion": None,
        "requires_confirmation":
            False
    }

    with patch(
        "routes.command_routes.CommandController.execute",
        return_value=expected
    ) as mock_execute:

        response = client.post(
            "/api/commands/execute",
            json={
                "command":
                    "BONJOUR"
            }
        )

    assert response.status_code == 200

    data = response.get_json()

    assert (
        data["success"]
        is False
    )

    assert (
        data["mode"]
        ==
        "REFORMULATE"
    )

    assert (
        data["requires_confirmation"]
        is False
    )

    mock_execute.assert_called_once_with(
        texte_commande="BONJOUR",
        id_formateur=None,
        data=None
    )

    print(
        "PASS : ROUTE REFORMULATE"
    )

def test_modifier_question():

    client = get_client()

    expected = {
        "success": True,
        "mode": "VALID",
        "commande_id": 3,
        "execution": {
            "action":
                "MODIFIER_QUESTION",
            "success": True,
            "question_id": 3
        },
        "resultat":
            "MODIFIER_QUESTION"
    }

    with patch(
        "routes.command_routes.CommandController.execute",
        return_value=expected
    ) as mock_execute:

        response = client.post(
            "/api/commands/execute",
            json={
                "command":
                    "MODIFIER QUESTION 3"
            }
        )

    assert response.status_code == 200

    data = response.get_json()

    assert (
        data["success"]
        is True
    )

    assert (
        data["execution"]["action"]
        ==
        "MODIFIER_QUESTION"
    )

    assert (
        data["execution"]["question_id"]
        ==
        3
    )

    mock_execute.assert_called_once_with(
        texte_commande="MODIFIER QUESTION 3",
        id_formateur=None,
        data=None
    )

    print(
        "PASS : ROUTE MODIFIER QUESTION"
    )


def test_supprimer_question():

    client = get_client()

    expected = {
        "success": True,
        "mode": "VALID",
        "commande_id": 4,
        "execution": {
            "action":
                "SUPPRIMER_QUESTION",
            "success": True,
            "question_id": 25
        },
        "resultat":
            "SUPPRIMER_QUESTION"
    }

    with patch(
        "routes.command_routes.CommandController.execute",
        return_value=expected
    ) as mock_execute:

        response = client.post(
            "/api/commands/execute",
            json={
                "command":
                    "SUPPRIMER QUESTION 25"
            }
        )

    assert response.status_code == 200

    data = response.get_json()

    assert (
        data["success"]
        is True
    )

    assert (
        data["execution"]["action"]
        ==
        "SUPPRIMER_QUESTION"
    )

    assert (
        data["execution"]["question_id"]
        ==
        25
    )

    mock_execute.assert_called_once_with(
        texte_commande= "SUPPRIMER QUESTION 25",
        id_formateur=None,
        data=None
    )

    print(
        "PASS : ROUTE SUPPRIMER QUESTION"
    )


def test_missing_command():

    client = get_client()

    response = client.post(
        "/api/commands/execute",
        json={}
    )

    assert response.status_code == 400

    data = response.get_json()

    assert (
        data["success"]
        is False
    )

    assert (
        data["error"]
        ==
        "MISSING_COMMAND"
    )

    print(
        "PASS : ROUTE COMMAND MANQUANTE"
    )


def test_missing_json():

    client = get_client()

    response = client.post(
        "/api/commands/execute"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert (
        data["success"]
        is False
    )

    assert (
        data["error"]
        ==
        "INVALID_JSON"
    )

    print(
        "PASS : ROUTE JSON ABSENT"
    )


def test_invalid_command_type():

    client = get_client()

    response = client.post(
        "/api/commands/execute",
        json={
            "command": 123
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert (
        data["success"]
        is False
    )

    assert (
        data["error"]
        ==
        "INVALID_COMMAND"
    )

    print(
        "PASS : ROUTE COMMAND TYPE INVALIDE"
    )


if __name__ == "__main__":

    print()
    print("=" * 80)
    print(
        "TEST COMMAND ROUTES"
    )
    print("=" * 80)
    print()

    test_valid()

    test_auto_correct()

    test_suggest()

    test_reformulate()

    test_modifier_question()

    test_supprimer_question()

    test_missing_command()

    test_missing_json()

    test_invalid_command_type()

    print()
    print("=" * 80)
    print(
        "TOUS LES TESTS COMMAND ROUTES "
        "SONT PASSÉS"
    )
    print("=" * 80)