import json
import os
from unittest.mock import mock_open, patch

from src.vacancy import Vacancy


def test_json_saver_init(json_saver, mock_file):
    """Тест инициализации JSONSaver"""
    assert json_saver.filename == mock_file
    assert os.path.exists(os.path.dirname(mock_file))


def test_read_file_empty(json_saver):
    """Тест чтения пустого файла"""
    with patch("builtins.open", mock_open(read_data="[]")):
        result = json_saver._read_file()
        assert result == []


def test_read_file_with_data(json_saver, sample_vacancies_data):
    """Тест чтения файла с данными"""
    mock_data = json.dumps(sample_vacancies_data)
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = json_saver._read_file()
        assert result == []


def test_read_file_invalid(json_saver):
    """Тест чтения невалидного файла"""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        result = json_saver._read_file()
        assert result == []


def test_write_file(json_saver, sample_vacancies_data):
    """Тест записи в файл"""
    m = mock_open()
    with patch("builtins.open", m):
        json_saver._write_file(sample_vacancies_data)

    m.assert_called_once_with(json_saver.filename, "w", encoding="utf-8")
    # проверка, что write хотя бы раз вызван
    handle = m()
    assert handle.write.called


def test_add_vacancy(json_saver, sample_vacancy, sample_vacancy_dict):
    """Тест добавления вакансии"""
    with (
        patch.object(json_saver, "_read_file", return_value=[]),
        patch.object(json_saver, "_write_file") as mock_write,
    ):
        json_saver.add_vacancy(sample_vacancy)

        mock_write.assert_called_once_with([sample_vacancy_dict])


def test_get_vacancies_all(json_saver, sample_vacancies_data):
    """Тест получения всех вакансий"""
    with patch.object(json_saver, "_read_file", return_value=sample_vacancies_data):
        vacancies = json_saver.get_vacancies()
        assert len(vacancies) == 2
        assert all(isinstance(v, Vacancy) for v in vacancies)


def test_get_vacancies_filtered(json_saver, sample_vacancies_data):
    """Тест фильтрации вакансий"""
    with patch.object(json_saver, "_read_file", return_value=sample_vacancies_data):
        # По ключевому слову
        python_vacancies = json_saver.get_vacancies({"keyword": "python"})
        assert len(python_vacancies) == 2

        # По зарплате
        high_salary_vacancies = json_saver.get_vacancies({"salary_from": 120000})
        assert len(high_salary_vacancies) == 2

        # По названию
        ds_vacancies = json_saver.get_vacancies({"title": "scientist"})
        assert len(ds_vacancies) == 1


def test_delete_vacancy(json_saver, sample_vacancy, sample_vacancies_data):
    """Тест удаления вакансии"""
    with (
        patch.object(json_saver, "_read_file", return_value=sample_vacancies_data),
        patch.object(json_saver, "_write_file") as mock_write,
    ):
        json_saver.delete_vacancy(sample_vacancy)

        # Проверяем что осталась только одна вакансия
        assert mock_write.call_args[0][0][0]["title"] == "Data Scientist"


def test_clear_all_vacancies(json_saver, sample_vacancies_data):
    """Тест очистки всех вакансий"""
    with (
        patch.object(json_saver, "_read_file", return_value=sample_vacancies_data),
        patch.object(json_saver, "_write_file") as mock_write,
    ):
        json_saver.clear_all_vacancies()
        mock_write.assert_called_once_with([])
