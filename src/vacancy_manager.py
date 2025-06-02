from typing import List

from src.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
    """Фильтрация вакансий по ключевым словам"""
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        description = vacancy.description.lower()
        if any(word.lower() in description for word in filter_words):
            filtered.append(vacancy)
    return filtered


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """Фильтрация вакансий по диапазону зарплат"""
    if not salary_range:
        return vacancies

    try:
        min_salary, max_salary = map(int, salary_range.split("-"))
    except ValueError:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        if min_salary <= vacancy.avg_salary <= max_salary:
            filtered.append(vacancy)
    return filtered


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортировка вакансий по зарплате (по убыванию)"""
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """Получение топ N вакансий"""
    return vacancies[:top_n]


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """Вывод вакансий на экран"""
    if not vacancies:
        print("Блин, облом, ничего не нашлось. Тут два варика,- либо ты слишком до хрена хочешь, либо они...")
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"Вакансия #{i}")
        print(vacancy)
        print("-" * 50)
