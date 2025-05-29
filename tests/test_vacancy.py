from src.vacancy import Vacancy


def test_vacancy_initialization(sample_vacancy_data):
    """Тест инициализации вакансии с полными данными"""
    vacancy = Vacancy(**sample_vacancy_data)

    assert vacancy.title == "Python Developer"
    assert vacancy.url == "https://hh.ru/vacancy/123"
    assert vacancy.salary == {"from": 100000, "to": 150000, "currency": "RUB"}
    assert vacancy.description == "Опыт работы с Python 3+"


def test_vacancy_no_salary(sample_vacancy_no_salary):
    """Тест инициализации вакансии без зарплаты"""
    vacancy = Vacancy(**sample_vacancy_no_salary)

    assert vacancy.salary == {"from": 0, "to": 0, "currency": "RUB"}


def test_vacancy_partial_salary(sample_vacancy_partial_salary):
    """Тест инициализации вакансии с частичной зарплатой"""
    vacancy = Vacancy(**sample_vacancy_partial_salary)

    assert vacancy.salary == {"from": 50000, "to": 0, "currency": "RUB"}


def test_avg_salary_calculation(sample_vacancy_data):
    """Тест расчета средней зарплаты"""
    vacancy = Vacancy(**sample_vacancy_data)
    assert vacancy.avg_salary == 125000.0


def test_avg_salary_no_to(sample_vacancy_partial_salary):
    """Тест расчета средней зарплаты когда указано только 'from'"""
    vacancy = Vacancy(**sample_vacancy_partial_salary)
    assert vacancy.avg_salary == 50000.0


def test_avg_salary_none(sample_vacancy_no_salary):
    """Тест расчета средней зарплаты когда зарплата не указана"""
    vacancy = Vacancy(**sample_vacancy_no_salary)
    assert vacancy.avg_salary == 0.0


def test_str_representation(sample_vacancy_data):
    """Тест строкового представления вакансии"""
    vacancy = Vacancy(**sample_vacancy_data)
    str_repr = str(vacancy)

    assert "Python Developer" in str_repr
    assert "100000 - 150000RUB" in str_repr
    assert "Опыт работы с Python 3+" in str_repr


def test_comparison_operators(sample_vacancy_data, sample_vacancy_partial_salary):
    """Тест операторов сравнения"""
    vacancy1 = Vacancy(**sample_vacancy_data)
    vacancy2 = Vacancy(**sample_vacancy_partial_salary)

    assert vacancy1 > vacancy2
    assert vacancy2 < vacancy1
    assert vacancy1 >= vacancy2
    assert vacancy2 <= vacancy1


def test_to_dict(sample_vacancy_data):
    """Тест преобразования в словарь"""
    vacancy = Vacancy(**sample_vacancy_data)
    vacancy_dict = vacancy.to_dict()

    assert vacancy_dict == sample_vacancy_data


def test_from_dict(sample_vacancy_data):
    """Тест создания вакансии из словаря"""
    vacancy = Vacancy.from_dict(sample_vacancy_data)

    assert vacancy.title == sample_vacancy_data["title"]
    assert vacancy.url == sample_vacancy_data["url"]
    assert vacancy.salary == sample_vacancy_data["salary"]
    assert vacancy.description == sample_vacancy_data["description"]


def test_cast_to_object_list(sample_vacancy_list):
    """Тест преобразования списка словарей в список объектов"""
    vacancies = Vacancy.cast_to_object_list(sample_vacancy_list)

    assert len(vacancies) == 2
    assert isinstance(vacancies[0], Vacancy)
    assert isinstance(vacancies[1], Vacancy)
    assert vacancies[0].title == "Python Developer"
    assert vacancies[1].title == "Data Scientist"
