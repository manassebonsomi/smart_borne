# test_parser_complet.py

from services.lexer import Lexer
from services.ll1_parser import LL1Parser
from services.ll1_table import LL1Table


# ==========================================================
# OUTILS
# ==========================================================

tests_total = 0
tests_passed = 0
tests_failed = 0


def run_test(name, condition, details=None):
    """
    Exécute une assertion de test et affiche le résultat.
    """

    global tests_total
    global tests_passed
    global tests_failed

    tests_total += 1

    if condition:

        tests_passed += 1

        print(f"PASS : {name}")

    else:

        tests_failed += 1

        print(f"FAIL : {name}")

        if details:
            print(f"       {details}")


def lex_and_parse(command):
    """
    Effectue le cycle complet :

        texte
          ↓
        lexer
          ↓
        tokens
          ↓
        parser LL(1)

    Retourne :

        (tokens, result)
    """

    lexer = Lexer()

    try:

        tokens = lexer.tokenize(command)

    except Exception as error:

        return None, {
            "success": False,
            "error": "LEXICAL_ERROR",
            "message": str(error)
        }

    result = LL1Parser.parse(
        tokens,
        return_trace=True
    )

    return tokens, result


# ==========================================================
# 1. TABLE LL(1)
# ==========================================================

def test_ll1_table():

    print()
    print("=" * 70)
    print("1. VALIDATION DE LA TABLE LL(1)")
    print("=" * 70)

    validation = LL1Table.validate()

    run_test(
        "Table LL(1) sans conflit",
        validation.get("success") is True,
        validation
    )


# ==========================================================
# 2. COMMANDES VALIDES
# ==========================================================

def test_valid_commands():

    print()
    print("=" * 70)
    print("2. COMMANDES VALIDES")
    print("=" * 70)

    commands = [

        "AFFICHER STATISTIQUES",

        "AFFICHER ERREURS",

        "LANCER ENQUETE CYBERSECURITE",

        "LANCER CAMPAGNE ECOLE",

        "CHERCHER ENFANTS KINSHASA",

        "CHERCHER ADOLESCENTS INTERESSES PAR PYTHON",

        "AJOUTER QUESTION",

        "MODIFIER QUESTION 3",

        "MODIFIER QUESTION 25",

        "SUPPRIMER QUESTION 2",

        "SUPPRIMER QUESTION 25",

        "EXPORTER RAPPORT",

        "RECOMMENCER SESSION",

        "QUITTER"
    ]

    passed_before = tests_passed

    for command in commands:

        tokens, result = lex_and_parse(
            command
        )

        run_test(
            command,
            (
                result is not None
                and
                result.get("success") is True
            ),
            (
                result.get("message")
                if result
                else "Aucun résultat"
            )
        )

    passed = tests_passed - passed_before

    print()
    print(
        f"Commandes valides : "
        f"{passed}/{len(commands)}"
    )


# ==========================================================
# 3. COMMANDES INVALIDES
# ==========================================================

def test_invalid_commands():

    print()
    print("=" * 70)
    print("3. COMMANDES INVALIDES")
    print("=" * 70)

    commands = [

        "AFFICHER QUESTION",

        "MODIFIER STATISTIQUES",

        "LANCER QUESTION",

        "AJOUTER STATISTIQUES",

        "SUPPRIMER RAPPORT",

        "EXPORTER QUESTION",

        "RECOMMENCER QUESTION",

        "CHERCHER QUESTION",

        "MODIFIER QUESTION",

        "SUPPRIMER QUESTION"
    ]

    passed_before = tests_passed

    for command in commands:

        tokens, result = lex_and_parse(
            command
        )

        run_test(
            command,
            (
                result is not None
                and
                result.get("success") is False
                and
                result.get("error") == "SYNTAX_ERROR"
            ),
            (
                result.get("message")
                if result
                else "Aucun résultat"
            )
        )

    passed = tests_passed - passed_before

    print()
    print(
        f"Commandes invalides correctement rejetées : "
        f"{passed}/{len(commands)}"
    )


# ==========================================================
# 4. ERREURS LEXICALES
# ==========================================================

def test_lexical_errors():

    print()
    print("=" * 70)
    print("4. ERREURS LEXICALES")
    print("=" * 70)

    commands = [

        "AFFICHER @",

        "AFFICHER SALUT",

        "MODIFIER QUESTION abc",

        "MODIFIER QUESTION 12abc"
    ]

    lexer = Lexer()

    passed_before = tests_passed

    for command in commands:

        try:

            lexer.tokenize(command)

            run_test(
                command,
                False,
                "Une erreur lexicale était attendue."
            )

        except Exception as error:

            run_test(
                command,
                True,
                str(error)
            )

    passed = tests_passed - passed_before

    print()
    print(
        f"Erreurs lexicales détectées : "
        f"{passed}/{len(commands)}"
    )


# ==========================================================
# 5. EOF INATTENDU
# ==========================================================

def test_unexpected_eof():

    print()
    print("=" * 70)
    print("5. EOF INATTENDU")
    print("=" * 70)

    commands = [

        "MODIFIER QUESTION",

        "SUPPRIMER QUESTION"
    ]

    passed_before = tests_passed

    for command in commands:

        tokens, result = lex_and_parse(
            command
        )

        errors = result.get(
            "errors",
            []
        )

        eof_error = any(
            error.get("received") == "EOF"
            and
            error.get("expected") == "NUMERO"
            for error in errors
        )

        run_test(
            command,
            (
                result.get("success") is False
                and
                eof_error
            ),
            result.get("message")
        )

    passed = tests_passed - passed_before

    print()
    print(
        f"EOF inattendus correctement détectés : "
        f"{passed}/{len(commands)}"
    )


