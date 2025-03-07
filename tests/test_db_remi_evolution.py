import sqlite3
import pytest
from datetime import date, datetime, timedelta

rn = datetime.today()

# Définition des fixtures

@pytest.fixture
def db_conn():
    """Créer une BDD SQLite dans la mémoire"""
    conn = sqlite3.connect(":memory:")
    yield conn
    conn.close()

@pytest.fixture
def setup_db(db_conn):
    """Créer les différentes tables pour chaque test"""
    cur = db_conn.cursor()
    cur.execute("""
        CREATE TABLE Ferme (
            idFerme INTEGER PRIMARY KEY AUTOINCREMENT,
            nom VARCHAR(40) UNIQUE CHECK (LENGTH(nom) >= 3) NOT NULL,
            ecus DECIMAL(10,2) DEFAULT 1500 CHECK (ecus >= 0) NOT NULL,
            enHibernation DATE,
            achatRestant SMALLINT DEFAULT 12 CHECK (achatRestant >= 0) NOT NULL,
            dernierAchat DATE
        );
    """)
    cur.execute("""
        CREATE TABLE Compte (
            idCompte INTEGER PRIMARY KEY AUTOINCREMENT,
            idFerme INTEGER UNIQUE REFERENCES Ferme(idFerme),
            pseudo VARCHAR(40) UNIQUE CHECK (LENGTH(pseudo) >= 3) NOT NULL,
            derniereConnexion TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE Poule (
            idPoule INTEGER PRIMARY KEY AUTOINCREMENT,
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
    """)
    cur.execute("""
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
    """)
    cur.execute("""
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
    """)

    cur.execute("""
        CREATE TABLE Produit (
            idProduit INTEGER PRIMARY KEY AUTOINCREMENT,
            nom VARCHAR(40) UNIQUE CHECK (LENGTH(nom) >= 2) NOT NULL,
            description VARCHAR(180),
            estVendable BOOLEAN NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE Commerce (
            idTransac INTEGER PRIMARY KEY AUTOINCREMENT,
            idAcheteur INTEGER REFERENCES Ferme(idFerme),
            idVendeur INTEGER REFERENCES Ferme(idFerme),
            produit INTEGER REFERENCES Produit(idProduit),
            quantite INTEGER CHECK (quantite >= 1) NOT NULL,
            prixUnitaire DECIMAL(10,2) CHECK (prixUnitaire > 0) NOT NULL,
            enVenteDepuis TIMESTAMP
        );
    """)
    cur.execute("""
        CREATE TABLE Remise (
            idProduit INTEGER PRIMARY KEY AUTOINCREMENT,
            proprietaire INTEGER REFERENCES Ferme(idFerme),
            type INTEGER REFERENCES Produit(idProduit),
            quantite INTEGER NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE Classement (
            idFerme INTEGER PRIMARY KEY REFERENCES Ferme(idFerme),
            score DECIMAL(10,2)
        );
    """)
    db_conn.commit()
    cur.close()

@pytest.fixture
def setup_ferme(db_conn, setup_db):
    """Donnéee d'exemple pour la table Ferme"""
    nomFerme = ['Marguerite et Pissenlit', 'Tégrité', 'Ferme3' ,'Ferme4']
    ids = []

    cur = db_conn.cursor()
    for nom in nomFerme:
        cur.execute("INSERT INTO Ferme (nom) VALUES (?) RETURNING idFerme", (nom,))
        ids.append(cur.fetchone()[0])

    db_conn.commit()
    cur.close()
    return ids

@pytest.fixture
def setup_poule(db_conn, setup_ferme):
    """Donnée d'exemple pour la table Poule"""
    pouleId = []
    cur = db_conn.cursor()
    cur.execute("""
                INSERT INTO Poule (proprietaire, poids, age, sexe, nb_oeuf, dernier_repas, dernier_breuvage, dernier_lavage)
                VALUES (?, 2.5, 5, 'F', 1, ?, ?, ?) RETURNING idPoule
            """, (setup_ferme[0], date.today(), date.today() - timedelta(days=1), date.today()))
    pouleId.append(cur.fetchone()[0])
    cur.execute("""
                INSERT INTO Poule (proprietaire, poids, age, sexe, nb_oeuf, dernier_repas, dernier_breuvage, dernier_lavage)
                VALUES (?, 3, 7, 'M', 1, ?, ?, ?) RETURNING idPoule
            """, (setup_ferme[0], date.today() - timedelta(days=1), date.today(), date.today() - timedelta(days=1)))
    pouleId.append(cur.fetchone()[0])
    cur.execute("""
                INSERT INTO Poule (proprietaire, poids, age, sexe, nb_oeuf, dernier_repas, dernier_breuvage, dernier_lavage)
                VALUES (?, 3, 2, 'U', 1, ?, ?, ?) RETURNING idPoule
            """, (setup_ferme[1], date.today() - timedelta(days=1), date.today(), date.today() - timedelta(days=1)))
    pouleId.append(cur.fetchone()[0])
    cur.execute("""
                INSERT INTO Poule (proprietaire, poids, age, sexe, nb_oeuf, dernier_repas, dernier_breuvage, dernier_lavage)
                VALUES (?, 3, 1, 'U', 1, ?, ?, ?) RETURNING idPoule
            """, (setup_ferme[0], date.today(), date.today(), date.today()))
    pouleId.append(cur.fetchone()[0])
    db_conn.commit()
    cur.close()
    return pouleId

