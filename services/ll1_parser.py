# services/ll1_parser.py

from services.grammar import (
    START_SYMBOL,
    EOF,
    is_non_terminal
)

from services.ll1_table import (
    LL1Table,
    GrammarConflictError
)


class LL1Parser:

    # ==========================================================
    # PARSE
    # ==========================================================

    @staticmethod
    def parse(
        tokens,
        return_trace=False
    ):

        trace = []

        # ------------------------------------------------------
        # Vérification de la table
        # ------------------------------------------------------

        try:

            table = LL1Table.get_table()

        except GrammarConflictError:

            result = {
                "success": False,
                "error":
                    "GRAMMAR_CONFLICT",
                "message":
                    "La grammaire contient "
                    "un conflit LL(1).",
                "trace": trace
            }

            return result if return_trace else False

        # ------------------------------------------------------
        # Tokens
        # ------------------------------------------------------

        if not tokens:

            result = {
                "success": False,
                "error":
                    "EMPTY_INPUT",
                "message":
                    "Aucune commande fournie.",
                "trace": trace
            }

            return result if return_trace else False

        # ------------------------------------------------------
        # Pile
        # ------------------------------------------------------

        stack = [
            EOF,
            START_SYMBOL
        ]

        index = 0

        # ------------------------------------------------------
        # Analyse
        # ------------------------------------------------------

        while stack:

            top = stack.pop()

            if index >= len(tokens):

                result = {
                    "success": False,
                    "error":
                        "UNEXPECTED_END",
                    "message":
                        "Fin inattendue de la commande.",
                    "trace": trace
                }

                return result if return_trace else False

            lookahead = tokens[index]

            lookahead_type = lookahead.type

            # --------------------------------------------------
            # Trace état initial
            # --------------------------------------------------

            trace.append({

                "step":
                    len(trace) + 1,

                "stack":
                    stack[:] + [top],

                "input":
                    [
                        token.type
                        for token in tokens[index:]
                    ],

                "action":
                    "LECTURE",

                "top":
                    top,

                "lookahead":
                    lookahead_type
            })

            # ==================================================
            # CAS 1 : $
            # ==================================================

            if top == EOF:

                if lookahead_type == EOF:

                    index += 1

                    trace.append({

                        "step":
                            len(trace) + 1,

                        "stack":
                            stack[:],

                        "input":
                            [],

                        "action":
                            "ACCEPTER"
                    })

                    result = {

                        "success":
                            True,

                        "message":
                            "Commande acceptée.",

                        "trace":
                            trace
                    }

                    return (
                        result
                        if return_trace
                        else True
                    )

                result = {

                    "success":
                        False,

                    "error":
                        "UNEXPECTED_TOKEN",

                    "message":
                        (
                            f"Fin attendue, "
                            f"mais reçu "
                            f"{lookahead_type}."
                        ),

                    "trace":
                        trace
                }

                return (
                    result
                    if return_trace
                    else False
                )

            # ==================================================
            # CAS 2 : TERMINAL
            # ==================================================

            if not is_non_terminal(top):

                if top == lookahead_type:

                    index += 1

                    trace.append({

                        "step":
                            len(trace) + 1,

                        "stack":
                            stack[:],

                        "input":
                            [
                                token.type
                                for token in tokens[index:]
                            ],

                        "action":
                            (
                                f"CORRESPONDANCE "
                                f"{top}"
                            )
                    })

                    continue

                # ----------------------------------------------
                # Erreur terminal
                # ----------------------------------------------

                result = {

                    "success":
                        False,

                    "error":
                        "SYNTAX_ERROR",

                    "message":
                        (
                            f"Erreur syntaxique : "
                            f"attendu '{top}', "
                            f"reçu "
                            f"'{lookahead_type}'."
                        ),

                    "expected":
                        [top],

                    "received":
                        lookahead_type,

                    "trace":
                        trace
                }

                return (
                    result
                    if return_trace
                    else False
                )

            # ==================================================
            # CAS 3 : NON-TERMINAL
            # ==================================================

            production = table.get(
                top,
                {}
            ).get(
                lookahead_type
            )

            if production is None:

                expected = sorted(
                    table.get(
                        top,
                        {}
                    ).keys()
                )

                result = {

                    "success":
                        False,

                    "error":
                        "SYNTAX_ERROR",

                    "message":
                        (
                            f"Aucune production "
                            f"pour "
                            f"M[{top}, "
                            f"{lookahead_type}]."
                        ),

                    "expected":
                        expected,

                    "received":
                        lookahead_type,

                    "trace":
                        trace
                }

                return (
                    result
                    if return_trace
                    else False
                )

            # --------------------------------------------------
            # Epsilon
            # --------------------------------------------------

            if len(production) == 0:

                trace.append({

                    "step":
                        len(trace) + 1,

                    "stack":
                        stack[:],

                    "input":
                        [
                            token.type
                            for token in tokens[index:]
                        ],

                    "action":
                        f"{top} → ε"
                })

                continue

            # --------------------------------------------------
            # Développement production
            # --------------------------------------------------

            for symbol in reversed(
                production
            ):

                stack.append(symbol)

            trace.append({

                "step":
                    len(trace) + 1,

                "stack":
                    stack[:],

                "input":
                    [
                        token.type
                        for token in tokens[index:]
                    ],

                "action":
                    (
                        f"{top} → "
                        f"{' '.join(production)}"
                    )
            })

        # ======================================================
        # FIN
        # ======================================================

        result = {

            "success":
                False,

            "error":
                "PARSER_ERROR",

            "message":
                "Le parseur s'est terminé de manière inattendue.",

            "trace":
                trace
        }

        return (
            result
            if return_trace
            else False
        )