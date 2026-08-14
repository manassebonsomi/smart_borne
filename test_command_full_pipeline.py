from unittest.mock import patch, MagicMock

from services.command_corrector import CommandCorrector
from services.lexer import Lexer
from services.ll1_parser import LL1Parser
from services.command_builder import CommandBuilder
from services.command_dispatcher import CommandDispatcher



def execute_pipeline(command_text, data=None):
    """
    Exécute la chaîne complète :

        Corrector
        ↓
        Lexer
        ↓
        Parser LL(1)
        ↓
        CommandBuilder
        ↓
        CommandDispatcher
        ↓
        CommandHandler
    """

    # ------------------------------------------------------
    # 1. CORRECTEUR
    # ------------------------------------------------------

    correction = CommandCorrector.correct(
        command_text
    )

    # ------------------------------------------------------
    # SUGGEST / REFORMULATE
    # ------------------------------------------------------

    if correction["mode"] in (
        "SUGGEST",
        "REFORMULATE"
    ):

        return {
            "stage": "CORRECTOR",
            "correction": correction,
            "result": None
        }

    corrected_command = correction.get(
        "corrected"
    )

    if not corrected_command:

        return {
            "stage": "CORRECTOR",
            "correction": correction,
            "result": None
        }

    tokens = Lexer.tokenize(
        corrected_command
    )


    parsed = LL1Parser.parse(
        tokens,
        return_trace=True
    )

    if not parsed["success"]:

        return {
            "stage": "PARSER",
            "correction": correction,
            "tokens": tokens,
            "parser": parsed,
            "result": None
        }


    command = CommandBuilder.build(
        tokens
    )

    result = CommandDispatcher.dispatch(
        command,
        data=data
    )

    return {
        "stage": "HANDLER",
        "correction": correction,
        "tokens": tokens,
        "parser": parsed,
        "command": command,
        "result": result
    }


def test_valid_command():

    with patch(
        "services.command_handler.DashboardController.statistics",
        return_value={
            "utilisateurs": 10,
            "questions": 5,
            "sessions": 3
        }
    ):

        result = execute_pipeline(
            "AFFICHER STATISTIQUES"
        )

    assert (
        result["correction"]["mode"]
        ==
        "VALID"
    )

    assert (
        result["parser"]["success"]
        is True
    )

    assert (
        result["command"].action
        ==
        "AFFICHER"
    )

    assert (
        result["command"].subject
        ==
        "STATISTIQUES"
    )

    assert (
        result["result"]["action"]
        ==
        "AFFICHER_STATISTIQUES"
    )

    assert (
        result["result"]["success"]
        is True
    )

    assert (
        result["result"]["data"]["utilisateurs"]
        ==
        10
    )

    print(
        "PASS : VALID → CORRECTOR → LEXER → "
        "PARSER → BUILDER → DISPATCHER → HANDLER"
    )


def test_auto_correct():

    with patch(
        "services.command_handler.DashboardController.statistics",
        return_value={
            "utilisateurs": 10,
            "questions": 5,
            "sessions": 3
        }
    ):

        result = execute_pipeline(
            "AFFICHER STATISTIQUESS"
        )

    assert (
        result["correction"]["mode"]
        ==
        "AUTO_CORRECT"
    )

    assert (
        "AFFICHER STATISTIQUES"
        ==
        result["correction"]["corrected"]
    )

    assert (
        result["parser"]["success"]
        is True
    )

    assert (
        result["command"].action
        ==
        "AFFICHER"
    )

    assert (
        result["command"].subject
        ==
        "STATISTIQUES"
    )

    assert (
        result["result"]["action"]
        ==
        "AFFICHER_STATISTIQUES"
    )

    assert (
        result["result"]["success"]
        is True
    )

    print(
        "PASS : AUTO_CORRECT → "
        "LEXER → PARSER → BUILDER → "
        "DISPATCHER → HANDLER"
    )


