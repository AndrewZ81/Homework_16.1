from flask import Flask, jsonify  # Подключаем необходимые инструменты из модуля flask
from sqlalchemy import ForeignKey, Column, String, Integer, Date
from config import FlaskConfig  # Подключаем конфигурационный класс
from flask_sqlalchemy import SQLAlchemy
from main_dao import DataDAO
from datetime import datetime

app = Flask(__name__)  # Создаём наше приложение
app.config.from_object(FlaskConfig)  # Подключаем для доступа к конфигурационным константам
database = SQLAlchemy(app)


class Users(database.Model):  # Создаём модель таблицы пользователей
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    age = Column(Integer)
    email = Column(String(100))
    role = Column(String(50))
    phone = Column(String(50))


class Orders(database.Model):  # Создаём модель таблицы заказов
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    address = Column(String(100))
    price = Column(Integer)
    customer_id = Column(Integer, ForeignKey('users.id'))
    executor_id = Column(Integer, ForeignKey('users.id'))


class Offers(database.Model):  # Создаём модель таблицы откликов
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    executor_id = Column(Integer, ForeignKey('users.id'))


users_as_list = DataDAO(FlaskConfig.USERS_PATH).load_data()  # Получаем пользователей в формате списка
orders_as_list = DataDAO(FlaskConfig.ORDERS_PATH).load_data()  # Получаем заказы в формате списка
offers_as_list = DataDAO(FlaskConfig.OFFERS_PATH).load_data()  # Получаем отклики в формате списка

database.drop_all()  # Удаляем старые таблицы, опционально
database.create_all()  # Создаём новые таблицы

users_for_append = []  # Заполняем таблицу пользователей
for i in users_as_list:
    user = Users(
                 id=i["id"], first_name=i["first_name"], last_name=i["last_name"], age=i["age"], email=i["email"],
                 role=i["role"], phone=i["phone"]
                 )
    users_for_append.append(user)
database.session.add_all(users_for_append)

orders_for_append = []  # Заполняем таблицу заказов
for i in orders_as_list:
    order = Orders(
                   id=i["id"], name=i["name"], description=i["description"],
                   start_date=datetime.strptime(i["start_date"], "%m/%d/%Y"),
                   end_date=datetime.strptime(i["end_date"], "%m/%d/%Y"), address=i["address"], price=i["price"],
                   customer_id=i["customer_id"], executor_id=i["executor_id"]
                  )
    orders_for_append.append(order)
database.session.add_all(orders_for_append)

offers_for_append = []  # Заполняем таблицу откликов
for i in offers_as_list:
    offer = Offers(id=i["id"], order_id=i["order_id"], executor_id=i["executor_id"])
    offers_for_append.append(offer)
database.session.add_all(offers_for_append)

database.session.commit()


@app.route("/users")  # Добавляем эндпоинт вывода всех пользователей
def show_all_users():
    users_list = Users.query.all()
    users_for_output = []
    for i in users_list:
        users_for_output.append(
            {"id": i.id,
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
    return jsonify(user_for_output)

# Добавляем обработчики ошибок
@app.errorhandler(500)
def internal_server_error(error):
    return """<h3>Похоже, такого ID не существует.</h3>""", 500


@app.errorhandler(404)
def page_not_found(error):
    return """<h3>Похоже, такого пути не существует.</h3>""", 404


if __name__ == "__main__":
    app.run()
