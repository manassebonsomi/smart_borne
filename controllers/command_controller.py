from models import Commande
from services.audit_service import AuditService
from services.command_corrector import CommandCorrector
from services.lexer import Lexer, LexerError
from services.ll1_parser import LL1Parser
from services.command_builder import CommandBuilder
from services.command_dispatcher import CommandDispatcher
from config.database import db


class CommandController:

    @staticmethod
    def execute(texte_commande, id_formateur=None, data=None):

        # VALIDATION DE LA COMMANDE
        correction = CommandCorrector.correct(texte_commande)

        # SUGGESTION
        if correction["mode"] == "SUGGEST":
            return {
                "success": False,
                "mode": "SUGGEST",
                "original": correction["original"],
                "corrected": correction.get("corrected"),
                "suggestion": correction.get("suggestion"),
                "suggestions": correction.get("suggestions", []),
                "score": correction.get("score", 0.0),
                "requires_confirmation": True,
                "interaction": {
                    "type": "CONFIRMATION",
                    "message": "Voulez-vous dire : " + correction.get("suggestion") + " ? ",
                    "value": correction.get("suggestion")
                },
                "trace": correction.get("trace", [])
            }

        # REFORMULATION
        if correction["mode"] == "REFORMULATE":
            return {
                "success": False,
                "mode": "REFORMULATE",
                "original": correction["original"],
                "corrected": correction.get("corrected"),
                "suggestion": correction.get("suggestion"),
                "suggestions": correction.get("suggestions", []),
                "score": correction.get("score", 0.0),
                "requires_confirmation": False,
                "interaction": {
                    "type": "MESSAGE",
                    "message": "Veuillez reformuler votre commande."
                },
                "trace": correction.get("trace", [])
            }

        # COMMANDE À ANALYSER
        command_text = correction.get("corrected") or correction.get("original")

        # LEXER
        try:
            tokens = Lexer.tokenize(command_text)
        except LexerError as error:
            trace = correction.get("trace", [])
            trace.append("ERREUR LEXICALE : " + str(error))
            AuditService.log_error(str(error))

            return {
                "success": False,
                "mode": "LEXICAL_ERROR",
                "error": "LEXICAL_ERROR",
                "message": str(error),
                "original": correction.get("original"),
                "corrected": command_text,
                "tokens": [],
                "trace": trace
            }

        # PARSER LL(1)
        parser_result = LL1Parser.parse(tokens, return_trace=True)

        if not parser_result["success"]:
            trace = correction.get("trace", [])
            trace.extend(parser_result.get("trace", []))

            return {
                "success": False,
                "mode": "SYNTAX_ERROR",
                "error": "SYNTAX_ERROR",
                "message": parser_result.get("message", "Erreur syntaxique."),
                "errors": parser_result.get("errors", []),
                "trace": trace
            }

        # COMMAND BUILDER
        try:
            command = CommandBuilder.build(tokens)
        except Exception as error:

            AuditService.log_error(str(error))

            return {
                "success": False,
                "mode": "BUILD_ERROR",
                "error": "BUILD_ERROR",
                "message": str(error),
                "trace": correction.get("trace", [])
            }

        # DISPATCHER
        try:
            execution = CommandDispatcher.dispatch(command, data=data)
        except Exception as error:
            db.session.rollback()
            AuditService.log_error(str(error))

            return {
                "success": False,
                "mode": "EXECUTION_ERROR",
                "error": "EXECUTION_ERROR",
                "message": str(error),
                "trace": correction.get("trace", [])
            }

        # SAUVEGARDE DE LA COMMANDE
        try:
            resultat = execution.get("action", "SUCCES")
            commande_db = Commande(
                texte_commande= correction.get("original"),
                tokens=str(tokens),
                resultat=str(execution),
                valide=True,
                id_formateur=id_formateur
            )

            db.session.add(commande_db)
            db.session.commit()

        except Exception as error:
            db.session.rollback()
            AuditService.log_error(str(error))

            return {
                "success": False,
                "mode": "DATABASE_ERROR",
                "error": "DATABASE_ERROR",
                "message": str(error),
                "execution": execution
            }

        # AUDIT
        AuditService.log(
            action="EXECUTION_COMMANDE",
            objet=correction.get("original"),
            resultat=("SUCCES" if execution.get("success", False) else "ECHEC"),
            details=str(execution)
        )

        # RÉSULTAT FINAL
        return {
            "success": execution.get("success", False),
            "mode": correction.get("mode"),
            "commande_id": commande_db.id_commande,
            "original": correction.get("original"),
            "corrected": correction.get("corrected"),
            "execution": execution,
            "resultat": resultat,
            "trace": correction.get("trace", [])
        }