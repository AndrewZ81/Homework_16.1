# Импортируем модуль JSON для работы с этим форматом
import json
from json import JSONDecodeError


class DataDAO:  # Создаём DAO для выборки данных из файлов формата JSON

    def __init__(self, path):
        """
        Создаёт атрибут path
        :param path: Путь к файлу формата JSON
        """
        self.path = path

    def load_data(self):
        """
        Загружает данные из файлов формата JSON
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
