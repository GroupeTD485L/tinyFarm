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

@pytest.fixture
def init_remise(headers):

    nom_produit = "Seringue"
    response = requests.post(f"{APP_URL}/remise",data=nom_produit, headers=headers)
    assert response.status_code == 200, f"Failed to add Seringue to remise: {response.text}"

    nom_produit = "Savon"
    response = requests.post(f"{APP_URL}/remise",data=nom_produit, headers=headers)
    assert response.status_code == 200, f"Failed to add Savon to remise: {response.text}"

    nom_produit = "Botte de foin"
    response = requests.post(f"{APP_URL}/remise",data=nom_produit, headers=headers)
    assert response.status_code == 200, f"Failed to add Botte de foi to remise: {response.text}"

    nom_produit = "Seau d'eau"
    response = requests.post(f"{APP_URL}/remise",data=nom_produit, headers=headers)
    assert response.status_code == 200, f"Failed to add Seau d'eau to remise: {response.text}"


#----------------------------------------------------------------------------------------------
def test_get_vache(headers,create_or_get_farm):
    response = requests.get(f"{APP_URL}/vache", headers=headers)
    assert response.status_code == 200, f"failed to fetch cow: {response.text}"
    vache_data = response.json()
    now = datetime.datetime.now()

    try:
        dernier_repas = parser.parse(vache_data["dernierRepas"])
        dernier_breuvage = parser.parse(vache_data["dernierBreuvage"])
        dernier_lavage = parser.parse(vache_data["dernierLavage"])
    except ValueError as e:
        assert False, f"Impossible de parser les dates: {e}"

    assert vache_data["age"] == 0
    assert vache_data["poids"] == 1
    assert vache_data["qt_lait"] == 0
    assert dernier_repas < now
    assert dernier_breuvage < now
    assert dernier_lavage < now
    assert vache_data["maladeDepuis"] is None
    expected_keys = {"poids","age","qt_lait","dernierRepas","dernierBreuvage","dernierLavage","maladeDepuis" }
    assert expected_keys.issubset(vache_data.keys()),f"missing keys in : {vache_data.keys()}"

    print("✅ Test passed: Cow was successfully retrieved.") 


#----------------------------------------------------------------------------------------------
def test_get_vache_no_header(create_or_get_farm):
    response = requests.get(f"{APP_URL}/vache")
    assert response.status_code == 401, f"failed to fetch cow: {response.text}"
    
    print("✅ Test passed: test successfully got denied") 


 #----------------------------------------------------------------------------------------------
def test_update_vache(headers):
    response1 = requests.get(f"{APP_URL}/vache", headers=headers)
    assert response1.status_code == 200, f"failed to fetch cow: {response1.text}"
    vache_data1 = response1.json()

    response2 = requests.put(f"{APP_URL}/vache", headers=headers)
    assert response2.status_code == 200, f"failed to fetch cow: {response2.text}"
    vache_data2 = response2.json()

    assert vache_data1["age"] == vache_data2["age"]-1 
    print("✅ Test passed: Cow was successfully updated.") 


 #----------------------------------------------------------------------------------------------
def test_update_vache_no_header():
    response1 = requests.get(f"{APP_URL}/vache")
    assert response1.status_code == 401, f"failed to fetch cow: {response1.text}"
    print("✅ Test passed: test successfully got denied") 


#----------------------------------------------------------------------------------------------
def test_soigner_vache(headers,init_remise):
    response = requests.put(f"{APP_URL}/vache/faireMalade", headers=headers)
    assert response.status_code == 200, f"failed to fetch cow: {response.text}"
    vache_data = response.json()

    assert vache_data["maladeDepuis"] is not None

    response = requests.put(f"{APP_URL}/vache/soigner", headers=headers)
    assert response.status_code == 200, f"failed to fetch cow: {response.text}"
    vache_data = response.json()
    assert vache_data["maladeDepuis"] is None

    print("✅ Test passed: Cow was successfully healed.") 


#----------------------------------------------------------------------------------------------
def test_soigner_vache_no_header(init_remise):
    response = requests.put(f"{APP_URL}/vache/faireMalade")
    assert response.status_code == 401, f"failed to fetch cow: {response.text}"

    response = requests.put(f"{APP_URL}/vache/soigner")
    assert response.status_code == 401, f"failed to fetch cow: {response.text}"

    print("✅ Test passed: test successfully got denied") 


