from enum import Enum


class Start(Enum):
    START = "Вы успешно зарегистрировались\n"\
            "Ваш id - <code>{from_user}</code>"


class Overdue(Enum):
    OVERDUE = "Просрочена задача - {id}\n"\
              "<a href=\"{host}/task/{id}\">Ссылка</a>"
    SOON = "Скоро дедлайн задачи - {id}\n"\
           "<a href=\"{host}/task/{id}\">Ссылка</a>"
