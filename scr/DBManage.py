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
        conn_temp = psycopg2.connect(dbname="postgres", **self.params)
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
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS products "
            "(id SERIAL PRIMARY KEY, "
            "price NUMERIC, "
            "count INTEGER, "
            "add_cost NUMERIC, "
            "product VARCHAR(25), "
            "company VARCHAR(25))"
        )
        # Создание индекса по столбцу product, для ускорения работы
        self.cur.execute("CREATE INDEX product_index ON products (product);")

    def insert_table(self, csv_file):
        """ "Вставка данных"""
        self.connect_to_database()
        # Ускорение загрузки, вместо insert используем Copy, разница в разы!
        with open(csv_file, "r") as f:
            self.cur.copy_expert(
                f"COPY products(price, count, add_cost, company, product) FROM STDIN WITH CSV HEADER",
                f,
            )
        self.conn.commit()

    def close_connection(self):
        """Закрытие соединения с базой данных"""
        self.connect_to_database()
        self.cur.close()
        self.conn.close()

    def error_table(self):
        """Отлов ошибки отсудствия таблиц, чтоб не ломать код"""
        self.connect_to_database()
        # Запрос SQL
        self.cur.execute(
            """
            SELECT * 
            FROM products

            """
        )
