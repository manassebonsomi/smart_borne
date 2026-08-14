from services.command_suggester import CommandSuggester


def test_auto_correct():
    """
    Vérifie qu'un mot très proche déclenche
    AUTO_CORRECT.
    """

    result = CommandSuggester.decide(
        "STATISTIQUE"
    )

    assert result["mode"] == "AUTO_CORRECT"
    assert result["candidate"] == "STATISTIQUES"

    print("PASS : AUTO_CORRECT")


def test_suggest():
    """
    Vérifie qu'un mot suffisamment proche mais
    pas assez proche pour une correction automatique
    déclenche SUGGEST.
    """

    result = CommandSuggester.decide(
        "STATISTIQ"
    )

    assert result["mode"] == "SUGGEST"
    assert result["candidate"] == "STATISTIQUES"

    print("PASS : SUGGEST")


def test_reformulate():
    """
    Vérifie qu'un mot trop éloigné déclenche
    REFORMULATE.
    """

    result = CommandSuggester.decide(
        "XYZABC"
    )

    assert result["mode"] == "REFORMULATE"
    assert result["candidate"] is None

    print("PASS : REFORMULATE")


def test_similarity():
    """
    Vérifie que la fonction de similarité
    retourne une valeur entre 0 et 1.
    """

    score = CommandSuggester.similarity(
        "STATISTIQ",
        "STATISTIQUES"
    )

    assert 0.0 <= score <= 1.0

    print(
        "PASS : SIMILARITY "
        f"({score:.4f})"
    )


def test_multiple_suggestions():
    """
    Vérifie que le système retourne une liste
    de suggestions structurées.
    """

    suggestions = CommandSuggester.suggest(
        "STATISTIQ"
    )

    assert isinstance(
        suggestions,
        list
    )

    assert len(suggestions) >= 1

    assert (
        suggestions[0]["word"]
        ==
        "STATISTIQUES"
    )

    assert (
        "score"
        in
        suggestions[0]
    )

    print(
        "PASS : MULTIPLE SUGGESTIONS"
    )


def test_trace():
    """
    Vérifie que la décision peut être
    transformée en trace exploitable.
    """

    result = CommandSuggester.decide(
        "STATISTIQUE"
    )

    trace = CommandSuggester.trace(
        result
    )

    assert (
        trace["component"]
        ==
        "CommandSuggester"
    )

    assert (
        trace["input"]
        ==
        "STATISTIQUE"
    )

    assert (
        "mode"
        in
        trace
    )

    assert (
        "score"
        in
        trace
    )

    print(
        "PASS : TRACE"
    )


if __name__ == "__main__":

    print()
    print("=" * 70)
    print(
        "TEST COMMAND SUGGESTER"
    )
    print("=" * 70)
    print()

    test_similarity()
    test_auto_correct()
    test_suggest()
    test_reformulate()
    test_multiple_suggestions()
    test_trace()

    print()
    print("=" * 70)
    print(
        "TOUS LES TESTS DU "
        "COMMAND SUGGESTER SONT PASSÉS"
    )
    print("=" * 70)