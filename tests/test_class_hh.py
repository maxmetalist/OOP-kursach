from typing import List
from unittest.mock import Mock

import pytest
import requests


def test_get_vacancies_success(hh_api, mock_requests_get, mock_hh_api_response):
    """Тест успешного получения вакансий"""
    search_query = "Python"
    vacancies = hh_api.get_vacancies(search_query)

    assert isinstance(vacancies, List)
    assert len(vacancies) == 2
    assert vacancies == mock_hh_api_response["items"]

    # Проверка вызова requests.get с правильными параметрами
    mock_requests_get.assert_called_once_with(
        hh_api.base_url,
        params={
            "text": search_query,
            "area": 113,
            "per_page": 100,
        },
    )


def test_get_vacancies_empty_response(hh_api, mock_requests_get):
    """Тест пустого ответа от API"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": []}
    mock_response.raise_for_status.return_value = None
    mock_requests_get.return_value = mock_response

    vacancies = hh_api.get_vacancies("Java")

    assert isinstance(vacancies, List)
    assert len(vacancies) == 0


def test_get_vacancies_http_error(hh_api, mock_requests_get):
    """Тест обработки HTTP ошибки"""
    mock_requests_get.side_effect = requests.exceptions.HTTPError("404 Not Found")

    with pytest.raises(requests.exceptions.HTTPError):
        hh_api.get_vacancies("C++")
