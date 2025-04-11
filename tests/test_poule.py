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
    products = ["Graine","Seau d'eau", "Seringue", "Savon"]
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
def test_verification_get_poulailler(headers, create_or_get_farm):
    response = requests.get(f"{APP_URL}/poulailler?page=0&size=5", headers=headers)
    assert response.status_code == 200, f"Failed to fetch chickens: {response.text}"
    poulailler = response.json()
    print(f"Response JSON: {poulailler}")

    # Vérifier qu'il y a au moins une poule
    assert len(poulailler['content']) > 0, "No chickens available to update."

"""Test globale sur les poules"""
def test_get_poules(headers,create_or_get_farm):
    response = requests.get(f"{APP_URL}/poulailler", headers=headers)
    assert response.status_code == 200, f"failed to fetch chicken: {response.text}"
    poule_data = response.json()
    print(f"Response JSON: {poule_data}")  # Ajouté pour vérifier la structure de la réponse

    now = datetime.datetime.now()
    # Vérifier que les champs de dates sont parsables
    for poule in poule_data['content']:
        try:
            dernier_repas = parser.parse(poule["dernierRepas"])
            dernier_breuvage = parser.parse(poule["dernierBreuvage"])
            dernier_lavage = parser.parse(poule["dernierLavage"])
        except KeyError as e:
            assert False, f"Key {e} is missing from the response JSON"
        except Exception as e:
            assert False, f"Error parsing date: {e}"

        # Effectuer des vérifications supplémentaires sur les dates si nécessaire
        assert dernier_repas < now
        assert dernier_breuvage < now 
        assert dernier_lavage < now

        assert poule["age"] >= 0
        assert poule["poids"] >= 0.05
        assert poule["nbOeuf"] >= 0
        expected_keys = {"poids","age","sexe","dernierRepas","dernierBreuvage","dernierLavage","maladeDepuis" }
        assert expected_keys.issubset(poule.keys()),f"missing keys in : {poule.keys()}"

        print("✅ Test passed: Chicken were successfully retrieved.") 

""" test pour s'assurer que chaque catégorie de poule ( poussin, poule et coq) est bien configuré"""
def test_bonne_configuration_poules(headers,create_or_get_farm):
    response = requests.get(f"{APP_URL}/poulailler", headers=headers)
    assert response.status_code == 200, f"failed to fetch chicken: {response.text}"
    poule_data = response.json()
    print(f"Response JSON: {poule_data}")  # Ajouté pour vérifier la structure de la réponse

    now = datetime.datetime.now()
    # Vérifier que les champs de dates sont parsables
    for poule in poule_data['content']:
        try:
            dernier_repas = parser.parse(poule["dernierRepas"])
            dernier_breuvage = parser.parse(poule["dernierBreuvage"])
            dernier_lavage = parser.parse(poule["dernierLavage"])
        except KeyError as e:
            assert False, f"Key {e} is missing from the response JSON"
        except Exception as e:
            assert False, f"Error parsing date: {e}"
        if poule["sexe"] == "U":
            assert poule["age"] >= 0 and poule["age"] <= 4
            assert poule["poids"] >= 0.05 and poule["poids"] < 2.5
            assert poule["nbOeuf"] == 0
        if poule["sexe"] == "F":
            assert poule["age"] >= 5
            assert poule["poids"] >= 1.5 and poule["poids"] <= 3.5 # la poule explose sinon, le poids peut être inferieur à 2.5 si elle n'a pas été nourrie
            assert poule["nbOeuf"] >= 0 # une poule peut pondre des oeufs
        if poule["sexe"] == "M":
            assert poule["age"] >= 5
            assert poule["poids"] >= 1.5 and poule["poids"] <= 3.5 # la poule explose sinon, le poids peut être inferieur à 2.5 si il n'a pas été nourri
            assert poule["nbOeuf"] == 0 # un coq ne peut pas pondre d'oeuf

