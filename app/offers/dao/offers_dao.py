# Импортируем модуль JSON для работы с этим форматом
import json
from json import JSONDecodeError
from app.models import Offers


class OffersDAO:  # Создаём DAO для заполнения таблицы Offers БД

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

    def get_offers(self):
        """
        Создаёт отклики для таблицы Offers
        :return: Список откликов
        """
        offers = []
        for i in self.get_data():
            offer = Offers(
                           id=i["id"],
                           order_id=i["order_id"],
                           executor_id=i["executor_id"]
                          )
            offers.append(offer)
        return offers
