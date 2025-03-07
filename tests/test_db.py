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



##### Tests concernant les poules (réalisés par Noé et Tony) #####

def test_poule_nourrie_une_fois(db_conn, setup_poule):
    """Teste qu'un animal n'est nourrie qu'une seule fois par jour"""
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Poule (idPoule, dernier_repas) VALUES (?, ?));", (setup_poule, date.today()))
    db_conn.commit()

    with pytest.raises(sqlite3.IntegrityError):  # Vérifie qu'on ne peut nourrir plusieurs fois
        cur.execute("INSERT INTO Poule (idPoule, dernier_repas) VALUES (?, ?));", (setup_poule, date.today()))
        db_conn.commit()

    cur.close() #on s'attend à ce que le test soit un échec



def test_mortalite_si_non_nourrie(db_conn, setup_poule):
    """Teste qu'un animal meurt après 4 jours sans nourriture"""
    cur = db_conn.cursor()

    for _ in range(4):  # Simule 4 jours sans nourriture
        cur.execute("UPDATE Poule SET poids = poids - 1 WHERE id = ?;", (setup_poule,)) # 3.5kg >= poids >= 2.5kg
    
    cur.execute("DELETE FROM Poule WHERE poids <= 0;")  # Suppression de l'animal
    cur.execute("SELECT COUNT(*) FROM Poule WHERE id = ?;", (setup_poule,))
    result = cur.fetchone()[0]

    cur.close()
    assert result == 0  # L'animal devrait être supprimé  



 
def test_poule_malade_mort(db_conn, setup_poule):
    """Teste qu'une poule malade meurt au bout de 4 jours"""
    cur = db_conn.cursor()
    
    cur.execute("UPDATE Poule SET malade_depuis = ? WHERE id = ?;", (date.today()-timedelta(days=4), setup_poule))
    
    cur.execute("DELETE FROM Poule WHERE date.today().day - malade_depuis.day >= 4;")  # Suppression de la poule
    cur.execute("SELECT COUNT(*) FROM Poule WHERE id = ?;", (setup_poule,))
    result = cur.fetchone()[0]

    cur.close()
    assert result == 0  # L'animal devrait être supprimé  


 
def test_poule_malade_pas_pondeuse(db_conn, setup_poule):
    """Teste qu'une poule malade ne peut pas pondre"""
    cur = db_conn.cursor()
    
    cur.execute("UPDATE Poule SET malade_depuis = ? WHERE id = ?;", (date.today(), setup_poule))
    
    cur.execute("UPDATE Poule SET nb_oeuf = 0 WHERE id = ?;", (setup_poule,))
    cur.execute("SELECT COUNT(*) FROM Poule WHERE id = ? AND nb_oeuf = 0;", (setup_poule,))
    result = cur.fetchone()[0]

    cur.close()
    assert result == 1  # L'animal a bien 0 oeuf



def test_poule_sale_pas_pondeuse(db_conn, setup_poule):
    """Teste qu'une poule sale ne peut pas pondre"""
    cur = db_conn.cursor()
    
    cur.execute("UPDATE Poule SET dernier_lavage = ? WHERE id = ?;", (date.today()-timedelta(days=1), setup_poule))

    cur.execute("UPDATE Poule SET nb_oeuf = 0 WHERE id = ?;", (setup_poule,))    
    cur.execute("SELECT COUNT(*) FROM Poule WHERE id = ? AND nb_oeuf = 0;", (setup_poule,))
    result = cur.fetchone()[0]

    cur.close()
    assert result == 1  # L'animal a bien 0 oeuf  
    
 


def test_poule_poids_correct_2_5(db_conn, setup_poule):
    """Teste qu'une poule *pondeuse* a un poids entre 2.5kg (inclus) et 3.5kg (inclus)"""
    cur = db_conn.cursor()
    
    
    cur.execute("INSERT INTO Poule (idPoule, poids) VALUES (?, 2.4));", (setup_poule,))

    cur.execute("UPDATE Poule SET nb_oeuf = 0 WHERE id = ?;", (setup_poule,))    
    cur.execute("SELECT COUNT(*) FROM Poule WHERE id = ? AND nb_oeuf = 0;", (setup_poule,))
    result = cur.fetchone()[0]

    cur.close()
    assert result == 1  # L'animal a bien 0 oeuf 



def test_poule_poids_correct_3_5(db_conn, setup_poule):
    """Teste qu'une poule *pondeuse* a un poids entre 2.5kg (inclus) et 3.5kg (inclus)"""
    cur = db_conn.cursor()
    
    
    cur.execute("INSERT INTO Poule (idPoule, poids) VALUES (?, 3.6));", (setup_poule,))
    
    cur.execute("UPDATE Poule SET poids = 3.5 WHERE id = ?;", (setup_poule,))    
    cur.execute("SELECT COUNT(*) FROM Poule WHERE id = ? AND poids = 3.5;", (setup_poule,))
    result = cur.fetchone()[0]

    cur.close()
    assert result == 1  # L'animal fait bien 3.5kg