@pytest.mark.usefixtures("init_remise")
def test_abreuver_poule(headers, init_remise):
    # Récupérer la liste des poules
    response1 = requests.get(f"{APP_URL}/poulailler/poules", headers=headers)
    assert response1.status_code == 200, f"Failed to fetch chickens: {response1.text}"
    poule_data1 = response1.json()
    print(f"Initial Response JSON: {poule_data1}")

    # Vérifier qu'il y a au moins une poule
    assert len(poule_data1['content']) > 0, "No chickens available to watered."

    # Sélectionner une poule spécifique (par exemple, la première)
    poule_id = poule_data1['content'][0]['idPoule']
    poule_before = poule_data1['content'][0]

    # Nourrir la poule sélectionnée
    response2 = requests.put(f"{APP_URL}/poulailler/{poule_id}/abreuver", data="Seau d'eau", headers=headers)
    assert response2.status_code == 200, f"Failed to watered chicken with ID {poule_id}: {response2.text}"
    poule_after = response2.json()
    print(f"Updated Response JSON: {poule_after}")

    # Vérifier que le poids a augmenté ou est resté le même
    assert poule_after["poids"] >= poule_before["poids"], "Weight did not increase as expected."

    # Vérifier que la date du dernier breuvage a été mise à jour
    try:
        dernier_breuvage = parser.parse(poule_after["dernierBreuvage"])
    except ValueError as e:
        assert False, f"Failed to parse 'dernierBreuvage': {e}"

    date_hier = datetime.datetime.now() - datetime.timedelta(days=1)
    assert dernier_breuvage > date_hier

    print("✅ Test passed: Chicken was successfully watered and updated.")

@pytest.mark.usefixtures("init_remise")
def test_laver_poule(headers, init_remise):
    # Récupérer la liste des poules
    response1 = requests.get(f"{APP_URL}/poulailler/poules", headers=headers)
    assert response1.status_code == 200, f"Failed to fetch chickens: {response1.text}"
    poule_data1 = response1.json()
    print(f"Initial Response JSON: {poule_data1}")

    # Vérifier qu'il y a au moins une poule
    assert len(poule_data1['content']) > 0, "No chickens available to washed."

    # Sélectionner une poule spécifique (par exemple, la première)
    poule_id = poule_data1['content'][0]['idPoule']
    poule_before = poule_data1['content'][0]

    # Nourrir la poule sélectionnée
    response2 = requests.put(f"{APP_URL}/poulailler/{poule_id}/laver", data="Savon", headers=headers)
    assert response2.status_code == 200, f"Failed to washed chicken with ID {poule_id}: {response2.text}"
    poule_after = response2.json()
    print(f"Updated Response JSON: {poule_after}")

    # Vérifier que la date du dernier lavage a été mise à jour
    try:
        dernier_lavage = parser.parse(poule_after["dernierLavage"])
    except ValueError as e:
        assert False, f"Failed to parse 'dernierLavage': {e}"

    date_hier = datetime.datetime.now() - datetime.timedelta(days=1)
    assert dernier_lavage > date_hier

    print("✅ Test passed: Chicken was successfully washed and updated.")

"""Test pour nourrir une poule, le test est ignoré si la poule a déjà été nourrie aujourd'hui"""
# il faudrait une méthode pour récupérer l'argent du fermier 
@pytest.mark.usefixtures("init_remise")
def test_nourrir_poule(headers, init_remise, create_or_get_farm):
    # Récupérer la liste des poules
    response1 = requests.get(f"{APP_URL}/poulailler/poules", headers=headers)
    assert response1.status_code == 200, f"Failed to fetch chickens: {response1.text}"
    poule_data1 = response1.json()
    print(f"Initial Response JSON: {poule_data1}")

    # Vérifier qu'il y a au moins une poule
    assert len(poule_data1['content']) > 0, "No chickens available to feed."

    # Sélectionner une poule spécifique (par exemple, la première)
    poule_id = poule_data1['content'][0]['idPoule']
    poule_before = poule_data1['content'][0]
    
    # Vérifier que la poule n'a pas été nourrie récemment
    try:
        dernier_repas = parser.parse(poule_before["dernierRepas"])
    except ValueError as e:
        assert False, f"Failed to parse 'dernierRepas': {e}"
    date_aujourdhui = datetime.datetime.now()
    # Vérifier si le dernier repas date d'aujourd'hui
    meme_jour = (
        dernier_repas.year == date_aujourdhui.year and 
        dernier_repas.month == date_aujourdhui.month and 
        dernier_repas.day == date_aujourdhui.day
    )
    # Si la poule a déjà été nourrie aujourd'hui, ne pas continuer le test
    if meme_jour:
        print("La poule a déjà été nourrie aujourd'hui, test ignoré.")
        pytest.skip("La poule a déjà été nourrie aujourd'hui")
    else:
        print("La poule n'a pas été nourrie aujourd'hui, on peut continuer le test.")
        print("La poule n'a pas été nourrie récemment et son poids est supérieur à 0.")
        # Nourrir la poule sélectionnée
        response2 = requests.put(f"{APP_URL}/poulailler/{poule_id}/nourrir", data="Graine", headers=headers)
        assert response2.status_code == 200, f"Failed to feed chicken with ID {poule_id}: {response2.text}"
        poule_after = response2.json()
        print(f"Updated Response JSON: {poule_after}")

        # Vérifier que le poids a augmenté
        assert poule_before["poids"] == poule_after["poids"] - 0.5, "Weight did not increase as expected."

        # Vérifier que la date du dernier repas a été mise à jour
        try:
            dernier_repas = parser.parse(poule_after["dernierRepas"])
        except ValueError as e:
            assert False, f"Failed to parse 'dernierRepas': {e}"

        date_hier = datetime.datetime.now() - datetime.timedelta(days=1)
        assert dernier_repas > date_hier

    print("✅ Test passed: Chicken was successfully fed and updated.")

