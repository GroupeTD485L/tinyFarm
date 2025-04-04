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
 
 
#----------------------------------------------------------------------------------------------
def test_info_remise(headers,create_or_get_farm, init_remise):
    response = requests.get(f"{APP_URL}/remise" ,headers=headers)
    assert response.status_code == 200, f"failed to fetch remise: {response.text}"
    remise_data = response.json()
    counter = 1
    for remise in remise_data:

        if counter == 1:
            assert remise["idProduit"]["nom"] == "Seringue"
            counter = 2
        else:
            assert remise["idProduit"]["nom"] == "Savon"

        assert remise["quantite"] == 1

    print("✅ Test passed: info remise was successfull.") 


#----------------------------------------------------------------------------------------------
def test_info_remise_no_header(create_or_get_farm):
    response = requests.get(f"{APP_URL}/remise")
    assert response.status_code == 401, f"failed to fetch remise: {response.text}"
    
    print("✅ Test passed: test successfully got denied.")


#----------------------------------------------------------------------------------------------
def test_info_produit(headers,create_or_get_farm):
    response = requests.get(f"{APP_URL}/remise/Savon",headers=headers)
    assert response.status_code == 200, f"failed to fetch remise: {response.text}"
    remise_data = response.json()

    assert remise_data["idProduit"]["nom"] == "Savon"
    assert remise_data["quantite"] == 1

    response = requests.get(f"{APP_URL}/remise/Seringue",headers=headers)
    assert response.status_code == 200, f"failed to fetch remise: {response.text}"
    remise_data = response.json()

    assert remise_data["idProduit"]["nom"] == "Seringue"
    assert remise_data["quantite"] == 1

    print("✅ Test passed: info remise was successfull.") 


#----------------------------------------------------------------------------------------------
def test_info_produit_no_header(create_or_get_farm):
    response = requests.get(f"{APP_URL}/remise/Savon")
    assert response.status_code == 401, f"failed to fetch remise: {response.text}"
    
    response = requests.get(f"{APP_URL}/remise/Seringue")
    assert response.status_code == 401, f"failed to fetch remise: {response.text}"
   
    print("✅ Test passed: test successfully got denied.")


#----------------------------------------------------------------------------------------------
def test_info_produit_pas_existant(headers,create_or_get_farm):
    response = requests.get(f"{APP_URL}/remise/Essaie",headers=headers)
    assert response.status_code == 500, f"failed to fetch remise: {response.text}"
    #produit inexistant throw exception dans produit service

    response = requests.get(f"{APP_URL}/remise/Seau d'eau",headers=headers)
    assert response.status_code == 404, f"failed to fetch remise: {response.text}"
    #pas de remise avec ce produit dans le proprietaire donc not found

    print("✅ Test passed: info remise was successfull.") 


#----------------------------------------------------------------------------------------------
def test_info_produit_pas_existant_no_header(create_or_get_farm):
    response = requests.get(f"{APP_URL}/remise/Essaie")
    assert response.status_code == 401, f"failed to fetch remise: {response.text}"

    response = requests.get(f"{APP_URL}/remise/Seau d'eau")
    assert response.status_code == 401, f"failed to fetch remise: {response.text}"

    print("✅ Test passed: test successfully got denied.") 



#----------------------------------------------------------------------------------------------
def test_add_remise(headers,create_or_get_farm):
    response = requests.post(f"{APP_URL}/remise", data="Seau d'eau" ,headers=headers)
    assert response.status_code == 200, f"failed to fetch remise: {response.text}"
    remise_data = response.json()
    assert remise_data["quantite"] == 1
    produit = remise_data.get("idProduit", {}) 
    nom_produit = produit.get("nom", "")
    assert nom_produit == "Seau d'eau"

    print("✅ Test passed: add remise was successfull.") 


#----------------------------------------------------------------------------------------------
def test_add_remise_no_header(create_or_get_farm):
    response = requests.post(f"{APP_URL}/remise", data="Seau d'eau")
    assert response.status_code == 401, f"failed to fetch remise: {response.text}"

    print("✅ Test passed: test successfully got denied.") 


 #----------------------------------------------------------------------------------------------
def test_update_produit(headers,create_or_get_farm):
    response = requests.put(f"{APP_URL}/remise", json = { "nomProduit": "Seau d'eau", "quantite": 10 } ,headers=headers)
    assert response.status_code == 200, f"failed to fetch remise: {response.text}"
    remise_data = response.json()

    assert remise_data["quantite"] == 10
    produit = remise_data.get("idProduit", {}) 
    nom_produit = produit.get("nom", "")
    assert nom_produit == "Seau d'eau"

    print("✅ Test passed: add remise was successfull.") 


#----------------------------------------------------------------------------------------------
def test_update_produit_no_header(create_or_get_farm):
    response = requests.put(f"{APP_URL}/remise", json = { "nomProduit": "Seau d'eau", "quantite": 10 })
    assert response.status_code == 401, f"failed to fetch remise: {response.text}"
   
    print("✅ Test passed: test successfully got denied.") 