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
def init_remise(headers):
    # produit dans service
    products = ["Seau d'eau", "Seringue", "Savon"]
    for product in products:
        response = requests.post(f"{APP_URL}/remise", data=product, headers=headers)
        assert response.status_code == 200, f"Failed to add {product} to remise: {response.text}"
    
    print("✅ Test passed: Les produits sont bien ajoutés.")
@pytest.fixture
def create_or_get_farm(headers):
    """Test fetching or creating a farm for the authenticated user."""
    response = requests.get(f"{APP_URL}/ferme/", headers=headers)
    assert response.status_code == 200, f"Failed to fetch/create farm: {response.text}"

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

@pytest.mark.usefixtures("init_remise")
def test_abreuver_poule(headers, init_remise):
    # Récupérer la liste des poules
    response1 = requests.get(f"{APP_URL}/poulailler/poules", headers=headers)
    assert response1.status_code == 200, f"Failed to fetch chickens: {response1.text}"
    poule_data1 = response1.json()
    print(f"Initial Response JSON: {poule_data1}")

    # Vérifier qu'il y a au moins une poule
    assert len(poule_data1['content']) > 0, "No chickens available to watered."

    # Sélectionner une poule spécifique (par exemple, la première)
    poule_id = poule_data1['content'][0]['idPoule']
    poule_before = poule_data1['content'][0]

    # Nourrir la poule sélectionnée
    response2 = requests.put(f"{APP_URL}/poulailler/{poule_id}/abreuver", data="Seau d'eau", headers=headers)
    assert response2.status_code == 200, f"Failed to watered chicken with ID {poule_id}: {response2.text}"
    poule_after = response2.json()
    print(f"Updated Response JSON: {poule_after}")

    # Vérifier que le poids a augmenté ou est resté le même
    assert poule_after["poids"] >= poule_before["poids"], "Weight did not increase as expected."

    # Vérifier que la date du dernier breuvage a été mise à jour
    try:
        dernier_breuvage = parser.parse(poule_after["dernierBreuvage"])
    except ValueError as e:
        assert False, f"Failed to parse 'dernierBreuvage': {e}"

    date_hier = datetime.datetime.now() - datetime.timedelta(days=1)
    assert dernier_breuvage > date_hier

    print("✅ Test passed: Chicken was successfully watered and updated.")

@pytest.mark.usefixtures("init_remise")
def test_laver_poule(headers, init_remise):
    # Récupérer la liste des poules
    response1 = requests.get(f"{APP_URL}/poulailler/poules", headers=headers)
    assert response1.status_code == 200, f"Failed to fetch chickens: {response1.text}"
    poule_data1 = response1.json()
    print(f"Initial Response JSON: {poule_data1}")

    # Vérifier qu'il y a au moins une poule
    assert len(poule_data1['content']) > 0, "No chickens available to washed."

    # Sélectionner une poule spécifique (par exemple, la première)
    poule_id = poule_data1['content'][0]['idPoule']
    poule_before = poule_data1['content'][0]

    # Nourrir la poule sélectionnée
    response2 = requests.put(f"{APP_URL}/poulailler/{poule_id}/laver", data="Savon", headers=headers)
    assert response2.status_code == 200, f"Failed to washed chicken with ID {poule_id}: {response2.text}"
    poule_after = response2.json()
    print(f"Updated Response JSON: {poule_after}")

    # Vérifier que la date du dernier lavage a été mise à jour
    try:
        dernier_lavage = parser.parse(poule_after["dernierLavage"])
    except ValueError as e:
        assert False, f"Failed to parse 'dernierLavage': {e}"

    date_hier = datetime.datetime.now() - datetime.timedelta(days=1)
    assert dernier_lavage > date_hier

    print("✅ Test passed: Chicken was successfully washed and updated.")

