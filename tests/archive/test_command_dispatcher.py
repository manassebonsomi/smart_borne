# test_command_dispatcher.py
from app import app
from services.lexer import Lexer
from services.command_builder import CommandBuilder
from services.command_dispatcher import CommandDispatcher


# ==========================================================
# OUTIL DE CONSTRUCTION
# ==========================================================

def build_command(text):

    tokens = Lexer.tokenize(
        text
    )

    return CommandBuilder.build(
        tokens
    )


# ==========================================================
# AFFICHER STATISTIQUES
# ==========================================================

def test_afficher_statistiques():

    command = build_command(
        "AFFICHER STATISTIQUES"
    )

    result = CommandDispatcher.dispatch(
        command
    )

    assert (
        result["action"]
        ==
        "AFFICHER_STATISTIQUES"
    )

    print(
        "PASS : DISPATCH AFFICHER STATISTIQUES"
    )


# ==========================================================
# EXPORTER RAPPORT
# ==========================================================

def test_exporter_rapport():

    command = build_command(
        "EXPORTER RAPPORT"
    )

    result = CommandDispatcher.dispatch(
        command
    )

    assert (
        result["action"]
        ==
        "EXPORTER_RAPPORT"
    )

    print(
        "PASS : DISPATCH EXPORTER RAPPORT"
    )


# ==========================================================
# QUITTER
# ==========================================================

def test_quitter():

    command = build_command(
        "QUITTER"
    )

    result = CommandDispatcher.dispatch(
        command
    )

    assert (
        result["action"]
        ==
        "QUITTER"
    )

    print(
        "PASS : DISPATCH QUITTER"
    )


# ==========================================================
# ACTION INCONNUE
# ==========================================================

def test_action_inconnue():

    command = {
        "action":
            "ACTION_INEXISTANTE"
    }

    result = CommandDispatcher.dispatch(
        command
    )

    assert (
        result["success"]
        is
        False
    )

    print(
        "PASS : ACTION INCONNUE"
    )


# ==========================================================
# COMMANDE NONE
# ==========================================================

def test_commande_none():

    result = CommandDispatcher.dispatch(
        None
    )

    assert (
        result["success"]
        is
        False
    )

    print(
        "PASS : COMMANDE NONE"
    )


# ==========================================================
# EXÉCUTION
# ==========================================================

# if __name__ == "__main__":
#     print()
#     print("=" * 80)
#     print(
#         "TEST COMMAND DISPATCHER"
#     )
#     print("=" * 80)
#     print()
#
#     test_afficher_statistiques()
#     test_exporter_rapport()
#     test_quitter()
#     test_action_inconnue()
#     test_commande_none()
#
#     print()
#     print("=" * 80)
#     print(
#         "TOUS LES TESTS COMMAND DISPATCHER "
#         "SONT PASSÉS"
#     )
#
#     print("=" * 80)

if __name__ == "__main__":

    print()
    print("=" * 80)
    print("TEST COMMAND DISPATCHER")
    print("=" * 80)
    print()

    with app.app_context():

        test_afficher_statistiques()
        test_exporter_rapport()
        test_quitter()
        test_action_inconnue()
        test_commande_none()

    print()
    print("=" * 80)
    print(
        "TOUS LES TESTS COMMAND DISPATCHER "
        "SONT PASSÉS"
    )
    print("=" * 80)