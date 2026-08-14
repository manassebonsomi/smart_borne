# Diagramme des états de session — CCC Orientation System

## 1. Présentation

La gestion des sessions constitue un élément central du **CCC Orientation System**. Elle permet de conserver l'état d'avancement d'un bénéficiaire dans le questionnaire, de sauvegarder sa progression et de reprendre une session interrompue.

Le cycle de vie d'une session est géré principalement par le `SessionManager` et repose sur un ensemble d'états permettant de représenter précisément la situation courante de la session.

---

## 2. États principaux

Les principaux états actuellement utilisés par le système sont :

```text
ACCUEIL
   ↓
QUESTIONNAIRE
   ↓
SESSION_INTERRUPTION
   ↓
REPRISE_SESSION
   ↓
QUESTIONNAIRE
   ↓
FIN_SESSION
```

## 3. Diagramme global du cycle de vie

```text
                    ┌──────────────┐
                    │   ACCUEIL    │
                    └──────┬───────┘
                           │
                           │ Démarrage
                           ▼
                    ┌──────────────┐
                    │ QUESTIONNAIRE│
                    └──────┬───────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              │ Pause / interruption    │ Fin
              ▼                         ▼
   ┌──────────────────────┐      ┌──────────────┐
   │ SESSION_INTERRUPTION │      │ FIN_SESSION  │
   └──────────┬───────────┘      └──────────────┘
              │
              │ Restauration
              ▼
      ┌──────────────────┐
      │ REPRISE_SESSION  │
      └────────┬─────────┘
               │
               │ Retour au questionnaire
               ▼
      ┌──────────────────┐
      │   QUESTIONNAIRE  │
      └────────┬─────────┘
               │
               │ Finalisation
               ▼
        ┌──────────────┐
        │ FIN_SESSION  │
        └──────────────┘