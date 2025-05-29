import json
import os
from typing import Dict, List, Optional

from src.vacancy import Vacancy
from src.vacancy_storage import VacancyStorage


class JSONSaver(VacancyStorage):
    """Класс для работы с хранилищем вакансий"""

    def __init__(self, filename: str = "vacancies.json"):
        self.data_dir = os.path.join("..", "data")
        self.filename = os.path.join(self.data_dir, filename)

        # Создаём директорию, если её нет
        os.makedirs(self.data_dir, exist_ok=True)

    def _read_file(self) -> List[Dict]:
        """Чтение данных из файла"""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return []

    def _write_file(self, data: List[Dict]) -> None:
        """Запись данных в файл"""
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка при сохранении файла: {e}")

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в файл"""
        vacancies = self._read_file()
        vacancies.append(vacancy.to_dict())
        self._write_file(vacancies)

    def get_vacancies(self, criteria: Optional[Dict] = None) -> List[Vacancy]:
        """Получение вакансий по критериям"""
        if criteria is None:
            criteria = {}

        vacancies_data = self._read_file()
        vacancies = [Vacancy.from_dict(v) for v in vacancies_data]

        filtered_vacancies = []
        for vacancy in vacancies:
            match = True
            for key, value in criteria.items():
                if key == "keyword" and value.lower() not in vacancy.description.lower():
                    match = False
                    break
                elif key == "salary_from" and vacancy.avg_salary < value:
                    match = False
                    break
                elif key == "title" and value.lower() not in vacancy.title.lower():
                    match = False
                    break

            if match:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из файла"""
        vacancies_data = self._read_file()
        vacancies = [Vacancy.from_dict(v) for v in vacancies_data]

        updated_vacancies = [v for v in vacancies if not (v.title == vacancy.title and v.url == vacancy.url)]

        self._write_file([v.to_dict() for v in updated_vacancies])

    def clear_all_vacancies(self) -> None:
        """Удаление всех вакансий из файла"""
        self._write_file([])
