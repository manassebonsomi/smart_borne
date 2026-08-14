from services.command_pipeline import CommandPipeline


# ==========================================================
# VALID
# ==========================================================

def test_valid_command():

    result = CommandPipeline.execute(
        "AFFICHER STATISTIQUES"
    )

    assert result["mode"] == "VALID"

    assert result["success"] is True

    assert result["command"] == (
        "AFFICHER STATISTIQUES"
    )

    assert len(
        result["tokens"]
    ) > 0

    assert (
        result["parser"] is not None
    )

    assert (
        result["parser"]["success"]
        is True
    )

    assert CommandPipeline.can_continue(
        result
    )

    print(
        "PASS : VALID → LEXER → PARSER"
    )


# ==========================================================
# AUTO CORRECT
# ==========================================================

def test_auto_correct_command():

    result = CommandPipeline.execute(
        "AFFICHER STATISTIQUESS"
    )

    assert (
        result["mode"]
        == "AUTO_CORRECT"
    )

    assert result["success"] is True

    assert (
        result["command"]
        == "AFFICHER STATISTIQUES"
    )

    assert (
        result["parser"] is not None
    )

    assert (
        result["parser"]["success"]
        is True
    )

    assert CommandPipeline.can_continue(
        result
    )

    print(
        "PASS : AUTO_CORRECT → "
        "LEXER → PARSER"
    )


# ==========================================================
# SUGGEST
# ==========================================================

def test_suggest_stops_before_parser():

    result = CommandPipeline.execute(
        "AFFICHER STATISTIQ"
    )

    assert (
        result["mode"]
        == "SUGGEST"
    )

    assert result["success"] is False

    assert (
        "STATISTIQUES"
        in result["suggestion"]
    )

    assert result["tokens"] == []

    assert result["parser"] is None

    assert not CommandPipeline.can_continue(
        result
    )

    print(
        "PASS : SUGGEST → ARRÊT"
    )


# ==========================================================
# REFORMULATE
# ==========================================================

def test_reformulate_stops():

    result = CommandPipeline.execute(
        "BONJOUR"
    )

    assert (
        result["mode"]
        == "REFORMULATE"
    )

    assert result["success"] is False

    assert result["tokens"] == []

    assert result["parser"] is None

    assert not CommandPipeline.can_continue(
        result
    )

    print(
        "PASS : REFORMULATE → ARRÊT"
    )


# ==========================================================
# AUTRE COMMANDE VALIDE
# ==========================================================

def test_lancer_command():

    result = CommandPipeline.execute(
        "LANCER ENQUETE CYBERSECURITE"
    )

    assert result["mode"] == "VALID"

    assert result["success"] is True

    assert (
        result["parser"]["success"]
        is True
    )

    print(
        "PASS : LANCER ENQUETE "
        "CYBERSECURITE"
    )


# ==========================================================
# NUMERO
# ==========================================================

def test_modifier_question():

    result = CommandPipeline.execute(
        "MODIFIER QUESTION 25"
    )

    assert result["mode"] == "VALID"

    assert result["success"] is True

    assert (
        result["parser"]["success"]
        is True
    )

    token_types = [
        token["type"]
        for token in result["tokens"]
    ]

    assert "NUMERO" in token_types

    print(
        "PASS : NUMERO → LEXER → PARSER"
    )


# ==========================================================
# TRACE
# ==========================================================

def test_full_trace():

    result = CommandPipeline.execute(
        "AFFICHER STATISTIQUESS"
    )

    assert "trace" in result

    assert isinstance(
        result["trace"],
        list
    )

    assert len(
        result["trace"]
    ) > 0

    components = [
        step.get("component")
        for step in result["trace"]
        if isinstance(step, dict)
    ]

    assert (
        "CommandCorrector"
        in components
    )

    assert (
        "Lexer"
        in components
    )

    assert (
        "LL1Parser"
        in components
    )

    print(
        "PASS : TRACE COMPLÈTE"
    )


# ==========================================================
# EXÉCUTION
# ==========================================================

if __name__ == "__main__":

    print()
    print("=" * 80)
    print(
        "TEST INTÉGRATION "
        "COMMAND → LEXER → PARSER"
    )
    print("=" * 80)
    print()

    test_valid_command()
    test_auto_correct_command()
    test_suggest_stops_before_parser()
    test_reformulate_stops()
    test_lancer_command()
    test_modifier_question()
    test_full_trace()

    print()
    print("=" * 80)
    print(
        "TOUS LES TESTS D'INTÉGRATION "
        "SONT PASSÉS"
    )
    print("=" * 80)