import os

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabaseConnector(metaclass=SingletonMeta):
    def __init__(self):
        self.host = os.environ.get("DB_HOST", "172.22.0.2")
        self.port = 5432
        self.password = os.environ.get("DB_PASS", "abc123")
        self.user, self.db_name = "movies", "movies"

    def get_postgres_uri(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


