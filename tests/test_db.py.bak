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
    """Donnée d'exemple pour la table Produit"""
    produits = [
        ('oeuf', 'ceci est un oeuf'),
        ('lait', 'lait de vache d\'une qualité supérieur'),
        ('Botte de Paille', 'De quoi nourir la vache'),
        ('Seau d\'eau', 'de l\'eau'),
        ('graines', 'miam les graines'),
        ('savon', 'ça mousse')
    ]
    # nomProduit = ['oeuf', 'lait', 'Botte de Paille', 'Seau d\'eau','graines','savon']
    # decrProduit = ['ceci est un oeuf', 'lait de vache d une qualité supérieur', 'De quoi nourir la vache', 'de l\'eau','miam les graines','ça mousse']
    idp = []
    cur = db_conn.cursor()
    for produit in produits:
        cur.execute("INSERT INTO Produit (nom, description, estVendable) VALUES (?, ?, 1) RETURNING idProduit", produit)
        idp.append(cur.fetchone()[0])
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
    """Teste qu'un animal meurt après 4 jours sans nourriture ou si son poids est à 0"""
    cur = db_conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Poule;")
    resultA = cur.fetchone()[0]
    cur.execute("UPDATE Poule SET poids=0 WHERE idPoule = ?;", (setup_poule[1],))
    cur.execute("UPDATE Poule SET dernier_repas = ? WHERE idPoule = ?;", (date.today() - timedelta(days=5), setup_poule[0],))   #elle meurt après 4 jours sans manger
    cur.execute("DELETE FROM Poule WHERE poids <= 0 OR dernier_repas<?;", (date.today()-timedelta(days=4),))  # Suppression de l'animal
    db_conn.commit()
    cur.execute("SELECT COUNT(*) FROM Poule;")
    resultB = cur.fetchone()[0]

    cur.close()
    assert resultB == resultA-2  # Les deux poules doivent être supprimées


def test_poule_malade_mort(db_conn, setup_poule):
    """Teste qu'une poule malade meurt au bout de 4 jours"""
    cur = db_conn.cursor()
    
    cur.execute("UPDATE Poule SET malade_depuis = ? WHERE idPoule = ?;", (date.today()-timedelta(days=5), setup_poule[0],))
    cur.execute("DELETE FROM Poule WHERE malade_depuis>? ;", (date.today() - timedelta(days=4),))  # Suppression de la poule
    db_conn.commit()
    cur.execute("SELECT COUNT(*) FROM Poule WHERE idPoule = ?;", (setup_poule[0],))
    result = cur.fetchone()[0]

    cur.close()
    assert result == 0  # L'animal devrait être supprimé  
    
 
def test_poule_malade_pas_pondeuse(db_conn, setup_poule):
    """Teste qu'une poule malade ne peut pas pondre"""
    cur = db_conn.cursor()
    
    cur.execute("UPDATE Poule SET malade_depuis = ? WHERE idPoule = ?;", (date.today(), setup_poule[0]))
    
    cur.execute("UPDATE Poule SET nb_oeuf = 0 WHERE idPoule = ?;", (setup_poule[0],))
    db_conn.commit()
    cur.execute("SELECT COUNT(*) FROM Poule WHERE proprietaire = ? AND nb_oeuf = 0;", (setup_poule[0],))
    result = cur.fetchone()[0]

    cur.close()
    assert result == 1  # L'animal a bien 0 oeuf



def test_poule_sale_pas_pondeuse(db_conn, setup_poule):
    """Teste qu'une poule sale ne peut pas pondre"""
    cur = db_conn.cursor()
    
    cur.execute("UPDATE Poule SET dernier_lavage = ? WHERE idPoule = ?;", (date.today()-timedelta(days=1), setup_poule[0]))

    cur.execute("UPDATE Poule SET nb_oeuf = 0 WHERE idPoule = ?;", (setup_poule[0],))   
    db_conn.commit() 
    cur.execute("SELECT COUNT(*) FROM Poule WHERE idPoule = ? AND nb_oeuf = 0;", (setup_poule[0],))
    result = cur.fetchone()[0]

    cur.close()
    assert result == 1  # L'animal a bien 0 oeuf  
    

def test_poule_age_correct(db_conn, setup_poule):
    """Teste qu'une poule pondeuse a un âge de 5 jours minimum"""
    cur = db_conn.cursor()
    
    cur.execute("SELECT age FROM Poule WHERE idPoule = ?", (setup_poule[0],))    
    # cur.execute("INSERT INTO Poule (idPoule) VALUES (?);", (setup_poule,))
    age_init = cur.fetchone()[0]

    for _ in range(5):  # Simule 5 jours
        cur.execute("UPDATE Poule SET age = age + 1 WHERE idPoule = ?;", (setup_poule[0],))
    
    cur.execute("SELECT age FROM Poule WHERE idPoule = ?;", (setup_poule[0],))
    result = cur.fetchone()[0]

    cur.close()
    assert result == age_init+5  # L'animal a bien 5 jours ou plus



