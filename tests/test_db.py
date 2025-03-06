import sqlite3
import pytest
from datetime import date, datetime, timedelta

rn = datetime.today()

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
    # Exemple pour insérer plusieurs données
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
    # Exemple pour insérer une unique donnée
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
    # Exemple pour insérer une unique donnée
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
    # Exemple pour insérer une unique donnée
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
    # Exemple pour insérer plusieurs données
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
    
"""
ajout_change ajout de nouvelles données (produit)
"""  
@pytest.fixture
def setup_Produit(db_conn,setup_db):
    """Donnéee d'exemple pour la table Produit"""
    nomProduit = ['oeuf', 'lait','graines','savon']
    decrProduit = ['ceci est un oeuf', 'lait de vache d une qualité supérieur','miam les graines','ça mousse']
    idp = []
             
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Produit (nom, description, estVendable) VALUES (?, ?, 1) RETURNING idProduit", (nomProduit[0], decrProduit[0]))
    idp.append(cur.fetchone()[0])
    cur.execute("INSERT INTO Produit (nom, description, estVendable) VALUES (?, ?, 1) RETURNING idProduit", (nomProduit[1], decrProduit[1]))
    idp.append(cur.fetchone()[0])
    db_conn.commit()
    cur.execute("INSERT INTO Produit (nom, description, estVendable) VALUES (?, ?, 1) RETURNING idProduit", (nomProduit[2], decrProduit[2]))
    idp.append(cur.fetchone()[0])
    cur.execute("INSERT INTO Produit (nom, description, estVendable) VALUES (?, ?, 1) RETURNING idProduit", (nomProduit[3], decrProduit[3]))
    idp.append(cur.fetchone()[0])
    cur.close()
    return idp
    
"""
ajout_change ajout de nouvelles données (nouvelles transactions)
"""    
@pytest.fixture
def setup_Commerce(db_conn,setup_ferme,setup_Produit):
    idp = []
             
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Commerce (idAcheteur, idVendeur, produit, quantite, prixUnitaire, enVenteDepuis) VALUES (?, ?, ?, 1, 500, ?) RETURNING idTransac", (setup_ferme[0], setup_ferme[1], setup_Produit[0], rn))
    idp.append(cur.fetchone()[0])
    cur.execute("INSERT INTO Commerce (idAcheteur, idVendeur, produit, quantite, prixUnitaire, enVenteDepuis) VALUES (?, ?, ?, 1, 1900, ?) RETURNING idTransac", (setup_ferme[0], setup_ferme[1], setup_Produit[1], rn))
    idp.append(cur.fetchone()[0])
    cur.execute("INSERT INTO Commerce (idAcheteur, idVendeur, produit, quantite, prixUnitaire, enVenteDepuis) VALUES (?, ?, ?, 2, 5000, ?) RETURNING idTransac", (setup_ferme[0], setup_ferme[1], setup_Produit[0], rn))
    idp.append(cur.fetchone()[0])
    cur.execute("INSERT INTO Commerce (idAcheteur, idVendeur, produit, quantite, prixUnitaire, enVenteDepuis) VALUES (?, ?, ?, 1, 700, ?) RETURNING idTransac", (setup_ferme[0], setup_ferme[1], setup_Produit[3], rn))
    idp.append(cur.fetchone()[0])
    cur.execute("INSERT INTO Commerce (idAcheteur, idVendeur, produit, quantite, prixUnitaire, enVenteDepuis) VALUES (?, ?, ?, 1, 5000, ?) RETURNING idTransac", (setup_ferme[0], setup_ferme[1], setup_Produit[2], rn))
    idp.append(cur.fetchone()[0])
    cur.execute("INSERT INTO Commerce (idAcheteur, idVendeur, produit, quantite, prixUnitaire, enVenteDepuis) VALUES (?, ?, ?, 15, 200, ?) RETURNING idTransac", (setup_ferme[0], setup_ferme[1], setup_Produit[2], rn))
    idp.append(cur.fetchone()[0])
    db_conn.commit()
    cur.close()
    return idp
    
    
def test_creation_ferme(db_conn, setup_db):
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Ferme (nom) VALUES ('Test')")
    ferme_id = cur.lastrowid

    cur.execute("SELECT nom, ecus, enHibernation, achatRestant, dernierAchat FROM Ferme WHERE idFerme = ?;", (ferme_id,))
    result = cur.fetchone()

    cur.close()
    assert result == ("Test", 1500, None, 12, None)

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
    
