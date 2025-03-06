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
    nomFerme = ['Marguerite et Pissenlit', 'Tégrité']
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
    nomProduit = ['oeuf', 'lait', 'Botte de Paille', 'Seau d\'eau']
    decrProduit = ['ceci est un oeuf', 'lait de vache d une qualité supérieur', 'De quoi nourir la vache', 'de l\'eau']
    idp = []
             
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Produit (nom, description, estVendable) VALUES (?, ?, 1) RETURNING idProduit", (nomProduit[0], decrProduit[0]))
    idp.append(cur.fetchone()[0])
    cur.execute("INSERT INTO Produit (nom, description, estVendable) VALUES (?, ?, 1) RETURNING idProduit", (nomProduit[1], decrProduit[1]))
    idp.append(cur.fetchone()[0])
    cur.execute("INSERT INTO Produit (nom, description, estVendable) VALUES (?, ?, 1) RETURNING idProduit", (nomProduit[2], decrProduit[2]))
    idp.append(cur.fetchone()[0])
    cur.execute("INSERT INTO Produit (nom, description, estVendable) VALUES (?, ?, 1) RETURNING idProduit", (nomProduit[3], decrProduit[3]))
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

@pytest.fixture
def setup_Coop(db_conn, setup_Produit):
    """Données d'exemple pour la table Commerce avec les produits de la coop"""
    idp = []
             
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Commerce (idVendeur, produit, quantite, prixUnitaire, enVenteDepuis) VALUES (-1, ?, 40, 20, ?) RETURNING idTransac", (setup_Produit[2], rn))
    idp.append(cur.fetchone()[0])
    cur.execute("INSERT INTO Commerce (idVendeur, produit, quantite, prixUnitaire, enVenteDepuis) VALUES (-1, ?, 5, 10, ?) RETURNING idTransac", (setup_Produit[3], rn))
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

def test_rajout_Coop(db_conn, setup_Coop, setup_Produit):
    cur = db_conn.cursor()
    cur.execute("SELECT produit, quantite, prixUnitaire FROM Commerce WHERE idVendeur = -1;")
    resultA = cur.fetchall()
    print(resultA)
    print("ok")
    cur.close()
    assert resultA[0] == (setup_Produit[2], 40, 20) and resultA[1] == (setup_Produit[3], 5, 10)

def test_achat_Coop(db_conn, setup_Coop, setup_ferme, setup_Produit):
    cur = db_conn.cursor()
    cur.execute("SELECT idTransac, produit, quantite, prixUnitaire FROM Commerce WHERE idVendeur = -1;")
    resultA = cur.fetchone()
    resultC = resultA
    print(resultA)
    quAchat = 40
    cur.execute("INSERT INTO Commerce (idAcheteur, idVendeur, produit, quantite, prixUnitaire, enVenteDepuis) VALUES (?, -1, ?, ?, 20, ?) RETURNING idTransac;", (setup_ferme[0], resultA[1], quAchat, rn))
    nTrans = cur.fetchone()
    print(nTrans)
    if quAchat < resultA[3] :
        cur.execute("UPDATE Commerce SET quantite = ? WHERE idTransac = ?;", (resultA[2]-quAchat, resultA[0]))
        cur.execute("SELECT produit, quantite, prixUnitaire FROM Commerce WHERE idTransac = ?;", (resultA[0],))
    else :
        cur.execute("DELETE FROM Commerce WHERE idTransac = ?;", (resultA[0],))
        cur.execute("SELECT produit, quantite, prixUnitaire FROM Commerce WHERE idTransac = ?;", (resultA[0],))
    resultB = cur.fetchone()
    cur.execute("SELECT produit, quantite, prixUnitaire FROM Commerce WHERE idTransac = ?;", (nTrans[0],))
    resultC = cur.fetchone()
    print(resultC)
    print(setup_Produit[2])
    cur.close()

    if quAchat < resultA[3] :
        assert resultB == (setup_Produit[2], resultA[2]-quAchat, resultA[3]) and resultC == (setup_Produit[2], quAchat, resultA[3])
    else :
        assert resultB == None and resultC == (setup_Produit[2], quAchat, resultA[3])


