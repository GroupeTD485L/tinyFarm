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
    # Need to create a farm in order to get the account
    response = requests.get(f"{APP_URL}/ferme/", headers=headers)
    assert response.status_code == 200, f"Failed to fetch the farm: {response.text}"

    response = requests.get(f"{APP_URL}/comptes/", headers=headers)
    assert response.status_code == 200, f"Failed to fetch the account information: {response.text}"

    account_data = response.json()
    print(account_data)
    expected_keys = {"derniereConnexion", "pseudo", "idCompte"}

    # Ensure the farm response contains the required fields
    assert expected_keys.issubset(account_data.keys()), f"Missing keys in response: {account_data.keys()}"

    # Need to delete the farm
    response = requests.delete(f"{APP_URL}/ferme/", headers=headers)
    assert response.status_code == 200, f"Failed to delete the farm: {response.text}"

    print("✅ Test passed: Account information was successfully retrieved.")



def test_noAuth_noCompte():
    """Test checking that no account is created for a not authenticated user."""
    response = requests.post(f"{APP_URL}/comptes/")

    assert response.status_code in [401, 403], "❌ access not protected !"

    print("✅ Test passed: No authentification provides no account.")




def test_derniereConnexion(headers):
    """Test that the last connexion is now for the authenticated user."""
    # Need to create a farm in order to get the account
    response = requests.get(f"{APP_URL}/ferme/", headers=headers)
    assert response.status_code == 200, f"Failed to fetch the farm: {response.text}"

    response = requests.get(f"{APP_URL}/comptes/", headers=headers)
    assert response.status_code == 200, f"Failed to fetch the account information: {response.text}"

    account_data = response.json()
    print(account_data)

    assert "derniereConnexion" in account_data
    last_connexion = datetime.fromisoformat(account_data["derniereConnexion"])
    assert last_connexion.date() == date.today()

    # Need to delete the farm
    response = requests.delete(f"{APP_URL}/ferme/", headers=headers)
    assert response.status_code == 200, f"Failed to delete the farm: {response.text}"

    print("✅ Test passed: last connexion date is today.")


def test_deleted_compte(headers):
    """Test that a deleted account is no longer reachable."""
     # Need to create a farm in order to get the account
    response = requests.get(f"{APP_URL}/ferme/", headers=headers)
    assert response.status_code == 200, f"Failed to fetch the farm: {response.text}"

    response = requests.delete(f"{APP_URL}/ferme/", headers=headers)
    # 200 is OK, 204 is No content
    assert response.status_code in [200, 204], f"Failed to delete the account: {response.text}"


    response = requests.get(f"{APP_URL}/comptes/", headers=headers)

    assert response.status_code == 404, f"Expected 404 after deletion, but got {response.status_code}:  {response.text}"

    print("✅ Test passed: The account was successfully deleted and cannot be accessed.")


def test_updated_compte(headers):
    """Test that an account is updated"""
     # Need to create a farm in order to get the account
    response = requests.get(f"{APP_URL}/ferme/", headers=headers)
    assert response.status_code == 200, f"Failed to fetch the farm: {response.text}"


    # Fetch account before update
    responseBeforePut = requests.get(f"{APP_URL}/comptes/", headers=headers)
    assert responseBeforePut.status_code == 200, f"Failed to fetch the account: {response.text}"

    account_dataBeforePut = responseBeforePut.json()
    print(account_dataBeforePut)

    assert "derniereConnexion" in account_dataBeforePut
    last_connexion_before = datetime.fromisoformat(account_dataBeforePut["derniereConnexion"])



    # Update
    response = requests.put(f"{APP_URL}/comptes/", headers=headers)
    assert response.status_code == 200, f"Failed to update the account: {response.text}"



    # Fetch account after update
    responseAfterPut = requests.get(f"{APP_URL}/comptes/", headers=headers)
    assert responseAfterPut.status_code == 200, f"Failed to fetch the account: {response.text}"

    account_dataAfterPut = responseAfterPut.json()
    print(account_dataAfterPut)

    assert "derniereConnexion" in account_dataAfterPut
    last_connexion_after = datetime.fromisoformat(account_dataAfterPut["derniereConnexion"])

    # Compare full timestamps
    assert last_connexion_after > last_connexion_before, (
        f"Expected derniereConnexion to be updated. Before: {last_connexion_before}, After: {last_connexion_after}"
    )


    # Need to delete the farm
    response = requests.delete(f"{APP_URL}/ferme/", headers=headers)
    assert response.status_code == 200, f"Failed to delete the farm: {response.text}"

    print("✅ Test passed: The account was successfully deleted and cannot be accessed.")
