# test_command_handler.py

from unittest.mock import patch, MagicMock

from services.command_handler import CommandHandler


# ==========================================================
# OUTILS
# ==========================================================

def build_handler_command(
    action,
    arguments=None
):
    """
    Construit une commande correspondant au contrat
    attendu par CommandHandler.

    Le Dispatcher est responsable de transformer
    une Command structurée en action métier avant
    d'appeler le Handler.
    """

    return {
        "action": action,
        "arguments": arguments or {}
    }


# ==========================================================
# AFFICHER STATISTIQUES
# ==========================================================

def test_afficher_statistiques():

    handler = CommandHandler()

    with patch(
        "services.command_handler.DashboardController.statistics",
        return_value={
            "utilisateurs": 10,
            "questions": 5,
            "sessions": 3
        }
    ) as mock_statistics:

        command = build_handler_command(
            "AFFICHER_STATISTIQUES"
        )

        result = handler.handle(
            command
        )

        assert (
            result["action"]
            ==
            "AFFICHER_STATISTIQUES"
        )

        assert result["success"] is True

        assert (
            result["data"]["utilisateurs"]
            ==
            10
        )

        mock_statistics.assert_called_once()

    print(
        "PASS : AFFICHER STATISTIQUES"
    )


# ==========================================================
# AFFICHER ERREURS
# ==========================================================

def test_afficher_erreurs():

    handler = CommandHandler()

    erreur = MagicMock()

    erreur.id_erreur = 1
    erreur.type_erreur = "LEXICALE"
    erreur.message = "Mot inconnu"
    erreur.corrigee = False

    with patch(
        "services.command_handler.ErreurController.get_all",
        return_value=[erreur]
    ) as mock_get_all:

        command = build_handler_command(
            "AFFICHER_ERREURS"
        )

        result = handler.handle(
            command
        )

        assert (
            result["action"]
            ==
            "AFFICHER_ERREURS"
        )

        assert result["success"] is True

        assert result["nombre"] == 1

        assert (
            result["data"][0]["type"]
            ==
            "LEXICALE"
        )

        mock_get_all.assert_called_once()

    print(
        "PASS : AFFICHER ERREURS"
    )


# ==========================================================
# ENQUÊTE CYBERSÉCURITÉ
# ==========================================================

def test_enquete_cybersecurite():

    handler = CommandHandler()

    command = build_handler_command(
        "ENQUETE_CYBERSECURITE"
    )

    result = handler.handle(
        command
    )

    assert (
        result["action"]
        ==
        "ENQUETE_CYBERSECURITE"
    )

    assert result["success"] is True

    assert (
        result["etat"]
        ==
        "ENQUETE_LANCEE"
    )

    print(
        "PASS : ENQUETE CYBERSECURITE"
    )


# ==========================================================
# CAMPAGNE ECOLE
# ==========================================================

def test_campagne_ecole():

    handler = CommandHandler()

    campagne = MagicMock()

    campagne.id_campagne = 25

    with patch(
        "services.command_handler.CampagneController.create",
        return_value=campagne
    ) as mock_create:

        command = build_handler_command(
            "CAMPAGNE_ECOLE"
        )

        result = handler.handle(
            command
        )

        assert (
            result["action"]
            ==
            "CAMPAGNE_ECOLE"
        )

        assert result["success"] is True

        assert (
            result["campagne_id"]
            ==
            25
        )

        assert (
            result["etat"]
            ==
            "CAMPAGNE_LANCEE"
        )

        mock_create.assert_called_once()

    print(
        "PASS : CAMPAGNE ECOLE"
    )


# ==========================================================
# RECHERCHE ENFANTS
# ==========================================================

def test_recherche_enfants():

    handler = CommandHandler()

    utilisateur = MagicMock()

    utilisateur.id_utilisateur = 1
    utilisateur.nom = "Dupont"
    utilisateur.prenom = "Jean"
    utilisateur.age = 10

    with patch(
        "services.command_handler.UtilisateurController.search_children",
        return_value=[utilisateur]
    ) as mock_search:

        command = build_handler_command(
            "RECHERCHE_ENFANTS"
        )

        result = handler.handle(
            command
        )

        assert (
            result["action"]
            ==
            "RECHERCHE_ENFANTS"
        )

        assert result["success"] is True

        assert result["nombre"] == 1

        assert (
            result["resultats"][0]["nom"]
            ==
            "Dupont"
        )

        mock_search.assert_called_once()

    print(
        "PASS : RECHERCHE ENFANTS"
    )


