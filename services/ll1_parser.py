# services/ll1_parser.py

from services.grammar import (
    GRAMMAR,
    START_SYMBOL,
    EOF,
    EPSILON
)

from services.grammar_analyzer import (
    GrammarAnalyzer
)

from services.ll1_table import (
    LL1Table,
    GrammarConflictError
)


class LL1Parser:

    # ==========================================================
    # PARSE
    # ==========================================================

    @classmethod
    def parse(
        cls,
        tokens,
        return_trace=False
    ):

        trace = []

        # ------------------------------------------------------
        # VÉRIFICATION TABLE LL(1)
        # ------------------------------------------------------

        validation = LL1Table.validate()

        if not validation["success"]:

            result = {
                "success": False,
                "error":
                    "GRAMMAR_CONFLICT",
                "message":
                    "La grammaire contient "
                    "un conflit LL(1).",
                "trace":
                    trace
            }

            return result

        table = validation["table"]

        # ------------------------------------------------------
        # VÉRIFICATION TOKENS
        # ------------------------------------------------------

        if not tokens:

            result = {
                "success": False,
                "error":
                    "EMPTY_INPUT",
                "message":
                    "Aucun token fourni.",
                "trace":
                    trace
            }

            return result

        # ------------------------------------------------------
        # COPIE DES TOKENS
        # ------------------------------------------------------

        token_list = list(tokens)

        # Le lexer ajoute normalement EOF.
        # On vérifie néanmoins sa présence.

        if token_list[-1].type != EOF:

            token_list.append(
                type(
                    "EOFToken",
                    (),
                    {
                        "type": EOF,
                        "value": EOF
                    }
                )()
            )

        # ------------------------------------------------------
        # PILE LL(1)
        # ------------------------------------------------------

        stack = [
            EOF,
            START_SYMBOL
        ]

        index = 0

        # ------------------------------------------------------
        # BOUCLE PRINCIPALE
        # ------------------------------------------------------

        while stack:

            top = stack.pop()

            lookahead = token_list[
                index
            ]

            lookahead_type = (
                lookahead.type
            )

            # --------------------------------------------------
            # TRACE
            # --------------------------------------------------

            trace_step = {
                "step":
                    len(trace) + 1,

                "stack":
                    list(reversed(stack))
                    + [top],

                "input":
                    [
                        token.type
                        for token in
                        token_list[index:]
                    ],

                "lookahead":
                    lookahead_type,

                "action":
                    None
            }

            # --------------------------------------------------
            # ACCEPTATION
            # --------------------------------------------------

            if (
                top == EOF
                and
                lookahead_type == EOF
            ):

                trace_step[
                    "action"
                ] = "ACCEPT"

                trace.append(
                    trace_step
                )

                result = {
                    "success": True,
                    "message":
                        "Commande acceptée.",
                    "trace":
                        trace
                }

                if return_trace:
                    return result

                return True

            # --------------------------------------------------
            # EPSILON
            # --------------------------------------------------

            if top == EPSILON:

                trace_step[
                    "action"
                ] = "EPSILON"

                trace.append(
                    trace_step
                )

                continue

            # --------------------------------------------------
            # TERMINAL
            # --------------------------------------------------

            if top not in GRAMMAR:

                if top == lookahead_type:

                    trace_step[
                        "action"
                    ] = (
                        f"Correspondance : "
                        f"{top}"
                    )

                    trace.append(
                        trace_step
                    )

                    index += 1

                    continue

                # --------------------------------------------------
                # ERREUR TERMINALE
                # --------------------------------------------------

                expected = [
                    top
                ]

                trace_step[
                    "action"
                ] = (
                    f"ERREUR : attendu "
                    f"{top}, reçu "
                    f"{lookahead_type}"
                )

                trace.append(
                    trace_step
                )

                result = {
                    "success": False,

                    "error":
                        "SYNTAX_ERROR",

                    "message":
                        (
                            "Erreur syntaxique : "
                            f"attendu "
                            f"{top}, "
                            f"reçu "
                            f"{lookahead_type}."
                        ),

                    "expected":
                        expected,

                    "received":
                        lookahead_type,

                    "trace":
                        trace
                }

                if return_trace:
                    return result

                return False

            # --------------------------------------------------
            # NON-TERMINAL
            # --------------------------------------------------

            production = table.get(
                top,
                {}
            ).get(
                lookahead_type
            )

            # --------------------------------------------------
            # AUCUNE PRODUCTION
            # --------------------------------------------------

            if production is None:

                expected = sorted(
                    table.get(
                        top,
                        {}
                    ).keys()
                )

                trace_step[
                    "action"
                ] = (
                    "ERREUR : "
                    "aucune production"
                )

                trace.append(
                    trace_step
                )

                result = {
                    "success": False,

                    "error":
                        "SYNTAX_ERROR",

                    "message":
                        (
                            f"Aucune production "
                            f"pour {top} "
                            f"avec le lookahead "
                            f"{lookahead_type}."
                        ),

                    "non_terminal":
                        top,

                    "expected":
                        expected,

                    "received":
                        lookahead_type,

                    "trace":
                        trace
                }

                if return_trace:
                    return result

                return False

            # --------------------------------------------------
            # APPLICATION PRODUCTION
            # --------------------------------------------------

            trace_step[
                "action"
            ] = (
                f"{top} → "
                + " ".join(
                    production
                )
            )

            trace.append(
                trace_step
            )

            # --------------------------------------------------
            # EMPILER À L'ENVERS
            # --------------------------------------------------

            for symbol in reversed(
                production
            ):

                if symbol != EPSILON:

                    stack.append(
                        symbol
                    )

        # ------------------------------------------------------
        # PILE VIDE MAIS TOKENS RESTANTS
        # ------------------------------------------------------

        if index < len(token_list):

            remaining = [
                token.type
                for token in
                token_list[index:]
            ]

            result = {
                "success": False,

                "error":
                    "UNEXPECTED_INPUT",

                "message":
                    (
                        "Entrée inattendue "
                        "après analyse."
                    ),

                "remaining":
                    remaining,

                "trace":
                    trace
            }

            if return_trace:
                return result

            return False

        # ------------------------------------------------------
        # ERREUR GÉNÉRIQUE
        # ------------------------------------------------------

        result = {
            "success": False,

            "error":
                "PARSER_ERROR",

            "message":
                "Erreur inconnue du parseur.",

            "trace":
                trace
        }

        if return_trace:
            return result

        return False

    # ==========================================================
    # AFFICHAGE TRACE
    # ==========================================================

    @classmethod
    def display_trace(cls, result):

        trace = result.get(
            "trace",
            []
        )

        print()
        print("=" * 80)
        print("TRACE LL(1)")
        print("=" * 80)

        if not trace:

            print(
                "Aucune trace disponible."
            )

            return

        for step in trace:

            print()
            print(
                f"Étape "
                f"{step['step']}"
            )

            print(
                "Pile :"
            )

            print(
                "  "
                + " ".join(
                    step["stack"]
                )
            )

            print(
                "Entrée restante :"
            )

            print(
                "  "
                + " ".join(
                    step["input"]
                )
            )

            print(
                "Lookahead :"
            )

            print(
                "  "
                + step["lookahead"]
            )

            print(
                "Action :"
            )

            print(
                "  "
                + str(
                    step["action"]
                )
            )

        print()

        if result.get(
            "success"
        ):

            print(
                "RESULTAT : "
                "ACCEPTATION"
            )

        else:

            print(
                "RESULTAT : "
                "ERREUR"
            )