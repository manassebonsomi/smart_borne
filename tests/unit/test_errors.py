import pytest
from unittest.mock import patch

from services.lexer import Lexer, LexerError
from services.command_corrector import CommandCorrector
from services.ll1_parser import LL1Parser
from services.command_builder import CommandBuilder
from services.command_dispatcher import CommandDispatcher
from services.command_handler import CommandHandler


def build_command(text):

    tokens = Lexer.tokenize(text)

    return CommandBuilder.build(tokens)


def parse_command(text):

    tokens = Lexer.tokenize(text)

    return LL1Parser.parse(
        tokens,
        return_trace=True
    )


def test_lexer_none():

    with pytest.raises(LexerError):

        Lexer.tokenize(None)


def test_lexer_commande_vide():

    result = Lexer.tokenize("")

    assert isinstance(result, list)

    assert len(result) == 1

    assert result[-1].type == "EOF"

def test_lexer_espace_seulement():

    result = Lexer.tokenize("   ")

    assert isinstance(result, list)

    assert len(result) == 1

    assert result[-1].type == "EOF"


def test_lexer_mot_inconnu():

    with pytest.raises(LexerError):

        Lexer.tokenize(
            "AFFICHER INCONNU"
        )


def test_lexer_caractere_invalide():

    with pytest.raises(LexerError):

        Lexer.tokenize(
            "AFFICHER @"
        )


def test_lexer_word_with_number():

    with pytest.raises(LexerError):

        Lexer.tokenize(
            "QUESTION123"
        )

def test_corrector_empty():

    result = CommandCorrector.correct("")

    assert isinstance(
        result,
        dict
    )

    assert result["success"] is False


def test_corrector_none():

    result = CommandCorrector.correct(None)

    assert isinstance(
        result,
        dict
    )

    assert result["success"] is False


def test_corrector_suggestion():

    result = CommandCorrector.correct(
        "AFFICHER STATISTIQ"
    )

    assert result["mode"] == "SUGGEST"

    assert result["suggestion"] == (
        "AFFICHER STATISTIQUES"
    )

    assert result["success"] is True


def test_corrector_suggestion_contains_trace():

    result = CommandCorrector.correct(
        "AFFICHER STATISTIQ"
    )

    assert "trace" in result

    assert isinstance(
        result["trace"],
        list
    )


def test_corrector_reformulate():

    result = CommandCorrector.correct(
        "AFFICHER @"
    )

    assert isinstance(
        result,
        dict
    )

    assert result["mode"] == "REFORMULATE"

    assert result["success"] is False


def test_corrector_valid():

    result = CommandCorrector.correct(
        "AFFICHER STATISTIQUES"
    )

    assert result["mode"] == "VALID"

    assert result["success"] is True


def test_parser_commande_incomplete():

    result = parse_command(
        "AFFICHER"
    )

    assert result["success"] is False


def test_parser_wrong_order():

    result = parse_command(
        "STATISTIQUES AFFICHER"
    )

    assert result["success"] is False


def test_parser_token_inattendu():

    result = parse_command(
        "QUITTER RAPPORT"
    )

    assert result["success"] is False


def test_parser_modifier_sans_numero():

    result = parse_command(
        "MODIFIER QUESTION"
    )

    assert result["success"] is False


def test_parser_supprimer_sans_numero():

    result = parse_command(
        "SUPPRIMER QUESTION"
    )

    assert result["success"] is False


def test_parser_lancer_incomplet():

    result = parse_command(
        "LANCER"
    )

    assert result["success"] is False


def test_parser_ajouter_incomplet():

    result = parse_command(
        "AJOUTER"
    )

    assert result["success"] is False

def test_builder_tokens_vides():

    with pytest.raises(Exception):

        CommandBuilder.build([])


def test_builder_none():

    with pytest.raises(Exception):

        CommandBuilder.build(None)


def test_builder_commande_invalide():

    tokens = Lexer.tokenize(
        "QUITTER"
    )

    command = CommandBuilder.build(
        tokens
    )

    assert command is not None


def test_dispatcher_none():

    result = CommandDispatcher.dispatch(
        None
    )

    assert result["success"] is False


def test_dispatcher_commande_vide():

    result = CommandDispatcher.dispatch(
        {}
    )

    assert result["success"] is False


def test_dispatcher_action_inconnue():

    result = CommandDispatcher.dispatch(
        {
            "action": "ACTION_INEXISTANTE"
        }
    )

    assert result["success"] is False

    assert result["action"] == "INCONNUE"


def test_dispatcher_resultat_structure():

    result = CommandDispatcher.dispatch(
        {
            "action": "ACTION_INEXISTANTE"
        }
    )

    assert isinstance(
        result,
        dict
    )

    assert "success" in result

    assert "action" in result


def test_handler_commande_none():

    handler = CommandHandler()

    result = handler.handle(None)

    assert result["success"] is False


def test_handler_action_inconnue():

    handler = CommandHandler()

    result = handler.handle(
        {
            "action": "ACTION_INEXISTANTE"
        }
    )

    assert result["success"] is False


def test_handler_resultat_structure():

    handler = CommandHandler()

    result = handler.handle(
        {
            "action": "ACTION_INEXISTANTE"
        }
    )

    assert isinstance(
        result,
        dict
    )

    assert "success" in result