# ==========================================================
# 6. NUMERO INVALIDE
# ==========================================================

def test_invalid_numero():

    print()
    print("=" * 70)
    print("6. NUMERO INVALIDE")
    print("=" * 70)

    lexer = Lexer()

    invalid_numbers = [

        "MODIFIER QUESTION abc",

        "SUPPRIMER QUESTION abc",

        "MODIFIER QUESTION 12abc"
    ]

    passed_before = tests_passed

    for command in invalid_numbers:

        try:

            lexer.tokenize(command)

            run_test(
                command,
                False,
                "Une erreur lexicale était attendue."
            )

        except Exception as error:

            run_test(
                command,
                True,
                str(error)
            )

    passed = tests_passed - passed_before

    print()
    print(
        f"NUMERO invalides détectés : "
        f"{passed}/{len(invalid_numbers)}"
    )


# ==========================================================
# 7. RÉCUPÉRATION D'ERREUR LL(1)
# ==========================================================

def test_error_recovery():

    print()
    print("=" * 70)
    print("7. RÉCUPÉRATION D'ERREUR LL(1)")
    print("=" * 70)

    commands = [

        "AFFICHER QUESTION",

        "MODIFIER STATISTIQUES",

        "LANCER QUESTION",

        "QUITTER QUESTION",

        "AFFICHER STATISTIQUES QUESTION"
    ]

    passed_before = tests_passed

    for command in commands:

        tokens, result = lex_and_parse(
            command
        )

        errors = result.get(
            "errors",
            []
        )

        trace = result.get(
            "trace",
            []
        )

        recovery_detected = any(
            (
                "Récupération"
                in str(step.get("action"))
            )
            for step in trace
        )

        run_test(
            command,
            (
                result.get("success") is False
                and
                len(errors) >= 1
                and
                recovery_detected
            ),
            result.get("message")
        )

    passed = tests_passed - passed_before

    print()
    print(
        f"Récupérations LL(1) validées : "
        f"{passed}/{len(commands)}"
    )


# ==========================================================
# 8. ERREURS SYNTAXIQUES
# ==========================================================

def test_syntax_errors():

    print()
    print("=" * 70)
    print("8. ERREURS SYNTAXIQUES")
    print("=" * 70)

    cases = [

        (
            "AFFICHER QUESTION",
            "NO_PRODUCTION"
        ),

        (
            "MODIFIER STATISTIQUES",
            "NO_PRODUCTION"
        ),

        (
            "LANCER QUESTION",
            "NO_PRODUCTION"
        ),

        (
            "MODIFIER QUESTION",
            "TERMINAL_MISMATCH"
        ),

        (
            "QUITTER QUESTION",
            "TERMINAL_MISMATCH"
        )
    ]

    passed_before = tests_passed

    for command, expected_category in cases:

        tokens, result = lex_and_parse(
            command
        )

        categories = [
            error.get("category")
            for error in
            result.get("errors", [])
        ]

        run_test(
            (
                f"{command} "
                f"→ {expected_category}"
            ),
            expected_category in categories,
            (
                f"Catégories reçues : "
                f"{categories}"
            )
        )

    passed = tests_passed - passed_before

    print()
    print(
        f"Erreurs syntaxiques catégorisées : "
        f"{passed}/{len(cases)}"
    )


# ==========================================================
# 9. TEST D'ENTRÉE RESTANTE
# ==========================================================

def test_unexpected_input():

    print()
    print("=" * 70)
    print("9. ENTRÉE INATTENDUE")
    print("=" * 70)

    command = "AFFICHER STATISTIQUES QUESTION"

    tokens, result = lex_and_parse(
        command
    )

    errors = result.get(
        "errors",
        []
    )

    unexpected = any(
        (
            error.get("category")
            == "UNEXPECTED_INPUT"
        )
        or
        (
            error.get("category")
            == "TERMINAL_MISMATCH"
            and
            error.get("expected") == "EOF"
        )
        for error in errors
    )

    run_test(
        command,
        (
            result.get("success") is False
            and
            unexpected
        ),
        (
            "Erreur détectée mais catégorie "
            "inattendue : "
            + str(
                [
                    error.get("category")
                    for error in errors
                ]
            )
        )
    )


# ==========================================================
# 10. EXÉCUTION
# ==========================================================

def main():

    print()
    print("=" * 70)
    print("TESTS AUTOMATISÉS COMPLETS — PARSER LL(1)")
    print("=" * 70)

    test_ll1_table()

    test_valid_commands()

    test_invalid_commands()

    test_lexical_errors()

    test_unexpected_eof()

    test_invalid_numero()

    test_error_recovery()

    test_syntax_errors()

    test_unexpected_input()

    # ------------------------------------------------------
    # RÉSUMÉ
    # ------------------------------------------------------

    print()
    print("=" * 70)
    print("RÉSUMÉ FINAL")
    print("=" * 70)

    print()
    print(
        f"Tests exécutés : {tests_total}"
    )

    print(
        f"Tests réussis  : {tests_passed}"
    )

    print(
        f"Tests échoués  : {tests_failed}"
    )

    print()

    if tests_failed == 0:

        print(
            "TOUS LES TESTS SONT PASSÉS"
        )

        print()

        return 0

    print(
        "DES TESTS ONT ÉCHOUÉ"
    )

    print()

    return 1


if __name__ == "__main__":

    raise SystemExit(
        main()
    )