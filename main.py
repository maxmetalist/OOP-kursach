from src.json_vacancy_storage import JSONSaver
from src.vacancy_manager import filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies, \
    print_vacancies
from src.class_hh import HeadHunterAPI
from src.vacancy import Vacancy


def user_interaction():
    """Функция для взаимодействия с пользователем"""
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    print("Здорово!Чё работку подыскиваешь? Ну, давай поможем.")
    search_query = input("Введи кем хочешь потрудиться (ну там, Тракторист ассенизатор, или Python разработчик): ")

    try:
        # Получаем вакансии с hh.ru
        print("\nПогоди,ответ с hh.ru придёт...")
        hh_vacancies = hh_api.get_vacancies(search_query)
        vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

        # Сохраняем в файл
        for vacancy in vacancies_list:
            json_saver.add_vacancy(vacancy)

        # Запрашиваем параметры у пользователя
        top_n = int(input("\nВведи топ N (сколько показать вакансий с самой жирной зарплатой) : "))
        filter_words = input("Введи ключевые слова для обработки  (через пробел,бро): ").split()
        salary_range = input("Введи свои аппетиты по зарплате (ну вот сколько хочешь денег. Например: 100000-150000): ")

        # Фильтрация и сортировка
        filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
        ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
        sorted_vacancies = sort_vacancies(ranged_vacancies)
        top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

        # Вывод результатов
        print("\nГлянь, что получилось:")
        print_vacancies(top_vacancies)

        # Дополнительные операции с сохраненными вакансиями
        while True:
            action = input("\nЕщё что-нибудь сделать? (да/нет): ").lower()
            if action != "да":
                break

            print("\nДоступные действия:")
            print("1. Показать все вакансии,что нарыли на hh")
            print("2. Искать по ключевому слову в сохраненных вакансиях")
            print("3. Удалить конкретную вакансию (там всё равно зп слёзы)")
            print("4. Удалить ВСЕ вакансии")
            print("5. Выход")

            choice = input("Ну так что, выбери действие (1-5): ")

            if choice == "1":
                all_vacancies = json_saver.get_vacancies({})
                print_vacancies(all_vacancies)
            elif choice == "2":
                keyword = input("Введи ключевое слово для поиска: ")
                found_vacancies = json_saver.get_vacancies({"keyword": keyword})
                print_vacancies(found_vacancies)
            elif choice == "3":
                title = input("Введи название вакансии для удаления: ")
                url = input("Введите URL вакансии для удаления: ")
                vacancy_to_delete = Vacancy(title, url, None, "")
                json_saver.delete_vacancy(vacancy_to_delete)
                print("Вакансия удалена")
            elif choice == "4":
                confirm = input("Чё, реально удалить ВСЕ вакансии? (да/нет): ").lower()
                if confirm == "да":
                    json_saver.clear_all_vacancies()
                    print("Да,согласен, там была одна фигня... Лучше это всё затереть")
            elif choice == "5":
                break
            else:
                print("Неверный выбор")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    user_interaction()