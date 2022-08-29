from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Column, String, Integer, Date

db = SQLAlchemy()


class Users(db.Model):  # Создаём модель таблицы пользователей
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    age = Column(Integer)
    email = Column(String(100))
    role = Column(String(50))
    phone = Column(String(50))


class Orders(db.Model):  # Создаём модель таблицы заказов
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


class Offers(db.Model):  # Создаём модель таблицы откликов
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    executor_id = Column(Integer, ForeignKey('users.id'))