@pytest.fixture
def setup_vache(db_conn, setup_ferme):
    """Donnée d'exemple pour la table Vache"""
    idOwner = []
    cur = db_conn.cursor()
    cur.execute("""
                INSERT INTO Vache (proprietaire, poids, age, qt_lait, dernier_repas, dernier_breuvage, dernier_lavage)
                VALUES (?, 1, 1, 0, ?, ?, ?) RETURNING proprietaire
            """, (setup_ferme[0], date.today(), date.today(), date.today()))
    idOwner.append(cur.fetchone()[0])
    cur.execute("""
                INSERT INTO Vache (proprietaire, poids, age, qt_lait, dernier_repas, dernier_breuvage, dernier_lavage)
                VALUES (?, 100, 19, 8, ?, ?, ?) RETURNING proprietaire
            """, (setup_ferme[1], date.today(), date.today(), date.today()))
    idOwner.append(cur.fetchone()[0])
    db_conn.commit()
    cur.close()
    return idOwner

@pytest.fixture
def setup_clapier(db_conn, setup_ferme):
    """Donnée d'exemple pour la table Clapier"""
    idOwner = []
    cur = db_conn.cursor()
    cur.execute("""
                INSERT INTO Clapier (proprietaire, dernier_repas, dernier_breuvage, dernier_lavage, nb_bebe, nb_petit, nb_gros, nb_adulte_m, nb_adulte_f)
                VALUES (?, ?, ?, ?, 20, 14, 6, 5, 25) RETURNING proprietaire
            """, (setup_ferme[0], date.today(), date.today() - timedelta(days=1),  date.today()))
    idOwner.append(cur.fetchone()[0])
    cur.execute("""
                INSERT INTO Clapier (proprietaire, dernier_repas, dernier_breuvage, dernier_lavage, nb_bebe, nb_petit, nb_gros, nb_adulte_m, nb_adulte_f)
                VALUES (?, ?, ?, ?, 20, 20, 0, 0, 10) RETURNING proprietaire
            """, (setup_ferme[1], date.today(), date.today() - timedelta(days=1),  date.today()))
    idOwner.append(cur.fetchone()[0])

    cur.execute("""
                INSERT INTO Clapier (proprietaire, dernier_repas, dernier_breuvage, dernier_lavage, nb_bebe, nb_petit, nb_gros, nb_adulte_m, nb_adulte_f)
                VALUES (?, ?, ?, ?, 1, 1, 1, 1, 1) RETURNING proprietaire
            """, (setup_ferme[2], date.today(), date.today(), date.today()))

    cur.execute("""
                INSERT INTO Clapier (proprietaire, dernier_repas, dernier_breuvage, dernier_lavage, nb_bebe, nb_petit, nb_gros, nb_adulte_m, nb_adulte_f)
                VALUES (?, ?, ?, ?, 1, 1, 1, 1, 1) RETURNING proprietaire
            """, (setup_ferme[3], date.today()-timedelta(days=1), date.today()-timedelta(days=1), date.today()))
    idOwner.append(cur.fetchone()[0])

    db_conn.commit()
    cur.close()
    return idOwner

@pytest.fixture
def setup_compte(db_conn, setup_ferme):
    """Donnéee d'exemple pour la table Compte"""
    nomCompte = ['Mageline', 'Henry']
    ids = []

    cur = db_conn.cursor()
    cur.execute("INSERT INTO Compte (idFerme, pseudo, derniereConnexion) VALUES (?, ?, ?) RETURNING idCompte", (setup_ferme[0], nomCompte[0], rn))
    ids.append(cur.fetchone()[0])
    cur.execute("INSERT INTO Compte (idFerme, pseudo, derniereConnexion) VALUES (?, ?, ?) RETURNING idCompte", (setup_ferme[1], nomCompte[1], rn))
    ids.append(cur.fetchone()[0])
    db_conn.commit()
    cur.close()
    return ids

