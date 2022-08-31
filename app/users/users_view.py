from flask import Blueprint, jsonify, request  # Подключаем для создания блюпринтов
from app.models import Users, db

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


@users_blueprint.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Cоздаёт эндпоинт удаления одного пользователя
    :return: Комментарий к операции
    """
    try:
        user = Users.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
    except Exception:
        raise Exception("Похоже, такого ID не существует")
    else:
        return f"<h3>Пользователь с ID = {user_id} удалён</h3>"


@users_blueprint.route("/", methods=["POST"])
def add_user():
    """
    Cоздаёт эндпоинт добавления одного пользователя
    :return: Комментарий к операции
    """
    try:
        post_data = request.json
        user = Users(
                     first_name=post_data["first_name"],
                     last_name=post_data["last_name"],
                     age=post_data["age"],
                     email=post_data["email"],
                     role=post_data["role"],
                     phone=post_data["phone"]
                    )
        db.session.add(user)
        db.session.commit()
    except KeyError:
        raise KeyError("Похоже, не все данные для заполнения присутствуют")
    else:
        return f"<h3>Пользователь добавлен</h3>"


@users_blueprint.route("/<int:user_id>", methods=["PUT"])
def modify_user(user_id):
    """
    Cоздаёт эндпоинт изменения одного пользователя
    :return: Комментарий к операции
    """
    try:
        user = Users.query.get(user_id)
        put_data = request.json
        if put_data.get("first_name"):
            user.first_name = put_data.get("first_name")
        if put_data.get("last_name"):
            user.last_name = put_data.get("last_name")
        if put_data.get("age"):
            user.age = put_data.get("age")
        if put_data.get("email"):
            user.email = put_data.get("email")
        if put_data.get("role"):
            user.role = put_data.get("role")
        if put_data.get("phone"):
            user.phone = put_data.get("phone")
        db.session.add(user)
        db.session.commit()
    except Exception:
        raise Exception("Похоже, такого ID не существует")
    else:
        return f"<h3>Пользователь изменен</h3>"
