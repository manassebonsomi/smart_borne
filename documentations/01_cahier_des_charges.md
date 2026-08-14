# Cahier des charges — CCC Orientation System

## 1. Présentation du projet

Le **CCC Orientation System** est un système numérique d’orientation destiné à accompagner les bénéficiaires dans l’identification d’un parcours de formation adapté à leur profil.

Le système repose sur plusieurs composants complémentaires permettant de gérer le processus complet d’orientation : collecte des informations, analyse des réponses, recommandation d’un parcours, gestion des sessions, exécution de commandes métier, suivi statistique, gestion des erreurs et conservation des données.

L’architecture a également été conçue pour intégrer une interface de commandes en langage contrôlé, capable d'interpréter, corriger et exécuter des commandes selon une grammaire formelle et un analyseur syntaxique **LL(1)**.

---

## 2. Contexte et problématique

L’orientation des bénéficiaires nécessite de pouvoir recueillir des informations structurées sur leur profil, leurs préférences et leurs intérêts, puis de transformer ces informations en une recommandation cohérente.

Le système doit également prendre en charge les contraintes opérationnelles associées à une utilisation réelle :

- interruption et reprise d’une session ;
- sauvegarde de la progression ;
- gestion des erreurs ;
- contrôle des commandes saisies ;
- protection et intégrité des données ;
- suivi des opérations ;
- production de statistiques et de rapports.

Le projet vise ainsi à disposer d’une solution **structurée, testable, maintenable et évolutive**.

---

## 3. Objectif général

L’objectif général du **CCC Orientation System** est de mettre en place une plateforme permettant de réaliser de manière structurée et sécurisée le processus d’orientation numérique, depuis la collecte des informations jusqu’à la recommandation d’un parcours et à la gestion des opérations du système.

---

## 4. Objectifs spécifiques

Le système doit permettre de :

1. recueillir les informations nécessaires à l’orientation des bénéficiaires ;
2. analyser les réponses fournies au questionnaire ;
3. calculer des scores pour différents parcours de formation ;
4. générer une recommandation adaptée au profil du bénéficiaire ;
5. gérer les sessions d’utilisation et leur progression ;
6. sauvegarder automatiquement les informations importantes ;
7. permettre la reprise d’une session interrompue ;
8. fournir des statistiques sur les données et l’utilisation du système ;
9. gérer les erreurs lexicales, syntaxiques, applicatives et liées aux données ;
10. permettre l’exécution de commandes métier contrôlées ;
11. corriger automatiquement certaines commandes mal saisies ;
12. proposer une suggestion lorsqu’une commande nécessite une confirmation utilisateur ;
13. garantir l’intégrité des données au niveau de la base de données ;
14. disposer d’une suite complète de tests automatisés ;
15. fournir une documentation technique et fonctionnelle complète.

---

## 5. Périmètre fonctionnel

Le système couvre principalement les domaines suivants :

### 5.1. Gestion de l’orientation

Le système prend en charge :

- l’identification du profil ;
- l’analyse de l’âge ;
- l’analyse du niveau scolaire ;
- l’analyse des réponses au questionnaire ;
- le calcul des scores ;
- la sélection du parcours recommandé.

Les parcours actuellement pris en compte sont :

- **Découverte Numérique** ;
- **Scratch Junior** ;
- **Scratch Avancé** ;
- **Python Débutant** ;
- **Mentor Junior**.

---

### 5.2. Gestion des sessions

Le système doit permettre :

- la création d’une session ;
- l’initialisation de son état ;
- la sauvegarde de la progression ;
- le suivi de la question actuelle ;
- la mise en pause ;
- la détection d’une interruption ;
- la reprise d’une session ;
- la restauration d’une session interrompue ;
- la gestion du temps d’inactivité ;
- le redémarrage d’une session ;
- la fermeture d’une session.

---

### 5.3. Gestion des commandes

Le système fournit une interface de commandes permettant notamment de :

```text
AFFICHER STATISTIQUES
AFFICHER ERREURS

LANCER ENQUETE CYBERSECURITE
LANCER CAMPAGNE ECOLE

CHERCHER ENFANTS KINSHASA
CHERCHER ADOLESCENTS INTERESSES PAR PYTHON

AJOUTER QUESTION
MODIFIER QUESTION 3
SUPPRIMER QUESTION 25

EXPORTER RAPPORT

RECOMMENCER SESSION
QUITTER