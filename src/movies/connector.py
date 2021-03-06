import os

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabaseConnector(metaclass=SingletonMeta):
    def __init__(self):
        pass 

    def get_postgres_uri(self):
        host = os.environ.get("DB_HOST", "172.22.0.2")
        port = 5432
        password = os.environ.get("DB_PASS", "abc123")
        user, db_name = "movies", "movies"

        print(f"{host} {port} {password} {user} {db_name}")
        print(f"postgresql://{user}:{password}@{host}:{port}/{db_name}")
        return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


