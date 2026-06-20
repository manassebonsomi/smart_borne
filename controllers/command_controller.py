from models import Commande
from services.audit_service import AuditService
from services.command_executor import CommandExecutor
from services.lexical_analyzer import LexicalAnalyzer
from services.ll1_parser import LL1Parser
from config.database import db


class CommandController:

    @staticmethod
    def execute(
        texte_commande,
        id_formateur=None,
        data=None
    ):

        try:

            tokens = LexicalAnalyzer.tokenize(
                texte_commande
            )

            valide = LL1Parser.parse(tokens)

            execution = None
            resultat = "SYNTAXE_INVALIDE"

            if valide:

                execution = CommandExecutor.execute(
                    tokens,
                    data=data
                )

                resultat = execution.get(
                    "action",
                    "SUCCES"
                )

            commande = Commande(
                texte_commande=texte_commande,
                tokens=str(tokens),
                resultat=str(execution) if execution else resultat,
                valide=valide,
                id_formateur=id_formateur
            )

            db.session.add(commande)
            db.session.commit()

            AuditService.log(
                action="EXECUTION_COMMANDE",
                objet=texte_commande,
                resultat="SUCCES" if valide else "ECHEC",
                details=str(execution)
            )

            return {
                "success": valide,
                "commande_id": commande.id_commande,
                "execution": execution,
                "resultat": resultat
            }

        except Exception as e:

            db.session.rollback()

            AuditService.log_error(str(e))

            return {
                "success": False,
                "message": str(e)
            }