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
                    "La grammaire contient "
                    "un conflit LL(1).",
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

            result = {
                "success": False,
                "error": "EMPTY_INPUT",
                "message":
                    "Aucun token fourni.",
                "errors": [
                    {
                        "type": "EMPTY_INPUT",
                        "message":
                            "Aucun token fourni."
                    }
                ],
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
        # VÉRIFICATION EOF
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

        # ------------------------------------------------------
        # BOUCLE PRINCIPALE
        # ------------------------------------------------------

        while stack:

            # --------------------------------------------------
            # PROTECTION INDEX
            # --------------------------------------------------

            if index >= len(token_list):

                # Sécurité : normalement impossible car EOF
                # doit toujours être présent.

                errors.append(
                    {
                        "type": "UNEXPECTED_EOF",
                        "message":
                            "Fin inattendue des tokens."
                    }
                )

                trace.append(
                    {
                        "step": len(trace) + 1,
                        "stack": list(reversed(stack)),
                        "input": [],
                        "lookahead": EOF,
                        "action":
                            "ERREUR : EOF inattendu"
                    }
                )

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

                if errors:

                    trace_step["action"] = (
                        "FIN DE L'ANALYSE "
                        "AVEC ERREURS"
                    )

                    trace.append(
                        trace_step
                    )

                    result = {
                        "success": False,
                        "error": "SYNTAX_ERROR",
                        "message":
                            (
                                f"Analyse terminée "
                                f"avec {len(errors)} "
                                f"erreur(s)."
                            ),
                        "errors": errors,
                        "trace": trace
                    }

                else:

                    trace_step["action"] = "ACCEPT"

                    trace.append(
                        trace_step
                    )

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

            # --------------------------------------------------
            # EPSILON
            # --------------------------------------------------

            if top == EPSILON:

                trace_step["action"] = "EPSILON"

                trace.append(
                    trace_step
                )

                continue

            # --------------------------------------------------
            # TERMINAL
            # --------------------------------------------------

            if top not in GRAMMAR:

                # ----------------------------------------------
                # CORRESPONDANCE
                # ----------------------------------------------

                if top == lookahead_type:

                    trace_step["action"] = (
                        f"Correspondance : {top}"
                    )

                    trace.append(
                        trace_step
                    )

                    index += 1

                    continue

                # ----------------------------------------------
                # ERREUR TERMINALE
                # ----------------------------------------------

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

                # ----------------------------------------------
                # CAS EOF
                # ----------------------------------------------
                #
                # Si EOF arrive alors qu'un terminal était
                # attendu, on considère que le terminal manque.
                #
                # On retire simplement le terminal de la pile
                # afin de continuer l'analyse.
                # ----------------------------------------------

                if lookahead_type == EOF:

                    trace_step["action"] = (
                        f"ERREUR : attendu {top}, "
                        f"reçu EOF. "
                        f"Récupération : "
                        f"terminal {top} ignoré."
                    )

                    trace.append(
                        trace_step
                    )

                    continue

                # ----------------------------------------------
                # AUTRE TOKEN
                # ----------------------------------------------
                #
                # On abandonne le terminal attendu et on avance
                # dans l'entrée afin d'éviter une boucle infinie.
                # ----------------------------------------------

                trace_step["action"] = (
                    f"ERREUR : attendu {top}, "
                    f"reçu {lookahead_type}. "
                    f"Récupération : "
                    f"token {lookahead_type} ignoré."
                )

                trace.append(
                    trace_step
                )

                index += 1

                continue

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
            # PRODUCTION TROUVÉE
            # --------------------------------------------------

            if production is not None:

                trace_step["action"] = (
                    f"{top} → "
                    + " ".join(production)
                )

                trace.append(
                    trace_step
                )

                # ----------------------------------------------
                # EMPILER À L'ENVERS
                # ----------------------------------------------

                for symbol in reversed(
                    production
                ):

                    if symbol != EPSILON:

                        stack.append(
                            symbol
                        )

                continue

            # --------------------------------------------------
            # AUCUNE PRODUCTION
            # --------------------------------------------------

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
            # RÉCUPÉRATION LL(1)
            # --------------------------------------------------
            #
            # Cas classique :
            #
            # si lookahead ∈ FOLLOW(A)
            #
            # alors on peut abandonner A.
            # --------------------------------------------------

            non_terminal_follow = follow.get(
                top,
                set()
            )

            if (
                lookahead_type
                in
                non_terminal_follow
            ):

                trace_step["action"] = (
                    f"ERREUR : aucune production "
                    f"pour {top} avec "
                    f"le lookahead "
                    f"{lookahead_type}. "
                    f"Récupération LL(1) : "
                    f"{lookahead_type} ∈ "
                    f"FOLLOW({top}), "
                    f"{top} est abandonné."
                )

                trace.append(
                    trace_step
                )

                # On ne remet pas le non-terminal dans
                # la pile. On passe au symbole suivant.

                continue

            # --------------------------------------------------
            # EOF
            # --------------------------------------------------
            #
            # Si EOF est rencontré et n'appartient pas au
            # FOLLOW du non-terminal, on abandonne quand même
            # le non-terminal pour permettre à l'analyse
            # de se terminer proprement.
            # --------------------------------------------------

            if lookahead_type == EOF:

                trace_step["action"] = (
                    f"ERREUR : aucune production "
                    f"pour {top} avec "
                    f"le lookahead EOF. "
                    f"Récupération : "
                    f"abandon de {top}."
                )

                trace.append(
                    trace_step
                )

                continue

            # --------------------------------------------------
            # SYNCHRONISATION PAR TOKEN
            # --------------------------------------------------
            #
            # On cherche un token permettant de reprendre
            # l'analyse.
            #
            # On avance jusqu'à :
            #
            # 1. trouver une production pour le non-terminal ;
            # 2. trouver un token de FOLLOW ;
            # 3. atteindre EOF.
            # --------------------------------------------------

            skipped = []

            while index < len(token_list):

                current_type = (
                    token_list[index].type
                )

                # ----------------------------------------------
                # Une production devient disponible
                # ----------------------------------------------

                if current_type in table.get(
                    top,
                    {}
                ):

                    break

                # ----------------------------------------------
                # Token de synchronisation FOLLOW
                # ----------------------------------------------

                if current_type in non_terminal_follow:

                    break

                # ----------------------------------------------
                # EOF
                # ----------------------------------------------

                if current_type == EOF:

                    break

                skipped.append(
                    current_type
                )

                index += 1

            # --------------------------------------------------
            # TRACE RÉCUPÉRATION
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

            trace.append(
                trace_step
            )

            # --------------------------------------------------
            # IMPORTANT :
            # --------------------------------------------------
            #
            # Le non-terminal a déjà été retiré de la pile.
            # On continue avec le prochain symbole.
            # --------------------------------------------------

        # ======================================================
        # FIN DE L'ANALYSE
        # ======================================================

        # ------------------------------------------------------
        # TOKENS RESTANTS
        # ------------------------------------------------------

        if index < len(token_list):

            remaining = [
                token.type
                for token in
                token_list[index:]
            ]

            # Si les tokens restants ne sont pas simplement EOF,
            # ils constituent une entrée inattendue.

            non_eof_remaining = [
                token
                for token in remaining
                if token != EOF
            ]

            if non_eof_remaining:

                error = {
                    "type": "SYNTAX_ERROR",
                    "category": "UNEXPECTED_INPUT",
                    "remaining":
                        non_eof_remaining,
                    "message":
                        (
                            "Entrée inattendue "
                            "après analyse."
                        )
                }

                errors.append(
                    error
                )

                trace.append(
                    {
                        "step": len(trace) + 1,
                        "stack": [],
                        "input": remaining,
                        "lookahead":
                            token_list[index].type,
                        "action":
                            (
                                "ERREUR : entrée "
                                "inattendue "
                                "après analyse."
                            )
                    }
                )

        # ------------------------------------------------------
        # RÉSULTAT FINAL
        # ------------------------------------------------------

        if errors:

            result = {
                "success": False,
                "error": "SYNTAX_ERROR",
                "message":
                    (
                        f"Analyse terminée "
                        f"avec {len(errors)} "
                        f"erreur(s)."
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
                    f"  {index}. "
                    f"{error.get('message')}"
                )

            print()

        # ------------------------------------------------------
        # RESULTAT
        # ------------------------------------------------------

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