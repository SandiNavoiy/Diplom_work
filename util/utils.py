from configparser import ConfigParser

import pandas as pd
import psycopg2

from scr.DBManage import DBManage


class WelcomeMessage:
    """Класс вывода приветсвия в стиле псевдографики"""

    def __init__(self, message):
        self.message = message

    def create_border(self, width, height):
        """Создание рамки"""
        border = "+" + "-" * (width + 1) + "+\n"
        return border * (height - 4) + border

    def create_welcome_message(self):
        """Создание сообшения"""
        width = len(self.message) + 3
        height = 3
        border = self.create_border(width, height)
        welcome = f"|  {self.message}  |\n"
        return border + welcome + border

    def __str__(self):
        return self.create_welcome_message()


def interact_with_user():
    """Функция для взаимодействия с пользователем."""
    # Инициируем обьекты классов для работы
    params = config()
    name_db = "testing"
    try:
        db_manager = DBManage(name_db, params)
    except psycopg2.OperationalError:
        # Проверка подключения и наличие БД
        print("Ошибка подключенния к базе данных")
        print(f"Пытаемся создать БД с названием {name_db}")
        try:
            create_database(params)
            print("Перезапустите программу")
        except psycopg2.OperationalError:
            print("Проверьте фаерволл")

    else:
        while True:
            # Запускаем бесконечный цикл для работы меню
            print("Выберите действие:")

            print("1 - Перевоздание базы данных и таблиц ")
            print("2 - Заполняем таблицe БД данными")
            print("3 - Прогнозирование цен методом линейной регресии")
            print("4 - Прогнозирование цен методом маштабирования веса влияния")
            print(
                "5 - Прогнозирование цен самым простым методом, подсчета средней цены"
            )

            print("9 - Выйти")
            choice = input("Введите значение---")

            # Непосредствено работы меню выбора
            if choice == "1":
                db_manager.create_tables()
                print(f"База данных {name_db} и таблицы  созданы")
            elif choice == "2":
                try:
                    csv_filename = "csv_data.csv"
                    df = pd.read_csv(csv_filename)
                except FileNotFoundError:
                    print("Нет файла, загрузите файл")
                else:
                    try:
                        db_manager.error_table()
                    except psycopg2.errors.UndefinedTable:
                        # Проверка наличие таблицы
                        print("Нет таблиц, создайте - пункт 1")
                    else:
                        print(
                            "Таблица заполняется. требуется много времени(несколько минут"
                        )
                        print(f"Всего в базе {len(df)} элементов")
                        db_manager.insert_table(csv_filename)
                        print("Таблицы заполнены")
            elif choice == "3":
                db_manager.load_data()
                db_manager.train_models()
                # Прогнозирование цен для всех продуктов
                all_predictions = db_manager.predict_prices_for_all_products()

                # Вывод результатов
                for product, price in all_predictions.items():

                    mse = db_manager.mse_scores.get(product, None)
                    print(f"Прогнозируемая цена на {product}: {price}, отклонение {mse}")

            elif choice == "4":
                db_manager.load_data()
                db_manager.train_models__not_line()
                # Прогнозирование цен для всех продуктов
                all_predictions = db_manager.predict_prices_for_all_products()

                # Вывод результатов
                for product, price in all_predictions.items():
                    mse = db_manager.mse_scores.get(product, None)
                    print(f"Прогнозируемая цена на {product}: {price}, отклонение {mse}")



            elif choice == "5":
                db_manager.load_data()
                average_prices = db_manager.get_average_prices_for_each_product()
                print("Вывод средних цен")
                for key, value in average_prices.items():
                    print(f'{key}:{value}')



            elif choice == "9":
                # Выход
                db_manager.close_connection()
                print("--------------")
                print("Спасибо за обращение\n" "Конец работы!")
                print("--------------")
                break


def config(filename="database.ini", section="postgresql"):
    """Словарь с данными для подключения к БД"""
    # создаем парсер
    parser = ConfigParser()
    # читаем конфиг файл
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} is not found in the {1} file.".format(section, filename)
        )
    return db


def create_database(params: dict):
    """Для первичного создания БД"""
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE testing")
    cur.close()
    conn.close()
