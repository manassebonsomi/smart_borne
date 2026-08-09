# services/grammar.py

"""
Grammaire LL(1) de la borne interactive CCC.

La grammaire est factorisée afin d'éviter les conflits LL(1).

Notation :
    ε     = production vide
    EOF   = fin de l'entrée
"""

GRAMMAR = {

    # ==========================================================
    # AXIOME
    # ==========================================================

    "COMMANDE": [
        ["CMD_AFFICHER"],
        ["CMD_LANCER"],
        ["CMD_CHERCHER"],
        ["CMD_AJOUTER"],
        ["CMD_MODIFIER"],
        ["CMD_SUPPRIMER"],
        ["CMD_EXPORTER"],
        ["CMD_RECOMMENCER"],
        ["CMD_QUITTER"],
    ],

    # ==========================================================
    # AFFICHER
    # ==========================================================

    "CMD_AFFICHER": [
        ["AFFICHER", "SUJET_AFFICHAGE"]
    ],

    "SUJET_AFFICHAGE": [
        ["STATISTIQUES"],
        ["ERREURS"]
    ],

    # ==========================================================
    # LANCER
    # ==========================================================

    "CMD_LANCER": [
        ["LANCER", "SUJET_LANCER"]
    ],

    "SUJET_LANCER": [
        ["ENQUETE", "CYBERSECURITE"],
        ["CAMPAGNE", "ECOLE"]
    ],

    # ==========================================================
    # CHERCHER
    # ==========================================================

    "CMD_CHERCHER": [
        ["CHERCHER", "SUJET_RECHERCHE"]
    ],

    "SUJET_RECHERCHE": [
        ["ENFANTS", "KINSHASA"],
        [
            "ADOLESCENTS",
            "INTERESSES",
            "PAR",
            "PYTHON"
        ]
    ],

    # ==========================================================
    # AJOUTER
    # ==========================================================

    "CMD_AJOUTER": [
        ["AJOUTER", "SUJET_AJOUTER"]
    ],

    "SUJET_AJOUTER": [
        ["QUESTION"]
    ],

    # ==========================================================
    # MODIFIER
    # ==========================================================

    "CMD_MODIFIER": [
        ["MODIFIER", "SUJET_MODIFIER"]
    ],

    "SUJET_MODIFIER": [
        ["QUESTION", "NUMERO"]
    ],

    # ==========================================================
    # SUPPRIMER
    # ==========================================================

    "CMD_SUPPRIMER": [
        ["SUPPRIMER", "SUJET_SUPPRIMER"]
    ],

    "SUJET_SUPPRIMER": [
        ["QUESTION", "NUMERO"]
    ],

    # ==========================================================
    # EXPORTER
    # ==========================================================

    "CMD_EXPORTER": [
        ["EXPORTER", "SUJET_EXPORTER"]
    ],

    "SUJET_EXPORTER": [
        ["RAPPORT"]
    ],

    # ==========================================================
    # RECOMMENCER
    # ==========================================================

    "CMD_RECOMMENCER": [
        ["RECOMMENCER", "SUJET_RECOMMENCER"]
    ],

    "SUJET_RECOMMENCER": [
        ["SESSION"]
    ],

    # ==========================================================
    # QUITTER
    # ==========================================================

    "CMD_QUITTER": [
        ["QUITTER"]
    ]
}


# ==============================================================
# CONFIGURATION
# ==============================================================

START_SYMBOL = "COMMANDE"

EPSILON = "ε"

EOF = "EOF"


# ==============================================================
# OUTILS
# ==============================================================

def get_non_terminals():
    """
    Retourne l'ensemble des non-terminaux.
    """
    return set(GRAMMAR.keys())


def get_terminals():
    """
    Retourne l'ensemble des terminaux utilisés par la grammaire.
    """
    non_terminals = get_non_terminals()

    terminals = set()

    for productions in GRAMMAR.values():

        for production in productions:

            for symbol in production:

                if symbol not in non_terminals:
                    terminals.add(symbol)

    terminals.add(EOF)

    return terminals


def is_non_terminal(symbol):
    """
    Vérifie si un symbole est un non-terminal.
    """
    return symbol in GRAMMAR


def is_terminal(symbol):
    """
    Vérifie si un symbole est un terminal.
    """
    return (
        symbol not in GRAMMAR
        and symbol != EPSILON
    )