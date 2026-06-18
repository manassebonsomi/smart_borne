from config.database import db

from models.commande import Commande

from services.lexical_analyzer import \
    LexicalAnalyzer

from services.ll1_parser import \
    LL1Parser

from services.audit_service import \
    AuditService

from services.command_executor import \
    CommandExecutor


class CommandController:

    @staticmethod
    def execute(
            texte_commande,
            id_formateur=None,
            data=None
    ):

        try:

            # ==========================
            # ANALYSE LEXICALE
            # ==========================

            tokens = \
                LexicalAnalyzer.tokenize(
                    texte_commande
                )

            # ==========================
            # ANALYSE SYNTAXIQUE
            # ==========================

            valide = \
                LL1Parser.parse(
                    tokens,
                    data
                )

            execution = None

            # ==========================
            # EXECUTION COMMANDE
            # ==========================

            if valide:

                execution = \
                    CommandExecutor.execute(
                        tokens
                    )

                resultat = \
                    execution.get(
                        "action",
                        "SUCCES"
                    )

            else:

                resultat = \
                    "SYNTAXE_INVALIDE"

            # ==========================
            # SAUVEGARDE COMMANDE
            # ==========================

            commande = Commande(

                texte_commande=
                texte_commande,

                tokens=
                str(tokens),

                resultat=
                str(execution)
                if execution
                else resultat,

                valide=
                valide,

                id_formateur=
                id_formateur
            )

            db.session.add(
                commande
            )

            db.session.commit()

            # ==========================
            # AUDIT SUCCES
            # ==========================

            AuditService.log(

                action=
                "EXECUTION_COMMANDE",

                objet=
                texte_commande,

                resultat=
                "SUCCES"
                if valide
                else
                "ECHEC",

                details=
                str(execution)
            )

            # ==========================
            # REPONSE
            # ==========================

            return {

                "success":
                    valide,

                "commande_id":
                    commande.id_commande,

                "commande":
                    texte_commande,

                "tokens":

                    [

                        {

                            "type":
                                token.type,

                            "value":
                                token.value

                        }

                        for token in tokens
                    ],

                "execution":
                    execution,

                "resultat":
                    resultat
            }

        except Exception as e:

            db.session.rollback()

            AuditService.log_error(
                str(e)
            )

            return {

                "success":
                    False,

                "commande":
                    texte_commande,

                "message":
                    str(e)
            }

    @staticmethod
    def get_all():

        return Commande.query.order_by(

            Commande.id_commande.desc()

        ).all()

    @staticmethod
    def get_by_id(
            id_commande
    ):

        return Commande.query.get(
            id_commande
        )

    @staticmethod
    def delete(
            id_commande
    ):

        try:

            commande = \
                Commande.query.get(
                    id_commande
                )

            if not commande:

                return False

            db.session.delete(
                commande
            )

            db.session.commit()

            AuditService.log(

                action=
                "SUPPRESSION_COMMANDE",

                objet=
                f"Commande {id_commande}",

                resultat=
                "SUCCES",

                details=
                "Suppression effectuée"
            )

            return True

        except Exception as e:

            db.session.rollback()

            AuditService.log_error(
                str(e)
            )

            return False