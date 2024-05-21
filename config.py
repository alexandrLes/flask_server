class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://admin:123@localhost:5432/main_db'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    TESTING = False

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