@pytest.fixture
def setup_Produit(db_conn, setup_db):
    """Données d'exemple pour la table Produit"""
    nomProduit = ['oeuf', 'lait']
    decrProduit = ['ceci est un oeuf', 'lait de vache d une qualité supérieur']
    idp = []

    cur = db_conn.cursor()
    cur.execute("INSERT INTO Produit (nom, description, estVendable) VALUES (?, ?, 1) RETURNING idProduit", (nomProduit[0], decrProduit[0]))
    idp.append(cur.fetchone()[0])
    cur.execute("INSERT INTO Produit (nom, description, estVendable) VALUES (?, ?, 1) RETURNING idProduit", (nomProduit[1], decrProduit[1]))
    idp.append(cur.fetchone()[0])
    db_conn.commit()
    cur.close()
    return idp

@pytest.fixture
def setup_Commerce(db_conn,setup_ferme,setup_Produit):
    """Données d'exemple pour la table Commerce"""
    idp = []

    cur = db_conn.cursor()
    cur.execute("INSERT INTO Commerce (idAcheteur, idVendeur, produit, quantite, prixUnitaire, enVenteDepuis) VALUES (?, ?, ?, 2, 500, ?) RETURNING idTransac", (setup_ferme[0], setup_ferme[1], setup_Produit[0], rn))
    idp.append(cur.fetchone()[0])
    cur.execute("INSERT INTO Commerce (idAcheteur, idVendeur, produit, quantite, prixUnitaire, enVenteDepuis) VALUES (?, ?, ?, 1, 1900, ?) RETURNING idTransac", (setup_ferme[0], setup_ferme[1], setup_Produit[1], rn))
    idp.append(cur.fetchone()[0])
    db_conn.commit()
    cur.close()
    return idp

# Début des tests

# Teste vérifiant que les données sont bien insérés
def test_rajout_ferme(db_conn, setup_compte, setup_ferme):
    cur = db_conn.cursor()
    cur.execute("SELECT idFerme, pseudo, derniereConnexion FROM Compte WHERE idCompte = ?;", (setup_compte[0],))
    resultA = cur.fetchone()

    cur.execute("SELECT idFerme, pseudo, derniereConnexion FROM Compte WHERE idCompte = ?;", (setup_compte[1],))
    resultB = cur.fetchone()

    cur.close()
    assert resultA == (setup_ferme[0], "Mageline", rn.strftime('%Y-%m-%d %H:%M:%S.%f') ) and resultB == (setup_ferme[1], "Henry", rn.strftime('%Y-%m-%d %H:%M:%S.%f'))

def test_rajout_vache(db_conn, setup_vache):

    cur = db_conn.cursor()
    cur.execute("SELECT poids, age, qt_lait, dernier_repas, dernier_breuvage, dernier_lavage FROM Vache WHERE proprietaire = ?;", (setup_vache[0],))
    resultA = cur.fetchone()

    cur.execute("SELECT poids, age, qt_lait, dernier_repas, dernier_breuvage, dernier_lavage FROM Vache WHERE proprietaire = ?;", (setup_vache[1],))
    resultB = cur.fetchone()

    cur.close()
    assert resultA == (1, 1, 0, date.today().strftime('%Y-%m-%d'), date.today().strftime('%Y-%m-%d'), date.today().strftime('%Y-%m-%d')) and resultB == (100, 19, 8, date.today().strftime('%Y-%m-%d'), date.today().strftime('%Y-%m-%d'), date.today().strftime('%Y-%m-%d'))

def test_rajout_clapier(db_conn, setup_clapier):

    cur = db_conn.cursor()

    cur.execute("SELECT dernier_repas, dernier_breuvage, dernier_lavage, nb_bebe, nb_petit, nb_gros, nb_adulte_m, nb_adulte_f FROM Clapier WHERE proprietaire = ?;", (setup_clapier[0],))
    resultA = cur.fetchone()

    cur.execute("SELECT dernier_repas, dernier_breuvage, dernier_lavage, nb_bebe, nb_petit, nb_gros, nb_adulte_m, nb_adulte_f FROM Clapier WHERE proprietaire = ?;", (setup_clapier[1],))
    resultB = cur.fetchone()

    cur.close()
    assert resultA == (date.today().strftime('%Y-%m-%d'), (date.today() - timedelta(days=1)).strftime('%Y-%m-%d'), date.today().strftime('%Y-%m-%d'), 20, 14, 6, 5, 25) and resultB == (date.today().strftime('%Y-%m-%d'), (date.today() - timedelta(days=1)).strftime('%Y-%m-%d'), date.today().strftime('%Y-%m-%d'), 20, 20, 0, 0, 10)

