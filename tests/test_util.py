from util.utils import WelcomeMessage, config, create_database
import pytest

# Фикстура для подключения к БД
@pytest.fixture
def db_params():
    return config()

# Тестируем класс WelcomeMessage
def test_welcome_message():
    message = "Тестовое приветствие"
    welcome_message = WelcomeMessage(message)
    # Тестирование
    message_test = f"+{'-' * (len(message) + 4)}+\n|  {message}  |\n+{'-' * (len(message) + 4)}+\n"
    assert str(welcome_message) == message_test


