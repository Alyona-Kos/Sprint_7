import requests
import random
import string

class TestCourierLogin:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'
    
    def setup_method(self):
        """Создание тестового курьера перед каждым тестом"""
        self.login = f"test_{random.randint(1000, 9999)}"
        self.password = "test_password_123"
        self.first_name = "Test Courier"
        
        payload = {
            "login": self.login,
            "password": self.password,
            "firstName": self.first_name
        }
        
        response = requests.post(self.BASE_URL, json=payload)
        assert response.status_code == 201
    
    def teardown_method(self):
        """Удаление тестового курьера после каждого теста"""
        login_response = requests.post(f'{self.BASE_URL}/login', 
                                     json={"login": self.login, "password": self.password})
        if login_response.status_code == 200:
            courier_id = login_response.json().get("id")
            if courier_id:
                requests.delete(f'{self.BASE_URL}/{courier_id}')

    def test_successful_login(self):
        """Успешный логин курьера возвращает ID"""
        payload = {
            "login": self.login,
            "password": self.password
        }
        
        response = requests.post(f'{self.BASE_URL}/login', json=payload)
        
        
        assert response.status_code == 200
        
        
        response_body = response.json()
        assert "id" in response_body
        assert isinstance(response_body["id"], int)

    def test_login_with_wrong_password(self):
        """Логин с неверным паролем возвращает ошибку 400"""
        payload = {
            "login": self.login,
            "password": "wrong_password"
        }
        
        response = requests.post(f'{self.BASE_URL}/login', json=payload)
        
        
        assert response.status_code == 400
        
        
        response_body = response.json()
        assert "message" in response_body
        assert response_body["message"] == "Недостаточно данных для входа"

    def test_login_with_wrong_login(self):
        """Логин с неверным логином возвращает ошибку 400"""
        payload = {
            "login": "nonexistent_login",
            "password": self.password
        }
        
        response = requests.post(f'{self.BASE_URL}/login', json=payload)
        
        
        assert response.status_code == 400
        
        
        response_body = response.json()
        assert "message" in response_body
        assert response_body["message"] == "Недостаточно данных для входа"

    def test_login_without_login(self):
        """Логин без логина возвращает ошибку 400"""
        payload = {
            "password": self.password
        }
        
        response = requests.post(f'{self.BASE_URL}/login', json=payload)
        
        assert response.status_code == 400
        
        
        response_body = response.json()
        assert "message" in response_body
        assert response_body["message"] == "Недостаточно данных для входа"

    def test_login_without_password(self):
        """Логин без пароля возвращает ошибку 400"""
        payload = {
            "login": self.login
        }
        
        response = requests.post(f'{self.BASE_URL}/login', json=payload)
        
        assert response.status_code == 400
        
        
        response_body = response.json()
        assert "message" in response_body
        assert response_body["message"] == "Недостаточно данных для входа"