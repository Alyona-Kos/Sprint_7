import requests
import random
import string

class TestCourierCreation:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'
    
    def generate_random_string(self, length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
    
    def create_courier_payload(self, login=None, password=None, first_name=None):
        return {
            "login": login or self.generate_random_string(10),
            "password": password or self.generate_random_string(10),
            "firstName": first_name or self.generate_random_string(10)
        }
    
    def login_courier(self, login, password):
        response = requests.post(f'{self.BASE_URL}/login', 
                               json={"login": login, "password": password})
        if response.status_code == 200:
            return response.json().get("id")
        return None
    
    def delete_courier(self, courier_id):
        if courier_id:
            requests.delete(f'{self.BASE_URL}/{courier_id}')

    def test_successful_courier_creation(self):
        """Создание курьера с валидными данными"""
        payload = self.create_courier_payload()
        
        response = requests.post(self.BASE_URL, json=payload)
        
        
        assert response.status_code == 201
        
        
        response_body = response.json()
        assert response_body == {"ok": True}
        
        
        courier_id = self.login_courier(payload["login"], payload["password"])
        self.delete_courier(courier_id)

    def test_duplicate_courier_creation(self):
        """Нельзя создать двух одинаковых курьеров"""
        payload = self.create_courier_payload()
        
        
        response1 = requests.post(self.BASE_URL, json=payload)
        assert response1.status_code == 201
        
        
        response2 = requests.post(self.BASE_URL, json=payload)
        
        
        assert response2.status_code == 409
        
        
        response_body = response2.json()
        assert "message" in response_body
        assert "уже используется" in response_body["message"]
        
        
        courier_id = self.login_courier(payload["login"], payload["password"])
        self.delete_courier(courier_id)

    def test_creation_without_login(self):
        """Создание курьера без логина возвращает ошибку с правильным сообщением"""
        payload = self.create_courier_payload()
        del payload["login"]  # Удаляем логин
        
        response = requests.post(self.BASE_URL, json=payload)
        
        
        assert response.status_code == 400
        
        
        response_body = response.json()
        assert "message" in response_body
        assert response_body["message"] == "Недостаточно данных для создания учетной записи"

    def test_creation_without_password(self):
        """Создание курьера без пароля возвращает ошибку с правильным сообщением"""
        payload = self.create_courier_payload()
        del payload["password"]  # Удаляем пароль
        
        response = requests.post(self.BASE_URL, json=payload)
        
        
        assert response.status_code == 400
        
        
        response_body = response.json()
        assert "message" in response_body
        assert response_body["message"] == "Недостаточно данных для создания учетной записи"

    def test_creation_without_first_name(self):
        """Создание курьера без имени возвращает ошибку с правильным сообщением"""
        payload = self.create_courier_payload()
        del payload["firstName"]  # Удаляем имя
        
        response = requests.post(self.BASE_URL, json=payload)
        
        
        assert response.status_code == 400
        
        
        response_body = response.json()
        assert "message" in response_body
        assert response_body["message"] == "Недостаточно данных для создания учетной записи"

    def test_creation_with_empty_login(self):
        """Создание курьера с пустым логином возвращает ошибку"""
        payload = self.create_courier_payload(login="")
        
        response = requests.post(self.BASE_URL, json=payload)
        
        
        assert response.status_code == 400
        
        
        response_body = response.json()
        assert "message" in response_body
        assert response_body["message"] == "Недостаточно данных для создания учетной записи"

    def test_creation_with_empty_password(self):
        """Создание курьера с пустым паролем возвращает ошибку"""
        payload = self.create_courier_payload(password="")
        
        response = requests.post(self.BASE_URL, json=payload)
        
        
        assert response.status_code == 400
        
        
        response_body = response.json()
        assert "message" in response_body
        assert response_body["message"] == "Недостаточно данных для создания учетной записи"