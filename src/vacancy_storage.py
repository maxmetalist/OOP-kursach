from abc import ABC, abstractmethod
from typing import Dict, List

from src.vacancy import Vacancy


class VacancyStorage(ABC):
    """Абстрактный класс для работы с хранилищем вакансий"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавить вакансию в хранилище"""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Dict) -> List[Vacancy]:
        """Получить вакансии по критериям"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удалить вакансии по критериям"""
        pass
