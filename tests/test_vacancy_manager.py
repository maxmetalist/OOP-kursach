from src.vacancy_manager import (filter_vacancies, get_top_vacancies, get_vacancies_by_salary, print_vacancies,
                                 sort_vacancies)


def test_filter_vacancies_no_filter(sample_vacancies):
    """Тест фильтрации без ключевых слов"""
    result = filter_vacancies(sample_vacancies, [])
    assert result == sample_vacancies


def test_filter_vacancies_with_filter(sample_vacancies):
    """Тест фильтрации по ключевым словам"""
    result = filter_vacancies(sample_vacancies, ["python"])
    assert len(result) == 2
    assert all("python" in vacancy.description.lower() for vacancy in result)


def test_filter_vacancies_case_insensitive(sample_vacancies):
    """Тест регистронезависимости фильтрации"""
    result = filter_vacancies(sample_vacancies, ["PYTHON"])
    assert len(result) == 2


def test_get_vacancies_by_salary_no_range(sample_vacancies):
    """Тест фильтрации по зарплате без диапазона"""
    result = get_vacancies_by_salary(sample_vacancies, "")
    assert result == sample_vacancies


def test_get_vacancies_by_salary_invalid_range(sample_vacancies):
    """Тест обработки невалидного диапазона зарплат"""
    result = get_vacancies_by_salary(sample_vacancies, "abc-def")
    assert result == sample_vacancies


def test_get_vacancies_by_salary_valid_range(sample_vacancies):
    """Тест фильтрации по валидному диапазону зарплат"""
    result = get_vacancies_by_salary(sample_vacancies, "110000-160000")
    assert len(result) == 3
    assert all(110000 <= vacancy.avg_salary <= 160000 for vacancy in result)


def test_sort_vacancies(sample_vacancies):
    """Тест сортировки вакансий по зарплате"""
    sorted_list = sort_vacancies(sample_vacancies)
    salaries = [vacancy.avg_salary for vacancy in sorted_list]
    assert salaries == sorted(salaries, reverse=True)


def test_get_top_vacancies(sample_vacancies):
    """Тест получения топ N вакансий"""
    top_n = 2
    result = get_top_vacancies(sample_vacancies, top_n)
    assert len(result) == top_n
    assert result == sample_vacancies[:top_n]


def test_get_top_vacancies_more_than_exists(sample_vacancies):
    """Тест получения топ N, когда N больше количества вакансий"""
    result = get_top_vacancies(sample_vacancies, 10)
    assert len(result) == len(sample_vacancies)


def test_print_vacancies(capsys, sample_vacancies):
    """Тест вывода вакансий"""
    print_vacancies(sample_vacancies)
    captured = capsys.readouterr()
    assert "Python Developer" in captured.out
    assert "Java Developer" in captured.out


def test_print_vacancies_empty(capsys):
    """Тест вывода пустого списка вакансий"""
    print_vacancies([])
    captured = capsys.readouterr()
    assert "Блин, облом" in captured.out
