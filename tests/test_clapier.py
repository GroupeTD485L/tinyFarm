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
    return response.text

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
    # produit dans service
    products = ["Graine", "Seau d'eau", "Seringue", "Savon"]
    for product in products:
        response = requests.post(f"{APP_URL}/remise", data=product, headers=headers)
        assert response.status_code == 200, f"Failed to add {product} to remise: {response.text}"
    
    print("✅ Test passed: Rabbits were successfully watered.")

#--------------------------------------------------------------------------------------------
def test_get_clapier(headers, create_or_get_farm):
    response = requests.get(f"{APP_URL}/clapier", headers=headers)
    assert response.status_code == 200, f"Failed to fetch rabbit hutch: {response.text}"
    clapier_data = response.json()

    # verif des valeurs init
    assert clapier_data["nb_bebe"] == 8
    assert clapier_data["nb_petit"] == 0
    assert clapier_data["nb_gros"] == 0
    assert clapier_data["nb_adulte_m"] == 0
    assert clapier_data["nb_adulte_f"] == 0
    
    # verif des dates
    try:
        dernier_repas = parser.parse(clapier_data["dernierRepas"])
        dernier_breuvage = parser.parse(clapier_data["dernierBreuvage"])
        dernier_lavage = parser.parse(clapier_data["dernierLavage"])
    except ValueError as e:
        assert False, f"Failed to parse dates: {e}"
    
    mainteant = datetime.datetime.now()
    assert dernier_repas < mainteant
    assert dernier_breuvage < mainteant
    assert dernier_lavage < mainteant
    assert clapier_data["maladeDepuis"] is None
    
    print("✅ Test passed: Rabbit hutch was successfully retrieved.")
    print("✅ Test passed: Rabbits were successfully watered.")

#--------------------------------------------------------------------------------------------
def test_update_clapier(headers):
    # nourir et abreuver
    requests.put(f"{APP_URL}/clapier/nourrir", headers=headers)
    requests.put(f"{APP_URL}/clapier/abreuver", headers=headers)
    
    response = requests.put(f"{APP_URL}/clapier", headers=headers)
    assert response.status_code == 200, f"Failed to update rabbit hutch: {response.text}"
    clapier_data = response.json()

    # verif changement de valeurs ( = progres)
    assert clapier_data["nb_bebe"] == 0
    assert clapier_data["nb_petit"] == 8
    assert clapier_data["nb_gros"] == 0 # verification correcte ?
    
    print("✅ Test passed: Rabbit hutch was successfully updated.")
    print("✅ Test passed: Rabbits were successfully watered.")

#--------------------------------------------------------------------------------------------
def test_nourrir_clapier(headers, init_remise):
    response = requests.put(f"{APP_URL}/clapier/nourrir", headers=headers)
    assert response.status_code == 200, f"Failed to feed rabbits: {response.text}"
    
    clapier_data = response.json()
    try:
        dernier_repas = parser.parse(clapier_data["dernierRepas"])
    except ValueError as e:
        assert False, f"Failed to parse date: {e}"
    
    date_hier = datetime.datetime.now() - datetime.timedelta(days=1)
    assert dernier_repas > date_hier
    print("✅ Test passed: Rabbits were successfully fed.")
    print("✅ Test passed: Rabbits were successfully watered.")

#--------------------------------------------------------------------------------------------
def test_abreuver_clapier(headers, init_remise):
    response = requests.put(f"{APP_URL}/clapier/abreuver", headers=headers)
    assert response.status_code == 200, f"Failed to water rabbits: {response.text}"
    clapier_data = response.json()

    try:
        dernier_breuvage = parser.parse(clapier_data["dernierBreuvage"])
    except ValueError as e:
        assert False, f"Failed to parse date: {e}"

    date_hier = datetime.datetime.now() - datetime.timedelta(days=1)
    assert dernier_breuvage > date_hier
    print("✅ Test passed: Rabbits were successfully watered.")

#--------------------------------------------------------------------------------------------
def test_soigner_clapier(headers, init_remise):
    response = requests.put(f"{APP_URL}/clapier/soigner", headers=headers)
    assert response.status_code == 200, f"Failed to heal rabbits: {response.text}"
    clapier_data = response.json()
    
    assert clapier_data["maladeDepuis"] is None
    print("✅ Test passed: Rabbits were successfully healed.")


#--------------------------------------------------------------------------------------------
def test_laver_clapier(headers, init_remise):
    """Test cleaning the rabbit hutch"""
    response = requests.put(f"{APP_URL}/clapier/laver", headers=headers)
    assert response.status_code == 200, f"Failed to clean rabbit hutch: {response.text}"
    clapier_data = response.json()
    
    try:
        dernier_lavage = parser.parse(clapier_data["dernierLavage"])
    except ValueError as e:
        assert False, f"Failed to parse date: {e}"

    date_hier = datetime.datetime.now() - datetime.timedelta(days=1)
    assert dernier_lavage > date_hier
    print("✅ Test passed: Rabbit hutch was successfully cleaned.")

#--------------------------------------------------------------------------------------------
def test_lapin_affame(headers):
    # current state
    response1 = requests.get(f"{APP_URL}/clapier", headers=headers)
    assert response1.status_code == 200, f"failed to fetch rabbit hutch: {response1.text}"
    initial_data = response1.json()
    
    # verif apres 24h
    response2 = requests.put(f"{APP_URL}/clapier", headers=headers)
    assert response2.status_code == 200, f"failed to fetch rabbit hutch: {response2.text}"
    updated_data = response2.json()
    
    # verif si les nombres a diminuer
    assert (updated_data["nb_bebe"] < initial_data["nb_bebe"] or 
            updated_data["nb_petit"] < initial_data["nb_petit"] or
            updated_data["nb_gros"] < initial_data["nb_gros"] or
            updated_data["nb_adulte_m"] < initial_data["nb_adulte_m"] or
            updated_data["nb_adulte_f"] < initial_data["nb_adulte_f"])
    
    print("✅ Test passed: Rabbit starvation behavior works correctly.")