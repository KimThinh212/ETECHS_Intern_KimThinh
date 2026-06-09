"""
tests/test_education_meta.py
Unit tests cho collection education_meta.
"""
import pytest
from datetime import datetime
from models.education_meta import (
    EducationMeta, VerificationStatus
)


class TestEducationMeta:
    """Test class cho EducationMeta."""

    def test_create_with_defaults(self):
        """Test tạo với giá trị mặc định."""
        meta = EducationMeta(education_id="E001")
        assert meta.education_id == "E001"
        assert meta.description is None
        assert meta.achievements == []
        assert meta.document_urls == []
        assert meta.verification_status == VerificationStatus.PENDING
        assert meta.verified_at is None

    def test_create_full(self):
        """Test tạo với đầy đủ dữ liệu."""
        meta = EducationMeta(
            education_id="E002",
            description="Học tại ĐHBK TP.HCM, ngành CNTT",
            achievements=["HSG Toán cấp tỉnh", "Giải 3 ACM"],
            document_urls=[
                "https://storage.etechs.vn/certs/E002_degree.pdf"
            ]
        )
        assert len(meta.achievements) == 2
        assert len(meta.document_urls) == 1

    def test_invalid_education_id_empty(self):
        """Test education_id rỗng → lỗi."""
        with pytest.raises(ValueError):
            EducationMeta(education_id="")

    def test_invalid_url_format(self):
        """Test URL không hợp lệ → lỗi."""
        with pytest.raises(ValueError):
            EducationMeta(
                education_id="E003",
                document_urls=["ftp://invalid-url.com/file.pdf"]
            )

    def test_verify_method(self):
        """Test phương thức verify."""
        meta = EducationMeta(education_id="E004")
        assert meta.verification_status == VerificationStatus.PENDING
        meta.verify()
        assert meta.verification_status == VerificationStatus.VERIFIED
        assert meta.verified_at is not None

    def test_reject_method(self):
        """Test phương thức reject."""
        meta = EducationMeta(education_id="E005")
        meta.verify()  # verify trước
        meta.reject()  # rồi reject
        assert meta.verification_status == VerificationStatus.REJECTED
        assert meta.verified_at is None

    def test_add_achievement(self):
        """Test thêm thành tích."""
        meta = EducationMeta(education_id="E006")
        meta.add_achievement("HSG Toán")
        meta.add_achievement("HSG Lý")
        meta.add_achievement("HSG Toán")  # trùng → bỏ qua
        assert len(meta.achievements) == 2

    def test_add_document_url(self):
        """Test thêm URL bằng cấp."""
        meta = EducationMeta(education_id="E007")
        meta.add_document_url("https://storage.etechs.vn/cert.pdf")
        assert len(meta.document_urls) == 1

    def test_verification_consistency(self):
        """Test verified_at tự động set khi status=verified."""
        meta = EducationMeta(
            education_id="E008",
            verification_status=VerificationStatus.VERIFIED
        )
        assert meta.verified_at is not None  # auto-set

    def test_to_mongo_dict(self):
        """Test chuyển đổi sang dict cho MongoDB."""
        meta = EducationMeta(
            education_id="E009",
            description="Test",
            achievements=["A", "B"]
        )
        data = meta.to_mongo_dict()
        assert isinstance(data, dict)
        assert data["education_id"] == "E009"
        assert isinstance(data["achievements"], list)
