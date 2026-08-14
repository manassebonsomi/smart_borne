from services.ll1_table import LL1Table
from services.grammar import (
    GRAMMAR,
    START_SYMBOL,
    EOF,
    EPSILON
)


def test_ll1_table_validation():

    result = LL1Table.validate()

    assert result["success"] is True
    assert "table" in result


def test_ll1_table_not_empty():

    result = LL1Table.validate()

    table = result["table"]

    assert table
    assert len(table) > 0

def test_start_symbol_exists():

    assert START_SYMBOL in GRAMMAR


def test_eof_defined():

    assert EOF is not None
    assert isinstance(EOF, str)


def test_epsilon_defined():

    assert EPSILON is not None
    assert isinstance(EPSILON, str)


def test_afficher_statistiques_production():

    result = LL1Table.validate()
    table = result["table"]

    assert "COMMANDE" in table
    assert "AFFICHER" in table["COMMANDE"]

    assert table["COMMANDE"]["AFFICHER"] == [
        "CMD_AFFICHER"
    ]


def test_modifier_question_production():

    result = LL1Table.validate()
    table = result["table"]

    assert "COMMANDE" in table
    assert "MODIFIER" in table["COMMANDE"]

    assert table["COMMANDE"]["MODIFIER"] == [
        "CMD_MODIFIER"
    ]


def test_supprimer_question_production():

    result = LL1Table.validate()
    table = result["table"]

    assert "COMMANDE" in table
    assert "SUPPRIMER" in table["COMMANDE"]

    assert table["COMMANDE"]["SUPPRIMER"] == [
        "CMD_SUPPRIMER"
    ]


def test_lancer_production():

    result = LL1Table.validate()
    table = result["table"]

    assert "COMMANDE" in table
    assert "LANCER" in table["COMMANDE"]

    assert table["COMMANDE"]["LANCER"] == [
        "CMD_LANCER"
    ]


def test_exporter_production():

    result = LL1Table.validate()
    table = result["table"]

    assert "COMMANDE" in table
    assert "EXPORTER" in table["COMMANDE"]

    assert table["COMMANDE"]["EXPORTER"] == [
        "CMD_EXPORTER"
    ]


def test_recommencer_production():

    result = LL1Table.validate()
    table = result["table"]

    assert "COMMANDE" in table
    assert "RECOMMENCER" in table["COMMANDE"]

    assert table["COMMANDE"]["RECOMMENCER"] == [
        "CMD_RECOMMENCER"
    ]


def test_quitter_production():

    result = LL1Table.validate()
    table = result["table"]

    assert "COMMANDE" in table
    assert "QUITTER" in table["COMMANDE"]

    assert table["COMMANDE"]["QUITTER"] == [
        "CMD_QUITTER"
    ]