def test_poule_age_correct(db_conn, setup_poule):
    """Teste qu'une poule pondeuse a un âge de 5 jours minimum"""
    cur = db_conn.cursor()
    
    
    cur.execute("INSERT INTO Poule (idPoule) VALUES (?));", (setup_poule,))

    for _ in range(5):  # Simule 5 jours
        cur.execute("UPDATE Poule SET age = age + 1 WHERE id = ?;", (setup_poule,))
    
    cur.execute("SELECT COUNT(*) FROM Poule WHERE id = ? AND age >= 5;", (setup_poule,))
    result = cur.fetchone()[0]

    cur.close()
    assert result == 1  # L'animal a bien 5 jours ou plus



def test_poule_poids_eau_plus_grain(db_conn, setup_poule):
    """Teste qu'un animal nourri avec de l'eau augmente son poids si nourri avec des graines le même jour"""
    cur = db_conn.cursor()
    cur.execute("INSERT INTO Poule (idPoule, dernier_jours, dernier_breuvage) VALUES (?, ?));", (setup_poule, date.today(), date.today()))
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
    cur.execute("UPDATE Poule SET sexe = 'M' WHERE age >= 4 AND id = ? AND sexe = 'U' AND poids >= 2.5;", (setup_poule,))
    
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
    cur.execute("UPDATE Poule SET sexe = 'M' WHERE age >= 4 AND id = ? AND sexe = 'U' AND poids >= 2.5;", (setup_poule,))
    
    cur.execute("SELECT COUNT(*) FROM Poule WHERE (sexe = 'M' OR sexe = 'F');") #nbr de poules après les 4jours
    nbr_poules_après = cur.fetchone()[0]

    cur.close()
    assert nbr_poules_avant+nbr_poussin_pret == nbr_poules_après



def test_adult_to_poussin(db_conn):
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
    cur.execute("UPDATE Poule SET sexe = 'U' WHERE id = ? AND M' OR sexe = 'F');") #nbr de pousins après les 4jours
    nbr_poussins_après = cur.fetchone()[0]

    cur.close()
    assert nbr_poussins_avant+nbr_poules_pret == nbr_poussins_après
    


def test_oeufs_frais(db_conn):
    """Teste que les poussins deviennent adultes lorsque poids < 2.5kg"""
    cur = db_conn.cursor()
    
    cur.execute("SELECT COUNT(idProduit) FROM Produit WHERE estVendable AND nom = \"oeufs\";") #nbr d'oeufs vendable un jour j
	nbr_oeufs_frais_j1 = cur.fetchone()[0]
    
    #PASSAGE AU PROCHAIN JOUR
    
    cur.execute("UPDATE Produit SET estVendable = False WHERE nom = \"oeufs\";") #Les oeufs ne sont plus vendables
    
    cur.execute("SELECT COUNT(idProduit) FROM Produit WHERE estVendable AND nom = \"oeufs\";") #nbr d'oeufs vendable un jour j
	nbr_oeufs_frais_j2 = cur.fetchone()[0]
	
    cur.close()
    assert (nbr_oeufs_frais_j1 > 0) && (nbr_oeufs_frais_j2 == 0)
    
    

def test_poule_perte_poids(db_conn, setup_poule):
    """Teste que le poids d'une poule diminue correctement en fonction des jours sans nourriture"""
    cur = db_conn.cursor()

    cur.execute("SELECT poids FROM Poule WHERE idPoule = ?;", (setup_poule,))
    poidsini = cur.fetchone()[0]

    dernier_repas = date.today() - timedelta(days=3)

    # Mettre à jour le poids en fonction des jours écoulés
    cur.execute("UPDATE Poule SET poids = poids - 0.2 WHERE idPoule = ? AND DATE('now') > DATE(dernier_repas, '+1 day');", (setup_poule,))
    cur.execute("UPDATE Poule SET poids = poids - 0.3 WHERE idPoule = ? AND DATE('now') > DATE(dernier_repas, '+2 days');", (setup_poule,))
    cur.execute("UPDATE Poule SET poids = poids - 0.5 WHERE idPoule = ? AND DATE('now') > DATE(dernier_repas, '+3 days');", (setup_poule,))
    db_conn.commit()

    # Vérifier le poids final
    cur.execute("SELECT poids FROM Poule WHERE idPoule = ?;", (setup_poule,))
    poidsfinal = cur.fetchone()[0]
    assert poidsfinal == pytest.approx(poidsini - 1.0)

    cur.close()