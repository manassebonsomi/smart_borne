# Construction et Validation de la Table LL(1)

La **table d'analyse LL(1)** constitue le mécanisme décisionnel du Parser. Elle est construite à partir des ensembles **FIRST** et **FOLLOW**, puis validée avant son utilisation.

---

## 1. Critères de validation

La table doit respecter les critères suivants :

- **Non-vacuité** : la table contient des transitions valides entre non-terminaux, lookahead et productions.
- **Symbole initial** : `<COMMANDE>` doit être présent.
- **Marqueurs spéciaux** : `EOF` et `EPSILON` doivent être définis.
- **Accessibilité** : les principales familles de commandes doivent être accessibles depuis `<COMMANDE>`.
- **Couverture** : les productions principales doivent être présentes pour :

```text
AFFICHER
LANCER
MODIFIER
SUPPRIMER
EXPORTER
RECOMMENCER
QUITTER
```

---

## 2. Validation automatisée

La table est couverte par **7 tests dédiés** :

| Test | Vérification | Statut |
|---|---|---|
| `TEST-LL1-01` | Table non vide | **PASSED** |
| `TEST-LL1-02` | Présence de `<COMMANDE>` | **PASSED** |
| `TEST-LL1-03` | `EOF` et `EPSILON` définis | **PASSED** |
| `TEST-LL1-04` | Accessibilité des commandes | **PASSED** |
| `TEST-LL1-05` | Absence de conflits LL(1) | **PASSED** |
| `TEST-LL1-06` | Couverture des productions principales | **PASSED** |
| `TEST-LL1-07` | Gestion des tokens inattendus | **PASSED** |

### Résultat

```text
7 / 7 tests passés
100 % de réussite
0 échec
```

La validation confirme que la table LL(1) est suffisamment cohérente pour être utilisée par le Parser syntaxique.