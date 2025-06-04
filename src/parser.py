from abc import ABC, abstractmethod
from typing import Dict, List


class VacancyAPI(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями"""

    __slots__ = ["__base_url"]

    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[Dict]:
        """Получить вакансии по поисковому запросу"""
        pass
