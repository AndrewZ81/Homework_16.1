# Создаём класс для конфигурации приложения Flask
class FlaskConfig:
    JSON_AS_ASCII = False
    USERS_PATH = "data/users.json"
    ORDERS_PATH = "data/orders.json"
    OFFERS_PATH = "data/offers.json"
    USERS_DATABASE_PATH = "data/users.db"
    ORDERS_DATABASE_PATH = "data/orders.db"
    OFFERS_DATABASE_PATH = "data/offers.db"
