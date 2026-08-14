import pytest
from unittest.mock import patch

from app import app
from config.database import db


# ==========================================================
# FIXTURE APPLICATION
# ==========================================================

@pytest.fixture
def client():

    app.config["TESTING"] = True

    with app.app_context():

        yield app.test_client()


# ==========================================================
# OUTIL
# ==========================================================

def execute_command(client, command, data=None):

    payload = {
        "command": command
    }

    if data is not None:
        payload["data"] = data

    return client.post(
        "/api/commands/execute",
        json=payload
    )


# ==========================================================
# COMMANDE VALIDE
# ==========================================================

def test_integration_commande_valide(client):

    response = execute_command(
        client,
        "AFFICHER STATISTIQUES"
    )

    assert response.status_code in (
        200,
        201
    )

    result = response.get_json()

    assert isinstance(
        result,
        dict
    )

    assert "success" in result


# ==========================================================
# SUGGESTION
# ==========================================================

def test_integration_suggestion(client):

    response = execute_command(
        client,
        "AFFICHER STATISTIQ"
    )

    assert response.status_code == 200

    result = response.get_json()

    assert result["mode"] == "SUGGEST"

    assert result["suggestion"] == (
        "AFFICHER STATISTIQUES"
    )

    assert result["requires_confirmation"] is True


# ==========================================================
# ERREUR LEXICALE
# ==========================================================

def test_integration_erreur_lexicale(client):

    response = execute_command(
        client,
        "AFFICHER @"
    )

    assert response.status_code in (
        200,
        400
    )

    result = response.get_json()

    assert isinstance(
        result,
        dict
    )

    assert result["success"] is False

    # Le correcteur peut intercepter la commande
    # avant le Lexer et proposer une reformulation.
    assert result["mode"] in (
        "LEXICAL_ERROR",
        "REFORMULATE"
    )

    if result["mode"] == "LEXICAL_ERROR":

        assert "error" in result

    elif result["mode"] == "REFORMULATE":

        assert (
            "suggestion" in result
            or "message" in result
            or "trace" in result
        )


# ==========================================================
# ERREUR SYNTAXIQUE
# ==========================================================

def test_integration_erreur_syntaxique(client):

    response = execute_command(
        client,
        "AFFICHER"
    )

    assert response.status_code in (
        200,
        400
    )

    result = response.get_json()

    assert isinstance(
        result,
        dict
    )

    assert result["success"] is False

    assert result["mode"] == (
        "SYNTAX_ERROR"
    )

    assert "error" in result


# ==========================================================
# COMMANDE MODIFIER QUESTION
# ==========================================================

def test_integration_modifier_question(client):

    response = execute_command(
        client,
        "MODIFIER QUESTION 3"
    )

    assert response.status_code in (
        200,
        400
    )

    result = response.get_json()

    assert isinstance(
        result,
        dict
    )

    assert "success" in result


# ==========================================================
# COMMANDE SUPPRIMER QUESTION
# ==========================================================

def test_integration_supprimer_question(client):

    response = execute_command(
        client,
        "SUPPRIMER QUESTION 999999"
    )

    assert response.status_code in (
        200,
        400
    )

    result = response.get_json()

    assert isinstance(
        result,
        dict
    )

    assert "success" in result


# ==========================================================
# COMMANDE EXPORTER RAPPORT
# ==========================================================

def test_integration_exporter_rapport(client):

    with patch(
        "services.command_handler.ReportController.export_pdf",
        return_value={
            "success": True,
            "filename": "rapport.pdf"
        }
    ):

        response = execute_command(
            client,
            "EXPORTER RAPPORT"
        )

    assert response.status_code in (
        200,
        201
    )

    result = response.get_json()

    assert isinstance(
        result,
        dict
    )

    assert "success" in result


# ==========================================================
# COMMANDE RECOMMENCER SESSION
# ==========================================================

def test_integration_recommencer_session(client):

    response = execute_command(
        client,
        "RECOMMENCER SESSION"
    )

    assert response.status_code in (
        200,
        400
    )

    result = response.get_json()

    assert isinstance(
        result,
        dict
    )

    assert "success" in result


# ==========================================================
# COMMANDE QUITTER
# ==========================================================

def test_integration_quitter(client):

    response = execute_command(
        client,
        "QUITTER"
    )

    assert response.status_code in (
        200,
        201
    )

    result = response.get_json()

    assert isinstance(
        result,
        dict
    )

    assert "success" in result


# ==========================================================
# COMMANDE VIDE
# ==========================================================

def test_integration_commande_vide(client):

    response = execute_command(
        client,
        ""
    )

    assert response.status_code in (
        200,
        400
    )

    result = response.get_json()

    assert isinstance(
        result,
        dict
    )

    assert result["success"] is False


# ==========================================================
# JSON ABSENT
# ==========================================================

def test_integration_json_absent(client):

    response = client.post(
        "/api/commands/execute"
    )

    assert response.status_code == 400

    result = response.get_json()

    assert isinstance(
        result,
        dict
    )

    assert result["success"] is False


# ==========================================================
# COMMAND ABSENTE
# ==========================================================

def test_integration_command_absente(client):

    response = client.post(
        "/api/commands/execute",
        json={}
    )

    assert response.status_code == 400

    result = response.get_json()

    assert isinstance(
        result,
        dict
    )

    assert result["success"] is False


# ==========================================================
# TYPE DE COMMAND INVALIDE
# ==========================================================

@pytest.mark.parametrize(
    "command",
    [
        123,
        True,
        [],
        {},
    ]
)
def test_integration_command_type_invalide(
    client,
    command
):

    response = execute_command(
        client,
        command
    )

    assert response.status_code == 400

    result = response.get_json()

    assert isinstance(
        result,
        dict
    )

    assert result["success"] is False


# ==========================================================
# TRACE DU PIPELINE
# ==========================================================

def test_integration_trace(client):

    response = execute_command(
        client,
        "AFFICHER STATISTIQUES"
    )

    result = response.get_json()

    assert isinstance(
        result,
        dict
    )

    if "trace" in result:

        assert isinstance(
            result["trace"],
            list
        )


# ==========================================================
# STRUCTURE RÉPONSE
# ==========================================================

def test_integration_structure_reponse(client):

    response = execute_command(
        client,
        "AFFICHER STATISTIQUES"
    )

    result = response.get_json()

    assert isinstance(
        result,
        dict
    )

    assert "success" in result
    assert "mode" in result