def test_rajout_poule(db_conn, setup_poule):

    cur = db_conn.cursor()
    cur.execute("SELECT poids, age, sexe, nb_oeuf, dernier_repas, dernier_breuvage, dernier_lavage FROM Poule WHERE proprietaire = ?;", (setup_poule[0],))
    resultA = cur.fetchone()

    cur.execute("SELECT poids, age, sexe, nb_oeuf, dernier_repas, dernier_breuvage, dernier_lavage FROM Poule WHERE proprietaire = ?;", (setup_poule[0],))
    resultB = cur.lastrowid

    cur.execute("SELECT poids, age, sexe, nb_oeuf, dernier_repas, dernier_breuvage, dernier_lavage FROM Poule WHERE proprietaire = ?;", (setup_poule[1],))
    resultC = cur.fetchone()

    cur.execute("SELECT poids, age, sexe, nb_oeuf, dernier_repas, dernier_breuvage, dernier_lavage FROM Poule WHERE proprietaire = ?;", (setup_poule[1],))
    resultD = cur.lastrowid

    cur.close()

    assert resultA == (2.5, 5, 'F', 1, date.today().strftime('%Y-%m-%d'), (date.today() - timedelta(days=1)).strftime('%Y-%m-%d'), date.today().strftime('%Y-%m-%d'))# and resultB == (3, 7, 'M', 1, (date.today() - timedelta(days=1)).strftime('%Y-%m-%d'), date.today().strftime('%Y-%m-%d'), (date.today() - timedelta(days=1)).strftime('%Y-%m-%d'))

def test_rajout_Produit(db_conn, setup_Produit):
    cur = db_conn.cursor()
    cur.execute("SELECT idProduit, nom, description, estVendable FROM Produit WHERE idProduit = ?;", (setup_Produit[0],))
    resultA = cur.fetchone()

    cur.execute("SELECT idProduit, nom, description, estVendable FROM Produit WHERE idProduit = ?;", (setup_Produit[1],))
    resultB = cur.fetchone()

    cur.close()
    assert resultA == (setup_Produit[0], "oeuf", "ceci est un oeuf", 1 ) and resultB != (setup_Produit[1], "lait", "ceci est un oeuf", 1)

def test_rajout_Commerce(db_conn, setup_Commerce, setup_ferme, setup_Produit):
    cur = db_conn.cursor()
    cur.execute("SELECT idAcheteur, idVendeur, produit, quantite, prixUnitaire FROM Commerce WHERE idTransac = ?;", (setup_Commerce[0],))
    resultA = cur.fetchone()

    cur.execute("SELECT idAcheteur, idVendeur, produit, quantite, prixUnitaire FROM Commerce WHERE idTransac = ?;", (setup_Commerce[1],))
    resultB = cur.fetchone()

    cur.close()
    assert resultA == (setup_ferme[0], setup_ferme[1], setup_Produit[0], 2, 500) and resultB == (setup_ferme[0], setup_ferme[1], setup_Produit[1], 1, 1900 )

# Futur test à venir...

def test_evolution_bebe_lapin(db_conn, setup_clapier, setup_ferme):
    # === Simuler le passage d'une nuit ===
    date_today = date.today()+timedelta(days=1)
    # Vieillissement des bébés lapins en petits lapins
    cur = db_conn.cursor()
    """Un bébé lapin nourri et abreuvé devient un petit lapin"""
    cur.execute("""
        UPDATE Clapier SET nb_bebe = nb_bebe - 1, nb_petit = nb_petit + 1 
        WHERE dernier_repas = ? AND dernier_breuvage = ? AND proprietaire = ?;""", 
        (date.today(), date.today(), setup_ferme[2]))

    """Un bébé lapin affamé ne devient pas un petit lapin"""
    cur.execute("""
        UPDATE Clapier SET nb_bebe = nb_bebe - 1, nb_petit = nb_petit + 1 
        WHERE dernier_repas = ? AND dernier_breuvage = ? AND proprietaire = ?;""", 
        (date.today(), date.today(), setup_ferme[3]))


    # Vérification des résultats après la nuit
    cur.execute("SELECT nb_bebe FROM Clapier WHERE proprietaire = ?;", (setup_ferme[2],))
    nb_bebe_lapin_ferme3 = cur.fetchone()[0]

    cur.execute("SELECT nb_petit FROM Clapier WHERE proprietaire = ?;", (setup_ferme[2],))
    nb_petit_lapin_ferme3 = cur.fetchone()[0]

    cur.execute("SELECT nb_bebe FROM Clapier WHERE proprietaire = ?;", (setup_ferme[3],))
    nb_bebe_lapin_ferme4 = cur.fetchone()[0]

    cur.execute("SELECT nb_petit FROM Clapier WHERE proprietaire = ?;", (setup_ferme[3],))
    nb_petit_lapin_ferme4 = cur.fetchone()[0]

    cur.close()

    # Vérifications
    assert nb_bebe_lapin_ferme3 == 0 # le nombre de bébés à diminuer
    assert nb_petit_lapin_ferme3 == 2 # le nombre de petits à augmenter

    assert nb_bebe_lapin_ferme4 == 1 # le nombre de bébés reste inchangé
    assert nb_petit_lapin_ferme4 == 1 # le nombre de petits reste inchangé

