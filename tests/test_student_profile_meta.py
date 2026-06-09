"""
tests/test_student_profile_meta.py
Unit tests cho collection student_profile_meta.
"""
import pytest
from datetime import datetime
from models.student_profile_meta import (
    StudentProfileMeta, DisplayPreferences,
    PrivacySettings, Onboarding,
    PrivacyLevel, UserTag
)


class TestStudentProfileMeta:
    """Test class cho StudentProfileMeta."""

    def test_create_with_defaults(self):
        """Test tạo instance với giá trị mặc định."""
        meta = StudentProfileMeta(profile_id="P001")
        assert meta.profile_id == "P001"
        assert meta.display_preferences.theme == "light"
        assert meta.display_preferences.language == "vi"
        assert meta.privacy_settings.show_avatar == PrivacyLevel.PUBLIC
        assert meta.onboarding.is_completed is False
        assert meta.tags == []
        assert meta.ai_summary is None

    def test_create_with_custom_values(self):
        """Test tạo instance với giá trị tùy chỉnh."""
        meta = StudentProfileMeta(
            profile_id="P002",
            display_preferences=DisplayPreferences(
                theme="dark", language="en"
            ),
            tags=["active", "premium"],
            ai_summary="Học sinh giỏi toán"
        )
        assert meta.display_preferences.theme == "dark"
        assert "active" in meta.tags
        assert meta.ai_summary == "Học sinh giỏi toán"
        assert meta.ai_summary_at is not None  # auto-set

    def test_invalid_profile_id_empty(self):
        """Test profile_id rỗng → lỗi."""
        with pytest.raises(ValueError):
            StudentProfileMeta(profile_id="")

    def test_invalid_profile_id_too_long(self):
        """Test profile_id quá dài → lỗi."""
        with pytest.raises(ValueError):
            StudentProfileMeta(profile_id="A" * 17)

    def test_invalid_theme(self):
        """Test theme không hợp lệ → lỗi."""
        with pytest.raises(ValueError):
            DisplayPreferences(theme="rainbow")

    def test_tags_normalized(self):
        """Test tags được chuẩn hóa lowercase + unique."""
        meta = StudentProfileMeta(
            profile_id="P003",
            tags=["Active", " PREMIUM ", "active"]
        )
        assert "active" in meta.tags
        assert "premium" in meta.tags
        assert len(meta.tags) == 2  # loại bỏ trùng

    def test_to_mongo_dict(self):
        """Test chuyển đổi sang dict cho MongoDB."""
        meta = StudentProfileMeta(profile_id="P004")
        data = meta.to_mongo_dict()
        assert isinstance(data, dict)
        assert data["profile_id"] == "P004"
        assert isinstance(data["display_preferences"], dict)
        # Verify sub-model _id is not present (cleaned by override)
        assert "_id" not in data["display_preferences"]

    def test_onboarding_step(self):
        """Test hoàn thành bước onboarding."""
        meta = StudentProfileMeta(profile_id="P005")
        meta.complete_onboarding_step("setup_profile")
        assert "setup_profile" in meta.onboarding.steps_done
        assert meta.onboarding.last_step_at is not None
