from typing import Dict, List, Optional


class Vacancy:
    """Класс для работы с вакансиями"""

    def __init__(self, title: str, url: str, salary: Optional[Dict], description: str):
        self.title = title
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description

    def _validate_salary(self, salary: Optional[Dict]) -> Dict:
        """Валидация данных о зарплате"""
        if salary is not None:
            validated = {
                "from": salary.get("from", 0),
                "to": salary.get("to", 0),
                "currency": salary.get("currency", "RUB"),
            }

            return validated

        return {"from": 0, "to": 0, "currency": "RUB"}

    @property
    def avg_salary(self) -> float:
        """геттер вычисления средней зарплаты для сравнения"""
        if self.salary["from"] and self.salary["to"]:
            return (self.salary["from"] + self.salary["to"]) / 2
        return self.salary["from"] or self.salary["to"] or 0

    def __str__(self):
        """магический метод для представления в строковом виде"""
        salary_info = ""
        if self.salary["from"] or self.salary["to"]:
            salary_info = f"Зарплата: {self.salary['from']} - {self.salary['to']}" f"{self.salary['currency']}"
        else:
            salary_info = "Зарплата не указана"

        return (
            f"Вакансия: {self.title}\n"
            f"Ссылка: {self.url}\n"
            f"{salary_info}\n"
            f"Описание: {self.description[:200]}...\n"
        )

    # магические методы сравнения средних зарплат по двум выбранным вакансиям
    def __lt__(self, other):
        """маг метод для сравнения когда первое меньше второго"""
        return self.avg_salary < other.avg_salary

    def __le__(self, other):
        """то же самое, только меньше или равно"""
        return self.avg_salary <= other.avg_salary

    def __gt__(self, other):
        """то же самое, только больше"""
        return self.avg_salary > other.avg_salary

    def __ge__(self, other):
        """то же самое только больше или равно"""
        return self.avg_salary >= other.avg_salary

    def to_dict(self):
        """Преобразование в словарь для сохранения"""
        return {"title": self.title, "url": self.url, "salary": self.salary, "description": self.description}

    @classmethod
    def from_dict(cls, vacancy_dict: Dict) -> "Vacancy":
        """Класс-метод для создания вакансии из словаря"""
        return cls(
            title=vacancy_dict["title"],
            url=vacancy_dict["url"],
            salary=vacancy_dict["salary"],
            description=vacancy_dict["description"],
        )

    @classmethod
    def cast_to_object_list(cls, vacancies_data: List[Dict]) -> List["Vacancy"]:
        """Класс-метод для преобразования списка словарей в список объектов класса Vacancy"""
        vacancies = []
        for item in vacancies_data:
            vacancy = cls(
                title=item.get("name", ""),
                url=item.get("alternate_url", ""),
                salary=item.get("salary"),
                description=item.get("snippet", {}).get("requirement", "") or "",
            )
            vacancies.append(vacancy)
        return vacancies
