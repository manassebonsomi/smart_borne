# Architecture générale — CCC Orientation System

## 1. Vue d’ensemble

Le **CCC Orientation System** repose sur une architecture en couches séparant clairement l’interface utilisateur, l’API, l’analyse des commandes, leur transformation en représentation structurée, leur dispatching vers les traitements métier et leur persistance dans la base de données.

L’architecture générale peut être représentée comme suit :

```text
┌──────────────────────────────────────────────┐
│        Interface utilisateur / borne         │
│                                              │
│  Saisie de commandes                         │
│  Affichage des résultats                     │
│  Confirmation OUI / NON                      │
│  Formulaires dynamiques                      │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│                 API Flask                    │
│                                              │
│        Routes HTTP / JSON                    │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│             CommandController                │
│                                              │
│  Orchestration du traitement de commande     │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│            CommandCorrector                 │
│                                              │
│  VALID                                       │
│  AUTO_CORRECT                                │
│  SUGGEST                                     │
│  REFORMULATE                                 │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│                    Lexer                     │
│                                              │
│  Texte → Tokens                              │
│  Mots réservés                               │
│  NUMERO                                      │
│  EOF                                         │
│  Erreurs lexicales                           │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│                 Parser LL(1)                 │
│                                              │
│  Grammaire                                   │
│  FIRST / FOLLOW                              │
│  Table LL(1)                                 │
│  Validation syntaxique                      │
│  Récupération d’erreurs                     │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│               CommandBuilder                 │
│                                              │
│  Tokens → Command                            │
│  Action                                      │
│  Sujet                                       │
│  Arguments                                   │
│  Représentation structurée                   │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│             CommandDispatcher               │
│                                              │
│  Identification de l’action métier          │
│  Sélection du handler                        │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│               CommandHandler                 │
│                                              │
│  Exécution de l’action métier                │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│             Contrôleurs métier               │
│                                              │
│  Questions                                   │
│  Utilisateurs                                │
│  Campagnes                                   │
│  Statistiques                                │
│  Rapports                                    │
│  Erreurs                                     │
│  Sessions                                    │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│          SQLAlchemy / MySQL                  │
│                                              │
│  Persistance                                 │
│  Contraintes                                 │
│  Relations                                   │
│  Intégrité des données                      │
└──────────────────────────────────────────────┘