from app import app
from config.database import db
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


CONSTRAINTS = [

    # ------------------------------------------------------
    # UTILISATEUR
    # ------------------------------------------------------

    (
        "utilisateur",
        "ck_utilisateur_age_positif",
        """
        ALTER TABLE utilisateur
        ADD CONSTRAINT ck_utilisateur_age_positif
        CHECK (age >= 0)
        """
    ),

    # ------------------------------------------------------
    # QUESTION
    # ------------------------------------------------------

    (
        "question",
        "ck_question_ordre_positif",
        """
        ALTER TABLE question
        ADD CONSTRAINT ck_question_ordre_positif
        CHECK (ordre_question > 0)
        """
    ),

    # ------------------------------------------------------
    # SESSION
    # ------------------------------------------------------

    (
        "session_utilisateur",
        "ck_session_question_actuelle",
        """
        ALTER TABLE session_utilisateur
        ADD CONSTRAINT ck_session_question_actuelle
        CHECK (question_actuelle >= 0)
        """
    ),

    (
        "session_utilisateur",
        "ck_session_temps_inactivite",
        """
        ALTER TABLE session_utilisateur
        ADD CONSTRAINT ck_session_temps_inactivite
        CHECK (temps_inactivite >= 0)
        """
    ),

    # ------------------------------------------------------
    # RECOMMANDATION
    # ------------------------------------------------------

    (
        "recommandation",
        "ck_recommandation_score_positif",
        """
        ALTER TABLE recommandation
        ADD CONSTRAINT ck_recommandation_score_positif
        CHECK (score >= 0)
        """
    ),
]


def constraint_exists(
    table_name,
    constraint_name
):

    sql = text(
        """
        SELECT COUNT(*)
        FROM information_schema.TABLE_CONSTRAINTS
        WHERE CONSTRAINT_SCHEMA = DATABASE()
        AND TABLE_NAME = :table_name
        AND CONSTRAINT_NAME = :constraint_name
        """
    )

    result = db.session.execute(
        sql,
        {
            "table_name": table_name,
            "constraint_name": constraint_name
        }
    )

    return result.scalar() > 0


def apply_constraints():

    print()
    print("=" * 80)
    print("RENFORCEMENT DE LA BASE DE DONNÉES")
    print("=" * 80)

    for (
        table,
        constraint,
        sql
    ) in CONSTRAINTS:

        print()
        print(
            f"[{table}] "
            f"{constraint}"
        )

        if constraint_exists(
            table,
            constraint
        ):

            print(
                "  -> Déjà présente."
            )

            continue

        try:

            db.session.execute(
                text(sql)
            )

            db.session.commit()

            print(
                "  -> Ajoutée avec succès."
            )

        except SQLAlchemyError as error:

            db.session.rollback()

            print(
                "  -> ERREUR :"
            )

            print(
                f"     {error}"
            )

    print()
    print("=" * 80)
    print("RENFORCEMENT TERMINÉ")
    print("=" * 80)


if __name__ == "__main__":

    with app.app_context():

        apply_constraints()