import requests
import pytest
import datetime
from dateutil import parser

# Base URL for the Spring Boot application
APP_URL = "http://localhost:8080"

@pytest.fixture(scope="module")
def auth_token():
    """Retrieve an authentication token for testing."""
    response = requests.get(f"{APP_URL}/auth/test-token")
    assert response.status_code == 200, f"Failed to retrieve token: {response.text}"
    
    token = response.text
    assert token is not None, "Token is missing in the response"
    
    return token


@pytest.fixture
def headers(auth_token):
    """Generate headers with the authentication token."""
    return {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }


@pytest.fixture
def create_or_get_farm(headers):
    """Test fetching or creating a farm for the authenticated user."""
    response = requests.get(f"{APP_URL}/ferme/", headers=headers)
    assert response.status_code == 200, f"Failed to fetch/create farm: {response.text}"

@pytest.fixture
def init_remise(headers):

    nom_produit = "Seringue"
    response = requests.post(f"{APP_URL}/remise",data=nom_produit, headers=headers)
    assert response.status_code == 200, f"Failed to add Seringue to remise: {response.text}"

    nom_produit = "Savon"
    response = requests.post(f"{APP_URL}/remise",data=nom_produit, headers=headers)
    assert response.status_code == 200, f"Failed to add Savon to remise: {response.text}"

    nom_produit = "Botte de foin"
    response = requests.post(f"{APP_URL}/remise",data=nom_produit, headers=headers)
    assert response.status_code == 200, f"Failed to add Paille to remise: {response.text}"


def test_get_vache(headers,create_or_get_farm):
    response = requests.get(f"{APP_URL}/vache", headers=headers)
    assert response.status_code == 200, f"failed to fetch cow: {response.text}"
    vache_data = response.json()
    now = datetime.datetime.now()

    try:
        dernier_repas = parser.parse(vache_data["dernierRepas"])
        dernier_breuvage = parser.parse(vache_data["dernierBreuvage"])
        dernier_lavage = parser.parse(vache_data["dernierLavage"])
    except ValueError as e:
        assert False, f"Impossible de parser les dates: {e}"

    assert vache_data["age"] == 0
    assert vache_data["poids"] == 1
    assert vache_data["qt_lait"] == 0
    assert dernier_repas < now
    assert dernier_breuvage < now
    assert dernier_lavage < now
    assert vache_data["maladeDepuis"] is None
    expected_keys = {"poids","age","qt_lait","dernierRepas","dernierBreuvage","dernierLavage","maladeDepuis" }
    assert expected_keys.issubset(vache_data.keys()),f"missing keys in : {vache_data.keys()}"

    print("✅ Test passed: Cow was successfully retrieved.") 

"""Test globale sur les poules"""
def test_get_poules(headers,create_or_get_farm):
    response = requests.get(f"{APP_URL}/poulailler", headers=headers)
    assert response.status_code == 200, f"failed to fetch chicken: {response.text}"
    poule_data = response.json()
    print(f"Response JSON: {poule_data}")  # Ajouté pour vérifier la structure de la réponse

    now = datetime.datetime.now()
    # Vérifier que les champs de dates sont parsables
    for poule in poule_data['content']:
        try:
            dernier_repas = parser.parse(poule["dernierRepas"])
            dernier_breuvage = parser.parse(poule["dernierBreuvage"])
            dernier_lavage = parser.parse(poule["dernierLavage"])
        except KeyError as e:
            assert False, f"Key {e} is missing from the response JSON"
        except Exception as e:
            assert False, f"Error parsing date: {e}"

        # Effectuer des vérifications supplémentaires sur les dates si nécessaire
        assert dernier_repas < now
        assert dernier_breuvage < now 
        assert dernier_lavage < now

        assert poule["age"] >= 0
        assert poule["poids"] >= 0.05
        assert poule["nbOeuf"] >= 0
        expected_keys = {"poids","age","sexe","dernierRepas","dernierBreuvage","dernierLavage","maladeDepuis" }
        assert expected_keys.issubset(poule.keys()),f"missing keys in : {poule.keys()}"

        print("✅ Test passed: Chicken were successfully retrieved.") 

