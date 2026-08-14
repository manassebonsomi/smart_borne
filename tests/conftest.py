import pytest

from app import app
from config.database import db


@pytest.fixture
def flask_app():
    """
    Fournit l'application Flask pour les tests.
    """

    app.config["TESTING"] = True

    with app.app_context():
        yield app


@pytest.fixture
def client(flask_app):
    """
    Client HTTP Flask pour les tests des routes.
    """

    return flask_app.test_client()


@pytest.fixture
def db_session(flask_app):
    """
    Fournit une session SQLAlchemy dans
    un contexte Flask actif.
    """

    yield db.session

    db.session.rollback()