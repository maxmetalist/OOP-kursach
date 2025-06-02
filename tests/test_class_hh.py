from unittest.mock import Mock, patch

import pytest

from src.class_hh import HeadHunterAPI


class TestHeadHunterAPI:
    """Тесты для класса HeadHunterAPI"""

    def test_init(self):
        """Тест инициализации класса"""
        api = HeadHunterAPI()
        assert hasattr(api, "_HeadHunterAPI__base_url")
        assert api._HeadHunterAPI__base_url == "https://api.hh.ru/vacancies"

    @patch("requests.get")
    def test_get_vacancies_success(self, mock_get):
        # Настраиваем мок для успешного ответа
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [{"name": "Python Developer"}]}
        mock_get.return_value = mock_response

        hh_api = HeadHunterAPI()
        result = hh_api.get_vacancies("Python")

        assert isinstance(result, list)
        assert len(result) > 0
        assert "Python Developer" in result[0]["name"]

    @patch("requests.get")
    def test_get_vacancies_empty(self, mock_get):
        # Настраиваем мок для пустого ответа
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        hh_api = HeadHunterAPI()
        result = hh_api.get_vacancies("NonExistentPosition")

        assert isinstance(result, list)
        assert len(result) == 0

    @patch("requests.get")
    def test_get_vacancies_failure(self, mock_get, mock_hh_api_failure):
        """Тест обработки ошибки API"""
        mock_get.return_value = mock_hh_api_failure
        hh_api = HeadHunterAPI()

        with pytest.raises(Exception, match="API Error"):
            hh_api.get_vacancies("Python")

    def test_slots(self):
        """Тест ограничения атрибутов через __slots__"""
        api = HeadHunterAPI()

        # Проверка, что __slots__ определяется
        assert hasattr(HeadHunterAPI, "__slots__")
        assert "_HeadHunterAPI__base_url" in HeadHunterAPI.__slots__

        # Проверка, что нельзя добавить новый атрибут
        with pytest.raises(AttributeError):
            api.new_attribute = "test"

        # Проверка работоспособности атрибута
        assert api._HeadHunterAPI__base_url == "https://api.hh.ru/vacancies"
