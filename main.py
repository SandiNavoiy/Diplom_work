from util.utils import WelcomeMessage, interact_with_user, config

if __name__ == "__main__":

    print("Введите ваше имя")
    user_name = input()
    welcome_message = (
        f"{user_name}  - добро пожаловать в программу прогнозирования цен на продукты"
    )
    welcome = WelcomeMessage(welcome_message)
    print(welcome)

    # Запуск контекстного меню
    interact_with_user()
