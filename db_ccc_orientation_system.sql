CREATE DATABASE IF NOT EXISTS db_ccc_orientation_system
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE db_ccc_orientation_system;

CREATE TABLE ville
(
    id_ville INT AUTO_INCREMENT PRIMARY KEY,
    nom_ville VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE utilisateur
(
    id_utilisateur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    type_profil ENUM(
        'ENFANT',
        'ADOLESCENT',
        'PARENT'
    ) NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_ville INT NOT NULL,
    CONSTRAINT fk_utilisateur_ville FOREIGN KEY(id_ville) REFERENCES ville(id_ville)
);

CREATE TABLE campagne
(
    id_campagne INT AUTO_INCREMENT PRIMARY KEY,
    nom_campagne VARCHAR(150) NOT NULL,
    description TEXT,
    date_debut DATE,
    date_fin DATE,
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE session_utilisateur
(
    id_session INT AUTO_INCREMENT PRIMARY KEY,
    date_debut DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_fin DATETIME,
    etat VARCHAR(50),
    sauvegardee BOOLEAN DEFAULT FALSE,
    question_actuelle INT DEFAULT 0,
    temps_inactivite INT DEFAULT 0,
    id_utilisateur INT NOT NULL,
    id_campagne INT,
    FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY(id_campagne) REFERENCES campagne(id_campagne)
);

CREATE TABLE categorie_question
(
    id_categorie INT AUTO_INCREMENT PRIMARY KEY,
    nom_categorie VARCHAR(100) NOT NULL
);

CREATE TABLE question
(
    id_question INT AUTO_INCREMENT PRIMARY KEY,
    texte_question TEXT NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    ordre_question INT NOT NULL,
    id_categorie INT NOT NULL,
    FOREIGN KEY(id_categorie) REFERENCES categorie_question(id_categorie)
);

CREATE TABLE reponse
(
    id_reponse INT AUTO_INCREMENT PRIMARY KEY,
    valeur_reponse TEXT NOT NULL,
    date_reponse TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_session INT NOT NULL,
    id_question INT NOT NULL,
    FOREIGN KEY(id_session) REFERENCES session_utilisateur(id_session),
    FOREIGN KEY(id_question) REFERENCES question(id_question)
);

CREATE TABLE parcours
(
    id_parcours INT AUTO_INCREMENT PRIMARY KEY,
    nom_parcours VARCHAR(150) NOT NULL,
    description TEXT
);

CREATE TABLE recommandation
(
    id_recommandation INT AUTO_INCREMENT PRIMARY KEY,
    score DECIMAL(5,2),
    profil_detecte VARCHAR(100),
    commentaire TEXT,
    date_generation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_session INT UNIQUE,
    id_parcours INT NOT NULL,
    FOREIGN KEY(id_session) REFERENCES session_utilisateur(id_session),
    FOREIGN KEY(id_parcours) REFERENCES parcours(id_parcours)
);

CREATE TABLE formateur
(
    id_formateur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    actif BOOLEAN DEFAULT TRUE
);

CREATE TABLE commande
(
    id_commande INT AUTO_INCREMENT PRIMARY KEY,
    texte_commande TEXT NOT NULL,
    tokens TEXT,
    resultat TEXT,
    valide BOOLEAN,
    date_execution TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_formateur INT,
    FOREIGN KEY(id_formateur) REFERENCES formateur(id_formateur)
);

CREATE TABLE erreur
(
    id_erreur INT AUTO_INCREMENT PRIMARY KEY,
    type_erreur VARCHAR(100),
    message TEXT,
    corrigee BOOLEAN DEFAULT FALSE,
    date_erreur TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_log
(
    id_audit INT AUTO_INCREMENT PRIMARY KEY,
    date_action TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    action VARCHAR(255),
    objet VARCHAR(255),
    resultat VARCHAR(100),
    details TEXT
);

CREATE TABLE evenement
(
    id_evenement INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(255),
    description TEXT,
    date_evenement DATETIME
);

CREATE INDEX idx_utilisateur_ville
ON utilisateur(id_ville);

CREATE INDEX idx_session_utilisateur
ON session_utilisateur(id_utilisateur);

CREATE INDEX idx_reponse_question
ON reponse(id_question);

CREATE INDEX idx_recommandation_score
ON recommandation(score);

CREATE INDEX idx_commande_formateur
ON commande(id_formateur);

CREATE VIEW vue_stat_utilisateurs AS
SELECT type_profil, COUNT(*) total
FROM utilisateur
GROUP BY type_profil;

CREATE VIEW vue_stat_villes AS
SELECT v.nom_ville, COUNT(u.id_utilisateur) total
FROM ville v
LEFT JOIN utilisateur u
ON v.id_ville=u.id_ville
GROUP BY v.nom_ville;

CREATE VIEW vue_stat_parcours AS
SELECT p.nom_parcours, COUNT(*) total
FROM recommandation r
INNER JOIN parcours p
ON p.id_parcours=r.id_parcours
GROUP BY p.nom_parcours;


DELIMITER $$
CREATE PROCEDURE AjouterCampagne(IN p_nom VARCHAR(150), IN p_description TEXT)
BEGIN
INSERT INTO campagne(nom_campagne, description, active)
VALUES(p_nom, p_description, TRUE);
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE AjouterErreur(IN p_type VARCHAR(100), IN p_message TEXT)
BEGIN
INSERT INTO erreur(type_erreur, message)
VALUES(p_type, p_message);
END $$
DELIMITER ;


DELIMITER $$
CREATE TRIGGER trg_commande_insert
AFTER INSERT
ON commande
FOR EACH ROW
BEGIN
INSERT INTO audit_log(action, objet, resultat, details)
VALUES('COMMANDE', NEW.texte_commande, 'EXECUTEE', NEW.resultat);
END $$
DELIMITER ;


DELIMITER $$
CREATE TRIGGER trg_erreur_insert
AFTER INSERT
ON erreur
FOR EACH ROW
BEGIN
INSERT INTO audit_log(action, objet, resultat, details)
VALUES('ERREUR', NEW.type_erreur, 'ENREGISTREE', NEW.message);
END $$
DELIMITER ;


INSERT INTO ville(nom_ville)
VALUES ('Kinshasa'), ('Matadi'), ('Goma'), ('Lubumbashi'), ('Mbandaka'), ('Kisangani'), ('Kananga'), ('Bukavu');

INSERT INTO categorie_question(nom_categorie)
VALUES ('Créativité'), ('Logique'), ('Programmation'), ('Leadership'), ('Numérique'), ('Téléphone'), ('Internet'), ('Scratch'), ('Python'), ('Robotique'), ('Cybersécurité'), ('Réseaux sociaux');

INSERT INTO parcours(nom_parcours, description)
VALUES ('Découverte Numérique', 'Initiation aux outils numériques'),
('Scratch Junior', 'Apprentissage de Scratch'), ('Scratch Avancé', 'Approfondissement Scratch'),
('Python Débutant', 'Introduction à Python'), ('Mentor Junior', 'Préparation au mentorat CCC');