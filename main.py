from flask import Flask  # Подключаем необходимые инструменты из модуля flask
from sqlalchemy import ForeignKey, Column, String, Integer, Date

from config import FlaskConfig  # Подключаем конфигурационный класс
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # Создаём наше приложение
app.config.from_object(FlaskConfig)  # Подключаем для доступа к конфигурационным константам
database = SQLAlchemy(app)


class Users(database.Model):
    __tablename__ = "users"
    id = Column(database.Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    age = Column(Integer)
    email = Column(String(100))
    role = Column(String(50))
    phone = Column(String(50))


class Orders(database.Model):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String(500))
    start_date = Column(Date)
    end_date =Column(Date)
    address = Column(String(100))
    price = Column(Integer)
    customer_id =Column(Integer, ForeignKey('users.id'))
    executor_id = Column(Integer, ForeignKey('users.id'))


class Offers(database.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    executor_id = Column(Integer, ForeignKey('users.id'))


database.create_all()

if __name__ == "__main__":
    app.run()
