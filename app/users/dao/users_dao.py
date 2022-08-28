# Импортируем модуль JSON для работы с этим форматом
import json
from json import JSONDecodeError


class UsersDAO:  # Создаём DAO для выборки постов (всех или одного)

    def __init__(self, path):
        """
        Создаёт атрибут path
        :param path: Путь к файлу со всеми пользователями
        """
        self.path = path

    def load_all_users(self):
        """
        Загружает всех пользователей
        :return: Список пользователей
        """
        try:
            file = open(self.path, encoding="utf-8")
            all_users = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self.path} с пользователями для загрузки не найден")
        except JSONDecodeError:
            raise ValueError(f"Файл {self.path} с пользователями для загрузки не удалось считать")
        else:
            file.close()
            return all_users
