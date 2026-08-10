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
    LL1Table
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
        errors = []

        # ------------------------------------------------------
        # VÉRIFICATION TABLE LL(1)
        # ------------------------------------------------------

        validation = LL1Table.validate()

        if not validation["success"]:

            result = {
                "success": False,
                "error": "GRAMMAR_CONFLICT",
                "message":
                    "La grammaire contient un conflit LL(1).",
                "errors": [],
                "trace": trace
            }

            if return_trace:
                return result

            return False

        table = validation["table"]

        # ------------------------------------------------------
        # VÉRIFICATION TOKENS
        # ------------------------------------------------------

        if not tokens:

            error = {
                "type": "EMPTY_INPUT",
                "message": "Aucun token fourni."
            }

            errors.append(error)

            result = {
                "success": False,
                "error": "EMPTY_INPUT",
                "message": "Aucun token fourni.",
                "errors": errors,
                "trace": trace
            }

            if return_trace:
                return result

            return False

        # ------------------------------------------------------
        # COPIE DES TOKENS
        # ------------------------------------------------------

        token_list = list(tokens)

        # ------------------------------------------------------
        # EOF
        # ------------------------------------------------------

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
        # FOLLOW
        # ------------------------------------------------------

        follow = GrammarAnalyzer.compute_follow()

        # ======================================================
        # BOUCLE PRINCIPALE
        # ======================================================

        while stack:

            # --------------------------------------------------
            # PROTECTION INDEX
            # --------------------------------------------------

            if index >= len(token_list):

                error = {
                    "type": "UNEXPECTED_EOF",
                    "message":
                        "Fin inattendue des tokens."
                }

                errors.append(error)

                trace.append({
                    "step": len(trace) + 1,
                    "stack": list(reversed(stack)),
                    "input": [],
                    "lookahead": EOF,
                    "action":
                        "ERREUR : EOF inattendu."
                })

                break

            # --------------------------------------------------
            # SOMMET DE PILE
            # --------------------------------------------------

            top = stack.pop()

            lookahead = token_list[index]
            lookahead_type = lookahead.type

            # --------------------------------------------------
            # TRACE
            # --------------------------------------------------

            trace_step = {
                "step": len(trace) + 1,

                "stack":
                    list(reversed(stack)) + [top],

                "input":
                    [
                        token.type
                        for token in token_list[index:]
                    ],

                "lookahead":
                    lookahead_type,

                "action": None
            }

            # ==================================================
            # ACCEPTATION
            # ==================================================

            if (
                top == EOF
                and
                lookahead_type == EOF
            ):

                trace_step["action"] = (
                    "ACCEPT"
                    if not errors
                    else
                    "FIN DE L'ANALYSE AVEC ERREURS"
                )

                trace.append(trace_step)

                break

            # ==================================================
            # EPSILON
            # ==================================================

            if top == EPSILON:

                trace_step["action"] = "EPSILON"

                trace.append(trace_step)

                continue

            # ==================================================
            # TERMINAL
            # ==================================================

            if top not in GRAMMAR:

                # ------------------------------------------------
                # CORRESPONDANCE
                # ------------------------------------------------

                if top == lookahead_type:

                    trace_step["action"] = (
                        f"Correspondance : {top}"
                    )

                    trace.append(trace_step)

                    index += 1

                    continue

                # ------------------------------------------------
                # ERREUR TERMINALE
                # ------------------------------------------------

                error = {
                    "type": "SYNTAX_ERROR",
                    "category": "TERMINAL_MISMATCH",
                    "expected": top,
                    "received": lookahead_type,
                    "message":
                        (
                            f"Erreur syntaxique : "
                            f"attendu {top}, "
                            f"reçu {lookahead_type}."
                        )
                }

                errors.append(error)

                # ------------------------------------------------
                # EOF
                # ------------------------------------------------

                if lookahead_type == EOF:

                    trace_step["action"] = (
                        f"ERREUR : attendu {top}, "
                        f"reçu EOF. "
                        f"Récupération : "
                        f"terminal {top} ignoré."
                    )

                    trace.append(trace_step)

                    continue

                # ------------------------------------------------
                # TOKEN INATTENDU
                # ------------------------------------------------

                trace_step["action"] = (
                    f"ERREUR : attendu {top}, "
                    f"reçu {lookahead_type}. "
                    f"Récupération : "
                    f"token {lookahead_type} ignoré."
                )

                trace.append(trace_step)

                index += 1

                continue

            # ==================================================
            # NON-TERMINAL
            # ==================================================

            production = table.get(
                top,
                {}
            ).get(
                lookahead_type
            )

            # --------------------------------------------------
            # PRODUCTION TROUVÉE
            # --------------------------------------------------

            if production is not None:

                trace_step["action"] = (
                    f"{top} → "
                    + " ".join(production)
                )

                trace.append(trace_step)

                for symbol in reversed(production):

                    if symbol != EPSILON:

                        stack.append(symbol)

                continue

            # ==================================================
            # AUCUNE PRODUCTION
            # ==================================================

            expected = sorted(
                table.get(
                    top,
                    {}
                ).keys()
            )

            error = {
                "type": "SYNTAX_ERROR",
                "category": "NO_PRODUCTION",
                "non_terminal": top,
                "expected": expected,
                "received": lookahead_type,
                "message":
                    (
                        f"Aucune production "
                        f"pour {top} "
                        f"avec le lookahead "
                        f"{lookahead_type}."
                    )
            }

            errors.append(error)

            # --------------------------------------------------
            # FOLLOW(A)
            # --------------------------------------------------

            non_terminal_follow = follow.get(
                top,
                set()
            )

            if lookahead_type in non_terminal_follow:

                trace_step["action"] = (
                    f"ERREUR : aucune production "
                    f"pour {top} avec le lookahead "
                    f"{lookahead_type}. "
                    f"Récupération LL(1) : "
                    f"{lookahead_type} ∈ "
                    f"FOLLOW({top}), "
                    f"{top} abandonné."
                )

                trace.append(trace_step)

                continue

            # --------------------------------------------------
            # EOF
            # --------------------------------------------------

            if lookahead_type == EOF:

                trace_step["action"] = (
                    f"ERREUR : aucune production "
                    f"pour {top} avec EOF. "
                    f"Récupération : "
                    f"{top} abandonné."
                )

                trace.append(trace_step)

                continue

            # --------------------------------------------------
            # SYNCHRONISATION
            # --------------------------------------------------

            skipped = []

            while index < len(token_list):

                current_type = (
                    token_list[index].type
                )

                # Une production est maintenant disponible.

                if current_type in table.get(
                    top,
                    {}
                ):

                    break

                # Token de synchronisation.

                if current_type in non_terminal_follow:

                    break

                # EOF.

                if current_type == EOF:

                    break

                skipped.append(current_type)

                index += 1

            # --------------------------------------------------
            # TRACE
            # --------------------------------------------------

            if skipped:

                trace_step["action"] = (
                    f"ERREUR : aucune production "
                    f"pour {top}. "
                    f"Récupération LL(1) : "
                    f"tokens ignorés = "
                    f"{', '.join(skipped)}."
                )

            else:

                trace_step["action"] = (
                    f"ERREUR : aucune production "
                    f"pour {top}. "
                    f"Récupération LL(1) : "
                    f"synchronisation sur "
                    f"{lookahead_type}."
                )

            trace.append(trace_step)

            # Le non-terminal est abandonné.
            continue

        # ======================================================
        # VÉRIFICATION DE L'ENTRÉE RESTANTE
        # ======================================================

        if index < len(token_list):

            remaining = [
                token.type
                for token in token_list[index:]
            ]

            non_eof_remaining = [
                token
                for token in remaining
                if token != EOF
            ]

            if non_eof_remaining:

                error = {
                    "type": "SYNTAX_ERROR",
                    "category": "UNEXPECTED_INPUT",
                    "remaining": non_eof_remaining,
                    "message":
                        (
                            "Entrée inattendue "
                            "après analyse."
                        )
                }

                errors.append(error)

                trace.append({
                    "step": len(trace) + 1,
                    "stack": [],
                    "input": remaining,
                    "lookahead":
                        token_list[index].type,
                    "action":
                        (
                            "ERREUR : entrée "
                            "inattendue après "
                            "analyse."
                        )
                })

        # ======================================================
        # RÉSULTAT FINAL
        # ======================================================

        if errors:

            result = {
                "success": False,
                "error": "SYNTAX_ERROR",
                "message":
                    (
                        f"Analyse terminée avec "
                        f"{len(errors)} erreur(s)."
                    ),
                "errors": errors,
                "trace": trace
            }

        else:

            result = {
                "success": True,
                "message":
                    "Commande acceptée.",
                "errors": [],
                "trace": trace
            }

        if return_trace:

            return result

        return result["success"]

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
                f"Étape {step['step']}"
            )

            print("Pile :")

            print(
                "  "
                + " ".join(
                    step["stack"]
                )
            )

            print("Entrée restante :")

            print(
                "  "
                + " ".join(
                    step["input"]
                )
            )

            print("Lookahead :")

            print(
                "  "
                + step["lookahead"]
            )

            print("Action :")

            print(
                "  "
                + str(
                    step["action"]
                )
            )

        print()

        # ------------------------------------------------------
        # ERREURS
        # ------------------------------------------------------

        errors = result.get(
            "errors",
            []
        )

        if errors:

            print(
                "ERREURS DÉTECTÉES : "
                f"{len(errors)}"
            )

            for index, error in enumerate(
                errors,
                start=1
            ):

                print()

                print(
                    f"{index}. "
                    f"{error.get('message')}"
                )

            print()

        # ------------------------------------------------------
        # RESULTAT
        # ------------------------------------------------------

        if result.get("success"):

            print(
                "RESULTAT : ACCEPTATION"
            )

        else:

            print(
                "RESULTAT : ERREUR"
            )