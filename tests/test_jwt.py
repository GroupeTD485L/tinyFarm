import requests
import pytest

# URL de ton application Spring Boot
APP_URL = "http://localhost:8080"


def get_test_jwt():
    """Récupère un token JWT de test depuis l'API"""
    response = requests.get(f"{APP_URL}/auth/test-token")

    assert response.status_code == 200, f"❌ Impossible d'obtenir un token : {response.text}"
    return response.text  # 🔥 Retourne le token JWT


def test_admin_access_with_valid_token():
    """Teste l'accès à /admin avec un token JWT valide"""
    
    jwt_token = get_test_jwt()  # 🔥 Récupère un token JWT

    headers = {
        "Authorization": f"Bearer {jwt_token}",  # 🔥 Envoie le token dans l'authentification
        "Accept": "application/json"
    }
    
    response = requests.get(f"{APP_URL}/admin", headers=headers)  # 🔥 Teste l'endpoint protégé

    print(f"🔍 DEBUG: Status = {response.status_code}")
    print(f"🔍 DEBUG: Body = {response.text}")

    assert response.status_code == 200, f"❌ Accès refusé : {response.status_code}"


def test_admin_access_without_token():
    """Teste que l'accès à /admin sans token est refusé (401 Unauthorized)"""
    
    response = requests.get(f"{APP_URL}/admin")

    print(f"🔍 DEBUG: Status = {response.status_code}")
    print(f"🔍 DEBUG: Body = {response.text}")

    assert response.status_code == 401, "❌ L'accès à /admin aurait dû être refusé sans token !"


def test_admin_access_with_invalid_token():
    """Teste que l'accès à /admin avec un token invalide est refusé (403 Forbidden)"""
    
    headers = {
        "Authorization": "Bearer faketoken123456",  # 🔥 Token invalide
        "Accept": "application/json"
    }
    
    response = requests.get(f"{APP_URL}/admin", headers=headers)

    print(f"🔍 DEBUG: Status = {response.status_code}")
    print(f"🔍 DEBUG: Body = {response.text}")

    assert response.status_code in [401, 403], "❌ L'accès aurait dû être refusé avec un token invalide !"


def test_counter_access_with_invalid_token():
    """Teste que l'accès à /admin avec un token invalide est refusé (403 Forbidden)"""
    
    response = requests.get(f"{APP_URL}/counter")

    assert response.status_code in [401, 403], "❌ access not protected !"

def test_increment_access_with_invalid_token():
    """Teste que l'accès à /admin avec un token invalide est refusé (403 Forbidden)"""
    
    response = requests.post(f"{APP_URL}/counter/increment")

    assert response.status_code in [401, 403], "❌ access not protected !"

def test_increment_access_with_valid_token():
    """Teste que l'accès à /admin avec un token invalide est refusé (403 Forbidden)"""
    
    jwt_token = get_test_jwt()  # 🔥 Récupère un token JWT

    headers = {
        "Authorization": f"Bearer {jwt_token}",  # 🔥 Envoie le token dans l'authentification
        "Accept": "application/json"
    }

    response = requests.post(f"{APP_URL}/counter/increment",headers=headers)

    assert response.status_code == 200, "❌ access refused  !"


def test_user_access_with_valid_token():
    """Teste l'accès à /admin avec un token JWT valide"""
    
    jwt_token = get_test_jwt()  # 🔥 Récupère un token JWT

    headers = {
        "Authorization": f"Bearer {jwt_token}",  # 🔥 Envoie le token dans l'authentification
        "Accept": "application/json"
    }
    
    response = requests.get(f"{APP_URL}/user", headers=headers)  # 🔥 Teste l'endpoint protégé

    print(f"🔍 DEBUG: Status = {response.status_code}")
    print(f"🔍 DEBUG: Body = {response.text}")

    assert response.status_code == 200, f"❌ Accès refusé : {response.status_code}"


if __name__ == "__main__":
    pytest.main()
