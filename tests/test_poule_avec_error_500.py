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
    products = ["Grain","Seau d'eau", "Seringue", "Savon"]
    for product in products:
        response = requests.post(f"{APP_URL}/remise", data=product, headers=headers)
        assert response.status_code == 200, f"Failed to add {product} to remise: {response.text}"
    
    print("✅ Test passed: Les produits sont bien ajoutés.")
@pytest.fixture
def create_or_get_farm(headers):
    """Test fetching or creating a farm for the authenticated user."""
    response = requests.get(f"{APP_URL}/ferme/", headers=headers)
    assert response.status_code == 200, f"Failed to fetch/create farm: {response.text}"


@pytest.mark.usefixtures("headers")
def test_verification_get_poulailler(headers):
    response = requests.get(f"{APP_URL}/poulailler", headers=headers)
    assert response.status_code == 200, f"Failed to fetch chickens: {response.text}"
    poulailler = response.json()
    print(f"Response JSON: {poulailler}")

    # Vérifier qu'il y a au moins une poule
    assert len(poulailler['content']) > 0, "No chickens available to update."

@pytest.mark.usefixtures("headers")
def test_evolution_possible_poulailler(headers):
    
    # Récupérer l'état du poulailler avant la mise à jour
    response1 = requests.get(f"{APP_URL}/poulailler", headers=headers)
    assert response1.status_code == 200, f"Failed to fetch chickens before update: {response1.text}"
    poulailler_avant = response1.json()
    print(f"Response JSON before update: {poulailler_avant}")

    response = requests.put(f"{APP_URL}/poulailler", headers=headers)
    assert response.status_code == 200, f"Failed to update all chickens: {response.text}"
    poulailler_après = response.json()
    print(f"Response JSON after update: {poulailler_après}")

@pytest.mark.usefixtures("headers")
def test_evolution_possible_poulailler_admin(headers):
    
    # Récupérer l'état du poulailler avant la mise à jour
    response1 = requests.get(f"{APP_URL}/poulailler", headers=headers)
    assert response1.status_code == 200, f"Failed to fetch chickens before update: {response1.text}"
    poulailler_avant = response1.json()
    print(f"Response JSON before update: {poulailler_avant}")
    
    response = requests.put(f"{APP_URL}/poulailler/admin/updateAllPoulailler", headers=headers)
    assert response.status_code == 200, f"Failed to update all chickens: {response.text}"
    poulailler_après = response.json()
    print(f"Response JSON after update: {poulailler_après}")