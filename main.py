from util.utils import WelcomeMessage, interact_with_user


if __name__ == "__main__":
    #csv_filename = "csv_data.csv"
    print("Введите ваше имя")
    user_name = input()
    welcome_message = (
        f"{user_name}  - добро пожаловать в программу прогнозирования цен на продукты"
    )
    welcome = WelcomeMessage(welcome_message)
    print(welcome)

    # Запуск контекстного меню
    interact_with_user()