def test_handler_ajouter_question_sans_donnees():

    handler = CommandHandler()

    command = build_command(
        "AJOUTER QUESTION"
    )

    result = handler.handle(
        command,
        data=None
    )

    assert result["success"] is False

    assert result["action"] in (
        "AJOUTER",
        "AJOUTER_QUESTION"
    )


def test_handler_modifier_question_sans_donnees():

    handler = CommandHandler()

    command = build_command(
        "MODIFIER QUESTION 3"
    )

    result = handler.handle(
        command,
        data=None
    )

    assert result["success"] is False

    assert result["action"] in (
        "MODIFIER",
        "MODIFIER_QUESTION"
    )


def test_handler_erreur_statistiques():

    handler = CommandHandler()

    command = build_command(
        "AFFICHER STATISTIQUES"
    )

    with patch(
        "services.command_handler."
        "DashboardController.statistics",
        side_effect=Exception(
            "Erreur statistiques"
        )
    ):

        result = handler.handle(
            command
        )

    assert result["success"] is False


def test_handler_erreur_export():

    handler = CommandHandler()

    command = build_command(
        "EXPORTER RAPPORT"
    )

    with patch(
        "services.command_handler."
        "ReportController.export_pdf",
        side_effect=Exception(
            "Erreur export"
        )
    ):

        result = handler.handle(
            command
        )

    assert result["success"] is False


def test_handler_modifier_question_erreur():

    handler = CommandHandler()

    command = build_command(
        "MODIFIER QUESTION 3"
    )

    data = {
        "texte_question": "Test",
        "ordre_question": 1,
        "active": True
    }

    with patch(
        "services.command_handler."
        "QuestionController.update",
        side_effect=Exception(
            "Erreur modification"
        )
    ):

        result = handler.handle(
            command,
            data=data
        )

    assert result["success"] is False


def test_handler_supprimer_question_erreur():

    handler = CommandHandler()

    command = build_command(
        "SUPPRIMER QUESTION 25"
    )

    with patch(
        "services.command_handler."
        "QuestionController.delete",
        side_effect=Exception(
            "Erreur suppression"
        )
    ):

        result = handler.handle(
            command
        )

    assert result["success"] is False


def test_pipeline_erreur_lexicale():

    text = "AFFICHER @"

    with pytest.raises(LexerError):

        Lexer.tokenize(text)


def test_pipeline_erreur_syntaxique():

    text = "AFFICHER"

    correction = CommandCorrector.correct(
        text
    )

    assert correction["mode"] == "VALID"

    command_text = (
        correction.get("corrected")
        or correction.get("original")
    )

    tokens = Lexer.tokenize(
        command_text
    )

    result = LL1Parser.parse(
        tokens,
        return_trace=True
    )

    assert result["success"] is False


def test_trace_erreur_syntaxique():

    result = parse_command(
        "AFFICHER"
    )

    assert result["success"] is False

    assert "trace" in result

    assert isinstance(
        result["trace"],
        list
    )


def test_trace_erreur_lexicale():

    try:

        Lexer.tokenize(
            "AFFICHER @"
        )

    except LexerError as error:

        assert str(error)

        return

    pytest.fail(
        "LexerError attendu"
    )


def test_erreur_dispatcher_structure():

    result = CommandDispatcher.dispatch(
        {
            "action": "ACTION_INEXISTANTE"
        }
    )

    assert isinstance(
        result,
        dict
    )

    assert "success" in result

    assert "action" in result


def test_erreur_handler_structure():

    handler = CommandHandler()

    result = handler.handle(
        {
            "action": "ACTION_INEXISTANTE"
        }
    )

    assert isinstance(
        result,
        dict
    )

    assert "success" in result


def test_erreurs_pipeline_complet():

    correction = CommandCorrector.correct(
        "AFFICHER STATISTIQUES"
    )

    assert correction["mode"] == "VALID"

    assert correction["success"] is True

    tokens = Lexer.tokenize(
        correction["corrected"]
    )

    parser = LL1Parser.parse(
        tokens,
        return_trace=True
    )

    assert parser["success"] is True


    correction = CommandCorrector.correct(
        "AFFICHER STATISTIQ"
    )

    assert correction["mode"] == "SUGGEST"

    assert correction["success"] is True

    assert correction["suggestion"] == (
        "AFFICHER STATISTIQUES"
    )


    correction = CommandCorrector.correct(
        "AFFICHER"
    )

    assert correction["mode"] == "VALID"

    assert correction["success"] is True

    tokens = Lexer.tokenize(
        correction["corrected"]
    )

    parser = LL1Parser.parse(
        tokens,
        return_trace=True
    )

    assert parser["success"] is False

    assert isinstance(
        parser.get("trace", []),
        list
    )


def test_corrector_vers_lexer():

    correction = CommandCorrector.correct(
        "AFFICHER STATISTIQ"
    )

    assert correction["mode"] == "SUGGEST"

    assert correction["success"] is True

    assert correction["suggestion"] == (
        "AFFICHER STATISTIQUES"
    )


    assert correction["suggestion"] != (
        "AFFICHER STATISTIQ"
    )


def test_lexer_vers_parser():

    tokens = Lexer.tokenize(
        "AFFICHER"
    )

    result = LL1Parser.parse(
        tokens,
        return_trace=True
    )

    assert result["success"] is False


def test_parser_echec_arrete_builder():

    tokens = Lexer.tokenize(
        "AFFICHER"
    )

    parser = LL1Parser.parse(
        tokens,
        return_trace=True
    )

    assert parser["success"] is False

    assert True