# Импортируем модуль JSON для работы с этим форматом
import json
from json import JSONDecodeError
from datetime import datetime
from app.models import Orders


class OrdersDAO:  # Создаём DAO для заполнения таблицы Orders БД

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

    def get_orders(self):
        """
        Cоздаёт заказы для таблицы Orders
        :return: Список заказов
        """
        orders = []
        for i in self.get_data():
            order = Orders(
                id=i["id"],
                name=i["name"],
                description=i["description"],
                start_date=datetime.strptime(i["start_date"], "%m/%d/%Y"),
                end_date=datetime.strptime(i["end_date"], "%m/%d/%Y"),
                address=i["address"],
                price=i["price"],
                customer_id=i["customer_id"],
                executor_id=i["executor_id"]
            )
            orders.append(order)
        return orders
