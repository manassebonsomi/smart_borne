from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, OperationalError
from app import app
from config.database import db


def expect_database_rejection(operation):
    """
    Vérifie que la base refuse une opération invalide.

    Selon MySQL/PyMySQL et le type de contrainte,
    SQLAlchemy peut remonter IntegrityError ou OperationalError.
    """

    try:

        operation()

        db.session.commit()

        raise AssertionError(
            "La base a accepté une donnée invalide."
        )

    except (
        IntegrityError,
        OperationalError
    ):

        db.session.rollback()

        return True


def test_age_negative():

    def operation():

        db.session.execute(
            text(
                """
                INSERT INTO utilisateur
                (
                    nom,
                    prenom,
                    age,
                    niveau_scolaire,
                    type_profil
                )
                VALUES
                (
                    'TEST',
                    'AGE',
                    -5,
                    'TEST',
                    'TEST'
                )
                """
            )
        )

    expect_database_rejection(
        operation
    )

    print(
        "PASS : CHECK AGE >= 0"
    )


def test_foreign_key_question():

    def operation():

        db.session.execute(
            text(
                """
                INSERT INTO question
                (
                    texte_question,
                    ordre_question,
                    id_categorie
                )
                VALUES
                (
                    'TEST FOREIGN KEY',
                    999999,
                    999999999
                )
                """
            )
        )

    expect_database_rejection(
        operation
    )

    print(
        "PASS : FOREIGN KEY QUESTION → CATEGORIE"
    )


def test_question_ordre():

    def operation():

        db.session.execute(
            text(
                """
                INSERT INTO question
                (
                    texte_question,
                    active,
                    ordre_question
                )
                VALUES
                (
                    'TEST',
                    TRUE,
                    0
                )
                """
            )
        )

    expect_database_rejection(
        operation
    )

    print(
        "PASS : CHECK ORDRE QUESTION"
    )

    def operation():

        db.session.execute(
            text(
                """
                INSERT INTO session_utilisateur
                (
                    question_actuelle
                )
                VALUES
                (
                    -1
                )
                """
            )
        )

    expect_database_rejection(
        operation
    )

    print(
        "PASS : CHECK SESSION QUESTION"
    )


def test_session_inactivite_negative():

    def operation():

        db.session.execute(
            text(
                """
                INSERT INTO session_utilisateur
                (
                    temps_inactivite
                )
                VALUES
                (
                    -10
                )
                """
            )
        )

    expect_database_rejection(
        operation
    )

    print(
        "PASS : CHECK TEMPS INACTIVITE"
    )


def test_null_question():

    def operation():

        db.session.execute(
            text(
                """
                INSERT INTO question
                (
                    texte_question,
                    ordre_question
                )
                VALUES
                (
                    NULL,
                    1
                )
                """
            )
        )

    expect_database_rejection(
        operation
    )

    print(
        "PASS : NOT NULL QUESTION"
    )


def test_unique_ville():

    result = db.session.execute(
        text(
            """
            SELECT nom_ville
            FROM ville
            LIMIT 1
            """
        )
    ).fetchone()

    if not result:

        print(
            "SKIP : UNIQUE VILLE "
            "(aucune ville existante)"
        )

        return

    nom = result[0]

    def operation():

        db.session.execute(
            text(
                """
                INSERT INTO ville
                (
                    nom_ville
                )
                VALUES
                (
                    :nom
                )
                """
            ),
            {
                "nom": nom
            }
        )

    expect_database_rejection(
        operation
    )

    print(
        "PASS : UNIQUE VILLE"
    )


def test_unique_formateur_email():

    result = db.session.execute(
        text(
            """
            SELECT email
            FROM formateur
            LIMIT 1
            """
        )
    ).fetchone()

    if not result:

        print(
            "SKIP : UNIQUE EMAIL "
            "(aucun formateur existant)"
        )

        return

    email = result[0]

    def operation():

        db.session.execute(
            text(
                """
                INSERT INTO formateur
                (
                    nom,
                    email,
                    mot_de_passe
                )
                VALUES
                (
                    'TEST',
                    :email,
                    'TEST'
                )
                """
            ),
            {
                "email": email
            }
        )

    expect_database_rejection(
        operation
    )

    print(
        "PASS : UNIQUE FORMATEUR EMAIL"
    )


def test_session_question_negative():
    def operation():
        db.session.execute(
            text(
                    """
                    INSERT INTO session_utilisateur
                    (
                        question_actuelle
                    )
                    VALUES
                    (
                        -1
                    )
                    """
                )
            )

        expect_database_rejection(
            operation
        )

        print(
            "PASS : CHECK SESSION QUESTION"
        )
def run_tests():

    print()
    print("=" * 80)
    print("TEST CONTRAINTES BASE DE DONNÉES")
    print("=" * 80)
    print()

    with app.app_context():

        test_age_negative()
        test_question_ordre()
        test_session_question_negative()
        test_session_inactivite_negative()
        test_null_question()
        test_unique_ville()
        test_unique_formateur_email()
        test_foreign_key_question()

    print()
    print("=" * 80)
    print(
        "TOUS LES TESTS DES CONTRAINTES "
        "BASE DE DONNÉES SONT PASSÉS"
    )
    print("=" * 80)


if __name__ == "__main__":
    run_tests()