# ==========================================================
# RECHERCHE ADOLESCENTS PYTHON
# ==========================================================

def test_recherche_adolescents():

    handler = CommandHandler()

    utilisateur = MagicMock()

    utilisateur.id_utilisateur = 2
    utilisateur.nom = "Martin"
    utilisateur.prenom = "Paul"
    utilisateur.age = 15

    with patch(
        "services.command_handler.UtilisateurController.search_adolescents",
        return_value=[utilisateur]
    ) as mock_search:

        command = build_handler_command(
            "RECHERCHE_ADOS_PYTHON"
        )

        result = handler.handle(
            command
        )

        assert (
            result["action"]
            ==
            "RECHERCHE_ADOS_PYTHON"
        )

        assert result["success"] is True

        assert result["nombre"] == 1

        assert (
            result["resultats"][0]["age"]
            ==
            15
        )

        mock_search.assert_called_once()

    print(
        "PASS : RECHERCHE ADOLESCENTS PYTHON"
    )


# ==========================================================
# AJOUTER QUESTION - SANS DONNÉES
# ==========================================================

def test_ajouter_question_sans_donnees():

    handler = CommandHandler()

    command = build_handler_command(
        "AJOUTER_QUESTION"
    )

    result = handler.handle(
        command,
        data=None
    )

    assert (
        result["action"]
        ==
        "AJOUTER_QUESTION"
    )

    assert result["success"] is False

    assert (
        result["etat"]
        ==
        "ATTENTE_DONNEES"
    )

    assert result["show_form"] is True

    assert (
        result["form_type"]
        ==
        "add_question"
    )

    print(
        "PASS : AJOUTER QUESTION SANS DONNEES"
    )


# ==========================================================
# AJOUTER QUESTION
# ==========================================================

def test_ajouter_question():

    handler = CommandHandler()

    question = MagicMock()

    question.id_question = 10

    with patch(
        "services.command_handler.QuestionController.create",
        return_value=question
    ) as mock_create:

        command = build_handler_command(
            "AJOUTER_QUESTION"
        )

        data = {
            "texte_question": "Question test",
            "ordre_question": 1,
            "id_categorie": 2
        }

        result = handler.handle(
            command,
            data=data
        )

        assert (
            result["action"]
            ==
            "AJOUTER_QUESTION"
        )

        assert result["success"] is True

        assert (
            result["question_id"]
            ==
            10
        )

        mock_create.assert_called_once_with(
            "Question test",
            1,
            2
        )

    print(
        "PASS : AJOUTER QUESTION"
    )


# ==========================================================
# MODIFIER QUESTION - SANS DONNÉES
# ==========================================================

def test_modifier_question_sans_donnees():

    handler = CommandHandler()

    command = build_handler_command(
        "MODIFIER_QUESTION",
        {
            "numero": 3
        }
    )

    result = handler.handle(
        command,
        data=None
    )

    assert (
        result["action"]
        ==
        "MODIFIER_QUESTION"
    )

    assert result["success"] is False

    assert (
        result["etat"]
        ==
        "ATTENTE_DONNEES"
    )

    assert (
        result["question_id"]
        ==
        3
    )

    assert (
        result["form_type"]
        ==
        "edit_question"
    )

    print(
        "PASS : MODIFIER QUESTION SANS DONNEES"
    )


# ==========================================================
# MODIFIER QUESTION
# ==========================================================

def test_modifier_question():

    handler = CommandHandler()

    question = MagicMock()

    question.id_question = 3

    with patch(
        "services.command_handler.QuestionController.update",
        return_value=question
    ) as mock_update:

        command = build_handler_command(
            "MODIFIER_QUESTION",
            {
                "numero": 3
            }
        )

        data = {
            "texte_question": "Question modifiée",
            "ordre_question": 2,
            "active": True
        }

        result = handler.handle(
            command,
            data=data
        )

        assert (
            result["action"]
            ==
            "MODIFIER_QUESTION"
        )

        assert result["success"] is True

        assert (
            result["question_id"]
            ==
            3
        )

        mock_update.assert_called_once_with(
            3,
            texte_question="Question modifiée",
            ordre_question=2,
            active=True
        )

    print(
        "PASS : MODIFIER QUESTION"
    )


