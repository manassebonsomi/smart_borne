# test_command_corrector.py

from services.command_corrector import CommandCorrector


def test_valid():

    result = CommandCorrector.correct(
        "AFFICHER STATISTIQUES"
    )

    assert result["mode"] == "VALID"

    print(
        "PASS : VALID"
    )


def test_auto_correct():

    result = CommandCorrector.correct(
        "AFFICHER STATISTIQUESS"
    )

    assert result["mode"] == "AUTO_CORRECT"

    assert (
        "STATISTIQUES"
        in result["corrected"]
    )

    print(
        "PASS : AUTO_CORRECT"
    )


def test_suggest():

    result = CommandCorrector.correct(
        "AFFICHER STATISTIQ"
    )

    assert result["mode"] == "SUGGEST"

    assert (
        "STATISTIQUES"
        in result["suggestion"]
    )

    print(
        "PASS : SUGGEST"
    )


def test_reformulate():

    result = CommandCorrector.correct(
        "BONJOUR"
    )

    assert result["mode"] == "REFORMULATE"

    print(
        "PASS : REFORMULATE"
    )


def test_multiple_words():

    result = CommandCorrector.correct(
        "AFFICHER STATISTIQ"
    )

    assert (
        len(result["suggestions"])
        >= 1
    )

    print(
        "PASS : MULTIPLE WORD ANALYSIS"
    )


def test_trace():

    result = CommandCorrector.correct(
        "AFFICHER STATISTIQ"
    )

    assert "trace" in result

    assert (
        len(result["trace"])
        > 0
    )

    print(
        "PASS : TRACE"
    )


def test_empty_command():

    result = CommandCorrector.correct(
        ""
    )

    assert (
        result["mode"]
        == "REFORMULATE"
    )

    print(
        "PASS : EMPTY COMMAND"
    )


def test_case_insensitive():

    result = CommandCorrector.correct(
        "afficher statistiq"
    )

    assert result["mode"] == "SUGGEST"

    print(
        "PASS : CASE INSENSITIVE"
    )


# ==========================================================
# EXÉCUTION
# ==========================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("TEST COMMAND CORRECTOR")
    print("=" * 70)
    print()

    test_valid()
    test_auto_correct()
    test_suggest()
    test_reformulate()
    test_multiple_words()
    test_trace()
    test_empty_command()
    test_case_insensitive()

    print()
    print("=" * 70)
    print(
        "TOUS LES TESTS DU COMMAND CORRECTOR "
        "SONT PASSÉS"
    )
    print("=" * 70)