# Импортируем модуль JSON для работы с этим форматом
import json
from json import JSONDecodeError
from app.models import Users


class UsersDAO:  # Создаём DAO для заполнения таблицы Users БД

    def __init__(self, path):
        """
        Создаёт атрибут path
        :param path: Путь к файлу формата JSON
        """
        self.path = path

    def get_data(self):
        """
        Получает данные из файлов формата JSON
        :return: Список данных
        """
        try:
            file = open(self.path, encoding="utf-8")
            data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self.path} для загрузки не найден")
        except JSONDecodeError:
            raise ValueError(f"Файл {self.path} для загрузки не удалось считать")
        else:
            file.close()
            return data

    def get_users(self):
        """
        Создаёт пользователей для таблицы Users
        :return: Список пользователей
        """
        users = []
        for i in self.get_data():
            user = Users(
                         id=i["id"],
                         first_name=i["first_name"],
                         last_name=i["last_name"],
                         age=i["age"],
                         email=i["email"],
                         role=i["role"], phone=i["phone"]
                        )
            users.append(user)
        return users
