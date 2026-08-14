import pytest
from unittest.mock import patch, MagicMock

from services.command_corrector import CommandCorrector
from services.lexer import Lexer, LexerError
from services.ll1_parser import LL1Parser
from services.command_builder import CommandBuilder
from services.command_dispatcher import CommandDispatcher
from services.command_handler import CommandHandler


def build_command(text):
    """
    Lexer → Parser → Builder
    """

    tokens = Lexer.tokenize(text)

    parser_result = LL1Parser.parse(
        tokens,
        return_trace=True
    )

    assert parser_result["success"] is True

    return CommandBuilder.build(tokens)


def run_pipeline(text, data=None):
    """
    Corrector → Lexer → Parser → Builder → Dispatcher → Handler
    """

    correction = CommandCorrector.correct(text)

    return correction

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
def test_commandes_valides(command):

    correction = CommandCorrector.correct(command)

    assert correction["mode"] == "VALID"
    assert correction["success"] is True


def test_auto_correct():

    result = CommandCorrector.correct(
        "AFFICHER STATISTIQ"
    )

    assert result["mode"] == "SUGGEST" or \
           result["mode"] == "AUTO_CORRECT"

    assert result["suggestion"] is not None or \
           result["corrected"] is not None


def test_suggestion():

    result = CommandCorrector.correct(
        "AFFICHER STATISTIQ"
    )

    assert result["mode"] == "SUGGEST"

    assert result["success"] is True

    assert result["suggestion"] == (
        "AFFICHER STATISTIQUES"
    )


def test_reformulation():

    result = CommandCorrector.correct(
        "XYZ ABC"
    )

    assert result["mode"] == "REFORMULATE"

    assert result["success"] is False

@pytest.mark.parametrize(
    "command",
    [
        "",
        "   ",
        None,
    ]
)
def test_commande_vide(command):

    result = CommandCorrector.correct(command)

    assert result["success"] is False
    assert result["mode"] == "REFORMULATE"


def test_builder_afficher():

    command = build_command(
        "AFFICHER STATISTIQUES"
    )

    assert command.action == "AFFICHER"
    assert command.subject == "STATISTIQUES"
    assert command.arguments == {}


def test_builder_modifier():

    command = build_command(
        "MODIFIER QUESTION 3"
    )

    assert command.action == "MODIFIER"
    assert command.subject == "QUESTION"

    assert command.arguments["numero"] == 3


def test_builder_supprimer():

    command = build_command(
        "SUPPRIMER QUESTION 25"
    )

    assert command.action == "SUPPRIMER"
    assert command.subject == "QUESTION"

    assert command.arguments["numero"] == 25


def test_builder_lancer():

    command = build_command(
        "LANCER ENQUETE CYBERSECURITE"
    )

    assert command.action == "LANCER"
    assert command.subject == "ENQUETE"

    assert command.arguments["nom"] == (
        "CYBERSECURITE"
    )


def test_builder_exporter():

    command = build_command(
        "EXPORTER RAPPORT"
    )

    assert command.action == "EXPORTER"
    assert command.subject == "RAPPORT"


def test_builder_recommencer():

    command = build_command(
        "RECOMMENCER SESSION"
    )

    assert command.action == "RECOMMENCER"
    assert command.subject == "SESSION"


def test_builder_quitter():

    command = build_command(
        "QUITTER"
    )

    assert command.action == "QUITTER"
    assert command.subject is None


@pytest.mark.parametrize(
    "command_text, expected_action",
    [
        (
            "AFFICHER STATISTIQUES",
            "AFFICHER_STATISTIQUES"
        ),
        (
            "EXPORTER RAPPORT",
            "EXPORTER_RAPPORT"
        ),
        (
            "QUITTER",
            "QUITTER"
        ),
    ]
)
def test_dispatcher(command_text, expected_action):

    command = build_command(command_text)

    with patch.object(
        CommandHandler,
        "handle"
    ) as mock_handle:

        mock_handle.return_value = {
            "action": expected_action,
            "success": True
        }

        result = CommandDispatcher.dispatch(
            command
        )

    assert result["action"] == expected_action
    assert result["success"] is True

    mock_handle.assert_called_once()


def test_dispatcher_none():

    result = CommandDispatcher.dispatch(None)

    assert result["success"] is False
    assert result["action"] == "INCONNUE"


def test_dispatcher_action_inconnue():

    command = {
        "action": "ACTION_INEXISTANTE"
    }

    result = CommandDispatcher.dispatch(
        command
    )

    assert result["success"] is False
    assert result["action"] == "INCONNUE"


def test_handler_afficher_statistiques():

    handler = CommandHandler()

    command = {
        "action": "AFFICHER_STATISTIQUES"
    }

    with patch(
        "services.command_handler."
        "DashboardController.statistics",
        return_value={
            "utilisateurs": 10,
            "questions": 5,
            "sessions": 3
        }
    ) as mock_statistics:

        result = handler.handle(command)

    assert result["action"] == (
        "AFFICHER_STATISTIQUES"
    )

    assert result["success"] is True

    assert result["data"]["utilisateurs"] == 10

    mock_statistics.assert_called_once()


