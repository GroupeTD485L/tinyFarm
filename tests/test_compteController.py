import requests
import pytest
from datetime import datetime, date

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

def test_get_existing_compte(headers):
    """Test fetching the account information for the authenticated user."""
    response = requests.get(f"{APP_URL}/comptes/", headers=headers)

    assert response.status_code == 200, f"Failed to fetch the account information: {response.text}"

    account_data = response.json()
    print(account_data)
    expected_keys = {"derniereConnexion", "pseudo", "idCompte"}

    # Ensure the farm response contains the required fields
    assert expected_keys.issubset(account_data.keys()), f"Missing keys in response: {account_data.keys()}"

    print("✅ Test passed: Account information was successfully retrieved.")



def test_noAuth_noCompte():
    """Test checking that no account is created for a not authenticated user."""
    response = requests.post(f"{APP_URL}/comptes/")

    assert response.status_code in [401, 403], "❌ access not protected !"

    print("✅ Test passed: No authentification provides no account.")




def test_derniereConnexion(headers):
    """Test that the last connexion is now for the authenticated user."""
    response = requests.get(f"{APP_URL}/comptes/", headers=headers)

    assert response.status_code == 200, f"Failed to fetch the account information: {response.text}"

    account_data = response.json()
    print(account_data)

    assert "derniereConnexion" in account_data
    last_connexion = datetime.fromisoformat(account_data["derniereConnexion"])
    assert last_connexion.date() == date.today()

    print("✅ Test passed: last connexion date is today.")