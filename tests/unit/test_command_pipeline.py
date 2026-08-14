from services.command_pipeline import CommandPipeline


def test_valid():

    result = CommandPipeline.process(
        "AFFICHER STATISTIQUES"
    )

    assert result["mode"] == "VALID"

    assert result["command"] == (
        "AFFICHER STATISTIQUES"
    )

    assert CommandPipeline.can_continue(
        result
    )

    print(
        "PASS : VALID"
    )


def test_auto_correct():

    result = CommandPipeline.process(
        "AFFICHER STATISTIQUESS"
    )

    assert result["mode"] == (
        "AUTO_CORRECT"
    )

    assert result["command"] == (
        "AFFICHER STATISTIQUES"
    )

    assert CommandPipeline.can_continue(
        result
    )

    print(
        "PASS : AUTO_CORRECT"
    )


def test_suggest():

    result = CommandPipeline.process(
        "AFFICHER STATISTIQ"
    )

    assert result["mode"] == (
        "SUGGEST"
    )

    assert (
        "STATISTIQUES"
        in result["suggestion"]
    )

    assert not CommandPipeline.can_continue(
        result
    )

    print(
        "PASS : SUGGEST"
    )


def test_reformulate():

    result = CommandPipeline.process(
        "BONJOUR"
    )

    assert result["mode"] == (
        "REFORMULATE"
    )

    assert not CommandPipeline.can_continue(
        result
    )

    print(
        "PASS : REFORMULATE"
    )


def test_case_insensitive():

    result = CommandPipeline.process(
        "afficher statistiq"
    )

    assert result["mode"] == (
        "SUGGEST"
    )

    assert (
        "STATISTIQUES"
        in result["suggestion"]
    )

    print(
        "PASS : CASE INSENSITIVE"
    )


def test_trace():

    result = CommandPipeline.process(
        "AFFICHER STATISTIQ"
    )

    assert "trace" in result

    assert isinstance(
        result["trace"],
        list
    )

    assert len(
        result["trace"]
    ) > 0

    print(
        "PASS : TRACE"
    )


if __name__ == "__main__":

    print()
    print("=" * 70)
    print(
        "TEST COMMAND PIPELINE"
    )
    print("=" * 70)
    print()

    test_valid()
    test_auto_correct()
    test_suggest()
    test_reformulate()
    test_case_insensitive()
    test_trace()

    print()
    print("=" * 70)
    print(
        "TOUS LES TESTS DU COMMAND PIPELINE "
        "SONT PASSÉS"
    )
    print("=" * 70)