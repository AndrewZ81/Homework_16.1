from flask import Flask  # Подключаем необходимые инструменты из модуля flask
from config import FlaskConfig  # Подключаем конфигурационный класс
from app.models import db  # Подключаем экземпляр БД

# Подключаем классы
from app.users.dao.users_dao import UsersDAO
from app.orders.dao.orders_dao import OrdersDAO
from app.offers.dao.offers_dao import OffersDAO

# Подключаем блюпринты
from app.users.users_view import users_blueprint
from app.orders.orders_view import orders_blueprint
from app.offers.offers_view import offers_blueprint

app = Flask(__name__)  # Создаём наше приложение
app.config.from_object(FlaskConfig)  # Подключаем для доступа к конфигурационным константам

# Регистрируем блюпринты
app.register_blueprint(users_blueprint)
app.register_blueprint(orders_blueprint)
app.register_blueprint(offers_blueprint)

db.init_app(app)  # Связываем БД с приложением


# Добавляем обработчики ошибок
@app.errorhandler(500)
def internal_server_error(error):
    return """<h3>Похоже, такого ID не существует.</h3>""", 500


@app.errorhandler(404)
def page_not_found(error):
    return """<h3>Похоже, такого пути не существует.</h3>""", 404


# Выполняем до первого запроса к приложению
@app.before_first_request
def load_tables():
    db.drop_all()  # Удаляем старые таблицы, опционально
    db.create_all()  # Создаём новые таблицы
    users = UsersDAO(FlaskConfig.USERS_PATH).get_users()  # Получаем пользователей в формате списка
    orders = OrdersDAO(FlaskConfig.ORDERS_PATH).get_orders()  # Получаем заказы в формате списка
    offers = OffersDAO(FlaskConfig.OFFERS_PATH).get_offers()  # Получаем отклики в формате списка

    # Наполняем таблицы данными
    db.session.add_all(users)
    db.session.add_all(orders)
    db.session.add_all(offers)

    db.session.commit()  # Сохраняем изменения


if __name__ == "__main__":
    app.run()
