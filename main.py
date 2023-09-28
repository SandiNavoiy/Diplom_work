import pandas as pd

from util.utils import WelcomeMessage, interact_with_user
UserWarning: pandas only supports SQLAlchemy connectable (engine/connection) or database string URI or sqlite3 DBAPI2 connection. Other DBAPI2 objects are not tested. Please consider using SQLAlchemy.
  self.data = pd.read_sql_query(sql_query, self.conn)
# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    csv_filename = "csv_data.csv"
    # df = pd.read_csv(csv_filename)
    # print(df.head(3)) #вывод перывых
    # print(df.tail(1)) #вывод последних
    # print(len(df)) #количество значений в таблице
    print("Введине веше имя")
    user_name = input()
    welcome_message = (
        f"{user_name}  - добро пожаловать в программу прогнозирования цен на продукты"
    )
    welcome = WelcomeMessage(welcome_message)
    print(welcome)

    # Запуск контекстного меню
    interact_with_user()

    # print(df.groupby('price').count())
    # print(df.groupby('count').count())
    # print(df.groupby('add_cost').count())
    # print(df.groupby('product').count())
    #
