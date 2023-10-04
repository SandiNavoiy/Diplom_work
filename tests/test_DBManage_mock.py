# import pytest
# import pandas as pd
# from scr.DBManage import DBManage
# import psycopg2
#
# from util.utils import config
#
#
# # Создаем мок-объект для базы данных
# @pytest.fixture
# def mock_db(mocker):
#     mocker.patch("psycopg2.connect")
#     db = mocker.MagicMock()
#     return db
#
#
# # Создаем мок-объект для DBManage
# @pytest.fixture
# def db_manager(mock_db, mocker):
#     params = config("../database.ini")
#     mocker.patch("scr.DBManage.config", return_value=params)
#     db_manager = DBManage("testing", params)
#     db_manager.conn = mock_db
#     return db_manager
#
#
# # Тест для создания таблицы
# def test_create_tables(db_manager, mocker):
#     mocker.patch("scr.DBManage.psycopg2")
#     db_manager.create_tables()
#     # Проверяем, что был вызван метод execute
#     db_manager.conn.cursor().execute.assert_called()
#
#
# # Тест для вставки данных в таблицу
# def test_insert_table(db_manager, mocker):
#     mocker.patch("scr.DBManage.pd.read_csv")
#     mocker.patch("scr.DBManage.os.path.isfile", return_value=True)
#     mocker.patch("scr.DBManage.os.remove")
#     mocker.patch("scr.DBManage.psycopg2")
#
#     db_manager.create_tables()
#     db_manager.insert_table("test_data.csv")
#     # Проверяем, что был вызван метод execute
#     db_manager.conn.cursor().execute.assert_called()
#
#
# # Тест для загрузки данных
# def test_load_data(db_manager, mocker):
#     mocker.patch("scr.DBManage.pd.DataFrame")
#     mocker.patch("scr.DBManage.psycopg2")
#
#     db_manager.load_data()
#     # Проверяем, что был вызван метод execute
#     db_manager.conn.cursor().execute.assert_called()
#
#
# # Тест для обучения модели (линейная регрессия)
# def test_train_models(db_manager, mocker):
#     mocker.patch("scr.DBManage.pd.read_csv")
#     mocker.patch("scr.DBManage.pd.DataFrame")
#     mocker.patch("scr.DBManage.train_test_split")
#     mocker.patch("scr.DBManage.LinearRegression")
#     mocker.patch("scr.DBManage.mean_squared_error")
#     mocker.patch("scr.DBManage.psycopg2")
#
#     db_manager.load_data()
#     db_manager.train_models()
#     # Проверяем, что был вызван метод fit
#     db_manager.models["A"].fit.assert_called()
#     # Проверяем, что был вызван метод predict
#     db_manager.models["A"].predict.assert_called()
#     # Проверяем, что был вызван метод mean_squared_error
#     db_manager.mean_squared_error.assert_called()
#
#
# # Тест для обучения модели (случайные деревья)
# def test_train_models_not_line(db_manager, mocker):
#     mocker.patch("scr.DBManage.pd.read_csv")
#     mocker.patch("scr.DBManage.pd.DataFrame")
#     mocker.patch("scr.DBManage.train_test_split")
#     mocker.patch("scr.DBManage.RandomForestRegressor")
#     mocker.patch("scr.DBManage.mean_squared_error")
#     mocker.patch("scr.DBManage.psycopg2")
#
#     db_manager.load_data()
#     db_manager.train_models__not_line()
#     # Проверяем, что был вызван метод fit
#     db_manager.models["A"].fit.assert_called()
#     # Проверяем, что был вызван метод predict
#     db_manager.models["A"].predict.assert_called()
#     # Проверяем, что был вызван метод mean_squared_error
#     db_manager.mean_squared_error.assert_called()
#
#
# # Тест для прогнозирования цен для всех продуктов
# def test_predict_prices_for_all_products(db_manager, mocker):
#     mocker.patch("scr.DBManage.pd.read_csv")
#     mocker.patch("scr.DBManage.pd.DataFrame")
#     mocker.patch("scr.DBManage.train_test_split")
#     mocker.patch("scr.DBManage.LinearRegression")
#     mocker.patch("scr.DBManage.mean_squared_error")
#     mocker.patch("scr.DBManage.psycopg2")
#
#     db_manager.load_data()
#     db_manager.train_models()
#     db_manager.predict_prices_for_all_products()
#     # Проверяем, что был вызван метод predict
#     db_manager.models["A"].predict.assert_called()
#
#
# # Тест для получения средних цен для каждого продукта
# def test_get_average_prices_for_each_product(db_manager, mocker):
#     mocker.patch("scr.DBManage.pd.read_csv")
#     mocker.patch("scr.DBManage.pd.DataFrame")
#     mocker.patch("scr.DBManage.psycopg2")
#
#     db_manager.load_data()
#     db_manager.get_average_prices_for_each_product()
#     # Проверяем, что был вызван метод execute
#     db_manager.conn.cursor().execute.assert_called()
#
#
# # Тест для получения максимальных и минимальных цен для каждого продукта
# def test_get_max_min_price_for_each_product(db_manager, mocker):
#     mocker.patch("scr.DBManage.pd.read_csv")
#     mocker.patch("scr.DBManage.pd.DataFrame")
#     mocker.patch("scr.DBManage.psycopg2")
#
#     db_manager.load_data()
#     db_manager.get_max_min_price_for_each_product()
#     # Проверяем, что был вызван метод execute
#     db_manager.conn.cursor().execute.assert_called()
#
#
# # Тест для получения количества записей для каждого продукта
# def test_get_record_count_for_each_product(db_manager, mocker):
#     mocker.patch("scr.DBManage.pd.read_csv")
#     mocker.patch("scr.DBManage.pd.DataFrame")
#     mocker.patch("scr.DBManage.psycopg2")
#
#     db_manager.load_data()
#     db_manager.get_record_count_for_each_product()
#     # Проверяем, что был вызван метод execute
#     db_manager.conn.cursor().execute.assert_called()
#
#
# # Тест для закрытия соединения
# def test_close_connection(db_manager, mocker):
#     mocker.patch("scr.DBManage.psycopg2")
#
#     db_manager.close_connection()
#     # Проверяем, что был вызван метод close
#     db_manager.conn.close.assert_called()
#
#
# # Тест для обработки ошибки отсутствия таблицы
# def test_error_table(db_manager, mocker):
#     mocker.patch("scr.DBManage.psycopg2")
#
#     db_manager.error_table()
#     # Проверяем, что был вызван метод execute
#     db_manager.conn.cursor().execute.assert_called()
#
# # Другие тесты можно написать аналогично, для остальных методов