def test_suggest_stops_pipeline():

    result = execute_pipeline(
        "AFFICHER STATISTIQ"
    )

    assert (
        result["correction"]["mode"]
        ==
        "SUGGEST"
    )

    assert (
        result["stage"]
        ==
        "CORRECTOR"
    )

    assert result["result"] is None

    assert (
        "STATISTIQUES"
        in
        result["correction"]["suggestion"]
    )

    print(
        "PASS : SUGGEST → ARRÊT AVANT LEXER"
    )


def test_reformulate_stops_pipeline():

    result = execute_pipeline(
        "BONJOUR"
    )

    assert (
        result["correction"]["mode"]
        ==
        "REFORMULATE"
    )

    assert (
        result["stage"]
        ==
        "CORRECTOR"
    )

    assert result["result"] is None

    print(
        "PASS : REFORMULATE → "
        "ARRÊT AVANT LEXER"
    )


def test_lancer_enquete():

    result = execute_pipeline(
        "LANCER ENQUETE CYBERSECURITE"
    )

    assert (
        result["correction"]["mode"]
        ==
        "VALID"
    )

    assert (
        result["parser"]["success"]
        is True
    )

    assert (
        result["command"].action
        ==
        "LANCER"
    )

    assert (
        result["command"].subject
        ==
        "ENQUETE"
    )

    assert (
        result["command"].arguments["nom"]
        ==
        "CYBERSECURITE"
    )

    assert (
        result["result"]["action"]
        ==
        "ENQUETE_CYBERSECURITE"
    )

    assert (
        result["result"]["success"]
        is True
    )

    assert (
        result["result"]["etat"]
        ==
        "ENQUETE_LANCEE"
    )

    print(
        "PASS : LANCER ENQUETE CYBERSECURITE"
    )


def test_modifier_question():

    question = MagicMock()
    question.id_question = 3

    with patch(
        "services.command_handler.QuestionController.update",
        return_value=question
    ) as mock_update:

        result = execute_pipeline(
            "MODIFIER QUESTION 3",
            data={
                "texte_question":
                    "Question modifiée",
                "ordre_question": 2,
                "active": True
            }
        )

    assert (
        result["correction"]["mode"]
        ==
        "VALID"
    )

    assert (
        result["parser"]["success"]
        is True
    )

    assert (
        result["command"].action
        ==
        "MODIFIER"
    )

    assert (
        result["command"].subject
        ==
        "QUESTION"
    )

    assert (
        result["command"].arguments["numero"]
        ==
        3
    )

    assert (
        result["result"]["action"]
        ==
        "MODIFIER_QUESTION"
    )

    assert (
        result["result"]["success"]
        is True
    )

    assert (
        result["result"]["question_id"]
        ==
        3
    )

    mock_update.assert_called_once_with(
        3,
        texte_question="Question modifiée",
        ordre_question=2,
        active=True
    )

    print(
        "PASS : MODIFIER QUESTION 3"
    )


def test_supprimer_question():

    with patch(
        "services.command_handler.QuestionController.delete",
        return_value=True
    ) as mock_delete:

        result = execute_pipeline(
            "SUPPRIMER QUESTION 25"
        )

    assert (
        result["correction"]["mode"]
        ==
        "VALID"
    )

    assert (
        result["parser"]["success"]
        is True
    )

    assert (
        result["command"].action
        ==
        "SUPPRIMER"
    )

    assert (
        result["command"].subject
        ==
        "QUESTION"
    )

    assert (
        result["command"].arguments["numero"]
        ==
        25
    )

    assert (
        result["result"]["action"]
        ==
        "SUPPRIMER_QUESTION"
    )

    assert (
        result["result"]["success"]
        is True
    )

    assert (
        result["result"]["question_id"]
        ==
        25
    )

    mock_delete.assert_called_once_with(
        25
    )

    print(
        "PASS : SUPPRIMER QUESTION 25"
    )


