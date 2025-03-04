-- Script de création des tables
DROP TABLE IF EXISTS Classement;
DROP TABLE IF EXISTS Remise;
DROP TABLE IF EXISTS Commerce;
DROP TABLE IF EXISTS Produit;
DROP TABLE IF EXISTS Vache;
DROP TABLE IF EXISTS Clapier;
DROP TABLE IF EXISTS Poule;
DROP TABLE IF EXISTS Compte;
DROP TABLE IF EXISTS Ferme;

-- Information global aux compte de l'utilisateur
CREATE TABLE Ferme (
    idFerme SERIAL PRIMARY KEY,
    nom VARCHAR(40) UNIQUE CHECK (LENGTH(nom) >= 3) NOT NULL,
    ecus DECIMAL(10,2) DEFAULT 1500 CHECK (ecus >= 0) NOT NULL,
    enHibernation DATE,
    achatRestant SMALLINT DEFAULT 12 CHECK (achatRestant >= 0) NOT NULL,
    dernierAchat DATE
);

CREATE TABLE Compte (
    idCompte SERIAL PRIMARY KEY,
    idFerme INTEGER UNIQUE REFERENCES Ferme(idFerme),
    pseudo VARCHAR(40) UNIQUE CHECK (LENGTH(pseudo) >= 3) NOT NULL,
    derniereConnexion TIMESTAMP
);

-- Gestion des animaux de la ferme
CREATE TABLE Poule (
    idPoule SERIAL PRIMARY KEY,
    proprietaire INTEGER REFERENCES Ferme(idFerme),
    poids DECIMAL(5,2) DEFAULT 0.05 CHECK (poids >= 0) NOT NULL,
    age INTEGER DEFAULT 0 CHECK (age >= 0),
    sexe CHAR(1) CHECK (sexe IN ('M', 'F', 'U')) NOT NULL,   -- U pour Unknown
    nb_oeuf INTEGER DEFAULT 0 CHECK (nb_oeuf >= 0) NOT NULL,
    dernier_repas DATE,
    dernier_breuvage DATE,
    dernier_lavage DATE,
    malade_depuis DATE
);

CREATE TABLE Clapier (
    proprietaire INTEGER PRIMARY KEY REFERENCES Ferme(idFerme),
    dernier_repas DATE,
    dernier_breuvage DATE,
    dernier_lavage DATE,
    malade_depuis DATE,
    nb_bebe INTEGER DEFAULT 8 CHECK (nb_bebe >= 0) NOT NULL,
    nb_petit INTEGER DEFAULT 0 CHECK (nb_petit >= 0) NOT NULL,
    nb_gros INTEGER DEFAULT 0 CHECK (nb_gros >= 0) NOT NULL,
    nb_adulte_m INTEGER DEFAULT 0 CHECK (nb_adulte_m >= 0) NOT NULL,
    nb_adulte_f INTEGER DEFAULT 0 CHECK (nb_adulte_f >= 0) NOT NULL
);

CREATE TABLE Vache (
    proprietaire INTEGER PRIMARY KEY REFERENCES Ferme(idFerme),
    poids INTEGER DEFAULT 1 CHECK (poids >= 0) NOT NULL,
    age INTEGER DEFAULT 0 CHECK (age >= 0) NOT NULL,
    qt_lait INTEGER DEFAULT 0 CHECK (qt_lait >= 0) NOT NULL,
    dernier_repas DATE,
    dernier_breuvage DATE,
    dernier_lavage DATE,
    malade_depuis DATE
);

-- Gestion du stock et de l'économie des fermes
CREATE TABLE Produit (
    idProduit SERIAL PRIMARY KEY,
    nom VARCHAR(40) UNIQUE CHECK (LENGTH(nom) >= 2) NOT NULL,
    description VARCHAR(180),
    estVendable BOOLEAN NOT NULL
    -- type VARCHAR(20) -- L'idée était de ditinguer les animaux du reste, mais je crois pas qu'il y ait besoin au final
);

CREATE TABLE Commerce (
    idTransac BIGSERIAL PRIMARY KEY,
    idAcheteur INTEGER REFERENCES Ferme(idFerme),
    idVendeur INTEGER REFERENCES Ferme(idFerme),
    produit INTEGER REFERENCES Produit(idProduit),
    quantite INTEGER CHECK (quantite >= 1) NOT NULL,
    prixUnitaire DECIMAL(10,2) CHECK (prixUnitaire > 0) NOT NULL,
    enVenteDepuis TIMESTAMP
);

CREATE TABLE Remise (
    idProduit SERIAL PRIMARY KEY,
    proprietaire INTEGER REFERENCES Ferme(idFerme),
    type INTEGER REFERENCES Produit(idProduit),
    quantite INTEGER NOT NULL
    -- UNIQUE(proprietaire, type) ?
);

-- Gestion du classement
CREATE TABLE Classement (
    idFerme INTEGER PRIMARY KEY REFERENCES Ferme(idFerme),
    score DECIMAL(10,2)
);