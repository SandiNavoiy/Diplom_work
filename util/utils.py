from configparser import ConfigParser

import psycopg2

from scr.DBManage import DBManage


class WelcomeMessage:
    """Класс вывода приветсвия в стиле псевдографики"""
    def __init__(self, message):
        self.message = message

    def create_border(self, width, height):
        """Создание рамки"""
        border = '+' + '-' * (width + 1) + '+\n'
        return border  * (height - 4) + border

    def create_welcome_message(self):
        """Создание сообшения"""
        width = len(self.message) + 3
        height = 3
        border = self.create_border(width, height)
        welcome = f'|  {self.message}  |\n'
        return border + welcome + border
    def __str__(self):
        return self.create_welcome_message()

def interact_with_user():
    """Функция для взаимодействия с пользователем."""
    # Инициируем обьекты классов для работы
    params = config()
    name_db = 'testing'
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
        print("safgs")

def config(filename="database.ini", section="postgresql"):
    """Словарь с данными для подключения к БД """
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
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
def create_database(params: dict):
    """Для первичного создания БД"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE testing")
    cur.close()
    conn.close()

