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
            poids DECIMAL(5,2) DEFAULT 0.05 CHECK ((poids >= 0) AND (poids <= 3.5)) NOT NULL,
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
            nb_bebe INTEGER DEFAULT 8 CHECK (nb_bebe >= 0 AND nb_bebe + nb_petit + nb_gros <= 50) NOT NULL,
            nb_petit INTEGER DEFAULT 0 CHECK (nb_petit >= 0 AND nb_bebe + nb_petit + nb_gros <= 50) NOT NULL,
            nb_gros INTEGER DEFAULT 0 CHECK (nb_gros >= 0 AND nb_bebe + nb_petit + nb_gros <= 50) NOT NULL,
            nb_adulte_m INTEGER DEFAULT 0 CHECK (nb_adulte_m >= 0 AND nb_adulte_m + nb_adulte_f <= 50) NOT NULL,
            nb_adulte_f INTEGER DEFAULT 0 CHECK (nb_adulte_f >= 0 AND nb_adulte_m + nb_adulte_f <= 50) NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE Vache (
            proprietaire INTEGER PRIMARY KEY REFERENCES Ferme(idFerme),
            poids INTEGER DEFAULT 1 CHECK ((poids >= 0) AND (poids<=750)) NOT NULL,
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
    nomProduit = ['oeuf', 'lait', 'Botte de Paille', 'Seau d\'eau','graines','savon']
    decrProduit = ['ceci est un oeuf', 'lait de vache d une qualité supérieur', 'De quoi nourir la vache', 'de l\'eau','miam les graines','ça mousse']
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



##### Tests concernant les poules (réalisés par Noé et Tony) #####

def test_poule_nourrie_une_fois(db_conn, setup_poule):
    """Teste qu'un animal n'est nourrie qu'une seule fois par jour"""
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Poule (idPoule, dernier_repas) VALUES (?, ?);", (setup_poule[0], date.today()))
    db_conn.commit()

    with pytest.raises(sqlite3.IntegrityError):  # Vérifie qu'on ne peut nourrir plusieurs fois
        cur.execute("INSERT INTO Poule (idPoule, dernier_repas) VALUES (?, ?);", (setup_poule[0], date.today()))
        db_conn.commit()

    cur.close() #on s'attend à ce que le test soit un échec



def test_mortalite_si_non_nourrie(db_conn, setup_poule):
    """Teste qu'un animal meurt après 4 jours sans nourriture"""
    cur = db_conn.cursor()

    for _ in range(4):  # Simule 4 jours sans nourriture
        cur.execute("UPDATE Poule SET poids = poids - 1 WHERE proprietaire = ?;", (setup_poule[0],)) # 3.5kg >= poids >= 2.5kg
    
    cur.execute("DELETE FROM Poule WHERE poids <= 0;")  # Suppression de l'animal
    cur.execute("SELECT COUNT(*) FROM Poule WHERE proprietaire = ?;", (setup_poule[0],))
    result = cur.fetchone()[0]

    cur.close()
    assert result == 0  # L'animal devrait être supprimé  



 
def test_poule_malade_mort(db_conn, setup_poule):
    """Teste qu'une poule malade meurt au bout de 4 jours"""
    cur = db_conn.cursor()
    
    cur.execute("UPDATE Poule SET malade_depuis = ? WHERE proprietaire = ?;", (date.today()-timedelta(days=4), setup_poule[0]))
    
    cur.execute("DELETE FROM Poule WHERE date.today().day - malade_depuis.day >= 4;")  # Suppression de la poule
    cur.execute("SELECT COUNT(*) FROM Poule WHERE proprietaire = ?;", (setup_poule[0],))
    result = cur.fetchone()[0]

    cur.close()
    assert result == 0  # L'animal devrait être supprimé  


 
def test_poule_malade_pas_pondeuse(db_conn, setup_poule):
    """Teste qu'une poule malade ne peut pas pondre"""
    cur = db_conn.cursor()
    
    cur.execute("UPDATE Poule SET malade_depuis = ? WHERE proprietaire = ?;", (date.today(), setup_poule[0]))
    
    cur.execute("UPDATE Poule SET nb_oeuf = 0 WHERE proprietaire = ?;", (setup_poule[0],))
    cur.execute("SELECT COUNT(*) FROM Poule WHERE proprietaire = ? AND nb_oeuf = 0;", (setup_poule[0],))
    result = cur.fetchone()[0]

    cur.close()
    assert result == 1  # L'animal a bien 0 oeuf



def test_poule_sale_pas_pondeuse(db_conn, setup_poule):
    """Teste qu'une poule sale ne peut pas pondre"""
    cur = db_conn.cursor()
    
    cur.execute("UPDATE Poule SET dernier_lavage = ? WHERE proprietaire = ?;", (date.today()-timedelta(days=1), setup_poule[0]))

    cur.execute("UPDATE Poule SET nb_oeuf = 0 WHERE proprietaire = ?;", (setup_poule[0],))    
    cur.execute("SELECT COUNT(*) FROM Poule WHERE proprietaire = ? AND nb_oeuf = 0;", (setup_poule[0],))
    result = cur.fetchone()[0]

    cur.close()
    assert result == 1  # L'animal a bien 0 oeuf  
    
 


def test_poule_poids_correct_2_5(db_conn, setup_poule):
    """Teste qu'une poule *pondeuse* a un poids entre 2.5kg (inclus) et 3.5kg (inclus)"""
    cur = db_conn.cursor()
    
    
    cur.execute("INSERT INTO Poule (idPoule, poids) VALUES (?, 2.4);", (setup_poule[0],))

    cur.execute("UPDATE Poule SET nb_oeuf = 0 WHERE id = ?;", (setup_poule[0],))    
    cur.execute("SELECT COUNT(*) FROM Poule WHERE id = ? AND nb_oeuf = 0;", (setup_poule[0],))
    result = cur.fetchone()[0]

    cur.close()
    assert result == 1  # L'animal a bien 0 oeuf 



def test_poule_poids_correct_3_5(db_conn, setup_poule):
    """Teste qu'une poule *pondeuse* a un poids entre 2.5kg (inclus) et 3.5kg (inclus)"""
    cur = db_conn.cursor()
    
    
    cur.execute("INSERT INTO Poule (idPoule, poids) VALUES (?, 3.6);", (setup_poule[0],))
    
    cur.execute("UPDATE Poule SET poids = 3.5 WHERE id = ?;", (setup_poule[0],))    
    cur.execute("SELECT COUNT(*) FROM Poule WHERE id = ? AND poids = 3.5;", (setup_poule[0],))
    result = cur.fetchone()[0]

    cur.close()
    assert result == 1  # L'animal fait bien 3.5kg



def test_poule_age_correct(db_conn, setup_poule):
    """Teste qu'une poule pondeuse a un âge de 5 jours minimum"""
    cur = db_conn.cursor()
    
    cur.execute("SELECT age FROM Poule WHERE proprietaire = ?", (setup_poule[0],))    
    # cur.execute("INSERT INTO Poule (idPoule) VALUES (?);", (setup_poule,))
    age_init = cur.fetchone()[0]

    for _ in range(5):  # Simule 5 jours
        cur.execute("UPDATE Poule SET age = age + 1 WHERE proprietaire = ?;", (setup_poule[0],))
    
    cur.execute("SELECT age FROM Poule WHERE proprietaire = ?;", (setup_poule[0],))
    result = cur.fetchone()[0]

    cur.close()
    assert result == age_init+5  # L'animal a bien 5 jours ou plus



def test_poule_poids_eau_plus_grain(db_conn, setup_poule):
    """Teste qu'un animal nourri avec de l'eau augmente son poids si nourri avec des graines le même jour"""
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Poule (idPoule, dernier_repas, dernier_breuvage) VALUES (?, ?);", (setup_poule, date.today(), date.today()))
    db_conn.commit()

    cur.execute("UPDATE Poule SET poids = poids + 0.5 WHERE id = ?;", (setup_poule,))
    cur.execute("UPDATE Poule SET poids = poids + 0.15 WHERE id = ? AND dernier_repas = ?;", (setup_poule, date.today()))
    cur.execute("SELECT poids FROM Poule WHERE id = ?;", (setup_poule,))
    result = cur.fetchone()[0]

    cur.close()
    assert result == 0.65  # Le poids devrait être de 0.65kg




def test_poussin_to_adult(db_conn, setup_poule):
    """Teste que les poussins deviennent adultes lorsque poids >= 2.5kg et age >= 4 jours"""
    cur = db_conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM Poule WHERE (sexe = 'M' OR sexe = 'F');") #nbr de poules initial
    nbr_poules_avant = cur.fetchone()[0]
    for _ in range(4): 
        cur.execute("UPDATE Poule SET age = age + 1;")
        cur.execute("UPDATE Poule SET poids = poids + 0.65;") #eau + graines (assez pour faire grandir)
        
    cur.execute("SELECT COUNT(*) FROM Poule WHERE (sexe = 'U' AND age >= 4 AND poids >= 2.5);")#nbr de poussins pret à devenir des adultes
	
    nbr_poussin_pret = cur.fetchone()[0]
    cur.execute("UPDATE Poule SET sexe = 'F' WHERE age >= 4 AND sexe = 'U' AND poids >= 2.5;")   
    cur.execute("UPDATE Poule SET sexe = 'M' WHERE age >= 4 AND proprietaire = ? AND sexe = 'U' AND poids >= 2.5;", (setup_poule[0],))
    
    cur.execute("SELECT COUNT(*) FROM Poule WHERE (sexe = 'M' OR sexe = 'F');") #nbr de poules après les 4jours
    nbr_poules_après = cur.fetchone()[0]

    cur.close()
    assert nbr_poules_avant+nbr_poussin_pret == nbr_poules_après 



def test_poussin_to_adult_nofood(db_conn, setup_poule):
	
    """Teste que les poussins deviennent ne deviennet pas des adultes lorsque poids < 2.5kg et age >= 4 jours"""
    cur = db_conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM Poule WHERE (sexe = 'M' OR sexe = 'F');") #nbr de poules initial
    nbr_poules_avant = cur.fetchone()[0]
    for _ in range(4):
        cur.execute("UPDATE Poule SET age = age + 1;")
        cur.execute("UPDATE Poule SET poids = poids + 0.5;") #graines seulement (pas assez pour grandir)
        
    cur.execute("SELECT COUNT(*) FROM Poule WHERE (sexe = 'U' AND age >= 4 AND poids >= 2.5);")#nbr de poussins pret à devenir des adultes
    nbr_poussin_pret = cur.fetchone()[0]
	
	#On ne met pas les updates dans la boucle pour pouvoir évaluer le nombre de poussins pouvant grandir, afin de vérifier l'assertion.
    cur.execute("UPDATE Poule SET sexe = 'F' WHERE age >= 4 AND sexe = 'U' AND poids >= 2.5;") 
    cur.execute("UPDATE Poule SET sexe = 'M' WHERE age >= 4 AND proprietaire = ? AND sexe = 'U' AND poids >= 2.5;", (setup_poule[0],))
    
    cur.execute("SELECT COUNT(*) FROM Poule WHERE (sexe = 'M' OR sexe = 'F');") #nbr de poules après les 4jours
    nbr_poules_après = cur.fetchone()[0]

    cur.close()
    assert nbr_poules_avant+nbr_poussin_pret == nbr_poules_après



def test_adult_to_poussin(db_conn, setup_poule):
    """Teste que les poussins deviennent adultes lorsque poids < 2.5kg"""
    cur = db_conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM Poule WHERE (sexe = 'U');") #nbr de poussin initial
    nbr_poussins_avant = cur.fetchone()[0]
    for i in [0.2,0.5,1]: 
        cur.execute("UPDATE Poule SET age = age + 1;")
        cur.execute("UPDATE Poule SET poids = poids - ?;",(i,))
        
    cur.execute("SELECT COUNT(*) FROM Poule WHERE ((sexe = 'M' OR sexe = 'F') AND poids < 2.5);")#nbr d'adultes pret à redevenir des poussins
    nbr_poules_pret = cur.fetchone()[0]
	
    cur.execute("UPDATE Poule SET sexe = 'U' WHERE (sexe = 'M' OR sexe = 'F') AND poids < 2.5;")   
    cur.execute("UPDATE Poule SET sexe = 'U' WHERE id = ? AND (sexe = 'M' OR sexe = 'F');") #nbr de pousins après les 4jours
    nbr_poussins_après = cur.fetchone()[0]

    cur.close()
    assert nbr_poussins_avant+nbr_poules_pret == nbr_poussins_après
    


def test_oeufs_frais(db_conn, setup_Produit):
    """Teste que les poussins deviennent adultes lorsque poids < 2.5kg"""
    cur = db_conn.cursor()
    
    cur.execute("SELECT COUNT(idProduit) FROM Produit WHERE estVendable AND nom = \"oeufs\";") #nbr d'oeufs vendable un jour j
    nbr_oeufs_frais_j1 = cur.fetchone()[0]
    
    #PASSAGE AU PROCHAIN JOUR
    
    cur.execute("UPDATE Produit SET estVendable = False WHERE nom = \"oeufs\";") #Les oeufs ne sont plus vendables
    
    cur.execute("SELECT COUNT(idProduit) FROM Produit WHERE estVendable AND nom = \"oeufs\";") #nbr d'oeufs vendable un jour j
    nbr_oeufs_frais_j2 = cur.fetchone()[0]
	
    cur.close()
    assert (nbr_oeufs_frais_j1 > 0) and (nbr_oeufs_frais_j2 == 0)
    
    

def test_poule_perte_poids(db_conn, setup_poule):
    """Teste que le poids d'une poule diminue correctement en fonction des jours sans nourriture"""
    cur = db_conn.cursor()

    cur.execute("SELECT poids FROM Poule WHERE idPoule = ?;", (setup_poule[0],))
    poidsini = cur.fetchone()[0]

    dernier_repas = date.today() - timedelta(days=3)

    # Mettre à jour le poids en fonction des jours écoulés
    cur.execute("UPDATE Poule SET poids = poids - 0.2 WHERE idPoule = ? AND DATE('now') > DATE(dernier_repas, '+1 day');", (setup_poule[0],))
    cur.execute("UPDATE Poule SET poids = poids - 0.3 WHERE idPoule = ? AND DATE('now') > DATE(dernier_repas, '+2 days');", (setup_poule[0],))
    cur.execute("UPDATE Poule SET poids = poids - 0.5 WHERE idPoule = ? AND DATE('now') > DATE(dernier_repas, '+3 days');", (setup_poule[0],))
    db_conn.commit()

    # Vérifier le poids final
    cur.execute("SELECT poids FROM Poule WHERE idPoule = ?;", (setup_poule[0],))
    poidsfinal = cur.fetchone()[0]
    assert poidsfinal == pytest.approx(poidsini - 1.0)

    cur.close()

def test_nom_ferme_valide(db_conn, setup_db):
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Ferme (nom) VALUES ('La fermette') RETURNING idFerme;")
    result = cur.fetchone()
    cur.close()
    assert result != None


def test_nom_ferme_invalide(db_conn, setup_db):
    cur = db_conn.cursor()
    
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO Ferme (nom) VALUES ('L') RETURNING idFerme;")
    
    cur.close()


def test_id_ferme_unique(db_conn, setup_db):
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Ferme (idFerme, nom) VALUES (1,'La fermette'); ")
    
    with pytest.raises(sqlite3.IntegrityError):    
        cur.execute("INSERT INTO Ferme (idFerme, nom) VALUES (1,'La nouvelle fermette');")
    
    cur.close()
	
def test_nombre_ecus_coherent(db_conn, setup_db):
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Ferme (nom) VALUES ('La fermette') RETURNING ecus;")
    result = cur.fetchone()[0]
    cur.close()
    assert result >=0

def test_nombre_ecus_incoherent(db_conn, setup_db):
    cur = db_conn.cursor()
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO Ferme (nom, ecus) VALUES ('La fermette', -550);")


def test_nom_compte_valide(db_conn, setup_db):
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Compte (pseudo) VALUES ('Romuald') RETURNING idCompte;")
    result = cur.fetchone()
    cur.close
    assert result != None


def test_nom_compte_invalide(db_conn, setup_db):
    cur = db_conn.cursor()
    
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO Compte (pseudo) VALUES ('R') RETURNING idCompte;")
    
    cur.close

def test_nom_compte_unique(db_conn, setup_db):
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Compte (pseudo) VALUES ('Romuald');")

    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO Compte (pseudo) VALUES ('Romuald');")
    
    cur.close

def test_id_compte_unique(db_conn, setup_db):
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Compte (idCompte, pseudo) VALUES (1, 'Romuald');")
    
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO Compte (idCompte, pseudo) VALUES (1, 'Albert');")
    
    cur.close


def test_nombre_achatRestant_coherent(db_conn, setup_db):
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Ferme (nom) VALUES ('La fermette') RETURNING achatRestant;")
    result = cur.fetchone()[0]
    cur.close()
    assert result >=0

def test_nombre_achatRestant_incoherent(db_conn, setup_db):
    cur = db_conn.cursor()
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO Ferme (nom, achatRestant) VALUES ('La fermette', -3) RETURNING achatRestant;")
    cur.close()



def test_nb_bebe_lapin_correct(db_conn, setup_ferme):
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Clapier (proprietaire,nb_bebe, nb_petit, nb_gros) VALUES (1, 28, 2, 7) RETURNING proprietaire;")
    result = cur.fetchone()
    cur.close()

    assert result != None

def test_nb_bebe_lapin_incorrect(db_conn, setup_ferme):
    cur = db_conn.cursor()
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO Clapier (proprietaire,nb_bebe, nb_petit, nb_gros) VALUES (1, 45, 30, 2) RETURNING proprietaire;")
    cur.close()
def test_nb_lapin_adultes_correct(db_conn, setup_ferme):
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Clapier (proprietaire, nb_adulte_m, nb_adulte_f) VALUES (1, 28, 22) RETURNING proprietaire;")
    result = cur.fetchone()
    cur.close()

    assert result != None

def test_nb_adulte_lapin_incorrect(db_conn, setup_ferme):
    cur = db_conn.cursor()
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO Clapier (proprietaire,nb_adulte_m, nb_adulte_f) VALUES (1, 35, 25) RETURNING proprietaire;")
    cur.close()

def test_nom_produit_valide(db_conn, setup_db):
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Produit (nom, estVendable) VALUES ('Caribou en conserve', true) RETURNING idProduit;")
    result = cur.fetchone()
    cur.close()
    assert result != None

def test_nom_produit_invalide(db_conn, setup_db):
    cur = db_conn.cursor()

    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO Produit (nom, estVendable) VALUES ('C', true) RETURNING idProduit;")

    cur.close()

def test_commerce_quantite_correct(db_conn, setup_db):
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Commerce (quantite, prixUnitaire) VALUES (10, 5) RETURNING idTransac;")
    result = cur.fetchone()
    cur.close()

    assert result != None

def test_commerce_quantite_incorrecte(db_conn, setup_db):

    cur = db_conn.cursor()

    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO Commerce (quantite, prixUnitaire) VALUES (0, 5) RETURNING idTransac;")
    cur.close()

def test_commerce_prixUnitaire_correct(db_conn, setup_db):
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Commerce (quantite, prixUnitaire) VALUES (10, 5) RETURNING idTransac;")
    result = cur.fetchone()
    cur.close()

    assert result != None

def test_commerce_prixUnitaire_incorrecte(db_conn, setup_db):

    cur = db_conn.cursor()
        
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO Commerce (quantite, prixUnitaire) VALUES (10, 0) RETURNING idTransac;")
    cur.close()


def test_poids_valide_poule(db_conn, setup_poule):

    cur = db_conn.cursor()

    cur.execute("INSERT INTO Poule (poids,sexe) VALUES (2,'M') RETURNING idPoule;")
    result = cur.fetchone()

    cur.close()
    assert result != None

def test_poids_inferieur_invalide_poule(db_conn, setup_poule):

    cur = db_conn.cursor()
	
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO Poule (poids, sexe) VALUES (-1,'F') RETURNING idPoule;")
    cur.close()

def test_age_valide_poule(db_conn, setup_poule):

    cur = db_conn.cursor()

    cur.execute("INSERT INTO Poule (sexe,age) VALUES ('M',12) RETURNING idPoule;")
    result = cur.fetchone()

    cur.close()
    assert result != None
    
def test_age_invalide_poule(db_conn, setup_poule):

    cur = db_conn.cursor()
		
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO Poule (sexe,age) VALUES ('F',-12) RETURNING idPoule;")
    cur.close()

def test_sexe_valide_poule(db_conn, setup_poule):

    cur = db_conn.cursor()

    cur.execute("INSERT INTO Poule (sexe) VALUES ('M') RETURNING idPoule;")
    result = cur.fetchone()

    cur.close()
    assert result != None

def test_sexe_invalide_poule(db_conn, setup_poule):

    cur = db_conn.cursor()
		
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO Poule (sexe) VALUES ('C') RETURNING idPoule;")
    cur.close()
    
def test_nb_oeufs_valide_poule(db_conn, setup_poule):

    cur = db_conn.cursor()

    cur.execute("INSERT INTO Poule (nb_oeuf,sexe) VALUES (30,'F') RETURNING idPoule;")
    result = cur.fetchone()

    cur.close()
    assert result != None
    
def test_nb_oeufs_invalide_poule(db_conn, setup_poule):

    cur = db_conn.cursor()
		
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO Poule (nb_oeuf,sexe) VALUES (-12,'F') RETURNING idPoule;")
    cur.close()   


def test_vache_poid_valide (db_conn,setup_ferme):

    cur = db_conn.cursor()
    cur.execute("INSERT INTO Vache(proprietaire , poids , age, qt_lait ) VALUES (1,50,1,1) RETURNING proprietaire ")
    result = cur.fetchone()[0]
    cur.close()
    assert result == 1

def test_vache_poid_inferieur_invalide (db_conn,setup_ferme):

    cur = db_conn.cursor()
    with pytest.raises(sqlite3.IntegrityError):

        cur.execute("INSERT INTO Vache(proprietaire , poids , age, qt_lait ) VALUES (1,-1,1,1) RETURNING proprietaire ")


def test_vache_age_valide (db_conn,setup_ferme):

    cur = db_conn.cursor()
    cur.execute("INSERT INTO Vache(proprietaire , poids , age, qt_lait ) VALUES (1,50,5,1) RETURNING age ")
    result = cur.fetchone()[0]
    cur.close()
    assert result == 5

def test_vache_age_invalide (db_conn,setup_ferme):

    cur = db_conn.cursor()
    with pytest.raises(sqlite3.IntegrityError):

        cur.execute("INSERT INTO Vache(proprietaire , poids , age, qt_lait ) VALUES (1,50,-1,1) RETURNING age ")
        cur.close()

def test_vache_qt_lait_valide (db_conn,setup_ferme):

    cur = db_conn.cursor()
    cur.execute("INSERT INTO Vache(proprietaire , poids , age, qt_lait ) VALUES (1,50,5,5) RETURNING qt_lait ")
    result = cur.fetchone()[0]
    cur.close()
    assert result == 5

def test_vache_qt_lait_invalide (db_conn,setup_ferme):

    cur = db_conn.cursor()
    with pytest.raises(sqlite3.IntegrityError):

        cur.execute("INSERT INTO Vache(proprietaire , poids , age, qt_lait ) VALUES (1,50,1,-1) RETURNING qt_lait ")
        cur.close()
          
def test_vache_proprietaire_existant(db_conn, setup_ferme):
    cur = db_conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("INSERT INTO Vache(proprietaire , poids , age, qt_lait ) VALUES (1,50,5,5) RETURNING proprietaire ")
    result = cur.fetchone()[0]
    cur.close()
    assert result == 1


def test_vache_proprietaire_non_existant(db_conn, setup_ferme):

    cur = db_conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO Vache(proprietaire , poids , age, qt_lait ) VALUES (4,50,1,1) RETURNING proprietaire ")
        cur.close()


def test_classement_idFerme_valide(db_conn, setup_ferme):

    cur = db_conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("INSERT INTO Classement(idFerme,score ) VALUES (1,2) RETURNING score ")
    result = cur.fetchone()[0]
    cur.close()
    assert result == 2

def test_classement_idFerme_invalide(db_conn, setup_ferme):

    cur = db_conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO Classement(idFerme,score ) VALUES (4,10) RETURNING score ")
        cur.close()

def test_vache_poid_superieur_invalide (db_conn,setup_ferme):

    cur = db_conn.cursor()
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO Vache(proprietaire , poids , age, qt_lait ) VALUES (1,950,1,1) RETURNING proprietaire ")

def test_poids_superieur_invalide_poule(db_conn, setup_poule):

    cur = db_conn.cursor()
	
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO Poule (poids, sexe) VALUES (10,'F') RETURNING idPoule;")
    cur.close()

def test_lait_vache(db_conn, setup_ferme, setup_vache):
    cur = db_conn.cursor()
    #cur.execute("UPDATE Vache SET age = age + 10, poids = poids + 80;")
   
    #dans le cas ou elle a était traite dans la journée
    cur.execute("""
                UPDATE Vache SET qt_lait=8 WHERE poids>=80 AND age>10 AND malade_depuis IS NULL AND dernier_repas=? AND qt_lait=0;
                """,(date.today(),))
    #dans le cas ou elle n'a pas était traite dans la journée
    cur.execute("""
                UPDATE Vache SET qt_lait=12 WHERE poids>=80 AND age>10 AND malade_depuis IS NULL AND dernier_repas=? AND qt_lait>0;
                """,(date.today(),))
    db_conn.commit()

    cur.execute("""
    SELECT qt_lait FROM Vache WHERE proprietaire=?;
    """, (setup_ferme[1],))
    resultA = cur.fetchone()[0]

    cur.close()
    assert resultA is not None and (resultA==8 or resultA==12 or resultA==16)

def test_mortalite_maladie_vache(db_conn, setup_ferme):
    cur = db_conn.cursor()
    #modification valeur malade_depuis
    cur.execute("""
    UPDATE Vache SET malade_depuis=? WHERE proprietaire=?;
                """, (date.today() - timedelta(days=5), setup_ferme[1],))
    cur.execute("""
                DELETE FROM Vache WHERE malade_depuis>=?;
                """, (date.today() - timedelta(days=4),))
    cur.execute("""SELECT COUNT(*) FROM Vache WHERE proprietaire=?""", (setup_ferme[1],))
    db_conn.commit()
    resultA=cur.fetchone()[0]

    cur.close()
    assert resultA==0


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


