from flask import Blueprint, jsonify  # Подключаем для создания блюпринтов
from app.models import Orders

# Создаём блюпринт страницы заказов (-а)
orders_blueprint = Blueprint("orders_blueprint", __name__, url_prefix="/orders")


@orders_blueprint.route("/", methods=["GET"])
def show_all_orders():
    """
    Создаёт эндпоинт вывода всех заказов
    :return: Список всех заказов
    """
    orders_list = Orders.query.all()
    orders_for_output = []
    for i in orders_list:
        orders_for_output.append(
                                {
                                 "id": i.id,
                                 "name": i.name,
                                 "description": i.description,
                                 "start_date": i.start_date,
                                 "end_date": i.end_date,
                                 "address": i.address,
                                 "price": i.price,
                                 "customer_id": i.customer_id,
                                 "executor_id": i.executor_id
                                }
                               )
    return jsonify(orders_for_output)


@orders_blueprint.route("/<int:order_id>", methods=["GET"])
def show_order(order_id):
    """
    Cоздаёт эндпоинт вывода одного заказа
    :return: Словарь из одного заказа
    """
    try:
        order = Orders.query.get(order_id)
        order_for_output = {
                            "id": order.id,
                            "name": order.name,
                            "description": order.description,
                            "start_date": order.start_date,
                            "end_date": order.end_date,
                            "address": order.address,
                            "price": order.price,
                            "customer_id": order.customer_id,
                            "executor_id": order.executor_id
                           }
    except AttributeError:
        raise AttributeError("Похоже, такого ID не существует")
    else:
        return jsonify(order_for_output)