@pytest.mark.usefixtures("init_remise")
def test_soigner_poule(headers, init_remise):
    # Récupérer la liste des poules
    response1 = requests.get(f"{APP_URL}/poulailler/poules", headers=headers)
    assert response1.status_code == 200, f"Failed to fetch chickens: {response1.text}"
    poule_data1 = response1.json()
    print(f"Initial Response JSON: {poule_data1}")

    # Vérifier qu'il y a au moins une poule
    assert len(poule_data1['content']) > 0, "No chickens available to cure."

    # Sélectionner une poule spécifique (par exemple, la première)
    poule_id = poule_data1['content'][0]['idPoule']

    # Rendre la poule malade (si elle ne l'est pas déjà)
    response_make_sick = requests.put(f"{APP_URL}/poulailler/{poule_id}/rendreMalade", headers=headers)
    assert response_make_sick.status_code == 200, f"Failed to make chicken sick: {response_make_sick.text}"

    # Vérifier que la poule est maintenant malade
    response_check = requests.get(f"{APP_URL}/poulailler/{poule_id}", headers=headers)
    assert response_check.status_code == 200, f"Failed to fetch chicken: {response_check.text}"
    poule_before = response_check.json()
    assert poule_before["maladeDepuis"] is not None, "The chicken is not sick and cannot be cured."

    # Soigner la poule sélectionnée
    response2 = requests.put(f"{APP_URL}/poulailler/{poule_id}/soigner", data="Seringue", headers=headers)
    assert response2.status_code == 200, f"Failed to cure chicken with ID {poule_id}: {response2.text}"
    poule_after = response2.json()
    print(f"Updated Response JSON: {poule_after}")

    # Vérifier que maladeDepuis est mis à null
    assert poule_after["maladeDepuis"] is None, "Chicken was not cured successfully."

    print("✅ Test passed: Chicken was successfully cured and updated.")


@pytest.mark.usefixtures("headers")
def test_evolution_possible_poulailler_admin(headers):
    
    # Récupérer l'état du poulailler avant la mise à jour
    response1 = requests.get(f"{APP_URL}/poulailler", headers=headers)
    assert response1.status_code == 200, f"Failed to fetch chickens before update: {response1.text}"
    poulailler_avant = response1.json()
    print(f"Response JSON before update: {poulailler_avant}")
    
    response = requests.put(f"{APP_URL}/poulailler/admin/updateAllPoulailler", headers=headers)
    assert response.status_code == 200, f"Failed to update all chickens: {response.text}"

    response2 = requests.get(f"{APP_URL}/poulailler", headers=headers)
    assert response2.status_code == 200, f"Failed to fetch chickens before update: {response2.text}"
    poulailler_après = response2.json()
    print(f"Response JSON before update: {poulailler_avant}")
    print(f"Response JSON after update: {poulailler_après}")

@pytest.fixture
def run_evolution_admin(headers):
    
    # Récupérer l'état du poulailler avant la mise à jour
    response1 = requests.get(f"{APP_URL}/poulailler", headers=headers)
    assert response1.status_code == 200, f"Failed to fetch chickens before update: {response1.text}"
    poulailler_avant = response1.json()
    print(f"Response JSON before update: {poulailler_avant}")
    
    response = requests.put(f"{APP_URL}/poulailler/admin/updateAllPoulailler", headers=headers)
    assert response.status_code == 200, f"Failed to update all chickens: {response.text}"

    response2 = requests.get(f"{APP_URL}/poulailler", headers=headers)
    assert response2.status_code == 200, f"Failed to fetch chickens before update: {response2.text}"
    poulailler_après = response2.json()
    print(f"Response JSON before update: {poulailler_avant}")
    print(f"Response JSON after update: {poulailler_après}")

    # Retourner les deux états pour comparaison
    return {"avant": poulailler_avant, "après": poulailler_après}