def test_exporter_rapport():

    with patch(
        "services.command_handler.ReportController.export_pdf",
        return_value={
            "success": True,
            "filename": "rapport.pdf"
        }
    ) as mock_export:

        result = execute_pipeline(
            "EXPORTER RAPPORT"
        )

    assert (
        result["correction"]["mode"]
        ==
        "VALID"
    )

    assert (
        result["parser"]["success"]
        is True
    )

    assert (
        result["command"].action
        ==
        "EXPORTER"
    )

    assert (
        result["command"].subject
        ==
        "RAPPORT"
    )

    assert (
        result["result"]["action"]
        ==
        "EXPORTER_RAPPORT"
    )

    assert (
        result["result"]["success"]
        is True
    )

    assert (
        result["result"]["rapport"]["filename"]
        ==
        "rapport.pdf"
    )

    mock_export.assert_called_once()

    print(
        "PASS : EXPORTER RAPPORT"
    )


def test_recommencer_session():

    session = MagicMock()
    session.id_session = 7

    with patch(
        "services.command_handler.SessionManager.get_last_session",
        return_value=session
    ) as mock_get_last, patch(
        "services.command_handler.SessionManager.restart_session"
    ) as mock_restart:

        result = execute_pipeline(
            "RECOMMENCER SESSION"
        )

    assert (
        result["correction"]["mode"]
        ==
        "VALID"
    )

    assert (
        result["parser"]["success"]
        is True
    )

    assert (
        result["command"].action
        ==
        "RECOMMENCER"
    )

    assert (
        result["command"].subject
        ==
        "SESSION"
    )

    assert (
        result["result"]["action"]
        ==
        "RECOMMENCER_SESSION"
    )

    assert (
        result["result"]["success"]
        is True
    )

    mock_get_last.assert_called_once_with(
        1
    )

    mock_restart.assert_called_once_with(
        7
    )

    print(
        "PASS : RECOMMENCER SESSION"
    )


def test_quitter():

    session = MagicMock()
    session.id_session = 8

    with patch(
        "services.command_handler.SessionManager.get_last_session",
        return_value=session
    ) as mock_get_last, patch(
        "services.command_handler.SessionManager.close_session"
    ) as mock_close:

        result = execute_pipeline(
            "QUITTER"
        )

    assert (
        result["correction"]["mode"]
        ==
        "VALID"
    )

    assert (
        result["parser"]["success"]
        is True
    )

    assert (
        result["command"].action
        ==
        "QUITTER"
    )

    assert (
        result["command"].subject
        is None
    )

    assert (
        result["result"]["action"]
        ==
        "QUITTER"
    )

    assert (
        result["result"]["success"]
        is True
    )

    mock_get_last.assert_called_once_with(
        1
    )

    mock_close.assert_called_once_with(
        8
    )

    print(
        "PASS : QUITTER"
    )


def test_trace_complete():

    with patch(
        "services.command_handler.DashboardController.statistics",
        return_value={
            "utilisateurs": 10,
            "questions": 5,
            "sessions": 3
        }
    ):

        result = execute_pipeline(
            "AFFICHER STATISTIQUES"
        )


    assert (
        "trace"
        in
        result["correction"]
    )

    assert (
        len(
            result["correction"]["trace"]
        )
        > 0
    )


    assert (
        "trace"
        in
        result["parser"]
    )

    assert (
        len(
            result["parser"]["trace"]
        )
        > 0
    )


    assert result["command"].raw == (
        "AFFICHER STATISTIQUES"
    )


    assert (
        result["result"]["action"]
        ==
        "AFFICHER_STATISTIQUES"
    )

    assert (
        result["result"]["success"]
        is True
    )

    print(
        "PASS : TRACE COMPLÈTE"
    )


if __name__ == "__main__":

    print()
    print("=" * 80)
    print(
        "TEST COMMAND FULL PIPELINE"
    )
    print("=" * 80)
    print()

    test_valid_command()

    test_auto_correct()

    test_suggest_stops_pipeline()

    test_reformulate_stops_pipeline()

    test_lancer_enquete()

    test_modifier_question()

    test_supprimer_question()

    test_exporter_rapport()

    test_recommencer_session()

    test_quitter()

    test_trace_complete()

    print()
    print("=" * 80)
    print(
        "RÉSUMÉ FINAL"
    )
    print("=" * 80)

    print()
    print(
        "TOUS LES TESTS DU PIPELINE "
        "COMPLET SONT PASSÉS"
    )

    print("=" * 80)