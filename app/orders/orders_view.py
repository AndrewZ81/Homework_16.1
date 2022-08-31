from flask import Blueprint, jsonify, request  # Подключаем для создания блюпринтов
from app.models import Orders, db
from datetime import datetime
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


@orders_blueprint.route("/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    """
    Cоздаёт эндпоинт удаления одного заказа
    :return: Комментарий к операции
    """
    try:
        order = Orders.query.get(order_id)
        db.session.delete(order)
        db.session.commit()
    except Exception:
        raise Exception("Похоже, такого ID не существует")
    else:
        return f"<h3>Заказ с ID = {order_id} удалён</h3>"


@orders_blueprint.route("/", methods=["POST"])
def add_order():
    """
    Cоздаёт эндпоинт добавления одного заказа
    :return: Комментарий к операции
    """
    try:
        post_data = request.json
        order = Orders(
                       name=post_data["name"],
                       description=post_data["description"],
                       start_date=datetime.strptime(post_data["start_date"], "%m/%d/%Y"),
                       end_date=datetime.strptime(post_data["end_date"], "%m/%d/%Y"),
                       address=post_data["address"],
                       price=post_data["price"],
                       customer_id=post_data["customer_id"],
                       executor_id=post_data["executor_id"]
                      )
        db.session.add(order)
        db.session.commit()
    except KeyError:
        raise KeyError("Похоже, не все данные для заполнения присутствуют")
    else:
        return f"<h3>Заказ добавлен</h3>"


@orders_blueprint.route("/<int:order_id>", methods=["PUT"])
def modify_order(order_id):
    """
    Cоздаёт эндпоинт изменения одного заказа
    :return: Комментарий к операции
    """
    try:
        order = Orders.query.get(order_id)
        put_data = request.json
        if put_data.get("name"):
            order.name = put_data.get("name")
        if put_data.get("description"):
            order.description = put_data.get("description")
        if put_data.get("start_date"):
            order.start_date = put_data.get("start_date")
        if put_data.get("end_date"):
            order.end_date = put_data.get("end_date")
        if put_data.get("address"):
            order.address = put_data.get("address")
        if put_data.get("price"):
            order.price = put_data.get("price")
        if put_data.get("customer_id"):
            order.customer_id = put_data.get("customer_id")
        if put_data.get("executor_id"):
            order.executor_id = put_data.get("executor_id")
        db.session.add(order)
        db.session.commit()
    except Exception:
        raise Exception("Похоже, такого ID не существует")
    else:
        return f"<h3>Заказ изменен</h3>"
