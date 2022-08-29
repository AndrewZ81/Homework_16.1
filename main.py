from flask import Flask, jsonify  # Подключаем необходимые инструменты из модуля flask
from config import FlaskConfig  # Подключаем конфигурационный класс
from models import db, Users
from main_dao import DataDAO

app = Flask(__name__)  # Создаём наше приложение
app.config.from_object(FlaskConfig)  # Подключаем для доступа к конфигурационным константам
db.init_app(app)


@app.route("/users")  # Добавляем эндпоинт вывода всех пользователей
def show_all_users():
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


@app.route("/users/<int:user_id>")  # Добавляем эндпоинт вывода одного пользователя
def show_user(user_id):
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


# Добавляем обработчики ошибок
@app.errorhandler(500)
def internal_server_error(error):
    return """<h3>Похоже, такого ID не существует.</h3>""", 500


@app.errorhandler(404)
def page_not_found(error):
    return """<h3>Похоже, такого пути не существует.</h3>""", 404


@app.before_first_request
def load_tables():
    db.drop_all()  # Удаляем старые таблицы, опционально
    db.create_all()  # Создаём новые таблицы
    users = DataDAO(FlaskConfig.USERS_PATH).create_users()  # Получаем пользователей в формате списка
    orders = DataDAO(FlaskConfig.ORDERS_PATH).create_orders()  # Получаем заказы в формате списка
    offers = DataDAO(FlaskConfig.OFFERS_PATH).create_offers()  # Получаем отклики в формате списка
    db.session.add_all(users)
    db.session.add_all(orders)
    db.session.add_all(offers)
    db.session.commit()


if __name__ == "__main__":
    app.run()
