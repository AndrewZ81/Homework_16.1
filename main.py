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
    return """<h3>Ошибка при работе с базой данных.</h3>""", 500


@app.errorhandler(404)
def page_not_found(error):
    return """<h3>Такого пути не существует.</h3>""", 404


@app.before_first_request
def load_tables():
    """
    Создаёт и заполняет таблицы до первого запроса к приложению, сохраняя изменения
    :return: Таблицы с сохранёнными данными
    """
    # Удаляём старые таблицы и создаём макеты новых. ОПЦИОНАЛЬНО!
    db.drop_all()
    db.create_all()

    # Получаем данные для наполнения таблиц
    users = UsersDAO(FlaskConfig.USERS_PATH).get_users()
    orders = OrdersDAO(FlaskConfig.ORDERS_PATH).get_orders()
    offers = OffersDAO(FlaskConfig.OFFERS_PATH).get_offers()

    # Наполняем таблицы данными
    db.session.add_all(users)
    db.session.add_all(orders)
    db.session.add_all(offers)

    db.session.commit()  # Сохраняем изменения


if __name__ == "__main__":
    app.run()
