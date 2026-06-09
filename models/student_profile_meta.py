"""
models/student_profile_meta.py
Collection 1: student_profile_meta
Bảng PG liên kết: profile
"""
from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import Field, field_validator, model_validator
from models.base import BaseMetaModel


# ───────── Enum Definitions ─────────
class PrivacyLevel(str, Enum):
    """Mức quyền riêng tư cho các thuộc tính profile."""
    PUBLIC = "public"
    FRIENDS_ONLY = "friends_only"
    PRIVATE = "private"


class UserTag(str, Enum):
    """Nhãn hệ thống gán cho user."""
    ACTIVE = "active"
    PREMIUM = "premium"
    SUSPENDED = "suspended"
    NEW_USER = "new_user"
    VERIFIED = "verified"


# ───────── Sub-Models (Nested Objects) ─────────
class DisplayPreferences(BaseMetaModel):
    theme: str = Field(default="light",
                       description="Giao diện: light / dark")
    language: str = Field(default="vi",
                          description="Ngôn ngữ: vi, en, ...")
    timezone: str = Field(default="Asia/Ho_Chi_Minh",
                          description="Múi giờ")

    @field_validator("theme")
    @classmethod
    def validate_theme(cls, v):
        allowed = ["light", "dark", "system"]
        if v not in allowed:
            raise ValueError(f"theme phải là một trong {allowed}")
        return v

    @field_validator("language")
    @classmethod
    def validate_language(cls, v):
        # Chuẩn hóa: chuyển về lowercase, trim whitespace
        return v.strip().lower()


class PrivacySettings(BaseMetaModel):
    show_avatar: PrivacyLevel = Field(
        default=PrivacyLevel.PUBLIC,
        description="Hiển thị avatar")
    show_bio: PrivacyLevel = Field(
        default=PrivacyLevel.PUBLIC,
        description="Hiển thị tiểu sử")
    show_interests: PrivacyLevel = Field(
        default=PrivacyLevel.FRIENDS_ONLY,
        description="Hiển thị sở thích")


class Onboarding(BaseMetaModel):
    is_completed: bool = Field(default=False,
                               description="Đã hoàn thành onboarding chưa")
    steps_done: List[str] = Field(default_factory=list,
                                  description="Các bước đã hoàn thành")
    last_step_at: Optional[datetime] = Field(
        default=None,
        description="Thời điểm hoàn thành bước cuối")


# ───────── Main Model ─────────
class StudentProfileMeta(BaseMetaModel):
    """
    Collection: student_profile_meta
    Bảng PG liên kết: profile
    """
    # ── Trường bắt buộc ──
    profile_id: str = Field(
        ...,
        min_length=1,
        max_length=16,
        description="ID hồ sơ học sinh — Ref → profile.profile_id"
    )

    # ── Trường tùy chọn (nested objects) ──
    display_preferences: DisplayPreferences = Field(
        default_factory=DisplayPreferences,
        description="Tuỳ chọn hiển thị: theme, language, timezone"
    )
    privacy_settings: PrivacySettings = Field(
        default_factory=PrivacySettings,
        description="Quyền riêng tư: show_avatar, show_bio, show_interests"
    )
    onboarding: Onboarding = Field(
        default_factory=Onboarding,
        description="Trạng thái onboarding"
    )

    # ── Tags ──
    tags: List[str] = Field(
        default_factory=list,
        description="Nhãn hệ thống: active, premium, suspended..."
    )

    # ── AI Summary ──
    ai_summary: Optional[str] = Field(
        default=None,
        description="Tóm tắt hồ sơ do AI sinh ra"
    )
    ai_summary_at: Optional[datetime] = Field(
        default=None,
        description="Thời điểm AI tạo summary gần nhất"
    )

    # ── Validators ──
    @field_validator("profile_id")
    @classmethod
    def validate_profile_id(cls, v):
        """Chuẩn hóa profile_id: trim whitespace."""
        v = v.strip()
        if not v:
            raise ValueError("profile_id không được rỗng")
        if len(v) > 16:
            raise ValueError("profile_id tối đa 16 ký tự")
        return v

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v):
        """Chuẩn hóa tags: lowercase, loại bỏ trùng lặp."""
        return list(set(tag.strip().lower() for tag in v if tag.strip()))

    @model_validator(mode="after")
    def validate_ai_summary_consistency(self):
        """Nếu có ai_summary thì phải có ai_summary_at."""
        if self.ai_summary and not self.ai_summary_at:
            self.ai_summary_at = datetime.utcnow()
        return self

    # ── Methods ──
    def to_mongo_dict(self) -> dict:
        """Override: chuyển nested objects thành dict."""
        data = super().to_mongo_dict()
        
        # Pydantic v2 recursive model_dump đã chuyển DisplayPreferences, etc thành dict.
        # Tuy nhiên, sub-models kế thừa từ BaseMetaModel sẽ có các trường '_id', 'created_at', 'updated_at'.
        for field in ["display_preferences", "privacy_settings", "onboarding"]:
            if field in data and isinstance(data[field], dict):
                # Loại bỏ _id nếu nó là None để dữ liệu MongoDB gọn sạch hơn
                if data[field].get("_id") is None:
                    data[field].pop("_id", None)
        return data

    def update_ai_summary(self, summary: str):
        """Cập nhật AI summary và timestamp."""
        self.ai_summary = summary
        self.ai_summary_at = datetime.utcnow()

    def complete_onboarding_step(self, step_name: str):
        """Đánh dấu hoàn thành một bước onboarding."""
        if step_name not in self.onboarding.steps_done:
            self.onboarding.steps_done.append(step_name)
            self.onboarding.last_step_at = datetime.utcnow()

    def mark_onboarding_completed(self):
        """Đánh dấu hoàn thành toàn bộ onboarding."""
        self.onboarding.is_completed = True
        self.onboarding.last_step_at = datetime.utcnow()