def test_evolution_petit_lapin(db_conn, setup_clapier, setup_ferme):
    # === Simuler le passage d'une nuit ===
    # Vieillissement des petits lapins en gros lapins
    cur = db_conn.cursor()

    """Un petit lapin nourri et abreuvé devient un gros lapin"""
    cur.execute("""
        UPDATE Clapier SET nb_petit = nb_petit - 1, nb_gros = nb_gros + 1 
        WHERE dernier_repas = ? AND dernier_breuvage = ? AND proprietaire = ?;""", 
        (date.today(), date.today(), setup_ferme[2]))

    """Un petit lapin affamé ne devient pas un gros lapin"""
    cur.execute("""
        UPDATE Clapier SET nb_petit = nb_petit - 1, nb_gros = nb_gros + 1
        WHERE dernier_repas = ? AND dernier_breuvage = ? AND proprietaire = ?;""",
        (date.today(), date.today(), setup_ferme[3]))


    # Vérification des résultats après la nuit

    cur.execute("SELECT nb_petit FROM Clapier WHERE proprietaire = ?;", (setup_ferme[2],))
    nb_petit_lapin_ferme3 = cur.fetchone()[0]

    cur.execute("SELECT nb_gros FROM Clapier WHERE proprietaire = ?;", (setup_ferme[2],))
    nb_gros_lapin_ferme3 = cur.fetchone()[0]

    cur.execute("SELECT nb_petit FROM Clapier WHERE proprietaire = ?;", (setup_ferme[3],))
    nb_petit_lapin_ferme4 = cur.fetchone()[0]

    cur.execute("SELECT nb_gros FROM Clapier WHERE proprietaire = ?;", (setup_ferme[3],))
    nb_gros_lapin_ferme4 = cur.fetchone()[0]

    cur.close()

    # Vérifications
    assert nb_petit_lapin_ferme3 == 0 # le nombre de petits à diminuer
    assert nb_gros_lapin_ferme3 == 2 # le nombre de gros à augmenter

    assert nb_petit_lapin_ferme4 == 1 # le nombre de petits reste inchangé
    assert nb_gros_lapin_ferme4 == 1 # le nombre de gros reste inchangé

def test_evolution_gros_lapin(db_conn, setup_clapier, setup_ferme):
    # === Simuler le passage d'une nuit ===
    # Vieillissement des gros lapereaux en lapins male ou femelle
    cur = db_conn.cursor()

    """Un gros lapereau nourri et abreuvé devient un lapin femelle"""

    probabilite = 2
    cur.execute("""
        UPDATE Clapier SET nb_gros = nb_gros - 1, 
        nb_adulte_m = CASE WHEN ? < 0.5 THEN  nb_adulte_m +1 ELSE nb_adulte_m END, 
        nb_adulte_f = CASE WHEN ? >= 0.5 THEN  nb_adulte_f +1 ELSE nb_adulte_f END 
        WHERE dernier_repas = ? AND dernier_breuvage = ? AND proprietaire = ?;""", 
        (probabilite,probabilite,date.today(), date.today(), setup_ferme[2],))

    """Un gros lapereau affamé ne devient pas un lapin femelle"""
    cur.execute("""
        UPDATE Clapier SET nb_gros = nb_gros - 1, 
        nb_adulte_m = CASE WHEN ? < 0.5 THEN  nb_adulte_m +1 ELSE nb_adulte_m END, 
        nb_adulte_f = CASE WHEN ? >= 0.5 THEN  nb_adulte_f +1 ELSE nb_adulte_f END 
        WHERE dernier_repas = ? AND dernier_breuvage = ? AND proprietaire = ?;""", 
        (probabilite,probabilite,date.today(), date.today(), setup_ferme[3],))
    
    # Vérification des résultats après la nuit

    cur.execute("SELECT nb_gros FROM Clapier WHERE proprietaire = ?;", (setup_ferme[2],))
    nb_gros_lapin_ferme3 = cur.fetchone()[0]

    cur.execute("SELECT nb_adulte_f FROM Clapier WHERE proprietaire = ?;", (setup_ferme[2],))
    nb_lapin_femelle_ferme3 = cur.fetchone()[0]

    cur.execute("SELECT nb_gros FROM Clapier WHERE proprietaire = ?;", (setup_ferme[3],))
    nb_gros_lapin_ferme4 = cur.fetchone()[0]

    cur.execute("SELECT nb_adulte_f FROM Clapier WHERE proprietaire = ?;", (setup_ferme[3],))
    nb_lapin_femelle_ferme4 = cur.fetchone()[0]

    cur.close()

    # Vérifications
    assert nb_gros_lapin_ferme3 == 0 # le nombre de gros à diminuer
    assert nb_lapin_femelle_ferme3 == 2 # le nombre de femelle à augmenter

    assert nb_gros_lapin_ferme4 == 1 # le nombre de gros reste inchangé
    assert nb_lapin_femelle_ferme4 == 1 # le nombre de femelle reste inchangé

