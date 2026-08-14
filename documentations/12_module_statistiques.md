# Module statistiques — CCC Orientation System

Le **module statistiques** permet de consulter les principales données d'activité du système à travers le contrôleur :

```text
DashboardController.statistics()
```

## 1. Accès par commande

Les statistiques peuvent être demandées à travers la commande :

```text
AFFICHER STATISTIQUES
```

Le traitement suit le pipeline de commandes :

```text
AFFICHER STATISTIQUES
        ↓
CommandCorrector
        ↓
Lexer
        ↓
Parser LL(1)
        ↓
CommandBuilder
        ↓
CommandDispatcher
        ↓
CommandHandler
        ↓
DashboardController.statistics()
```

---

## 2. Réponse du backend

La réponse retournée par le backend conserve les données métier produites par :

```text
DashboardController.statistics()
```

Le résultat peut ensuite être transmis au frontend pour affichage.

L'intégration respecte donc le principe :

```text
Commande
   ↓
Validation
   ↓
Traitement statistique
   ↓
Données métier
   ↓
Réponse JSON
   ↓
Interface utilisateur
```

---

## 3. Intégration dans le système

Le module statistiques est principalement accessible à travers :

```text
CommandHandler
        ↓
DashboardController
        ↓
Données statistiques
```

Il permet ainsi d'intégrer les statistiques au moteur de commandes sans mélanger la logique d'analyse syntaxique avec la logique métier.

---

## 4. Résumé

Le module statistiques repose principalement sur :

```text
AFFICHER STATISTIQUES
        ↓
DashboardController.statistics()
        ↓
Résultat métier
        ↓
Réponse backend
```

Il constitue le point d'accès aux statistiques du système depuis le moteur de commandes du **CCC Orientation System**.