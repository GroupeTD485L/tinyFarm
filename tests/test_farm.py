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

def test_create_or_get_farm(headers):
    """Test fetching or creating a farm for the authenticated user."""
    response = requests.get(f"{APP_URL}/farm", headers=headers)
    assert response.status_code == 200, f"Failed to fetch/create farm: {response.text}"

    farm_data = response.json()
    expected_keys = {"username", "name", "location"}

    # Ensure the farm response contains the required fields
    assert expected_keys.issubset(farm_data.keys()), f"Missing keys in response: {farm_data.keys()}"

    print("✅ Test passed: Farm was successfully retrieved or created.")