def test_mortalite_lapin(db_conn, setup_clapier, setup_ferme):
    # === Simuler le passage d'une nuit ===
    # Modification des clapiers des 4 fermes pour simuler la mortalité des lapins
    
    cur = db_conn.cursor()
    # Les bébés lapins salent meurent
    cur.execute("""
        UPDATE Clapier SET nb_bebe = 10, dernier_lavage = ?
        WHERE proprietaire = ?;""",
        (date.today()-timedelta(days=1), setup_ferme[0]))

    # Les bébés lapins malades meurent
    cur.execute("""
        UPDATE Clapier SET nb_bebe = 10, malade_depuis = ?
        WHERE proprietaire = ?;""",
        (date.today()-timedelta(days=1), setup_ferme[1]))

    # Les bébés lapins affamés et assoiffés meurent
    cur.execute("""
        UPDATE Clapier SET nb_bebe = 10, dernier_repas = ?, dernier_breuvage = ?
        WHERE proprietaire = ?;""",
        (date.today()-timedelta(days=1), date.today()-timedelta(days=1), setup_ferme[2]))
    
    # Les petits lapins affamés et assoiffés meurent dans le cas où il n'y a pas de bébés lapins dans le clapier
    cur.execute("""
        UPDATE Clapier SET nb_bebe = 0, nb_petit = 10, dernier_repas = ?, dernier_breuvage = ?
        WHERE proprietaire = ?;""",
        (date.today()-timedelta(days=1), date.today()-timedelta(days=1), setup_ferme[3]))     
 # Vérification des valeurs avant la mise à jour
    """cur.execute("SELECT dernier_repas, dernier_breuvage FROM Clapier WHERE proprietaire = ?;", (setup_ferme[2],))
    print("Ferme 2 - Avant mise à jour:", cur.fetchone())

    cur.execute("SELECT dernier_repas, dernier_breuvage FROM Clapier WHERE proprietaire = ?;", (setup_ferme[3],))
    print("Ferme 3 - Avant mise à jour:", cur.fetchone())"""
    
    """La moitié des bébés lapins sales meurent"""
    cur.execute("""
    UPDATE Clapier SET 
        nb_bebe = CASE WHEN nb_bebe > 0 THEN nb_bebe / 2 ELSE nb_bebe END,
        nb_petit = CASE WHEN nb_petit > 0 AND nb_bebe = 0 THEN nb_petit / 2 ELSE nb_petit END,
        nb_gros = CASE WHEN nb_gros > 0 AND nb_petit = 0 AND nb_bebe = 0 THEN nb_gros / 2 ELSE nb_gros END,
        nb_adulte_m = CASE WHEN nb_adulte_m > 0 AND nb_gros = 0 AND nb_petit = 0 AND nb_bebe = 0 THEN nb_adulte_m / 2 ELSE nb_adulte_m END,
        nb_adulte_f = CASE WHEN nb_adulte_f > 0 AND nb_gros = 0 AND nb_petit = 0 AND nb_bebe = 0 THEN nb_adulte_f / 2 ELSE nb_adulte_f END
        WHERE dernier_lavage < ? AND proprietaire = ?;""",
        (date.today(), setup_ferme[0]))
    
    """La moitié des bébés lapins malades meurent"""
    cur.execute("""
    UPDATE Clapier SET 
        nb_bebe = CASE WHEN nb_bebe > 0 THEN nb_bebe / 2 ELSE nb_bebe END,
        nb_petit = CASE WHEN nb_petit > 0 AND nb_bebe = 0 THEN nb_petit / 2 ELSE nb_petit END,
        nb_gros = CASE WHEN nb_gros > 0 AND nb_petit = 0 AND nb_bebe = 0 THEN nb_gros / 2 ELSE nb_gros END,
        nb_adulte_m = CASE WHEN nb_adulte_m > 0 AND nb_gros = 0 AND nb_petit = 0 AND nb_bebe = 0 THEN nb_adulte_m / 2 ELSE nb_adulte_m END,
        nb_adulte_f = CASE WHEN nb_adulte_f > 0 AND nb_gros = 0 AND nb_petit = 0 AND nb_bebe = 0 THEN nb_adulte_f / 2 ELSE nb_adulte_f END
        WHERE malade_depuis < ? AND proprietaire = ?;""",
        (date.today(), setup_ferme[1]))

    """La moitié des bébés lapins affamés et assoiffés meurent dans le cas où il y a des bébés lapins dans le clapier"""
    
    cur.execute("""
    UPDATE Clapier SET 
        nb_bebe = CASE WHEN nb_bebe > 0 THEN nb_bebe / 2 ELSE nb_bebe END,
        nb_petit = CASE WHEN nb_petit > 0 AND nb_bebe = 0 THEN nb_petit / 2 ELSE nb_petit END,
        nb_gros = CASE WHEN nb_gros > 0 AND nb_petit = 0 AND nb_bebe = 0 THEN nb_gros / 2 ELSE nb_gros END,
        nb_adulte_m = CASE WHEN nb_adulte_m > 0 AND nb_gros = 0 AND nb_petit = 0 AND nb_bebe = 0 THEN nb_adulte_m / 2 ELSE nb_adulte_m END,
        nb_adulte_f = CASE WHEN nb_adulte_f > 0 AND nb_gros = 0 AND nb_petit = 0 AND nb_bebe = 0 THEN nb_adulte_f / 2 ELSE nb_adulte_f END
        WHERE dernier_repas < ? AND dernier_breuvage < ? AND proprietaire = ?;""",
        (date.today(), date.today(), setup_ferme[2]))
    
    """La moitié des petits lapins affamés et assoiffés meurent dans le cas où il y a aucun bébé lapin est présent dans le clapier"""
    cur.execute("""
        UPDATE Clapier SET 
        nb_bebe = CASE WHEN nb_bebe > 0 THEN nb_bebe / 2 ELSE nb_bebe END,
        nb_petit = CASE WHEN nb_petit > 0 AND nb_bebe = 0 THEN nb_petit / 2 ELSE nb_petit END,
        nb_gros = CASE WHEN nb_gros > 0 AND nb_petit = 0 AND nb_bebe = 0 THEN nb_gros / 2 ELSE nb_gros END,
        nb_adulte_m = CASE WHEN nb_adulte_m > 0 AND nb_gros = 0 AND nb_petit = 0 AND nb_bebe = 0 THEN nb_adulte_m / 2 ELSE nb_adulte_m END,
        nb_adulte_f = CASE WHEN nb_adulte_f > 0 AND nb_gros = 0 AND nb_petit = 0 AND nb_bebe = 0 THEN nb_adulte_f / 2 ELSE nb_adulte_f END
        WHERE dernier_repas < ? AND dernier_breuvage < ? AND proprietaire = ?;""", 
        (date.today(), date.today(), setup_ferme[3]))
    
    # Vérification des résultats après la nuit
    cur.execute("SELECT nb_bebe FROM Clapier WHERE proprietaire = ?;", (setup_ferme[0],))
    nb_bebe_lapin_ferme0 = cur.fetchone()[0]
    
    cur.execute("SELECT nb_bebe FROM Clapier WHERE proprietaire = ?;", (setup_ferme[1],))
    nb_bebe_lapin_ferme1 = cur.fetchone()[0]

    cur.execute("SELECT nb_bebe FROM Clapier WHERE proprietaire = ?;", (setup_ferme[2],))
    nb_bebe_lapin_ferme2 = cur.fetchone()[0]

    cur.execute("SELECT nb_bebe,nb_petit FROM Clapier WHERE proprietaire = ?;", (setup_ferme[3],))
    nb_petit_lapin_ferme3 = cur.fetchone()
    
    cur.close()

    # Vérifications
    assert nb_bebe_lapin_ferme0 == 5 # la moitié des bébés lapins sont morts
    assert nb_bebe_lapin_ferme1 == 5 # la moitié des bébés lapins sont morts

    assert nb_bebe_lapin_ferme2 == 5 # la moitié des bébés lapins sont morts
    assert nb_petit_lapin_ferme3 == (0,5) # la moitié des petits lapins sont morts car il n'y avait pas de bébés lapins

