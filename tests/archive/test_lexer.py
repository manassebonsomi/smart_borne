from services.lexer import Lexer, LexerError


def test_valid(command, expected):

    print()
    print("=" * 70)
    print(f"TEST : {command}")
    print("=" * 70)

    tokens = Lexer.tokenize(command)

    result = [
        token.type
        for token in tokens
    ]

    print("TOKENS :", result)

    assert result == expected

    print("PASS")


def test_lexical_error(command):

    print()
    print("=" * 70)
    print(f"TEST ERREUR LEXICALE : {command}")
    print("=" * 70)

    try:

        Lexer.tokenize(command)

    except LexerError as error:

        print(
            "ERREUR DETECTEE :",
            error
        )

        print("PASS")

        return

    raise AssertionError(
        "Une erreur lexicale était attendue."
    )


# ==========================================================
# TESTS VALIDES
# ==========================================================

test_valid(
    "AFFICHER STATISTIQUES",
    [
        "AFFICHER",
        "STATISTIQUES",
        "EOF"
    ]
)

test_valid(
    "LANCER ENQUETE CYBERSECURITE",
    [
        "LANCER",
        "ENQUETE",
        "CYBERSECURITE",
        "EOF"
    ]
)

test_valid(
    "LANCER CAMPAGNE ECOLE",
    [
        "LANCER",
        "CAMPAGNE",
        "ECOLE",
        "EOF"
    ]
)

test_valid(
    "CHERCHER ENFANTS KINSHASA",
    [
        "CHERCHER",
        "ENFANTS",
        "KINSHASA",
        "EOF"
    ]
)

test_valid(
    "CHERCHER ADOLESCENTS INTERESSES PAR PYTHON",
    [
        "CHERCHER",
        "ADOLESCENTS",
        "INTERESSES",
        "PAR",
        "PYTHON",
        "EOF"
    ]
)

test_valid(
    "AJOUTER QUESTION",
    [
        "AJOUTER",
        "QUESTION",
        "EOF"
    ]
)

test_valid(
    "MODIFIER QUESTION 3",
    [
        "MODIFIER",
        "QUESTION",
        "NUMERO",
        "EOF"
    ]
)

test_valid(
    "SUPPRIMER QUESTION 25",
    [
        "SUPPRIMER",
        "QUESTION",
        "NUMERO",
        "EOF"
    ]
)

test_valid(
    "EXPORTER RAPPORT",
    [
        "EXPORTER",
        "RAPPORT",
        "EOF"
    ]
)

test_valid(
    "RECOMMENCER SESSION",
    [
        "RECOMMENCER",
        "SESSION",
        "EOF"
    ]
)

test_valid(
    "QUITTER",
    [
        "QUITTER",
        "EOF"
    ]
)


# ==========================================================
# ERREURS LEXICALES
# ==========================================================

test_lexical_error(
    "AFFICHER @"
)

test_lexical_error(
    "AFFICHER SALUT"
)

test_lexical_error(
    "MODIFIER QUESTION abc"
)

test_lexical_error(
    "MODIFIER QUESTION 12abc"
)


print()
print("=" * 70)
print("TOUS LES TESTS DU LEXER SONT PASSES")
print("=" * 70)