"""
models/education_meta.py
Collection 2: education_meta
Bảng PG liên kết: education
"""
from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import Field, field_validator, model_validator
from models.base import BaseMetaModel


# ───────── Enum Definitions ─────────
class VerificationStatus(str, Enum):
    """Trạng thái xác minh tài liệu giáo dục."""
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"


# ───────── Main Model ─────────
class EducationMeta(BaseMetaModel):
    """
    Collection: education_meta
    Bảng PG liên kết: education
    """
    # ── Trường bắt buộc ──
    education_id: str = Field(
        ...,
        min_length=1,
        max_length=16,
        description="ID bản ghi học vấn — Ref → education.education_id"
    )

    # ── Trường tùy chọn ──
    description: Optional[str] = Field(
        default=None,
        description="Mô tả chi tiết quá trình học tập"
    )

    achievements: List[str] = Field(
        default_factory=list,
        description="Danh sách thành tích: HSG, giải thưởng..."
    )

    document_urls: List[str] = Field(
        default_factory=list,
        description="URL file bằng cấp/chứng chỉ trên Object Storage"
    )

    verification_status: VerificationStatus = Field(
        default=VerificationStatus.PENDING,
        description="Trạng thái xác minh tài liệu"
    )

    verified_at: Optional[datetime] = Field(
        default=None,
        description="Thời điểm admin xác minh — NULL nếu chưa xác minh"
    )

    # ── Validators ──
    @field_validator("education_id")
    @classmethod
    def validate_education_id(cls, v):
        """Chuẩn hóa education_id: trim whitespace."""
        v = v.strip()
        if not v:
            raise ValueError("education_id không được rỗng")
        if len(v) > 16:
            raise ValueError("education_id tối đa 16 ký tự")
        return v

    @field_validator("achievements")
    @classmethod
    def validate_achievements(cls, v):
        """Chuẩn hóa: trim whitespace, loại bỏ phần tử rỗng."""
        return [item.strip() for item in v if item.strip()]

    @field_validator("document_urls")
    @classmethod
    def validate_document_urls(cls, v):
        """Validate URLs: kiểm tra format cơ bản."""
        validated = []
        for url in v:
            url = url.strip()
            if not url:
                continue
            # Kiểm tra URL hợp lệ cơ bản
            if not (url.startswith("http://") or
                    url.startswith("https://") or
                    url.startswith("s3://")):
                raise ValueError(
                    f"URL không hợp lệ: {url}. "
                    f"Phải bắt đầu bằng http://, https://, hoặc s3://"
                )
            validated.append(url)
        return validated

    @model_validator(mode="after")
    def validate_verification_consistency(self):
        """
        Đảm bảo tính nhất quán
        """
        if self.verification_status == VerificationStatus.VERIFIED:
            if not self.verified_at:
                self.verified_at = datetime.utcnow()
        elif self.verification_status in (
            VerificationStatus.PENDING,
            VerificationStatus.REJECTED
        ):
            # Khi reject hoặc pending, xóa verified_at
            self.verified_at = None
        return self

    # ── Methods ──
    def verify(self):
        """Admin xác minh tài liệu."""
        self.verification_status = VerificationStatus.VERIFIED
        self.verified_at = datetime.utcnow()

    def reject(self):
        """Admin từ chối xác minh."""
        self.verification_status = VerificationStatus.REJECTED
        self.verified_at = None

    def add_achievement(self, achievement: str):
        """Thêm thành tích mới."""
        achievement = achievement.strip()
        if achievement and achievement not in self.achievements:
            self.achievements.append(achievement)

    def add_document_url(self, url: str):
        """Thêm URL bằng cấp/chứng chỉ."""
        url = url.strip()
        if url and url not in self.document_urls:
            # Validate URL format
            if not (url.startswith("http://") or
                    url.startswith("https://") or
                    url.startswith("s3://")):
                raise ValueError(f"URL không hợp lệ: {url}")
            self.document_urls.append(url)
