"""
services/metadata_service.py
Service CRUD cho MongoDB metadata collections.
Dùng chung cho cả student_profile_meta và education_meta.
"""
from typing import Optional, List, Type, TypeVar
from bson import ObjectId
from pymongo.collection import Collection
from config.database import Database
from models.base import BaseMetaModel

T = TypeVar("T", bound=BaseMetaModel)


class MetadataService:
    """
    Service CRUD tổng quát cho metadata collections.
    """

    def __init__(self, collection_name: str, db_name: str = None):
        self.db = Database.get_db(db_name)
        self.collection: Collection = self.db[collection_name]
        self.collection_name = collection_name

    # ── CREATE ──
    def create(self, model: BaseMetaModel) -> str:
        """
        Insert document mới vào MongoDB.
        Returns: inserted_id (string)
        """
        data = model.to_mongo_dict()
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    # ── READ ──
    def find_by_id(
        self, doc_id: str, model_class: Type[T]
    ) -> Optional[T]:
        """Tìm document theo _id."""
        doc = self.collection.find_one(
            {"_id": ObjectId(doc_id)}
        )
        return model_class.from_mongo(doc) if doc else None

    def find_by_ref_id(
        self, ref_field: str, ref_value: str,
        model_class: Type[T]
    ) -> Optional[T]:
        """
        Tìm document theo trường tham chiếu.
        """
        doc = self.collection.find_one({ref_field: ref_value})
        return model_class.from_mongo(doc) if doc else None

    def find_all(
        self, model_class: Type[T],
        filter_dict: dict = None,
        limit: int = 100
    ) -> List[T]:
        """Tìm nhiều documents với filter tùy chọn."""
        cursor = self.collection.find(
            filter_dict or {}
        ).limit(limit)
        return [
            model_class.from_mongo(doc) for doc in cursor
        ]

    # ── UPDATE ──
    def update(self, doc_id: str, model: BaseMetaModel) -> bool:
        data = model.to_mongo_dict()
        data.pop("_id", None)  # Không update _id
        result = self.collection.update_one(
            {"_id": ObjectId(doc_id)},
            {"$set": data}
        )
        return result.modified_count > 0

    def update_field(
        self, doc_id: str, field: str, value
    ) -> bool:
        """Cập nhật một trường cụ thể."""
        result = self.collection.update_one(
            {"_id": ObjectId(doc_id)},
            {"$set": {field: value}}
        )
        return result.modified_count > 0

    # ── DELETE ──
    def delete(self, doc_id: str) -> bool:
        """Xóa document theo _id."""
        result = self.collection.delete_one(
            {"_id": ObjectId(doc_id)}
        )
        return result.deleted_count > 0

    # ── UTILITY ──
    def count(self, filter_dict: dict = None) -> int:
        """Đếm số documents."""
        return self.collection.count_documents(
            filter_dict or {}
        )

    def create_indexes(self, indexes: list):
        """
        Tạo index cho collection.
        """
        for index in indexes:
            self.collection.create_index(index)
