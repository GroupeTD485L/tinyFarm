import requests
import pytest

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

def test_get_info_compte(headers):
    """Test fetching the account information for the authenticated user."""
    response = requests.get(f"{APP_URL}/comptes/", headers=headers)

    assert response.status_code == 200, f"Failed to fetch the account information: {response.text}"

    farm_data = response.json()
    print(farm_data)
    expected_keys = {"derniereConnexion", "pseudo", "idCompte"}

    # Ensure the farm response contains the required fields
    assert expected_keys.issubset(farm_data.keys()), f"Missing keys in response: {farm_data.keys()}"

    print("✅ Test passed: Account information was successfully retrieved.")