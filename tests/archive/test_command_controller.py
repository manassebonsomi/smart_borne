# test_command_controller.py

from unittest.mock import patch, MagicMock

from controllers.command_controller import CommandController


# ==========================================================
# OUTIL : COMMANDE VALIDE
# ==========================================================

def test_valid():

    with patch(
        "services.command_handler.DashboardController.statistics",
        return_value={
            "utilisateurs": 10,
            "questions": 5,
            "sessions": 3
        }
    ), patch(
        "controllers.command_controller.Commande"
    ) as mock_commande, patch(
        "controllers.command_controller.db.session"
    ) as mock_session, patch(
        "controllers.command_controller.AuditService.log"
    ) as mock_audit:

        commande_instance = MagicMock()
        commande_instance.id_commande = 1

        mock_commande.return_value = (
            commande_instance
        )

        result = CommandController.execute(
            "AFFICHER STATISTIQUES"
        )

    assert result["success"] is True

    assert result["mode"] == "VALID"

    assert (
        result["execution"]["action"]
        ==
        "AFFICHER_STATISTIQUES"
    )

    assert (
        result["execution"]["success"]
        is True
    )

    assert (
        result["commande_id"]
        ==
        1
    )

    mock_session.add.assert_called_once()

    mock_session.commit.assert_called_once()

    mock_audit.assert_called_once()

    print(
        "PASS : CONTROLLER VALID"
    )


# ==========================================================
# AUTO CORRECT
# ==========================================================

def test_auto_correct():

    with patch(
        "services.command_handler.DashboardController.statistics",
        return_value={
            "utilisateurs": 10,
            "questions": 5,
            "sessions": 3
        }
    ), patch(
        "controllers.command_controller.Commande"
    ) as mock_commande, patch(
        "controllers.command_controller.db.session"
    ) as mock_session, patch(
        "controllers.command_controller.AuditService.log"
    ):

        commande_instance = MagicMock()
        commande_instance.id_commande = 2

        mock_commande.return_value = (
            commande_instance
        )

        result = CommandController.execute(
            "AFFICHER STATISTIQUESS"
        )

    assert (
        result["success"]
        is True
    )

    assert (
        result["mode"]
        ==
        "AUTO_CORRECT"
    )

    assert (
        result["corrected"]
        ==
        "AFFICHER STATISTIQUES"
    )

    assert (
        result["execution"]["action"]
        ==
        "AFFICHER_STATISTIQUES"
    )

    assert (
        result["execution"]["success"]
        is True
    )

    mock_session.add.assert_called_once()

    mock_session.commit.assert_called_once()

    print(
        "PASS : CONTROLLER AUTO_CORRECT"
    )


# ==========================================================
# SUGGEST
# ==========================================================

def test_suggest():

    with patch(
        "controllers.command_controller.Commande"
    ) as mock_commande, patch(
        "controllers.command_controller.db.session"
    ) as mock_session, patch(
        "controllers.command_controller.AuditService.log"
    ):

        result = CommandController.execute(
            "AFFICHER STATISTIQ"
        )

    assert (
        result["success"]
        is False
    )

    assert (
        result["mode"]
        ==
        "SUGGEST"
    )

    assert (
        result["requires_confirmation"]
        is True
    )

    assert (
        "STATISTIQUES"
        in
        result["suggestion"]
    )

    # ------------------------------------------------------
    # Très important :
    # aucune action métier ne doit être exécutée.
    # La commande ne doit pas encore être enregistrée
    # comme exécutée.
    # ------------------------------------------------------

    mock_commande.assert_not_called()

    mock_session.add.assert_not_called()

    mock_session.commit.assert_not_called()

    print(
        "PASS : CONTROLLER SUGGEST"
    )


# ==========================================================
# REFORMULATE
# ==========================================================

def test_reformulate():

    with patch(
        "controllers.command_controller.Commande"
    ) as mock_commande, patch(
        "controllers.command_controller.db.session"
    ) as mock_session:

        result = CommandController.execute(
            "BONJOUR"
        )

    assert (
        result["success"]
        is False
    )

    assert (
        result["mode"]
        ==
        "REFORMULATE"
    )

    assert (
        result["requires_confirmation"]
        is False
    )

    mock_commande.assert_not_called()

    mock_session.add.assert_not_called()

    mock_session.commit.assert_not_called()

    print(
        "PASS : CONTROLLER REFORMULATE"
    )


# ==========================================================
# MODIFIER QUESTION
# ==========================================================

def test_modifier_question():

    question = MagicMock()

    question.id_question = 3

    with patch(
            "services.command_handler.QuestionController.update",
        return_value=question
    ) as mock_update, patch(
        "controllers.command_controller.Commande"
    ) as mock_commande, patch(
        "controllers.command_controller.db.session"
    ) as mock_session, patch(
        "controllers.command_controller.AuditService.log"
    ):

        commande_instance = MagicMock()

        commande_instance.id_commande = 3

        mock_commande.return_value = (
            commande_instance
        )

        result = CommandController.execute(
            "MODIFIER QUESTION 3",
            data={
                "texte_question":
                    "Question modifiée",
                "ordre_question": 2,
                "active": True
            }
        )

    assert (
        result["success"]
        is True
    )

    assert (
        result["mode"]
        ==
        "VALID"
    )

    assert (
        result["execution"]["action"]
        ==
        "MODIFIER_QUESTION"
    )

    assert (
        result["execution"]["question_id"]
        ==
        3
    )

    mock_update.assert_called_once_with(
        3,
        texte_question="Question modifiée",
        ordre_question=2,
        active=True
    )

    mock_session.add.assert_called_once()

    mock_session.commit.assert_called_once()

    print(
        "PASS : CONTROLLER MODIFIER QUESTION"
    )


