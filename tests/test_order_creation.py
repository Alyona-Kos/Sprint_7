class TestOrderCreation:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'
    
    def create_valid_order_payload(self):
        """Создает валидный payload для заказа"""
        return {
            "firstName": "Иван",
            "lastName": "Петров",
            "address": "ул. Ленина, 1",
            "metroStation": 4,
            "phone": "+79991112233",
            "rentTime": 3,
            "deliveryDate": "2024-12-31",
            "comment": "Тестовый заказ"
        }

    def test_create_order_with_black_color(self):
        """Создание заказа с черным цветом"""
        payload = self.create_valid_order_payload()
        payload["color"] = ["BLACK"]
        
        response = requests.post(self.BASE_URL, json=payload)
        
        assert response.status_code == 201
        response_body = response.json()
        assert "track" in response_body
        assert isinstance(response_body["track"], int)

    def test_create_order_with_grey_color(self):
        """Создание заказа с серым цветом"""
        payload = self.create_valid_order_payload()
        payload["color"] = ["GREY"]
        
        response = requests.post(self.BASE_URL, json=payload)
        
        assert response.status_code == 201
        response_body = response.json()
        assert "track" in response_body

    def test_create_order_with_both_colors(self):
        """Создание заказа с обоими цветами"""
        payload = self.create_valid_order_payload()
        payload["color"] = ["BLACK", "GREY"]
        
        response = requests.post(self.BASE_URL, json=payload)
        
        assert response.status_code == 201
        response_body = response.json()
        assert "track" in response_body

    def test_create_order_without_color(self):
        """Создание заказа без указания цвета"""
        payload = self.create_valid_order_payload()
        # Не добавляем поле color
        
        response = requests.post(self.BASE_URL, json=payload)
        
        assert response.status_code == 201
        response_body = response.json()
        assert "track" in response_body

    def test_create_order_without_first_name(self):
        """Создание заказа без имени возвращает ошибку"""
        payload = self.create_valid_order_payload()
        del payload["firstName"]  # Удаляем обязательное поле
        
        response = requests.post(self.BASE_URL, json=payload)
        
        # Проверяем код ошибки (должен быть 400 согласно аналогичным endpoint)
        assert response.status_code == 400
        
        # Проверяем тело ответа с сообщением об ошибке
        if response.text:  # Если API возвращает сообщение
            response_body = response.json()
            assert "message" in response_body

    def test_create_order_without_last_name(self):
        """Создание заказа без фамилии возвращает ошибку"""
        payload = self.create_valid_order_payload()
        del payload["lastName"]
        
        response = requests.post(self.BASE_URL, json=payload)
        
        assert response.status_code == 400

    def test_create_order_without_address(self):
        """Создание заказа без адреса возвращает ошибку"""
        payload = self.create_valid_order_payload()
        del payload["address"]
        
        response = requests.post(self.BASE_URL, json=payload)
        
        assert response.status_code == 400

    def test_create_order_without_metro_station(self):
        """Создание заказа без станции метро возвращает ошибку"""
        payload = self.create_valid_order_payload()
        del payload["metroStation"]
        
        response = requests.post(self.BASE_URL, json=payload)
        
        assert response.status_code == 400

    def test_create_order_without_phone(self):
        """Создание заказа без телефона возвращает ошибку"""
        payload = self.create_valid_order_payload()
        del payload["phone"]
        
        response = requests.post(self.BASE_URL, json=payload)
        
        assert response.status_code == 400

    def test_create_order_without_rent_time(self):
        """Создание заказа без времени аренды возвращает ошибку"""
        payload = self.create_valid_order_payload()
        del payload["rentTime"]
        
        response = requests.post(self.BASE_URL, json=payload)
        
        assert response.status_code == 400

    def test_create_order_without_delivery_date(self):
        """Создание заказа без даты доставки возвращает ошибку"""
        payload = self.create_valid_order_payload()
        del payload["deliveryDate"]
        
        response = requests.post(self.BASE_URL, json=payload)
        
        assert response.status_code == 400

    def test_create_order_with_empty_required_fields(self):
        """Создание заказа с пустыми обязательными полями возвращает ошибку"""
        payload = {
            "firstName": "",
            "lastName": "",
            "address": "",
            "metroStation": 4,
            "phone": "",
            "rentTime": 3,
            "deliveryDate": "2024-12-31",
            "comment": "Тестовый заказ"
        }
        
        response = requests.post(self.BASE_URL, json=payload)
        
        assert response.status_code == 400

    def test_create_order_with_invalid_phone_format(self):
        """Создание заказа с неверным форматом телефона возвращает ошибку"""
        payload = self.create_valid_order_payload()
        payload["phone"] = "invalid_phone"
        
        response = requests.post(self.BASE_URL, json=payload)
        
        assert response.status_code == 400

    def test_create_order_with_invalid_delivery_date(self):
        """Создание заказа с неверной датой доставки возвращает ошибку"""
        payload = self.create_valid_order_payload()
        payload["deliveryDate"] = "invalid_date"
        
        response = requests.post(self.BASE_URL, json=payload)
        
        assert response.status_code == 400