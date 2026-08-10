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
    # ENSEMBLE DES NON-TERMINAUX
    # ==========================================================

    @classmethod
    def get_non_terminals(cls):
        """
        Retourne l'ensemble des non-terminaux
        de la grammaire.
        """

        return set(GRAMMAR.keys())

    # ==========================================================
    # ENSEMBLE DES TERMINAUX
    # ==========================================================

    @classmethod
    def get_terminals(cls):
        """
        Détermine automatiquement les terminaux
        présents dans la grammaire.
        """

        terminals = set()

        for productions in GRAMMAR.values():

            for production in productions:

                for symbol in production:

                    if (
                        symbol != EPSILON
                        and not is_non_terminal(symbol)
                    ):
                        terminals.add(symbol)

        terminals.add(EOF)

        return terminals

    # ==========================================================
    # PROPRIÉTÉS PUBLIQUES
    # ==========================================================

    @classmethod
    def non_terminals(cls):
        """
        Compatibilité avec le parseur et les autres composants.
        """

        return cls.get_non_terminals()

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
    # FIRST D'UNE SÉQUENCE
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

        if cls._first_cache is not None:
            return cls._first_cache

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
    # FIRST D'UNE SÉQUENCE AVEC CACHE
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

        if cls._follow_cache is not None:
            return cls._follow_cache

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

                        first_beta = (
                            cls.first_sequence_cached(
                                beta,
                                first
                            )
                        )

                        before = len(
                            follow[symbol]
                        )

                        # FIRST(beta) - EPSILON
                        follow[symbol].update(
                            first_beta - {EPSILON}
                        )

                        # Si beta peut produire epsilon
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
    # ANALYSE COMPLÈTE
    # ==========================================================

    @classmethod
    def analyze(cls):

        first = cls.compute_first()
        follow = cls.compute_follow()

        return {
            "first": first,
            "follow": follow,
            "non_terminals":
                cls.get_non_terminals(),
            "terminals":
                cls.get_terminals()
        }

    # ==========================================================
    # RÉINITIALISATION DU CACHE
    # ==========================================================

    @classmethod
    def reset_cache(cls):

        cls._first_cache = None
        cls._follow_cache = None

    # ==========================================================
    # AFFICHAGE
    # ==========================================================

    @classmethod
    def display(cls):

        result = cls.analyze()

        first = result["first"]
        follow = result["follow"]

        non_terminals = result[
            "non_terminals"
        ]

        terminals = result[
            "terminals"
        ]

        print()
        print("=" * 70)
        print("ANALYSE DE LA GRAMMAIRE LL(1)")
        print("=" * 70)

        # ------------------------------------------------------
        # NON-TERMINAUX
        # ------------------------------------------------------

        print()
        print("=" * 70)
        print("NON-TERMINAUX")
        print("=" * 70)

        for non_terminal in sorted(
            non_terminals
        ):

            print(
                non_terminal
            )

        # ------------------------------------------------------
        # TERMINAUX
        # ------------------------------------------------------

        print()
        print("=" * 70)
        print("TERMINAUX")
        print("=" * 70)

        for terminal in sorted(
            terminals
        ):

            print(
                terminal
            )

        # ------------------------------------------------------
        # FIRST
        # ------------------------------------------------------

        print()
        print("=" * 70)
        print("FIRST")
        print("=" * 70)

        for non_terminal in sorted(
            first
        ):

            print(
                f"FIRST({non_terminal}) = "
                f"{sorted(first[non_terminal])}"
            )

        # ------------------------------------------------------
        # FOLLOW
        # ------------------------------------------------------

        print()
        print("=" * 70)
        print("FOLLOW")
        print("=" * 70)

        for non_terminal in sorted(
            follow
        ):

            print(
                f"FOLLOW({non_terminal}) = "
                f"{sorted(follow[non_terminal])}"
            )

        print()