from typing import Dict, List
from unittest.mock import Mock, patch

import pytest

from src.class_hh import HeadHunterAPI
from src.json_vacancy_storage import JSONSaver
from src.vacancy import Vacancy


# Фикстуры для тестов модуля class_hh
@pytest.fixture
def mock_hh_api_response():
    """Фикстура с моком ответа API HeadHunter"""
    return {
        "items": [
            {
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/123",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "snippet": {"requirement": "Опыт работы с Python"},
            },
            {
                "name": "Data Scientist",
                "alternate_url": "https://hh.ru/vacancy/456",
                "salary": None,
                "snippet": {"requirement": "Знание ML"},
            },
        ]
    }


@pytest.fixture
def mock_requests_get(mock_hh_api_response):
    """Фикстура для мока requests.get"""
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = mock_hh_api_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def hh_api():
    """Фикстура для экземпляра HeadHunterAPI"""
    return HeadHunterAPI()


@pytest.fixture
def mock_hh_api_failure():
    """Фикстура для ошибочного ответа API HH"""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.side_effect = Exception("API Error")
    mock_response.raise_for_status.side_effect = Exception("API Error")
    return mock_response


# Фикстуры для тестов модуля vacancy
@pytest.fixture
def sample_vacancy_data() -> Dict:
    """Фикстура с тестовыми данными вакансии"""
    return {
        "title": "Python Developer",
        "url": "https://hh.ru/vacancy/123",
        "salary": {"from": 100000, "to": 150000, "currency": "RUB"},
        "description": "Опыт работы с Python 3+",
    }


@pytest.fixture
def sample_vacancy_no_salary() -> Dict:
    """Фикстура с тестовыми данными вакансии без зарплаты"""
    return {
        "title": "Intern",
        "url": "https://hh.ru/vacancy/456",
        "salary": None,
        "description": "Обучение программированию",
    }


@pytest.fixture
def sample_vacancy_partial_salary() -> Dict:
    """Фикстура с тестовыми данными вакансии с одним порогом"""
    return {
        "title": "Junior Python",
        "url": "https://hh.ru/vacancy/789",
        "salary": {"from": 50000, "currency": "RUB"},
        "description": "Начальные знания Python",
    }


@pytest.fixture
def sample_vacancy_list() -> List[Dict]:
    """Фикстура со списком тестовых вакансий"""
    return [
        {
            "name": "Python Developer",
            "alternate_url": "https://hh.ru/vacancy/123",
            "salary": {"from": 100000, "to": 150000, "currency": "RUB"},
            "snippet": {"requirement": "Опыт работы с Python 3+"},
        },
        {
            "name": "Data Scientist",
            "alternate_url": "https://hh.ru/vacancy/456",
            "salary": None,
            "snippet": {"requirement": "Знание ML"},
        },
    ]


# Фикструры для тестов модуля json_vacancy_storage
@pytest.fixture
def sample_vacancy_dict():
    """Фикстура с тестовыми данными вакансии в виде словаря"""
    return {
        "title": "Python Developer",
        "url": "https://hh.ru/vacancy/123",
        "salary": {"from": 100000, "to": 150000, "currency": "RUB"},
        "description": "Опыт работы с Python 3+",
    }


@pytest.fixture
def sample_vacancy(sample_vacancy_dict):
    """Фикстура с тестовым объектом Vacancy"""
    return Vacancy.from_dict(sample_vacancy_dict)


@pytest.fixture
def sample_vacancies_data(sample_vacancy_dict):
    """Фикстура с тестовыми данными нескольких вакансий"""
    return [
        sample_vacancy_dict,
        {
            "title": "Data Scientist",
            "url": "https://hh.ru/vacancy/456",
            "salary": {"from": 150000, "currency": "RUB"},
            "description": "Знание ML и Python",
        },
    ]


@pytest.fixture
def mock_file(tmp_path):
    """Фикстура для мока файла"""
    filename = tmp_path / "vacancies.json"
    return str(filename)


@pytest.fixture
def json_saver(mock_file):
    """Фикстура для экземпляра JSONSaver с 'моком' файла"""
    return JSONSaver(filename=mock_file)


# Фикстура для тестов модуля vacancy_manager
@pytest.fixture
def sample_vacancies() -> List[Vacancy]:
    """Фикстура с тестовыми вакансиями"""
    return [
        Vacancy(
            title="Python Developer",
            url="https://example.com/1",
            salary={"from": 100000, "to": 150000, "currency": "RUB"},
            description="Требуется опыт работы с Python и Django",
        ),
        Vacancy(
            title="Java Developer",
            url="https://example.com/2",
            salary={"from": 120000, "to": 180000, "currency": "RUB"},
            description="Ищем Java разработчика с Spring Framework",
        ),
        Vacancy(
            title="Data Scientist",
            url="https://example.com/3",
            salary={"from": 150000, "currency": "RUB"},
            description="Python, ML, Data Analysis",
        ),
        Vacancy(
            title="Frontend Developer",
            url="https://example.com/4",
            salary=None,
            description="JavaScript, React, HTML/CSS",
        ),
    ]
