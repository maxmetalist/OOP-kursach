from typing import Dict, List

import requests

from src.parser import VacancyAPI


class HeadHunterAPI(VacancyAPI):
    """Класс для работы с API HeadHunter(наследуется от класса VacancyAPI из модуля parser)"""

    __slots__ = ["_HeadHunterAPI__base_url"]

    def __init__(self):
        self.__base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, search_query: str) -> List[Dict]:
        """Получить вакансии по поисковому запросу"""
        params = {
            "text": search_query,
            "area": 113,  # Россия
            "per_page": 100,  # Максимальное количество вакансий на странице
        }
        try:
            response = requests.get(self.__base_url, params=params)
            response.raise_for_status()
            return response.json().get("items", [])
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API hh.ru: {e}")
            return []
