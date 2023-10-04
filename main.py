from util.utils import WelcomeMessage, interact_with_user
from colorama import init, Fore

# Для WIN10+
init(autoreset=True)

if __name__ == "__main__":
    print(Fore.YELLOW + "Введите ваше имя")
    user_name = input()
    welcome_message = (
        f"{user_name}  - добро пожаловать в программу прогнозирования цен на продукты"
    )
    welcome = WelcomeMessage(welcome_message)
    print(Fore.BLUE + f'{welcome}')

    # Запуск контекстного меню
    interact_with_user()