def test_poule_poids_eau_plus_grain(db_conn, setup_poule):
    """Teste qu'un animal nourri avec de l'eau augmente son poids si nourri avec des graines le même jour"""
    cur = db_conn.cursor()
    cur.execute("SELECT poids FROM Poule WHERE idPoule = ?;", (setup_poule[0],))
    resutlA = cur.fetchone()[0]
    cur.execute("UPDATE Poule SET poids = poids + 0.5 WHERE idPoule = ?;", (setup_poule[0],))
    cur.execute("UPDATE Poule SET poids = poids + 0.15 WHERE idPoule = ? AND dernier_repas = ?;", (setup_poule[0], date.today()))
    db_conn.commit()
    cur.execute("SELECT poids FROM Poule WHERE idPoule = ?;", (setup_poule[0],))
    resultB = cur.fetchone()[0]

    cur.close()
    assert resultB == resutlA+0.65  # Le poids devrait être de 0.65kg




def test_poussin_to_adult(db_conn, setup_poule):
    """Teste que les poussins deviennent adultes lorsque poids >= 2.5kg et age >= 4 jours"""
    cur = db_conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM Poule WHERE (sexe = 'M' OR sexe = 'F');") #nbr de poules initial
    nbr_poules_avant = cur.fetchone()[0]
    # for _ in range(4): 
    #     cur.execute("UPDATE Poule SET age = age + 1;")
    #     cur.execute("UPDATE Poule SET poids = poids + 0.65;") #eau + graines (assez pour faire grandir)

    cur.execute("UPDATE Poule SET age = age + 4 WHERE idPoule = ?;", (setup_poule[0],))
    cur.execute("UPDATE Poule SET poids = 2.6 WHERE idPoule = ?;", (setup_poule[0],))
    db_conn.commit()
    cur.execute("SELECT COUNT(*) FROM Poule WHERE (sexe = 'U' AND age >= 4 AND poids >= 2.5);")#nbr de poussins pret à devenir des adultes
    nbr_poussin_pret = cur.fetchone()[0]

    cur.execute("UPDATE Poule SET sexe = 'F' WHERE age >= 4 AND sexe = 'U' AND poids >= 2.5;")   
    cur.execute("UPDATE Poule SET sexe = 'M' WHERE age >= 4 AND idPoule = ? AND sexe = 'U' AND poids >= 2.5;", (setup_poule[0],))
    db_conn.commit()
    cur.execute("SELECT COUNT(*) FROM Poule WHERE (sexe = 'M' OR sexe = 'F');") #nbr de poules après les 4jours
    nbr_poules_après = cur.fetchone()[0]

    cur.close()
    assert nbr_poules_avant+nbr_poussin_pret == nbr_poules_après 



def test_poussin_to_adult_nofood(db_conn, setup_poule):
	
    """Teste que les poussins ne deviennent pas des adultes lorsque poids < 2.5kg et age >= 4 jours"""
    cur = db_conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM Poule WHERE (sexe = 'M' OR sexe = 'F');") #nbr de poules initial
    nbr_poules_avant = cur.fetchone()[0]
    # for _ in range(4):
    #     cur.execute("UPDATE Poule SET age = age + 1;")
    #     cur.execute("UPDATE Poule SET poids = poids + 0.5;") #graines seulement (pas assez pour grandir)
    cur.execute("UPDATE Poule SET age = age + 4 WHERE idPoule = ?;", (setup_poule[0],))
    cur.execute("UPDATE Poule SET poids = 2 WHERE idPoule = ?;", (setup_poule[0],)) 
    db_conn.commit()
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
    db_conn.commit()
    cur.execute("SELECT COUNT(*) FROM Poule WHERE ((sexe = 'M' OR sexe = 'F') AND poids < 2.5);")#nbr d'adultes pret à redevenir des poussins
    nbr_poules_pret = cur.fetchone()[0]
	
    cur.execute("UPDATE Poule SET sexe = 'U' WHERE (sexe = 'M' OR sexe = 'F') AND poids < 2.5;")  
    db_conn.commit() 
    cur.execute("SELECT COUNT(*) FROM Poule WHERE (sexe = 'U');") #nbr de pousins après les 4jours
    nbr_poussins_après = cur.fetchone()[0]

    cur.close()
    assert nbr_poussins_avant+nbr_poules_pret == nbr_poussins_après
    


def test_oeufs_frais(db_conn, setup_Produit):
    """Teste que les poussins deviennent adultes lorsque poids < 2.5kg"""
    cur = db_conn.cursor()
    
    cur.execute("SELECT COUNT(idProduit) FROM Produit WHERE estVendable AND nom = \"oeuf\";") #nbr d'oeufs vendable un jour j
    nbr_oeufs_frais_j1 = cur.fetchone()[0]
    
    #PASSAGE AU PROCHAIN JOUR
    
    cur.execute("UPDATE Produit SET estVendable = False WHERE nom = \"oeuf\";") #Les oeufs ne sont plus vendables
    db_conn.commit()
    cur.execute("SELECT COUNT(idProduit) FROM Produit WHERE estVendable AND nom = \"oeuf\";") #nbr d'oeufs vendable un jour j
    nbr_oeufs_frais_j2 = cur.fetchone()[0]
	
    cur.close()
    assert (nbr_oeufs_frais_j1 > 0) and (nbr_oeufs_frais_j2 == 0)
    
    

