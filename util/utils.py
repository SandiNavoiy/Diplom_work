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

