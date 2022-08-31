from flask import Blueprint, jsonify, request  # Подключаем для создания блюпринтов
from app.models import Offers, db

# Создаём блюпринт страницы откликов (-а)
offers_blueprint = Blueprint("offers_blueprint", __name__, url_prefix="/offers")


@offers_blueprint.route("/", methods=["GET"])
def show_all_offers():
    """
    Создаёт эндпоинт вывода всех откликов
    :return: Список всех откликов
    """
    offers_list = Offers.query.all()
    offers_for_output = []
    for i in offers_list:
        offers_for_output.append(
                                 {
                                  "id": i.id,
                                  "order_id": i.order_id,
                                  "executor_id": i.executor_id
                                 }
                                )
    return jsonify(offers_for_output)


@offers_blueprint.route("/<int:offer_id>", methods=["GET"])
def show_offer(offer_id):
    """
    Создаёт эндпоинт вывода одного отклика
    :return: Словарь из одного отклика
    """
    try:
        offer = Offers.query.get(offer_id)
        offer_for_output = {
                            "id": offer.id,
                            "order_id": offer.order_id,
                            "executor_id": offer.executor_id
                           }
    except AttributeError:
        raise AttributeError("Похоже, такого ID не существует")
    else:
        return jsonify(offer_for_output)


@offers_blueprint.route("/<int:offer_id>", methods=["DELETE"])
def delete_offer(offer_id):
    """
    Cоздаёт эндпоинт удаления одного отклика
    :return: Комментарий к операции
    """
    try:
        offer = Offers.query.get(offer_id)
        db.session.delete(offer)
        db.session.commit()
    except Exception:
        raise Exception("Похоже, такого ID не существует")
    else:
        return f"<h3>Отклик с ID = {offer_id} удалён</h3>"


@offers_blueprint.route("/", methods=["POST"])
def add_offer():
    """
    Cоздаёт эндпоинт добавления одного отклика
    :return: Комментарий к операции
    """
    try:
        post_data = request.json
        offer = Offers(
                       order_id=post_data["order_id"],
                       executor_id=post_data["executor_id"]
                      )
        db.session.add(offer)
        db.session.commit()
    except KeyError:
        raise KeyError("Похоже, не все данные для заполнения присутствуют")
    else:
        return f"<h3>Отклик добавлен</h3>"


@offers_blueprint.route("/<int:offer_id>", methods=["PUT"])
def modify_offer(offer_id):
    """
    Cоздаёт эндпоинт изменения одного отклика
    :return: Комментарий к операции
    """
    try:
        offer = Offers.query.get(offer_id)
        put_data = request.json
        if put_data.get("order_id"):
            offer.order_id = put_data.get("order_id")
        if put_data.get("executor_id"):
            offer.executor_id = put_data.get("executor_id")
        db.session.add(offer)
        db.session.commit()
    except Exception:
        raise Exception("Похоже, такого ID не существует")
    else:
        return f"<h3>Отклик изменен</h3>"