""" test pour s'assurer que chaque catégorie de poule ( poussin, poule et coq) est bien configuré"""
def test_bonne_configuration_poules(headers,create_or_get_farm):
    response = requests.get(f"{APP_URL}/poulailler", headers=headers)
    assert response.status_code == 200, f"failed to fetch chicken: {response.text}"
    poule_data = response.json()
    print(f"Response JSON: {poule_data}")  # Ajouté pour vérifier la structure de la réponse

    now = datetime.datetime.now()
    # Vérifier que les champs de dates sont parsables
    for poule in poule_data['content']:
        try:
            dernier_repas = parser.parse(poule["dernierRepas"])
            dernier_breuvage = parser.parse(poule["dernierBreuvage"])
            dernier_lavage = parser.parse(poule["dernierLavage"])
        except KeyError as e:
            assert False, f"Key {e} is missing from the response JSON"
        except Exception as e:
            assert False, f"Error parsing date: {e}"
        if poule["sexe"] == "U":
            assert poule["age"] >= 0 and poule["age"] <= 4
            assert poule["poids"] >= 0.05 and poule["poids"] < 2.5
            assert poule["nbOeuf"] == 0
        if poule["sexe"] == "F":
            assert poule["age"] >= 5
            assert poule["poids"] >= 2.5 and poule["poids"] <= 3.5 # la poule explose sinon
            assert poule["nbOeuf"] >= 0 # une poule peut pondre des oeufs
        if poule["sexe"] == "M":
            assert poule["age"] >= 5
            assert poule["poids"] >= 2.5 and poule["poids"] <= 3.5 # la poule explose sinon
            assert poule["nbOeuf"] == 0 # un coq ne peut pas pondre d'oeuf

""" test pour s'assurer que les poussins prennent bien un jour de plus"""
def test_update_poussin(headers):
    response1 = requests.get(f"{APP_URL}/poulailler/poussins", headers=headers)
    assert response1.status_code == 200, f"failed to fetch chick: {response1.text}"
    poussin_data1 = response1.json()
    print(f"Response JSON: {poussin_data1}")

    # on vérifie qu'il y a des poussins
    if len(poussin_data1['content']) != 0:
        response2 = requests.put(f"{APP_URL}/poulailler/poussins", headers=headers)
        assert response2.status_code == 200, f"failed to fetch chick: {response2.text}"
        poussin_data2 = response2.json()
        print(f"Response JSON: {poussin_data2}")

    for poussin1 in poussin_data1['content']:
        for poussin2 in poussin_data2['content']:
            print(poussin1)
            assert poussin1["age"] == poussin2["age"]-1 
    print("✅ Test passed: chick was successfully updated.") 

""" test pour s'assurer que les poules prennent bien un jour de plus"""
def test_update_poule(headers):
    response1 = requests.get(f"{APP_URL}/poulailler/poules", headers=headers)
    assert response1.status_code == 200, f"failed to fetch chicken: {response1.text}"
    poule_data1 = response1.json()
    print(f"Response JSON: {poule_data1}")

    # on vérifie qu'il y a des poules dans le poulailler
    if len(poule_data1['content']) != 0:
        response2 = requests.put(f"{APP_URL}/poulailler/poules", headers=headers)
        assert response2.status_code == 200, f"failed to fetch chicken: {response2.text}"
        poule_data2 = response2.json()
        print(f"Response JSON: {poule_data2}")

    for poule1 in poule_data1['content']:
        for poule2 in poule_data2['content']:
            print(poule1)
            assert poule1["age"] == poule2["age"]-1 
    print("✅ Test passed: chicken was successfully updated.") 

""" test pour s'assurer que les coqs prennent bien un jour de plus"""
def test_update_coq(headers):
    response1 = requests.get(f"{APP_URL}/poulailler/coqs", headers=headers)
    assert response1.status_code == 200, f"failed to fetch chicken: {response1.text}"
    coq_data1 = response1.json()
    print(f"Response JSON: {coq_data1}")

    # on vérifie qu'il y a des coqs dans le poulailler
    if len(coq_data1['content']) != 0:
        response2 = requests.put(f"{APP_URL}/poulailler/coqs", headers=headers)
        assert response2.status_code == 200, f"failed to fetch chicken: {response2.text}"
        coq_data2 = response2.json()
        print(f"Response JSON: {coq_data2}")

    for coq1 in coq_data1['content']:
        for coq2 in coq_data2['content']:
            print(coq1)
            assert coq1["age"] == coq2["age"]-1 
    print("✅ Test passed: chicken was successfully updated.") 