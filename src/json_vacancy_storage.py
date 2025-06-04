import json
import os
from typing import Dict, List, Optional

from src.vacancy import Vacancy
from src.vacancy_storage import VacancyStorage


class JSONSaver(VacancyStorage):
    """Класс для работы с хранилищем вакансий"""

    __slots__ = ["__data_dir", "__filename"]

    def __init__(self, filename: str = "vacancies.json"):
        self.__data_dir = os.path.join("..", "data")
        self.__filename = os.path.join(self.__data_dir, filename)

        # Создаём директорию, если её нет
        os.makedirs(self.__data_dir, exist_ok=True)

    def _read_file(self) -> List[Dict]:
        """Чтение данных из файла"""
        if not os.path.exists(self.__filename):
            return []
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return []

    def _write_file(self, data: List[Dict]) -> None:
        """Запись данных в файл"""
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Какая то хрень с сохранением файла произошла, посмотри: {e}")

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в файл"""
        vacancies = self._read_file()

        # Вот тут я добавил проверку, существует ли уже такая вакансия
        vacancy_dict = vacancy.to_dict()
        if not any(
            v.get("url") == vacancy_dict.get("url") and v.get("title") == vacancy_dict.get("title") for v in vacancies
        ):
            vacancies.append(vacancy_dict)
            self._write_file(vacancies)
        else:
            print(f"Ну такая хрень, как '{vacancy.title}' у нас уже есть. А нафига нам их две...")

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

    @property
    def filename(self) -> str:
        """Геттер для имени файла(пришлось добавить раз теперь оно приватное"""
        return self.__filename

    @property
    def data_dir(self) -> str:
        """Геттер для директории данных(та же шляпа,что и с именем)"""
        return self.__data_dir