def test_poule_perte_poids(db_conn, setup_poule):
    """Teste que le poids d'une poule diminue correctement en fonction des jours sans nourriture"""
    cur = db_conn.cursor()

    cur.execute("SELECT poids FROM Poule WHERE idPoule = ?;", (setup_poule[0],))
    poidsini_poule1 = cur.fetchone()[0]
    cur.execute("SELECT poids FROM Poule WHERE idPoule = ?;", (setup_poule[1],))
    poidsini_poule2 = cur.fetchone()[0]

    dernier_repas = date.today() - timedelta(days=3)

    # Mettre à jour le poids en fonction des jours écoulés
    cur.execute("UPDATE Poule SET dernier_repas = ? WHERE idPoule = ?;", (date.today()-timedelta(days=3), setup_poule[0],))
    cur.execute("UPDATE Poule SET poids = poids - 0.2 WHERE idPoule = ? AND DATE('now') = DATE(?);", (setup_poule[0], dernier_repas+timedelta(days=1),))
    cur.execute("UPDATE Poule SET poids = poids - 0.3 WHERE idPoule = ? AND DATE('now') = DATE(?);", (setup_poule[0], dernier_repas+timedelta(days=2),))
    cur.execute("UPDATE Poule SET poids = poids - 0.5 WHERE idPoule = ? AND DATE('now') >= DATE(?);", (setup_poule[0], dernier_repas+timedelta(days=3),))
    db_conn.commit()

    # Vérifier le poids final
    cur.execute("SELECT poids FROM Poule WHERE idPoule = ?;", (setup_poule[0],))
    poidsfinal_poule1 = cur.fetchone()[0]
    cur.execute("SELECT poids FROM Poule WHERE idPoule = ?;", (setup_poule[1],))
    poidsfinal_poule2 = cur.fetchone()[0]
    assert poidsfinal_poule1 == poidsini_poule1-0.5 and  poidsfinal_poule2 == poidsini_poule2

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
        cur.execute("INSERT INTO Vache(proprietaire , poids , age, qt_lait ) VALUES (8,50,1,1) RETURNING proprietaire ")
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
        cur.execute("INSERT INTO Classement(idFerme,score ) VALUES (8,10) RETURNING score ")
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
    # Fonctionnait quand seulement 2 fermes étaient présentes dans setup_ferme
    assert e1 == (resultA[1], len(setup_ferme)*20, 20) and e2 == (resultD[1], len(setup_ferme)*20, 10)


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
    
def test_abreuver_nourrir(db_conn, setup_ferme, setup_clapier):

    # === Simuler le passage d'une nuit ===
    cur = db_conn.cursor()

    # === Mettre à jour les dates de dernier repas et dernier breuvage, on passe les dates au date d'hier pour ===
    cur.execute("""
        UPDATE Clapier SET dernier_repas = ?, dernier_breuvage = ? WHERE proprietaire = ? AND dernier_repas = ? AND dernier_breuvage = ?;
    """, (date.today()-timedelta(days=1), date.today()-timedelta(days=1), setup_ferme[0], date.today(), date.today()))
    # après on select les dates de dernier repas et dernier breuvage pour chaque clapier
    cur.execute("SELECT dernier_repas, dernier_breuvage FROM Clapier  WHERE proprietaire = ?;",(setup_ferme[0],))
    poule_non_nourri_non_abreuve = cur.fetchone()
    # Regarder si clapier nourri et abreuvé après une nuit devient non nourri et non abreuvé
    assert poule_non_nourri_non_abreuve ==(date.today().strftime('%Y-%m-%d'),((date.today()- timedelta(days=1)).strftime('%Y-%m-%d')))

def test_laver(db_conn, setup_ferme, setup_clapier):
    cur = db_conn.cursor()
    # === Mettre à jour les dates du dernier lavage, on passe les dates au date d'hier pour ===
    cur.execute("""
            UPDATE Clapier SET dernier_lavage = ? WHERE proprietaire = ? AND dernier_lavage = ?;
        """, ( (date.today()-timedelta(days=1)),setup_ferme[0], date.today()))
    # après on selecte les dates du dernier lavage pour chaque clapier
    cur.execute("SELECT dernier_lavage FROM Clapier  WHERE proprietaire = ?;", (setup_ferme[0],))
    poule_non_laver = cur.fetchone()
    # Regarder si clapier n'est pas lavé
    assert poule_non_laver == ( ((date.today() - timedelta(days=1)).strftime('%Y-%m-%d'),))