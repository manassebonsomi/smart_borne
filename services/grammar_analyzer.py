# services/grammar_analyzer.py

from services.grammar import (
    GRAMMAR,
    START_SYMBOL,
    EPSILON,
    EOF,
    is_non_terminal
)


class GrammarAnalyzer:

    _first_cache = None
    _follow_cache = None

    # ==========================================================
    # FIRST D'UN SYMBOLE
    # ==========================================================

    @classmethod
    def first_symbol(cls, symbol):

        if symbol == EPSILON:
            return {EPSILON}

        if not is_non_terminal(symbol):
            return {symbol}

        first = set()

        for production in GRAMMAR[symbol]:

            first_production = cls.first_sequence(
                production
            )

            first.update(
                first_production
            )

        return first

    # ==========================================================
    # FIRST D'UNE SEQUENCE
    # ==========================================================

    @classmethod
    def first_sequence(cls, symbols):

        if not symbols:
            return {EPSILON}

        result = set()

        all_nullable = True

        for symbol in symbols:

            first_symbol = cls.first_symbol(symbol)

            result.update(
                first_symbol - {EPSILON}
            )

            if EPSILON not in first_symbol:
                all_nullable = False
                break

        if all_nullable:
            result.add(EPSILON)

        return result

    # ==========================================================
    # CALCUL COMPLET FIRST
    # ==========================================================

    @classmethod
    def compute_first(cls):

        first = {
            non_terminal: set()
            for non_terminal in GRAMMAR
        }

        changed = True

        while changed:

            changed = False

            for non_terminal, productions in GRAMMAR.items():

                for production in productions:

                    production_first = set()

                    nullable = True

                    for symbol in production:

                        if symbol in GRAMMAR:

                            symbol_first = first[symbol]

                        else:

                            symbol_first = {symbol}

                        production_first.update(
                            symbol_first - {EPSILON}
                        )

                        if EPSILON not in symbol_first:

                            nullable = False

                            break

                    if nullable:
                        production_first.add(EPSILON)

                    before = len(
                        first[non_terminal]
                    )

                    first[non_terminal].update(
                        production_first
                    )

                    if len(
                        first[non_terminal]
                    ) > before:

                        changed = True

        cls._first_cache = first

        return first

    # ==========================================================
    # FIRST D'UNE SEQUENCE AVEC CACHE
    # ==========================================================

    @classmethod
    def first_sequence_cached(
        cls,
        symbols,
        first
    ):

        if not symbols:
            return {EPSILON}

        result = set()

        nullable = True

        for symbol in symbols:

            if symbol in GRAMMAR:

                symbol_first = first[symbol]

            else:

                symbol_first = {symbol}

            result.update(
                symbol_first - {EPSILON}
            )

            if EPSILON not in symbol_first:

                nullable = False

                break

        if nullable:
            result.add(EPSILON)

        return result

    # ==========================================================
    # CALCUL FOLLOW
    # ==========================================================

    @classmethod
    def compute_follow(cls):

        first = cls.compute_first()

        follow = {
            non_terminal: set()
            for non_terminal in GRAMMAR
        }

        # L'axiome reçoit EOF
        follow[START_SYMBOL].add(EOF)

        changed = True

        while changed:

            changed = False

            for lhs, productions in GRAMMAR.items():

                for production in productions:

                    for index, symbol in enumerate(production):

                        if not is_non_terminal(symbol):
                            continue

                        beta = production[
                            index + 1:
                        ]

                        first_beta = cls.first_sequence_cached(
                            beta,
                            first
                        )

                        before = len(
                            follow[symbol]
                        )

                        # FIRST(beta) - epsilon
                        follow[symbol].update(
                            first_beta - {EPSILON}
                        )

                        # Si beta => epsilon
                        if (
                            EPSILON in first_beta
                            or not beta
                        ):

                            follow[symbol].update(
                                follow[lhs]
                            )

                        if len(
                            follow[symbol]
                        ) > before:

                            changed = True

        cls._follow_cache = follow

        return follow

    # ==========================================================
    # VERIFICATION
    # ==========================================================

    @classmethod
    def analyze(cls):

        first = cls.compute_first()
        follow = cls.compute_follow()

        return {
            "first": first,
            "follow": follow
        }

    # ==========================================================
    # AFFICHAGE
    # ==========================================================

    @classmethod
    def display(cls):

        result = cls.analyze()

        first = result["first"]
        follow = result["follow"]

        print()
        print("=" * 70)
        print("ANALYSE DE LA GRAMMAIRE LL(1)")
        print("=" * 70)

        print()
        print("=" * 70)
        print("NON-TERMINAUX")
        print("=" * 70)

        for non_terminal in GRAMMAR:

            print(
                f"{non_terminal}"
            )

        print()
        print("=" * 70)
        print("FIRST")
        print("=" * 70)

        for non_terminal in sorted(first):

            print(
                f"FIRST({non_terminal}) = "
                f"{sorted(first[non_terminal])}"
            )

        print()
        print("=" * 70)
        print("FOLLOW")
        print("=" * 70)

        for non_terminal in sorted(follow):

            print(
                f"FOLLOW({non_terminal}) = "
                f"{sorted(follow[non_terminal])}"
            )

        print()