def test_creation_ferme(db_conn, setup_compte, setup_ferme):
    cur = db_conn.cursor()
    cur.execute("SELECT idFerme, pseudo, derniereConnexion FROM Compte WHERE idCompte = ?;", (setup_compte[0],))
    resultA = cur.fetchone()
    
    cur.execute("SELECT idFerme, pseudo, derniereConnexion FROM Compte WHERE idCompte = ?;", (setup_compte[1],))
    resultB = cur.fetchone()
    
    cur.close()
    assert resultA == (setup_ferme[0], "Mageline", rn.strftime('%Y-%m-%d %H:%M:%S.%f') ) and resultB == (setup_ferme[1], "Henry", rn.strftime('%Y-%m-%d %H:%M:%S.%f'))
    





def test_creation_Produit(db_conn, setup_Produit):
    cur = db_conn.cursor()
    cur.execute("SELECT idProduit, nom, description, estVendable FROM Produit WHERE idProduit = ?;", (setup_Produit[0],))
    resultA = cur.fetchone()
    
    cur.execute("SELECT idProduit, nom, description, estVendable FROM Produit WHERE idProduit = ?;", (setup_Produit[1],))
    resultB = cur.fetchone()


    cur.close()
    assert resultA == (setup_Produit[0], "oeuf", "ceci est un oeuf", 1 ) and resultB != (setup_Produit[1], "lait", "ceci est un oeuf", 1)

    


def test_creation_Commerce(db_conn, setup_Commerce, setup_ferme, setup_Produit):
    cur = db_conn.cursor()
    cur.execute("SELECT idAcheteur, idVendeur, produit, quantite, prixUnitaire FROM Commerce WHERE idTransac = ?;", (setup_Commerce[0],))
    resultA = cur.fetchone()
    
    cur.execute("SELECT idAcheteur, idVendeur, produit, quantite, prixUnitaire FROM Commerce WHERE idTransac = ?;", (setup_Commerce[1],))
    resultB = cur.fetchone()

    """ 
    premier test le 2 est changer en 1 de part les changement de la base
    """
    cur.close()
    assert resultA == (setup_ferme[0], setup_ferme[1], setup_Produit[0], 1, 500) and resultB == (setup_ferme[0], setup_ferme[1], setup_Produit[1], 1, 1900 )


"""
ajout_change
"""
"""tests transactions"""

"""fonction qui permet d'avoir la moyenne du prix du produit 'prod' vendu à la coopérative"""
def calcule_avg_prix(db_conn,setup_Commerce,prod):
    cur = db_conn.cursor()
    cur.execute("SELECT nom FROM Produit WHERE idProduit = ?;", (prod,))
    nom_article = cur.fetchone()[0]
    cur.execute("SELECT prixUnitaire,quantite FROM Commerce JOIN Produit ON idProduit=produit WHERE nom = ?;", (nom_article,))
    avg_tab = cur.fetchall()
    avg = 0
    nb=0
    for i in range(len(avg_tab)):
        avg += avg_tab[i][0]*avg_tab[i][1]
        nb += avg_tab[i][1]
    return avg /nb

"""
ajout_change 
"""
"""fonction permettant de tester si l'utilisateur peut acheter un produit à la coopérative.
 On a un cas où il ne peut pas acheter car le produit seul coûte trop cher, un où il peut acheter car le prix du produit passe, 
 un où il peut acheter car la moyenne des prix passe, et un où la moyenne des prix du produit est trop cher """
def test_possibiliter_achat(db_conn, setup_ferme, setup_Produit,setup_Commerce):
    cur= db_conn.cursor()
    avg_ventes_non_suffisant = calcule_avg_prix(db_conn,setup_Commerce,setup_Produit[1])
    cur.execute("SELECT ecus FROM Ferme WHERE idFerme = ?;", (setup_ferme[1],))
    argent_acheteur_non_suffisant = cur.fetchone()[0]

    avg_ventes_non_suffisant_moyenne = calcule_avg_prix(db_conn,setup_Commerce,setup_Produit[0])
    cur.execute("SELECT ecus FROM Ferme WHERE idFerme = ?;", (setup_ferme[0],))
    argent_acheteur_non_suffisant_moyenne = cur.fetchone()[0]


    avg_ventes_suffisant_moyenne = calcule_avg_prix(db_conn,setup_Commerce,setup_Produit[2])
    cur.execute("SELECT ecus FROM Ferme WHERE idFerme = ?;", (setup_ferme[0],))
    argent_acheteur_suffisant_moyenne = cur.fetchone()[0]

    avg_ventes_suffisant = calcule_avg_prix(db_conn,setup_Commerce,setup_Produit[3])
    cur.execute("SELECT ecus FROM Ferme WHERE idFerme = ?;", (setup_ferme[0],))
    argent_acheteur_suffisant = cur.fetchone()[0]

    cur.close()
    assert avg_ventes_non_suffisant >= argent_acheteur_non_suffisant and avg_ventes_non_suffisant_moyenne >= argent_acheteur_non_suffisant_moyenne and avg_ventes_suffisant_moyenne <= argent_acheteur_suffisant_moyenne and avg_ventes_suffisant <= argent_acheteur_suffisant