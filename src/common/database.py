import psycopg2
from dotenv import find_dotenv, load_dotenv
from threading import Lock, Thread
import os
import logging

load_dotenv(find_dotenv())
DB_NAME = os.environ.get("POSTGRES_DATABASE")
DB_HOST = os.environ.get("POSTGRES_HOST")
DB_USERNAME = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

logging.basicConfig(
    level=logging.INFO,
    format="SERVICE %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class DatabaseConnectorMetaclass(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class DatabaseConnector(metaclass=DatabaseConnectorMetaclass):
    def __init__(self):
        try:
            logger.info("Attempting to connect to postgres")
            self.conn = psycopg2.connect(dbname=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST)
            logger.info("Successfully connected to postgres")
        except:
            logger.error("Unable to connect to postgres", exc_info=True)
            raise Exception("Failed to connect to postgres database")
