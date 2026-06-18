from controllers.dashboard_controller import \
    DashboardController

from controllers.question_controller import \
    QuestionController

from controllers.utilisateur_controller import \
    UtilisateurController

from controllers.campagne_controller import \
    CampagneController

from controllers.erreur_controller import \
    ErreurController

from controllers.report_controller import \
    ReportController

from services.session_manager import \
    SessionManager


class CommandExecutor:

    @staticmethod
    def execute(tokens, data=None):

        token_types = [

            token.type

            for token in tokens

            if token.type != "EOF"
        ]

        # =====================================
        # AFFICHER STATISTIQUES
        # =====================================

        if token_types == [

            "AFFICHER",
            "STATISTIQUES"
        ]:

            return {

                "action":
                    "AFFICHER_STATISTIQUES",

                "success":
                    True,

                "data":
                    DashboardController
                    .statistics()
            }

        # =====================================
        # AFFICHER ERREURS
        # =====================================

        elif token_types == [

            "AFFICHER",
            "ERREURS"
        ]:

            erreurs = \
                ErreurController.get_all()

            return {

                "action":
                    "AFFICHER_ERREURS",

                "success":
                    True,

                "nombre":
                    len(erreurs),

                "data":

                    [

                        {

                            "id":
                                e.id_erreur,

                            "type":
                                e.type_erreur,

                            "message":
                                e.message,

                            "corrigee":
                                e.corrigee

                        }

                        for e in erreurs
                    ]
            }

        # =====================================
        # LANCER ENQUETE CYBERSECURITE
        # =====================================

        elif token_types == [

            "LANCER",
            "ENQUETE",
            "CYBERSECURITE"
        ]:

            return {

                "action":
                    "ENQUETE_CYBERSECURITE",

                "success":
                    True,

                "etat":
                    "ENQUETE_LANCEE"
            }

        # =====================================
        # LANCER CAMPAGNE ECOLE
        # =====================================

        elif token_types == [

            "LANCER",
            "CAMPAGNE",
            "ECOLE"
        ]:

            return {

                "action":
                    "CAMPAGNE_ECOLE",

                "success":
                    True,

                "etat":
                    "CAMPAGNE_LANCEE"
            }

        # =====================================
        # CHERCHER ENFANTS KINSHASA
        # =====================================

        elif token_types == [

            "CHERCHER",
            "ENFANTS",
            "KINSHASA"
        ]:

            utilisateurs = \
                UtilisateurController \
                .search_children()

            return {

                "action":
                    "RECHERCHE_ENFANTS",

                "success":
                    True,

                "nombre":
                    len(utilisateurs),

                "resultats":

                    [

                        {

                            "id":
                                u.id_utilisateur,

                            "nom":
                                u.nom,

                            "prenom":
                                u.prenom,

                            "age":
                                u.age

                        }

                        for u in utilisateurs
                    ]
            }

        # =====================================
        # CHERCHER ADOLESCENTS PYTHON
        # =====================================

        elif token_types == [

            "CHERCHER",
            "ADOLESCENTS",
            "INTERESSES",
            "PAR",
            "PYTHON"
        ]:

            utilisateurs = \
                UtilisateurController \
                .search_adolescents()

            return {

                "action":
                    "RECHERCHE_ADOS_PYTHON",

                "success":
                    True,

                "nombre":
                    len(utilisateurs),

                "resultats":

                    [

                        {

                            "id":
                                u.id_utilisateur,

                            "nom":
                                u.nom,

                            "prenom":
                                u.prenom,

                            "age":
                                u.age

                        }

                        for u in utilisateurs
                    ]
            }

        # =====================================
        # AJOUTER QUESTION
        # =====================================

        elif token_types == [

            "AJOUTER",
            "QUESTION"
        ]:
            if data:
                question = \
                    QuestionController.create(
                        data["texte_question"],
                        data["ordre_question"],
                        data["id_categorie"]
                    )

            return {

                "action":
                    "AJOUTER_QUESTION",

                "success":
                    question is not None,

                "question_id":
                    question.id_question
                    if question
                    else None
            }

        # else:
        #
        #     return {
        #
        #         "action":
        #             "AJOUTER_QUESTION",
        #
        #         "success":
        #             True,
        #
        #         "etat":
        #             "ATTENTE_DONNEES"
        #     }

        # =====================================
        # MODIFIER QUESTION NUMERO X
        # =====================================

        elif (

            len(token_types) >= 2

            and

            token_types[0:2] == [

                "MODIFIER",
                "QUESTION"
            ]
        ):

            numero = next(

                (

                    token.value

                    for token in tokens

                    if token.type == "NUMERO"

                ),

                None
            )

            if data:
                question = \
                    QuestionController.update(

                        int(numero),

                        texte_question=
                        data.get(
                            "texte_question"
                        ),

                        ordre_question=
                        data.get(
                            "ordre_question"
                        ),

                        active=
                        data.get(
                            "active"
                        )
                    )

                return {

                    "action":
                        "MODIFIER_QUESTION",

                    "success":
                        question is not None,

                    "question_id":
                        numero
                }

            # return {
            #
            #     "action":
            #         "MODIFIER_QUESTION",
            #
            #     "success":
            #         True,
            #
            #     "question_id":
            #         numero,
            #
            #     "etat":
            #         "ATTENTE_NOUVELLES_DONNEES"
            # }

        # =====================================
        # SUPPRIMER QUESTION NUMERO X
        # =====================================

        elif (

            len(token_types) >= 2

            and

            token_types[0:2] == [

                "SUPPRIMER",
                "QUESTION"
            ]
        ):

            numero = next(

                (

                    token.value

                    for token in tokens

                    if token.type == "NUMERO"

                ),

                None
            )

            success = False

            if numero:

                success = \
                    QuestionController.delete(
                        int(numero)
                    )

            return {

                "action":
                    "SUPPRIMER_QUESTION",

                "success":
                    success,

                "question_id":
                    numero
            }

        # =====================================
        # EXPORTER RAPPORT
        # =====================================

        elif token_types == [

            "EXPORTER",
            "RAPPORT"
        ]:

            rapport = \
                ReportController.export_pdf()

            return {

                "action":
                    "EXPORTER_RAPPORT",

                "success":
                    rapport.get(
                        "success",
                        False
                    ),

                "rapport":
                    rapport
            }

        # =====================================
        # RECOMMENCER SESSION
        # =====================================

        elif token_types == [

            "RECOMMENCER",
            "SESSION"
        ]:

            return {

                "action":
                    "RECOMMENCER_SESSION",

                "success":
                    True,

                "etat":
                    "SESSION_REINITIALISEE"
            }

        # =====================================
        # QUITTER
        # =====================================

        elif token_types == [

            "QUITTER"
        ]:

            return {

                "action":
                    "QUITTER",

                "success":
                    True,

                "etat":
                    "FIN_SESSION"
            }

        # =====================================
        # COMMANDE INCONNUE
        # =====================================

        return {

            "action":
                "INCONNUE",

            "success":
                False,

            "message":
                "Commande non reconnue"
        }