# ==========================================================
# SUPPRIMER QUESTION
# ==========================================================

def test_supprimer_question():

    with patch(
        "services.command_handler.QuestionController.delete",
        return_value=True
    ) as mock_delete, patch(
        "controllers.command_controller.Commande"
    ) as mock_commande, patch(
        "controllers.command_controller.db.session"
    ) as mock_session, patch(
        "controllers.command_controller.AuditService.log"
    ):

        commande_instance = MagicMock()

        commande_instance.id_commande = 4

        mock_commande.return_value = (
            commande_instance
        )

        result = CommandController.execute(
            "SUPPRIMER QUESTION 25"
        )

    assert (
        result["success"]
        is True
    )

    assert (
        result["mode"]
        ==
        "VALID"
    )

    assert (
        result["execution"]["action"]
        ==
        "SUPPRIMER_QUESTION"
    )

    assert (
        result["execution"]["question_id"]
        ==
        25
    )

    mock_delete.assert_called_once_with(
        25
    )

    mock_session.add.assert_called_once()

    mock_session.commit.assert_called_once()

    print(
        "PASS : CONTROLLER SUPPRIMER QUESTION"
    )


# ==========================================================
# EXPORTER RAPPORT
# ==========================================================

def test_exporter_rapport():

    with patch(
        "services.command_handler.ReportController.export_pdf",
        return_value={
            "success": True,
            "filename": "rapport.pdf"
        }
    ) as mock_export, patch(
        "controllers.command_controller.Commande"
    ) as mock_commande, patch(
        "controllers.command_controller.db.session"
    ) as mock_session, patch(
        "controllers.command_controller.AuditService.log"
    ):

        commande_instance = MagicMock()

        commande_instance.id_commande = 5

        mock_commande.return_value = (
            commande_instance
        )

        result = CommandController.execute(
            "EXPORTER RAPPORT"
        )

    assert (
        result["success"]
        is True
    )

    assert (
        result["execution"]["action"]
        ==
        "EXPORTER_RAPPORT"
    )

    assert (
        result["execution"]["rapport"]["filename"]
        ==
        "rapport.pdf"
    )

    mock_export.assert_called_once()

    mock_session.add.assert_called_once()

    mock_session.commit.assert_called_once()

    print(
        "PASS : CONTROLLER EXPORTER RAPPORT"
    )


# ==========================================================
# LANCER ENQUÊTE
# ==========================================================

def test_lancer_enquete():

    with patch(
        "controllers.command_controller.Commande"
    ) as mock_commande, patch(
        "controllers.command_controller.db.session"
    ) as mock_session, patch(
        "controllers.command_controller.AuditService.log"
    ):

        commande_instance = MagicMock()

        commande_instance.id_commande = 6

        mock_commande.return_value = (
            commande_instance
        )

        result = CommandController.execute(
            "LANCER ENQUETE CYBERSECURITE"
        )

    assert (
        result["success"]
        is True
    )

    assert (
        result["execution"]["action"]
        ==
        "ENQUETE_CYBERSECURITE"
    )

    assert (
        result["execution"]["etat"]
        ==
        "ENQUETE_LANCEE"
    )

    mock_session.add.assert_called_once()

    mock_session.commit.assert_called_once()

    print(
        "PASS : CONTROLLER LANCER ENQUETE"
    )

# ==========================================================
# ERREUR LEXICALE
# ==========================================================

def test_lexical_error():

    correction_result = {
        "success": True,
        "mode": "VALID",
        "original": "AFFICHER @",
        "corrected": "AFFICHER @",
        "suggestion": None,
        "suggestions": [],
        "score": 1.0,
        "trace": [
            "Commande reçue : AFFICHER @",
            "Commande considérée comme valide pour le test lexical."
        ]
    }

    with patch(
        "controllers.command_controller.CommandCorrector.correct",
        return_value=correction_result
    ), patch(
        "controllers.command_controller.Commande"
    ) as mock_commande, patch(
        "controllers.command_controller.db.session"
    ) as mock_session, patch(
        "controllers.command_controller.AuditService.log_error"
    ) as mock_log_error:

        result = CommandController.execute(
            "AFFICHER @"
        )

    assert (
        result["success"]
        is False
    )

    assert (
        result["mode"]
        ==
        "LEXICAL_ERROR"
    )

    assert (
        result["error"]
        ==
        "LEXICAL_ERROR"
    )

    assert (
        "message"
        in
        result
    )

    assert (
        result["message"]
    )

    mock_commande.assert_not_called()

    mock_session.add.assert_not_called()

    mock_session.commit.assert_not_called()

    mock_log_error.assert_called_once()

    print(
        "PASS : CONTROLLER LEXICAL ERROR"
    )

# ==========================================================
# COMMANDE VIDE
# ==========================================================

def test_empty_command():

    result = CommandController.execute(
        ""
    )

    assert (
        result["success"]
        is False
    )

    assert (
        result["mode"]
        ==
        "REFORMULATE"
    )

    print(
        "PASS : CONTROLLER EMPTY"
    )


# ==========================================================
# EXÉCUTION
# ==========================================================

if __name__ == "__main__":

    print()
    print("=" * 80)
    print(
        "TEST COMMAND CONTROLLER"
    )
    print("=" * 80)
    print()

    test_valid()

    test_auto_correct()

    test_suggest()

    test_reformulate()

    test_modifier_question()

    test_supprimer_question()

    test_exporter_rapport()

    test_lancer_enquete()

    test_lexical_error()

    test_empty_command()

    print()
    print("=" * 80)
    print(
        "TOUS LES TESTS COMMAND CONTROLLER "
        "SONT PASSÉS"
    )
    print("=" * 80)