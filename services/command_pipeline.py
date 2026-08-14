from services.command_corrector import CommandCorrector
from services.lexer import Lexer, LexerError
from services.ll1_parser import LL1Parser


class CommandPipeline:

    # CORRECTION UNIQUEMENT
    @classmethod
    def process(cls, command):
        """
        Première étape du pipeline.

        Analyse la commande avec CommandCorrector.

        Modes :

        VALID
        AUTO_CORRECT
        SUGGEST
        REFORMULATE

        Cette méthode ne lance pas encore
        le lexer ni le parser.
        """

        correction = CommandCorrector.correct(command)
        mode = correction.get("mode")

        # VALID
        if mode == "VALID":
            return {
                "success": True,
                "mode": "VALID",
                "original": correction.get("original"),
                "command": correction.get("corrected"),
                "suggestion": None,
                "score": correction.get("score", 1.0),
                "suggestions": correction.get("suggestions", []),
                "trace": correction.get("trace", [])
            }

        # AUTO_CORRECT
        if mode == "AUTO_CORRECT":
            corrected = correction.get("corrected")

            return {
                "success": True,
                "mode": "AUTO_CORRECT",
                "original": correction.get("original"
                ),
                "command": corrected,
                "suggestion": corrected,
                "score": correction.get("score", 0.0),
                "suggestions": correction.get("suggestions", []),
                "trace": correction.get("trace", [])
            }

        # SUGGEST
        if mode == "SUGGEST":
            return {
                "success": False,
                "mode": "SUGGEST",
                "original": correction.get("original"),
                "command": None,
                "suggestion": correction.get("suggestion"),
                "score": correction.get("score", 0.0),
                "suggestions": correction.get("suggestions", []),
                "trace": correction.get("trace", [])
            }

        # REFORMULATE
        return {
            "success": False,
            "mode": "REFORMULATE",
            "original": correction.get("original"),
            "command": None,
            "suggestion": None,
            "score": correction.get("score",0.0),
            "suggestions": correction.get("suggestions", []),
            "trace": correction.get("trace", [])}

    # EXÉCUTION COMPLÈTE
    @classmethod
    def execute(cls, command, return_trace=True):
        """
        Exécute le pipeline complet :
        """
        # CORRECTION
        correction = cls.process(command)
        mode = correction.get("mode")
        pipeline_trace = []

        # TRACE CORRECTION
        pipeline_trace.append({
            "component": "CommandCorrector",
            "mode": mode,
            "score": correction.get("score",0.0),
            "input": correction.get("original"),
            "command": correction.get("command")
        })

        # SUGGEST
        if mode == "SUGGEST":
            pipeline_trace.append({
                "component": "CommandPipeline",
                "action": (
                    "SUGGEST : "
                    "arrêt avant le lexer."
                )
            })

            result = {
                "success": False,
                "mode": "SUGGEST",
                "original": correction.get("original"),
                "command": None,
                "suggestion": correction.get("suggestion"),
                "score": correction.get("score",0.0),
                "suggestions": correction.get("suggestions",[]),
                "tokens": [],
                "lexer_error": None,
                "parser": None,
                "trace": (correction.get("trace",[]) + pipeline_trace)
            }

            return result

        # REFORMULATE
        if mode == "REFORMULATE":
            pipeline_trace.append({
                "component": "CommandPipeline",
                "action": (
                    "REFORMULATE : "
                    "arrêt avant le lexer."
                )
            })

            result = {
                "success": False,
                "mode": "REFORMULATE",
                "original": correction.get("original"),
                "command": None,
                "suggestion": None,
                "score": correction.get("score",0.0),
                "suggestions": correction.get("suggestions", []),
                "tokens": [],
                "lexer_error": None,
                "parser": None,
                "trace": (correction.get("trace", []) + pipeline_trace)
            }

            return result

        # COMMANDE À ANALYSER=
        command_to_parse = correction.get("command")
        pipeline_trace.append({
            "component": "CommandPipeline",
            "action": (
                "Commande acceptée par "
                "le correcteur."
            ),
            "command": command_to_parse
        })

        # LEXER==
        try:
            tokens = Lexer.tokenize(command_to_parse)
        except LexerError as error:

            pipeline_trace.append({
                "component": "Lexer",
                "action": "LEXER_ERROR",
                "message": str(error),
                "position": getattr(error, "position", None)
            })

            result = {
                "success": False,
                "mode": "LEXER_ERROR",
                "original": correction.get("original"
                ),
                "command": command_to_parse,
                "suggestion": correction.get("suggestion"),
                "score": correction.get("score", 0.0),
                "suggestions": correction.get("suggestions", []),
                "tokens": [],
                "lexer_error": {
                    "message": str(error),
                    "position": getattr(error, "position", None),
                    "character": getattr(error, "character", None)
                },
                "parser": None,
                "trace": (correction.get("trace", []) + pipeline_trace)
            }

            return result

        # TRACE LEXER
        pipeline_trace.append({
            "component": "Lexer",
            "action": "TOKENIZE_SUCCESS",
            "tokens": [token.type for token in tokens]
        })

        # PARSER LL(1)
        parser_result = LL1Parser.parse(tokens, return_trace=True)

        # TRACE PARSER
        pipeline_trace.append({
            "component": "LL1Parser",
            "action": ("ACCEPT" if parser_result.get("success") else "SYNTAX_ERROR"),
            "success": parser_result.get("success")
        })

        # RÉSULTAT FINAL
        success = (parser_result.get("success") is True)
        result = {
            "success": success,
            "mode": mode,
            "original": correction.get("original"),
            "command": command_to_parse,
            "suggestion": correction.get("suggestion"),
            "score": correction.get("score", 0.0),
            "suggestions": correction.get("suggestions", []),
            "tokens": [token.to_dict() if hasattr(token, "to_dict")
                else {
                    "type": token.type,
                    "value": token.value,
                    "position": getattr(token, "position", None)
                }
                for token in tokens
            ],
            "lexer_error": None,
            "parser": parser_result,
            "trace": (correction.get("trace", []) + pipeline_trace
            )
        }

        return result

    # VÉRIFICATION CONTINUATION
    @staticmethod
    def can_continue(result):
        if not isinstance(result, dict):
            return False

        if result.get("success") is not True:
            return False

        mode = result.get("mode")

        return mode in ("VALID", "AUTO_CORRECT")

    # AFFICHAGE
    @staticmethod
    def display(result):

        print()
        print("=" * 80)
        print("PIPELINE COMPLET DE COMMANDE")
        print("=" * 80)
        print(
            f"Commande originale : "
            f"{result.get('original')}"
        )

        print(
            f"Mode : "
            f"{result.get('mode')}"
        )

        print(
            f"Score : "
            f"{result.get('score', 0.0):.4f}"
        )

        if result.get("command"):
            print(
                f"Commande exécutée : "
                f"{result.get('command')}"
            )

        if result.get("suggestion"):
            print()
            print("Suggestion :")
            print(f"  {result.get('suggestion')}")

        # TOKENS
        tokens = result.get("tokens", [])

        if tokens:
            print()
            print("TOKENS :")

            for token in tokens:
                print(
                    f"  {token.get('type')} -"
                    f"{token.get('value')}"
                )

        # ERREUR LEXICALE
        lexer_error = result.get("lexer_error")

        if lexer_error:
            print()
            print("ERREUR LEXICALE :")
            print(f"  " f"{lexer_error.get('message')}")


        # PARSER
        parser = result.get("parser")
        if parser:
            print()
            print(
                "PARSER LL(1) : "
                + (
                    "ACCEPTÉ"
                    if parser.get(
                        "success"
                    )
                    else "ERREUR"
                )
            )

            if parser.get("errors"):
                for error in parser.get("errors", []):
                    print(f"  - " f"{error.get('message')}")


        # TRACE
        print()
        print("TRACE PIPELINE :")

        for step in result.get("trace", []):
            print(f"  - {step}")
        print()