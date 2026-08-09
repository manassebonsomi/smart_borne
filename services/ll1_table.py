# services/ll1_table.py

from services.grammar import (
    GRAMMAR,
    EPSILON,
    EOF,
    is_non_terminal
)

from services.grammar_analyzer import (
    GrammarAnalyzer
)


class GrammarConflictError(Exception):

    def __init__(
        self,
        non_terminal,
        terminal,
        existing,
        incoming
    ):

        self.non_terminal = non_terminal
        self.terminal = terminal
        self.existing = existing
        self.incoming = incoming

        message = (
            f"Conflit LL(1) : "
            f"M[{non_terminal}, {terminal}] "
            f"contient déjà {existing}, "
            f"nouvelle production : {incoming}"
        )

        super().__init__(message)


class LL1Table:

    _table = None

    # ==========================================================
    # CONSTRUCTION
    # ==========================================================

    @classmethod
    def build(cls):

        first = GrammarAnalyzer.compute_first()

        follow = GrammarAnalyzer.compute_follow()

        table = {
            non_terminal: {}
            for non_terminal in GRAMMAR
        }

        for non_terminal, productions in GRAMMAR.items():

            for production in productions:

                first_alpha = (
                    GrammarAnalyzer
                    .first_sequence_cached(
                        production,
                        first
                    )
                )

                # --------------------------------------------------
                # FIRST(alpha)
                # --------------------------------------------------

                for terminal in (
                    first_alpha - {EPSILON}
                ):

                    cls._add_production(
                        table,
                        non_terminal,
                        terminal,
                        production
                    )

                # --------------------------------------------------
                # FOLLOW(A) si epsilon
                # --------------------------------------------------

                if EPSILON in first_alpha:

                    for terminal in follow[
                        non_terminal
                    ]:

                        cls._add_production(
                            table,
                            non_terminal,
                            terminal,
                            production
                        )

        cls._table = table

        return table

    # ==========================================================
    # AJOUT PRODUCTION
    # ==========================================================

    @staticmethod
    def _add_production(
        table,
        non_terminal,
        terminal,
        production
    ):

        if terminal in table[non_terminal]:

            existing = table[
                non_terminal
            ][terminal]

            if existing != production:

                raise GrammarConflictError(
                    non_terminal,
                    terminal,
                    existing,
                    production
                )

        table[
            non_terminal
        ][terminal] = production

    # ==========================================================
    # GET TABLE
    # ==========================================================

    @classmethod
    def get_table(cls):

        if cls._table is None:

            cls.build()

        return cls._table

    # ==========================================================
    # PRODUCTION
    # ==========================================================

    @classmethod
    def get_production(
        cls,
        non_terminal,
        terminal
    ):

        table = cls.get_table()

        return table.get(
            non_terminal,
            {}
        ).get(
            terminal
        )

    # ==========================================================
    # VALIDATION
    # ==========================================================

    @classmethod
    def validate(cls):

        try:

            cls.build()

            return {
                "success": True,
                "message":
                    "La grammaire est LL(1).",
                "table":
                    cls._table
            }

        except GrammarConflictError as e:

            return {
                "success": False,
                "message": str(e)
            }

    # ==========================================================
    # AFFICHAGE
    # ==========================================================

    @classmethod
    def display(cls):

        print()
        print("=" * 70)
        print("TABLE LL(1)")
        print("=" * 70)

        try:

            table = cls.get_table()

        except GrammarConflictError as e:

            print()
            print(
                "ERREUR : "
                + str(e)
            )

            return

        terminals = set()

        for entries in table.values():

            terminals.update(
                entries.keys()
            )

        terminals = sorted(terminals)

        print()

        header = (
            "NON-TERMINAL".ljust(30)
            + " | "
            + " | ".join(
                terminal.ljust(25)
                for terminal in terminals
            )
        )

        print(header)

        print("-" * len(header))

        for non_terminal in GRAMMAR:

            row = non_terminal.ljust(30)

            row += " | "

            cells = []

            for terminal in terminals:

                production = table[
                    non_terminal
                ].get(
                    terminal
                )

                if production:

                    text = (
                        non_terminal
                        + " → "
                        + " ".join(production)
                    )

                else:

                    text = ""

                cells.append(
                    text.ljust(25)
                )

            row += " | ".join(cells)

            print(row)

        print()
        print(
            "Validation : "
            "Aucun conflit LL(1) détecté."
        )