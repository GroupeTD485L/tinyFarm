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

def test_get_classement(headers):
    """Test fetching or creating a farm for the authenticated user."""
    response = requests.get(f"{APP_URL}/classement?page=0&size=5", headers=headers)
    assert response.status_code == 200, f"Failed to fetch classement: {response.text}"

    classement_data = response.json()
    print(classement_data)
    expected_keys = {"content", "pageable", "totalPages", "totalElements", "last", "size", "number", "sort", "numberOfElements", "first", "empty"}

    # Ensure the farm response contains the required fields
    assert expected_keys.issubset(classement_data.keys()), f"Missing keys in response: {classement_data.keys()}"

    print("✅ Test passed: Classement was successfully retrieved.")


def test_get_classement():
    """Test fetching or creating a farm for the authenticated user."""
    response = requests.get(f"{APP_URL}/classement?page=0&size=5")
    assert response.status_code == 401, f"Managed to do something with : {response.text}"

    print("✅ Test passed: Classement was not successfully retrieved.")


def test_has_farms(headers):
    """Test fetching or creating a farm for the authenticated user."""
    responseA = requests.get(f"{APP_URL}/ferme/", headers=headers)
    assert responseA.status_code == 200, f"Failed to fetch/create farm: {response.text}"
    responseB = requests.get(f"{APP_URL}/classement?page=0&size=5", headers=headers)
    assert responseB.status_code == 200, f"Failed to fetch classement: {response.text}"


    classement_data = responseB.json()
    ferme_data = responseA.json()
    print(classement_data)

    # Ensure the farm response contains the required fields
    assert "content" in classement_data
    assert classement_data["content"] != []

    print("✅ Test passed: Classement was successfully retrieved.")