# ==========================================================
# SUPPRIMER QUESTION
# ==========================================================

def test_supprimer_question():

    handler = CommandHandler()

    with patch(
        "services.command_handler.QuestionController.delete",
        return_value=True
    ) as mock_delete:

        command = build_handler_command(
            "SUPPRIMER_QUESTION",
            {
                "numero": 25
            }
        )

        result = handler.handle(
            command
        )

        assert (
            result["action"]
            ==
            "SUPPRIMER_QUESTION"
        )

        assert result["success"] is True

        assert (
            result["question_id"]
            ==
            25
        )

        mock_delete.assert_called_once_with(
            25
        )

    print(
        "PASS : SUPPRIMER QUESTION"
    )


# ==========================================================
# EXPORTER RAPPORT
# ==========================================================

def test_exporter_rapport():

    handler = CommandHandler()

    with patch(
        "services.command_handler.ReportController.export_pdf",
        return_value={
            "success": True,
            "filename": "rapport.pdf"
        }
    ) as mock_export:

        command = build_handler_command(
            "EXPORTER_RAPPORT"
        )

        result = handler.handle(
            command
        )

        assert (
            result["action"]
            ==
            "EXPORTER_RAPPORT"
        )

        assert result["success"] is True

        assert (
            result["rapport"]["filename"]
            ==
            "rapport.pdf"
        )

        mock_export.assert_called_once()

    print(
        "PASS : EXPORTER RAPPORT"
    )


# ==========================================================
# RECOMMENCER SESSION
# ==========================================================

def test_recommencer_session():

    handler = CommandHandler()

    session = MagicMock()

    session.id_session = 7

    with patch(
        "services.command_handler.SessionManager.get_last_session",
        return_value=session
    ) as mock_get_last, patch(
        "services.command_handler.SessionManager.restart_session"
    ) as mock_restart:

        command = build_handler_command(
            "RECOMMENCER_SESSION"
        )

        result = handler.handle(
            command
        )

        assert (
            result["action"]
            ==
            "RECOMMENCER_SESSION"
        )

        assert result["success"] is True

        mock_get_last.assert_called_once_with(
            1
        )

        mock_restart.assert_called_once_with(
            7
        )

    print(
        "PASS : RECOMMENCER SESSION"
    )


# ==========================================================
# QUITTER
# ==========================================================

def test_quitter():

    handler = CommandHandler()

    session = MagicMock()

    session.id_session = 8

    with patch(
        "services.command_handler.SessionManager.get_last_session",
        return_value=session
    ) as mock_get_last, patch(
        "services.command_handler.SessionManager.close_session"
    ) as mock_close:

        command = build_handler_command(
            "QUITTER"
        )

        result = handler.handle(
            command
        )

        assert (
            result["action"]
            ==
            "QUITTER"
        )

        assert result["success"] is True

        mock_get_last.assert_called_once_with(
            1
        )

        mock_close.assert_called_once_with(
            8
        )

    print(
        "PASS : QUITTER"
    )


# ==========================================================
# ACTION INCONNUE
# ==========================================================

def test_action_inconnue():

    handler = CommandHandler()

    result = handler.handle(
        {
            "action": "ACTION_INEXISTANTE",
            "arguments": {}
        }
    )

    assert result["success"] is False

    print(
        "PASS : ACTION INCONNUE"
    )


# ==========================================================
# EXÉCUTION
# ==========================================================

if __name__ == "__main__":

    print()
    print("=" * 80)
    print("TEST COMMAND HANDLER")
    print("=" * 80)
    print()

    test_afficher_statistiques()

    test_afficher_erreurs()

    test_enquete_cybersecurite()

    test_campagne_ecole()

    test_recherche_enfants()

    test_recherche_adolescents()

    test_ajouter_question_sans_donnees()

    test_ajouter_question()

    test_modifier_question_sans_donnees()

    test_modifier_question()

    test_supprimer_question()

    test_exporter_rapport()

    test_recommencer_session()

    test_quitter()

    test_action_inconnue()

    print()
    print("=" * 80)
    print(
        "TOUS LES TESTS COMMAND HANDLER "
        "SONT PASSÉS"
    )
    print("=" * 80)