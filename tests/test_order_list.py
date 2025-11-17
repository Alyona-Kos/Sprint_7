class TestOrderList:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'
    
    def setup_method(self):
        """Создание тестового заказа перед проверкой списка"""
        self.payload = {
            "firstName": "Тест",
            "lastName": "Список",
            "address": "ул. Тестовая, 1",
            "metroStation": 1,
            "phone": "+79998887766",
            "rentTime": 1,
            "deliveryDate": "2024-12-31",
            "comment": "Заказ для проверки списка"
        }
        
        response = requests.post(self.BASE_URL, json=self.payload)
        assert response.status_code == 201
        self.track = response.json().get("track")

    def test_get_orders_list(self):
        """Получение списка заказов"""
        response = requests.get(self.BASE_URL)
        
        
        assert response.status_code == 200
        
        
        response_body = response.json()
        assert "orders" in response_body
        assert isinstance(response_body["orders"], list)
        
        
        if len(response_body["orders"]) > 0:
            order = response_body["orders"][0]
            assert "id" in order
            assert "track" in order
            assert "firstName" in order

    def test_orders_list_with_limit(self):
        """Получение списка заказов с лимитом"""
        response = requests.get(self.BASE_URL, params={"limit": 5})
        
        
        assert response.status_code == 200
        
        
        response_body = response.json()
        orders = response_body["orders"]
        assert len(orders) <= 5