#----------------------------------------------------------------------------------------------
def test_nourrir_vache(headers,init_remise):
    response1 = requests.get(f"{APP_URL}/vache" , headers=headers)
    assert response1.status_code == 200, f"failed to feed cow: {response1.text}"
    vache_data1 = response1.json()

    response2 = requests.put(f"{APP_URL}/vache/nourrir", data="Botte de foin" , headers=headers)
    assert response2.status_code == 200, f"failed to feed cow: {response2.text}"
    vache_data2 = response2.json()

    assert vache_data1["poids"] == vache_data2["poids"]-3
    try:
        dernier_repas = parser.parse(vache_data2["dernierRepas"])
    except ValueError as e:
        assert False, f"Impossible de parser les dates: {e}"
    
    date_hier = datetime.datetime.now() - datetime.timedelta(days=1)
    assert dernier_repas > date_hier
    print("✅ Test passed: Cow was successfully feed.")


#----------------------------------------------------------------------------------------------
def test_nourrir_vache_no_header(init_remise):
    response1 = requests.get(f"{APP_URL}/vache" )
    assert response1.status_code == 401, f"failed to feed cow: {response1.text}"

    response2 = requests.put(f"{APP_URL}/vache/nourrir", data="Botte de foin")
    assert response2.status_code == 401, f"failed to feed cow: {response2.text}"
    
    print("✅ Test passed: test successfully got denied")


#----------------------------------------------------------------------------------------------
def test_abreuver_vache(headers,init_remise):
    response = requests.put(f"{APP_URL}/vache/abreuver", headers=headers)
    assert response.status_code == 200, f"failed to drink cow: {response.text}"
    vache_data = response.json()

    try:
        dernier_breuvage = parser.parse(vache_data["dernierBreuvage"])
    except ValueError as e:
        assert False, f"Impossible de parser les dates: {e}"
    
    date_hier = datetime.datetime.now() - datetime.timedelta(days=1)
    assert dernier_breuvage > date_hier
    print("✅ Test passed: Cow successfully drank.")


#----------------------------------------------------------------------------------------------
def test_abreuver_vache_no_header(init_remise):
    response = requests.put(f"{APP_URL}/vache/abreuver")
    assert response.status_code == 401, f"failed to drink cow: {response.text}"

    print("✅ Test passed: test successfully got denied")


#----------------------------------------------------------------------------------------------
def test_laver_vache(headers,init_remise):
    response = requests.put(f"{APP_URL}/vache/laver", headers=headers)
    assert response.status_code == 200, f"failed to wash cow: {response.text}"
    vache_data = response.json()

    try:
        dernier_lavage = parser.parse(vache_data["dernierLavage"])
    except ValueError as e:
        assert False, f"Impossible de parser les dates: {e}"
    
    date_hier = datetime.datetime.now() - datetime.timedelta(days=1)
    assert dernier_lavage > date_hier
    print("✅ Test passed: Cow successfully washed.")


#----------------------------------------------------------------------------------------------
def test_laver_vache_no_header(init_remise):
    response = requests.put(f"{APP_URL}/vache/laver")
    assert response.status_code == 401, f"failed to wash cow: {response.text}"
    
    print("✅ Test passed: test successfully got denied")


#----------------------------------------------------------------------------------------------
def test_update_vache_mourrir_vache(headers):
    response1 = requests.put(f"{APP_URL}/vache/faireMalade", headers=headers)
    assert response1.status_code == 200, f"failed to make the cow sick: {response1.text}"

    response2 = requests.put(f"{APP_URL}/vache", headers=headers)
    assert response2.status_code == 404, f"vache shouldn't be alive: {response2.text}"

    print("✅ Test passed: Cow successfully died.")


#----------------------------------------------------------------------------------------------
def test_update_vache_mourrir_vache_no_header():
    response1 = requests.put(f"{APP_URL}/vache/faireMalade")
    assert response1.status_code == 401, f"failed to make the cow sick: {response1.text}"

    response2 = requests.put(f"{APP_URL}/vache")
    assert response2.status_code == 401, f"vache shouldn't be alive: {response2.text}"

    print("✅ Test passed: test successfully got denied")


#----------------------------------------------------------------------------------------------
