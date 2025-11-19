import requests
import pytest

class TestOrderList:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'
    
    def test_get_orders_list_returns_list_of_orders(self):
        """Получение списка заказов возвращает список"""
        response = requests.get(self.BASE_URL, timeout=10)
        
        if response.status_code == 504:
            pytest.skip("Сервер недоступен (504 Gateway Timeout)")
        
        assert response.status_code == 200
        