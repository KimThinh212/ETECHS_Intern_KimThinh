"""
config/database.py
Singleton class quản lý kết nối MongoDB.
Sử dụng python-dotenv để đọc biến môi trường từ file .env.
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


class Database:
    """Singleton class quản lý kết nối MongoDB."""
    _client = None
    _db = None

    @classmethod
    def get_client(cls) -> MongoClient:
        if cls._client is None:
            uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
            cls._client = MongoClient(uri)
        return cls._client

    @classmethod
    def get_db(cls, db_name: str = None):
        if db_name is None:
            db_name = os.getenv("MONGO_DB_NAME", "etechs_metadata")
        return cls.get_client()[db_name]

    @classmethod
    def close(cls):
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
