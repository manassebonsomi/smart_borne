# Modèle de données — CCC Orientation System

## 1. Présentation

Le **CCC Orientation System** s'appuie sur une base de données relationnelle MySQL permettant de centraliser les informations relatives aux utilisateurs, aux questionnaires, aux sessions, aux recommandations, aux commandes et aux opérations du système.

La couche d'accès aux données est assurée par **SQLAlchemy / Flask-SQLAlchemy**.

Le modèle de données est conçu autour de plusieurs entités principales reliées par des clés primaires et des clés étrangères.

---

## 2. Vue générale des entités

Les principales entités du système sont :

```text
Utilisateur
Ville
Formateur
Campagne
SessionUtilisateur
Question
CategorieQuestion
Reponse
Recommandation
Parcours
Commande
Erreur
AuditLog
Evenement
```

## 3. Schéma conceptuel simplifié
```
                              ┌──────────────┐
                              │     Ville    │
                              └──────┬───────┘
                                     │
                                     │ 1:N
                                     ▼
                              ┌──────────────┐
                              │ Utilisateur  │
                              └──────┬───────┘
                                     │
                                     │ 1:N
                                     ▼
                           ┌──────────────────────┐
                           │ SessionUtilisateur   │
                           └──────┬───────┬───────┘
                                  │       │
                           1:N    │       │ N:1
                                  │       ▼
                                  │   ┌──────────────┐
                                  │   │   Campagne   │
                                  │   └──────────────┘
                                  │
                                  │ 1:N
                                  ▼
                           ┌──────────────┐
                           │   Reponse    │
                           └──────┬───────┘
                                  │
                                  │ N:1
                                  ▼
                           ┌──────────────┐
                           │   Question   │
                           └──────┬───────┘
                                  │
                                  │ N:1
                                  ▼
                        ┌─────────────────────┐
                        │ CategorieQuestion   │
                        └─────────────────────┘


                           SessionUtilisateur
                                  │
                                  │ 1:1
                                  ▼
                           ┌────────────────┐
                           │ Recommandation │
                           └───────┬────────┘
                                   │
                                   │ N:1
                                   ▼
                             ┌──────────────┐
                             │   Parcours   │
                             └──────────────┘


                           ┌──────────────┐
                           │  Formateur   │
                           └──────┬───────┘
                                  │
                                  │ 1:N
                                  ▼
                           ┌──────────────┐
                           │   Commande   │
                           └──────────────┘
```


