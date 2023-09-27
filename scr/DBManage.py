import psycopg2


class DBManage:
    """Класс для работы с данными в БД"""
    def __init__(self, database_name: str, params: dict):
        self.database_name = database_name
        self.params = params
        self.conn = psycopg2.connect(dbname=self.database_name, **self.params)
        self.cur = self.conn.cursor()

    def connect_to_database(self):
        """Переподключение к базе данных, чтоб не писать одно и тоже"""
        self.conn.close()
        self.conn = psycopg2.connect(dbname=self.database_name, **self.params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def create_database(self):
        """Создание базы данных или удаление текущей"""
        self.conn.close()  # Закрыть текущее соединение
        # Создать новое соединение для выполнения операций создания и удаления базы данных
        conn_temp = psycopg2.connect(dbname='postgres', **self.params)
        conn_temp.autocommit = True
        cur_temp = conn_temp.cursor()
        # Удалить базу данных, если она существует
        cur_temp.execute(f"DROP DATABASE IF EXISTS {self.database_name}")
        # Создать базу данных
        cur_temp.execute(f"CREATE DATABASE {self.database_name}")
        # Закрыть временное соединение
        cur_temp.close()
        conn_temp.close()
        # Подключиться заново к базе данных
        self.connect_to_database()

    def create_tables(self):
        """Создание таблиц для работодателей и вакансий"""
        self.connect_to_database()
        # Запрос SQL
        self.cur.execute("CREATE TABLE IF NOT EXISTS employers "
                         "(employer_id INTEGER PRIMARY KEY, "
                         "name VARCHAR(255), "
                         "description TEXT, "
                         "website VARCHAR(255))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS vacancies "
                         "(vacancy_id varchar(10) PRIMARY KEY, "
                         "employer_id INTEGER,"
                         "title VARCHAR(255), "
                         "salary INTEGER, "
                         "link VARCHAR(255), "
                         "FOREIGN KEY (employer_id) REFERENCES employers (employer_id))"
                         )