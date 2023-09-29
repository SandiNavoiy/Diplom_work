import pandas as pd
import psycopg2
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


class DBManage:
    """Класс для работы с данными в БД"""

    def __init__(self, database_name: str, params: dict):
        self.database_name = database_name
        self.params = params
        self.conn = psycopg2.connect(dbname=self.database_name, **self.params)
        self.cur = self.conn.cursor()
        self.models = {}
        self.mse_scores = {}

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
            "price float, "
            "count float, "
            "add_cost float, "
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

    def load_data(self):
        # Загрузка данных из базы данных
        sql_query = f"SELECT price, count, add_cost, product FROM products"
        self.cur.execute(sql_query)
        columns = [desc[0] for desc in self.cur.description]
        data = self.cur.fetchall()
        self.data = pd.DataFrame(data, columns=columns)



    def train_models(self):
        # Разделение данных по продуктам и обучение моделей, линейная регрессия
        unique_products = self.data["product"].unique()
        for product in unique_products:
            product_data = self.data[self.data["product"] == product]
            X = product_data[["count", "add_cost"]]
            y = product_data["price"]
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            model = LinearRegression()
            model.fit(X_train, y_train)
            self.models[product] = model
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            self.mse_scores[product] = mse

    def train_models__not_line(self):
        unique_products = self.data["product"].unique()
        for product in unique_products:
            product_data = self.data[self.data["product"] == product]
            X = product_data[["count", "add_cost"]]
            y = product_data["price"]
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            self.models[product] = model
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            self.mse_scores[product] = mse

    def predict_prices_for_all_products(self):
        # Прогнозирование цен для всех продуктов
        predictions = {}
        for product in self.models:
            product_data = self.data[self.data["product"] == product].iloc[
                0
            ]  # Берем первую строку
            count = product_data["count"]
            add_cost = product_data["add_cost"]
            model = self.models[product]
            price = model.predict([[count, add_cost]])
            predictions[product] = price[0]
        return predictions

    def get_average_prices_for_each_product(self):
        unique_products = self.data["product"].unique()
        average_prices = {}
        for product in unique_products:
            # Запрос SQL для получения средней цены для конкретного продукта
            sql_query = f"""
                SELECT AVG(price) AS average_price
                FROM products
                WHERE product = '{product}'
            """
            self.cur.execute(sql_query)
            result = self.cur.fetchone()
            average_price = result[0] if result[
                                             0] is not None else 0.0  # Обработка случая, когда среднее значение равно NULL
            average_prices[product] = average_price
        return average_prices

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
            LIMIT 1
            """
        )