def test_creation_bebe_lapin(db_conn, setup_clapier, setup_ferme):
    # === Simuler le passage d'une nuit ===
    # Création de nouveaux bébés lapins si il y a au moins un couple de lapins
    # Modification des clapiers des 4 fermes pour simuler la création de nouveaux bébés lapins
    
    cur = db_conn.cursor()
    # Le nombre de bébés lapins est augmenté 
    cur.execute("""
        UPDATE Clapier SET nb_bebe = 10, nb_adulte_f = 3, nb_adulte_m = 4, dernier_repas = ?, dernier_breuvage = ?, dernier_lavage = ?
        WHERE proprietaire = ?;""",
        (date.today(), date.today(), date.today(), setup_ferme[0]))

    # Le  nombre de bébés lapins n'est pas augmenté car il n'y a pas de couple de lapins
    cur.execute("""
        UPDATE Clapier SET nb_bebe = 10, nb_adulte_f = 0, nb_adulte_m = 5, dernier_repas = ?, dernier_breuvage = ?, dernier_lavage = ?
        WHERE proprietaire = ?;""",
        (date.today(), date.today(), date.today(), setup_ferme[1]))
    
    # Le nombre de bébés lapins n'est pas augmenté car les conditions ne sont pas respectées
    cur.execute("""
        UPDATE Clapier SET nb_bebe = 10, nb_adulte_f = 3, nb_adulte_m = 4, dernier_repas = ?, dernier_breuvage = ?, dernier_lavage = ?
        WHERE proprietaire = ?;""",
        (date.today(), date.today(), date.today()-timedelta(days=1), setup_ferme[2]))   
    
    # si il y a au moins un couple de lapins et que toutes les conditions sont respectées : nourris, abreuvé, lavé, en bonne santé, alors des bébés lapins sont créés 
    cur.execute("""
        UPDATE Clapier SET nb_bebe = nb_bebe + MIN(nb_adulte_m, nb_adulte_f) 
        WHERE nb_adulte_f > 0 AND nb_adulte_m > 0 AND dernier_repas = ? AND dernier_breuvage = ? AND dernier_lavage = ? AND proprietaire = ?;""",
        (date.today(), date.today(), date.today(),setup_ferme[0],))
    
    # si il n'y a pas de couple de lapins, alors aucun bébé lapin n'est créé 
    cur.execute("""
        UPDATE Clapier SET nb_bebe = nb_bebe + MIN(nb_adulte_m, nb_adulte_f) 
        WHERE nb_adulte_f > 0 AND nb_adulte_m > 0 AND dernier_repas = ? AND dernier_breuvage = ? AND dernier_lavage = ? AND proprietaire = ?;""",
        (date.today(), date.today(), date.today(),setup_ferme[1],))
    
    # si il y a un couple de lapins mais que toutes les conditions ne sont pas respectées, alors aucun bébé lapin n'est créé
    cur.execute("""
        UPDATE Clapier SET nb_bebe = nb_bebe + MIN(nb_adulte_m, nb_adulte_f) 
        WHERE nb_adulte_f > 0 AND nb_adulte_m > 0 AND dernier_repas = ? AND dernier_breuvage = ? AND dernier_lavage = ? AND proprietaire = ?;""",
        (date.today(), date.today(), date.today(),setup_ferme[2],))

    # Vérification des résultats après la nuit
    cur.execute("SELECT nb_bebe FROM Clapier WHERE proprietaire = ?;", (setup_ferme[0],))
    nb_bebe_lapin_ferme0 = cur.fetchone()[0]
    
    cur.execute("SELECT nb_bebe FROM Clapier WHERE proprietaire = ?;", (setup_ferme[1],))
    nb_bebe_lapin_ferme1 = cur.fetchone()[0]

    cur.execute("SELECT nb_bebe FROM Clapier WHERE proprietaire = ?;", (setup_ferme[2],))
    nb_bebe_lapin_ferme2 = cur.fetchone()[0]

    cur.close()
    # Vérifications
    assert nb_bebe_lapin_ferme0 == 13 # le nombre de bébés lapins est augmenté
    assert nb_bebe_lapin_ferme1 == 10 # le nombre de bébés lapins n'est pas augmenté
    assert nb_bebe_lapin_ferme2 == 10 # la moitié des bébés lapins sont morts
    