from flask import Blueprint, jsonify  # Подключаем для создания блюпринтов
from app.models import Users

# Создаём блюпринт страницы пользователей (-я)
users_blueprint = Blueprint("users_blueprint", __name__, url_prefix="/users")


@users_blueprint.route("/", methods=["GET"])
def show_all_users():
    """
    Создаёт эндпоинт вывода всех пользователей
    :return: Список всех пользователей
    """
    users_list = Users.query.all()
    users_for_output = []
    for i in users_list:
       users_for_output.append(
                               {
                                "id": i.id,
                                "first_name": i.first_name,
                                "last_name": i.last_name,
                                "age": i.age,
                                "email": i.email,
                                "role": i.role,
                                "phone": i.phone
                               }
                              )
    return jsonify(users_for_output)


@users_blueprint.route("/<int:user_id>", methods=["GET"])
def show_user(user_id):
    """
    Cоздаёт эндпоинт вывода одного пользователя
    :return: Словарь из одного пользователя
    """
    try:
        user = Users.query.get(user_id)
        user_for_output = {
                           "id": user.id,
                           "first_name": user.first_name,
                           "last_name": user.last_name,
                           "age": user.age,
                           "email": user.email,
                           "role": user.role,
                           "phone": user.phone
                          }
    except AttributeError:
        raise AttributeError("Похоже, такого ID не существует")
    else:
        return jsonify(user_for_output)