@pytest.mark.usefixtures("headers")
def test_update_poulailler(headers, run_evolution_admin):
    """Test de mise à jour du poulailler qui dépend de la mise à jour administrative"""
    # Utiliser les données de la mise à jour administrative
    poulailler_avant = run_evolution_admin["avant"]
    poulailler_après_admin = run_evolution_admin["après"]
    
    print(f"Response JSON avant admin: {poulailler_avant}")
    print(f"Response JSON après admin: {poulailler_après_admin}")
    
    # Vérifier qu'il y a au moins une poule
    assert len(poulailler_avant['content']) > 0, "No chickens available to update."
    
    # Effectuer la mise à jour normale du poulailler
    response2 = requests.put(f"{APP_URL}/poulailler", headers=headers)
    assert response2.status_code == 200, f"Failed to update all chicken: {response2.text}"
    poulailler_après = response2.json()
    print(f"Response JSON après update normal: {poulailler_après}")
    
    # Créer un dictionnaire pour faciliter la recherche par idPoule
    poules_après = {poule["idPoule"]: poule for poule in poulailler_après['content']}
    
    for poule in poulailler_avant['content']:
        try:
            dernier_repas = parser.parse(poule["dernierRepas"])
            dernier_breuvage = parser.parse(poule["dernierBreuvage"])
            dernier_lavage = parser.parse(poule["dernierLavage"])
        except KeyError as e:
            assert False, f"Key {e} is missing from the response JSON"
        except Exception as e:
            assert False, f"Error parsing date: {e}"
        
        # Vérifier si cette poule existe toujours après la mise à jour
        if poule["idPoule"] in poules_après:
            poule_après = poules_après[poule["idPoule"]]
            
            # On vérifie les conditions requises pour mise à jour
            date_aujourdhui = datetime.datetime.now() 
            dernier_repas = dernier_repas.date() == date_aujourdhui.date()
            dernier_breuvage = dernier_breuvage.date() == date_aujourdhui.date()
            dernier_lavage = dernier_lavage.date() == date_aujourdhui.date()
            
            if dernier_repas and dernier_breuvage and dernier_lavage and poule["maladeDepuis"] is None:
                # évolution du poussin
                if poule["sexe"] == "U":
                    if poule["age"] >= 4 and poule["poids"] >= 2.5:
                        assert poule_après["age"] >= 5
                        assert poule_après["poids"] >= 2.5 and poule_après["poids"] <= 3.5
                        assert poule_après["nbOeuf"] == 0
                        assert poule_après["sexe"] in ["F", "M"]
                    if poule["age"] >= 4 and poule["poids"] < 2.5:
                        assert poule_après["age"] >= 5
                        assert poule_après["poids"] >= 0.05 and poule_après["poids"] < 2.5
                        assert poule_après["nbOeuf"] == 0
                        assert poule_après["sexe"] == "U"
                    if poule["age"] < 4 and poule["poids"] >= 2.5:
                        assert poule_après["age"] < 5
                        assert poule_après["poids"] >= 2.5 and poule_après["poids"] <= 3.5
                        assert poule_après["nbOeuf"] == 0
                        assert poule_après["sexe"] == "U"
                    if poule["age"] < 4 and poule["poids"] < 2.5:
                        assert poule_après["age"] < 5
                        assert poule_après["poids"] >= 0.05 and poule_après["poids"] < 2.5
                        assert poule_après["nbOeuf"] == 0
                        assert poule_après["sexe"] == "U"
                if poule["sexe"] == "F":
                    assert poule_après["age"] >= 5
                    assert poule_après["poids"] >= 2.5 and poule_après["poids"] <= 3.5
                    assert poule_après["nbOeuf"] >= 0
                    assert poule_après["sexe"] == "F"
                if poule["sexe"] == "M":
                    assert poule_après["age"] >= 5
                    assert poule_après["poids"] >= 2.5 and poule_après["poids"] <= 3.5
                    assert poule_après["nbOeuf"] == 0
                    assert poule_après["sexe"] == "M"

    print("✅ Test passed: Chicken was successfully updated.")


@pytest.mark.usefixtures("headers")
def test_verification_conditions_update(headers):
    response = requests.get(f"{APP_URL}/poulailler", headers=headers)
    assert response.status_code == 200, f"Failed to fetch chickens: {response.text}"
    poulailler = response.json()

    date_hier = datetime.datetime.now() - datetime.timedelta(days=1)
    for poule in poulailler['content']:
        if poule["dernierRepas"] == date_hier and poule["dernierBreuvage"] == date_hier and poule["dernierLavage"] == date_hier and poule["maladeDepuis"] is None:
            print(f"Poule {poule['idPoule']} meets update conditions.")