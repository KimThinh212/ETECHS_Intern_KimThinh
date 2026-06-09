"""
models/base.py
Base model cho tất cả MongoDB metadata collections.
Dùng Pydantic v2 để validation & serialization.
"""
from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import core_schema
from bson import ObjectId


class PyObjectId(str):
    """Custom type để xử lý ObjectId của MongoDB tương thích Pydantic v2."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(
                        lambda v: str(ObjectId(v)) if ObjectId.is_valid(v) else ValueError(f"Invalid ObjectId: {v}")
                    )
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )


class BaseMetaModel(BaseModel):
    """
    Base class cho tất cả metadata models.
    Cung cấp:
    - _id handling (ObjectId ↔ string)
    - Phương thức to_mongo_dict() để insert vào MongoDB
    - Phương thức from_mongo() để đọc từ MongoDB
    - created_at, updated_at tự động
    """
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,       # Cho phép dùng cả "id" và "_id"
        "arbitrary_types_allowed": True, # Cho phép ObjectId
    }

    def to_mongo_dict(self) -> dict:
        """
        Chuyển model thành dict phù hợp để insert vào MongoDB.
        - Bỏ trường _id nếu None (để MongoDB tự tạo ObjectId)
        - Cập nhật updated_at
        - Đảm bảo _id trong mongo là dạng ObjectId thực tế nếu có
        """
        data = self.model_dump(by_alias=True, exclude_none=False)
        if data.get("_id") is None:
            data.pop("_id", None)
        else:
            # Chuyển chuỗi string _id thành ObjectId cho MongoDB
            data["_id"] = ObjectId(data["_id"])
        data["updated_at"] = datetime.utcnow()
        return data

    @classmethod
    def from_mongo(cls, data: dict):
        """
        Tạo model instance từ document MongoDB.
        - Chuyển ObjectId thành string
        """
        if data is None:
            return None
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return cls(**data)