def test_update_Coop(db_conn, setup_Coop, setup_ferme, setup_Produit) :
    cur = db_conn.cursor()
    cur.execute("SELECT idTransac, produit, quantite, prixUnitaire FROM Commerce WHERE idVendeur = -1;")
    resultA = cur.fetchone()
    resultD = cur.fetchone()
    print(resultA)
    print(resultD)
    resultC = resultA
    quAchatA = 40
    quAchatB = 2
    cur.execute("INSERT INTO Commerce (idAcheteur, idVendeur, produit, quantite, prixUnitaire, enVenteDepuis) VALUES (?, -1, ?, ?, 20, ?) RETURNING idTransac;", (setup_ferme[0], resultA[1], quAchatA, rn))
    nTransA = cur.fetchone()
    cur.execute("INSERT INTO Commerce (idAcheteur, idVendeur, produit, quantite, prixUnitaire, enVenteDepuis) VALUES (?, -1, ?, ?, 10, ?) RETURNING idTransac;", (setup_ferme[0], resultD[1], quAchatB, rn))
    nTransB = cur.fetchone()
    if quAchatA < resultA[2] :
        cur.execute("UPDATE Commerce SET quantite = ? WHERE idTransac = ?;", (resultA[2]-quAchatA, resultA[0]))
        cur.execute("SELECT produit, quantite, prixUnitaire FROM Commerce WHERE idTransac = ?;", (resultA[0],))
    else :
        cur.execute("DELETE FROM Commerce WHERE idTransac = ?;", (resultA[0],))
        cur.execute("SELECT produit, quantite, prixUnitaire FROM Commerce WHERE idTransac = ?;", (resultA[0],))
    resultB = cur.fetchone()


    if quAchatB < resultD[2] :
        cur.execute("UPDATE Commerce SET quantite = ? WHERE idTransac = ?;", (resultD[2]-quAchatB, resultD[0]))
        cur.execute("SELECT produit, quantite, prixUnitaire FROM Commerce WHERE idTransac = ?;", (resultD[0],))
        print("yup")
    else :
        cur.execute("DELETE FROM Commerce WHERE idTransac = ?;", (resultD[0],))
        cur.execute("SELECT produit, quantite, prixUnitaire FROM Commerce WHERE idTransac = ?;", (resultD[0],))
    resultE = cur.fetchone()


    #------------Partie update journalière-----------
    e1 = None
    e2 = None

    if resultB == None :
        cur.execute("INSERT INTO Commerce (idVendeur, produit, quantite, prixUnitaire, enVenteDepuis) VALUES (-1, ?, ?, 20, ?) RETURNING idTransac;", (resultA[1], len(setup_ferme)*20, rn))
        #e1 = cur.fetchone()
        #print('a')
    else :
        cur.execute("UPDATE Commerce SET quantite = ? WHERE idTransac = ?;", (len(setup_ferme)*20, resultA[0]))
        #e1 = cur.fetchone()
        #print('b')
    if resultE == None :
        cur.execute("INSERT INTO Commerce (idVendeur, produit, quantite, prixUnitaire, enVenteDepuis) VALUES (-1, ?, ?, 10, ?) RETURNING idTransac;", (resultD[1], len(setup_ferme)*20, rn))
        #e2 = cur.fetchone()
        #print('c')
    else :
        cur.execute("UPDATE Commerce SET quantite = 40 WHERE idTransac = ?;", (resultD[0],))
        #e2 = cur.fetchone()
        #print('d')
    

    cur.execute("SELECT produit, quantite, prixUnitaire FROM Commerce WHERE idVendeur = -1 AND idAcheteur IS NULL;")
    e2 = cur.fetchone()
    e1 = cur.fetchone()
    #dans cette ordre car e2 garde la même id mais e1 change
    cur.close()
    
    assert e1 == (resultA[1], len(setup_ferme)*20, 20) and e2 == (resultD[1], len(setup_ferme)*20, 10)


