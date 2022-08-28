# Создаём класс для конфигурации приложения Flask
class FlaskConfig:
    JSON_AS_ASCII = False
    USERS_PATH = "data/users.json"
    ORDERS_PATH = "data/orders.json"
    OFFERS_PATH = "data/offers.json"
    SQLALCHEMY_DATABASE_URI = "sqlite:///data/database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
