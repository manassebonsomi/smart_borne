import pytest

from app import app
from config.database import db
from services.session_manager import SessionManager
from models.session import SessionUtilisateur


@pytest.fixture
def app_context():
    with app.app_context():
        yield


@pytest.fixture
def session_db(app_context):
    session = SessionUtilisateur(
        id_utilisateur=1,
        etat="ACCUEIL",
        question_actuelle=0,
        temps_inactivite=0,
        sauvegardee=False
    )

    db.session.add(session)
    db.session.commit()

    yield session

    db.session.delete(session)
    db.session.commit()


def test_create_session(app_context):

    session = SessionManager.create_session(
        utilisateur_id=1
    )

    assert session is not None
    assert session.id_session is not None
    assert session.id_utilisateur == 1
    assert session.etat == "ACCUEIL"
    assert session.question_actuelle == 0

    db.session.delete(session)
    db.session.commit()


def test_save_progress(session_db):

    result = SessionManager.save_progress(
        session_db.id_session,
        5,
        "QUESTIONNAIRE"
    )

    assert result is not None
    assert result.question_actuelle == 5
    assert result.etat == "QUESTIONNAIRE"
    assert result.sauvegardee is True


def test_save_progress_session_inexistante(app_context):

    result = SessionManager.save_progress(
        999999,
        5,
        "QUESTIONNAIRE"
    )

    assert result is None


def test_pause_session(session_db):

    result = SessionManager.pause_session(
        session_db.id_session
    )

    assert result is not None
    assert result.etat == "SESSION_INTERRUPTION"


def test_is_interrupted_true(session_db):

    SessionManager.pause_session(
        session_db.id_session
    )

    assert (
        SessionManager.is_interrupted(
            session_db.id_session
        )
        is True
    )


def test_is_interrupted_false(session_db):

    assert (
        SessionManager.is_interrupted(
            session_db.id_session
        )
        is False
    )


def test_is_interrupted_session_inexistante(app_context):

    assert (
        SessionManager.is_interrupted(999999)
        is False
    )


def test_set_state(session_db):

    result = SessionManager.set_state(
        session_db.id_session,
        "QUESTIONNAIRE"
    )

    assert result is not None
    assert result.etat == "QUESTIONNAIRE"


def test_set_state_session_inexistante(app_context):

    result = SessionManager.set_state(
        999999,
        "QUESTIONNAIRE"
    )

    assert result is None


def test_resume_session(session_db):

    result = SessionManager.resume_session(
        session_db.id_session
    )

    assert result is not None
    assert result.etat == "REPRISE_SESSION"


def test_update_inactivity(session_db):

    SessionManager.update_inactivity(
        session_db.id_session,
        120
    )

    result = SessionManager.get_session(
        session_db.id_session
    )

    assert result.temps_inactivite == 120


def test_get_session(session_db):

    result = SessionManager.get_session(
        session_db.id_session
    )

    assert result is not None
    assert result.id_session == session_db.id_session


def test_get_last_session(session_db):

    result = SessionManager.get_last_session(
        1
    )

    assert result is not None
    assert result.id_session == session_db.id_session


def test_restart_session(session_db):

    SessionManager.save_progress(
        session_db.id_session,
        8,
        "QUESTIONNAIRE"
    )

    SessionManager.update_inactivity(
        session_db.id_session,
        100
    )

    result = SessionManager.restart_session(
        session_db.id_session
    )

    assert result is not None
    assert result.question_actuelle == 0
    assert result.etat == "ACCUEIL"
    assert result.temps_inactivite == 0


def test_get_interrupted_session(session_db):

    SessionManager.pause_session(
        session_db.id_session
    )

    result = SessionManager.get_interrupted_session(
        1
    )

    assert result is not None
    assert result.id_session == session_db.id_session
    assert result.etat == "SESSION_INTERRUPTION"


def test_can_resume_true(session_db):

    SessionManager.pause_session(
        session_db.id_session
    )

    assert (
        SessionManager.can_resume(1)
        is True
    )


def test_can_resume_false(session_db):

    assert (
        SessionManager.can_resume(1)
        is False
    )


def test_restore_session(session_db):

    SessionManager.pause_session(
        session_db.id_session
    )

    result = SessionManager.restore_session(1)

    assert result is not None
    assert result.id_session == session_db.id_session
    assert result.etat == "QUESTIONNAIRE"


def test_restore_session_inexistante(app_context):

    result = SessionManager.restore_session(
        999999
    )

    assert result is None


def test_finish_if_inactive(session_db):

    SessionManager.update_inactivity(
        session_db.id_session,
        300
    )

    result = SessionManager.finish_if_inactive(
        session_db.id_session,
        limite=300
    )

    assert result is not None
    assert result.etat == "FIN_SESSION"


def test_finish_if_inactive_below_limit(session_db):

    SessionManager.update_inactivity(
        session_db.id_session,
        100
    )

    result = SessionManager.finish_if_inactive(
        session_db.id_session,
        limite=300
    )

    assert result is not None
    assert result.etat != "FIN_SESSION"


def test_finish_if_inactive_session_inexistante(app_context):

    result = SessionManager.finish_if_inactive(
        999999,
        limite=300
    )

    assert result is None


def test_close_session(session_db):

    SessionManager.close_session(
        session_db.id_session
    )

    result = SessionManager.get_session(
        session_db.id_session
    )

    assert result is not None
    assert result.etat == "FIN_SESSION"
    assert result.date_fin is not None


def test_get_state(session_db):

    result = SessionManager.get_state(
        session_db.id_session
    )

    assert result == "ACCUEIL"


def test_get_state_session_inexistante(app_context):

    result = SessionManager.get_state(
        999999
    )

    assert result is None