def test_handler_supprimer_question():

    handler = CommandHandler()

    command = {
        "action": "SUPPRIMER_QUESTION",
        "question_id": 25
    }

    with patch(
        "services.command_handler."
        "QuestionController.delete",
        return_value=True
    ) as mock_delete:

        result = handler.handle(command)

    assert result["action"] == (
        "SUPPRIMER_QUESTION"
    )

    assert result["success"] is True
    assert result["question_id"] == 25

    mock_delete.assert_called_once_with(25)


def test_handler_modifier_question_sans_donnees():

    handler = CommandHandler()

    command = {
        "action": "MODIFIER_QUESTION",
        "question_id": 3
    }

    result = handler.handle(
        command,
        data=None
    )

    assert result["action"] == (
        "MODIFIER_QUESTION"
    )

    assert result["success"] is False

    assert result["etat"] == (
        "ATTENTE_DONNEES"
    )

    assert result["show_form"] is True

    assert result["form_type"] == (
        "edit_question"
    )

    assert result["question_id"] == 3


def test_handler_ajouter_question_sans_donnees():

    handler = CommandHandler()

    command = {
        "action": "AJOUTER_QUESTION"
    }

    result = handler.handle(
        command,
        data=None
    )

    assert result["action"] == (
        "AJOUTER_QUESTION"
    )

    assert result["success"] is False

    assert result["etat"] == (
        "ATTENTE_DONNEES"
    )

    assert result["show_form"] is True

    assert result["form_type"] == (
        "add_question"
    )

def test_handler_exporter_rapport():

    handler = CommandHandler()

    command = {
        "action": "EXPORTER_RAPPORT"
    }

    with patch(
        "services.command_handler."
        "ReportController.export_pdf",
        return_value={
            "success": True,
            "filename": "rapport.pdf"
        }
    ) as mock_export:

        result = handler.handle(command)

    assert result["action"] == (
        "EXPORTER_RAPPORT"
    )

    assert result["success"] is True

    assert result["rapport"]["filename"] == (
        "rapport.pdf"
    )

    mock_export.assert_called_once()


def test_handler_recommencer_session():

    handler = CommandHandler()

    command = {
        "action": "RECOMMENCER_SESSION"
    }

    session = MagicMock()
    session.id_session = 7

    with patch(
        "services.command_handler."
        "SessionManager.get_last_session",
        return_value=session
    ) as mock_get_last, patch(
        "services.command_handler."
        "SessionManager.restart_session"
    ) as mock_restart:

        result = handler.handle(command)

    assert result["action"] == (
        "RECOMMENCER_SESSION"
    )

    assert result["success"] is True

    mock_get_last.assert_called_once_with(1)

    mock_restart.assert_called_once_with(7)


def test_handler_quitter():

    handler = CommandHandler()

    command = build_command(
        "QUITTER"
    )

    session = MagicMock()
    session.id_session = 8

    with patch(
        "services.command_handler."
        "SessionManager.get_last_session",
        return_value=session
    ) as mock_get_last, patch(
        "services.command_handler."
        "SessionManager.close_session"
    ) as mock_close:

        result = handler.handle(command)

    assert result["action"] == "QUITTER"
    assert result["success"] is True

    mock_get_last.assert_called_once_with(1)

    mock_close.assert_called_once_with(8)


def test_full_command_pipeline_valid():

    text = "AFFICHER STATISTIQUES"

    correction = CommandCorrector.correct(text)

    assert correction["mode"] == "VALID"

    tokens = Lexer.tokenize(
        correction["corrected"]
    )

    parser_result = LL1Parser.parse(
        tokens,
        return_trace=True
    )

    assert parser_result["success"] is True

    command = CommandBuilder.build(
        tokens
    )

    assert command.action == "AFFICHER"

    with patch(
        "services.command_handler."
        "DashboardController.statistics",
        return_value={
            "utilisateurs": 10,
            "questions": 5,
            "sessions": 3
        }
    ):

        result = CommandDispatcher.dispatch(
            command
        )

    assert result["success"] is True

    assert result["action"] == (
        "AFFICHER_STATISTIQUES"
    )


def test_full_command_pipeline_suggestion():

    text = "AFFICHER STATISTIQ"

    correction = CommandCorrector.correct(
        text
    )

    assert correction["mode"] == "SUGGEST"

    assert correction["success"] is True

    assert correction["suggestion"] == (
        "AFFICHER STATISTIQUES"
    )


def test_full_command_pipeline_reformulate():

    text = "XYZ ABC"

    correction = CommandCorrector.correct(
        text
    )

    assert correction["mode"] == (
        "REFORMULATE"
    )

    assert correction["success"] is False


@pytest.mark.parametrize(
    "text, numero",
    [
        (
            "MODIFIER QUESTION 3",
            3
        ),
        (
            "SUPPRIMER QUESTION 25",
            25
        ),
    ]
)
def test_command_question_numero(text, numero):

    command = build_command(text)

    assert command.arguments["numero"] == numero


def test_command_case_insensitive():

    correction = CommandCorrector.correct(
        "afficher statistiques"
    )

    assert correction["mode"] == "VALID"

    assert correction["corrected"] == (
        "AFFICHER STATISTIQUES"
    )


def test_command_trace():

    correction = CommandCorrector.correct(
        "AFFICHER STATISTIQ"
    )

    assert "trace" in correction

    assert isinstance(
        correction["trace"],
        list
    )

    assert len(
        correction["trace"]
    ) > 0