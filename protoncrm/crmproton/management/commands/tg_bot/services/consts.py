from enum import Enum


class Start(Enum):
    START = ("Вы успешно зарегистрировались\n"
             "Ваш id - <code>{from_user}</code>\n"
             "Вернитесь на сайт и вставьте полученный id")
    DEEPLINK = "Ваш аккаунт успешно подключен для отправки уведомлений"


class Overdue(Enum):
    OVERDUE = ("Просрочена задача - {id}\n"
               "<a href=\"{host}/task/{id}\">Ссылка</a>")
    SOON = ("Скоро дедлайн задачи - {id}\n"
            "<a href=\"{host}/task/{id}\">Ссылка</a>")
