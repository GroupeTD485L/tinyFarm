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

    farm_data = response.json()
    #print(farm_data)
    expected_keys = {"idFerme", "compte", "remise", "classement", "poules", "vache", "clapier", "nom", "ecus", "enHibernation", "achatRestant", "dernierAchat"}

    # Ensure the farm response contains the required fields
    assert expected_keys.issubset(farm_data.keys()), f"Missing keys in response: {farm_data.keys()}"

    print("✅ Test passed: Farm was successfully retrieved or created.")


def test_create_or_get_farms():
    """Test fetching or creating a farm for the authenticated user."""
    response = requests.get(f"{APP_URL}/ferme/")
    assert response.status_code == 401, f"Failed to fetch/create farm: {response.text}"
    # Ensure the farm response contains the required fields
    # assert expected_keys.issubset(farm_data.keys()), f"Missing keys in response: {farm_data.keys()}"

    print("✅ Test passed: Farm was successfully retrieved or created.")

def test_get_farm_admin(headers):
    """Test fetching a farm as admin"""
    response = requests.get(f"{APP_URL}/ferme/", headers=headers)
    assert response.status_code == 200
    response = requests.get(f"{APP_URL}/ferme/admin/getFerme", headers=headers)
    assert response.status_code == 200
    
    farm_data = response.json()
    expected_keys = {"idFerme", "compte", "remise", "classement", "poules", "vache", "clapier", "nom", "ecus", "enHibernation", "achatRestant", "dernierAchat"}
    assert expected_keys.issubset(farm_data.keys()), f"Missing keys in response: {farm_data.keys()}"


def test_delete_farms(headers):
    """Test the deletion of a farm for the authenticated user."""
    response = requests.get(f"{APP_URL}/ferme/", headers=headers)
    assert response.status_code == 200

    response = requests.delete(f"{APP_URL}/ferme/", headers=headers)
    assert response.status_code == 200
    response = requests.get(f"{APP_URL}/ferme/admin/getFerme", headers=headers)
    assert response.status_code == 404

    response = requests.delete(f"{APP_URL}/ferme/", headers=headers)
    assert response.status_code == 404