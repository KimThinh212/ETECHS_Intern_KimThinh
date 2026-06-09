"""
main.py
Script demo tích hợp 2 collections với MongoDB.
Chạy: python main.py
"""
import pymongo
from datetime import datetime
from config.database import Database
from models.student_profile_meta import (
    StudentProfileMeta, DisplayPreferences,
    PrivacySettings, Onboarding, PrivacyLevel
)
from models.education_meta import (
    EducationMeta, VerificationStatus
)
from services.metadata_service import MetadataService


def demo_student_profile_meta():
    """Demo CRUD cho student_profile_meta."""
    print("=" * 60)
    print("DEMO: student_profile_meta")
    print("=" * 60)

    service = MetadataService("student_profile_meta")

    # Tạo index
    service.create_indexes([
        [("profile_id", pymongo.ASCENDING)]
    ])
    print("[✓] Index profile_id đã tạo")

    # CREATE
    meta = StudentProfileMeta(
        profile_id="P001",
        display_preferences=DisplayPreferences(
            theme="dark", language="vi",
            timezone="Asia/Ho_Chi_Minh"
        ),
        privacy_settings=PrivacySettings(
            show_avatar=PrivacyLevel.PUBLIC,
            show_bio=PrivacyLevel.FRIENDS_ONLY,
            show_interests=PrivacyLevel.PRIVATE
        ),
        tags=["active", "new_user"],
        ai_summary="Học sinh lớp 12, yêu thích toán và lập trình"
    )
    doc_id = service.create(meta)
    print(f"[✓] Created: _id = {doc_id}")

    # READ
    found = service.find_by_ref_id(
        "profile_id", "P001", StudentProfileMeta
    )
    if found:
        print(f"[✓] Found: profile_id={found.profile_id}")
        print(f"    Theme: {found.display_preferences.theme}")
        print(f"    Tags: {found.tags}")
        print(f"    AI Summary: {found.ai_summary}")

    # UPDATE - hoàn thành onboarding
    found.complete_onboarding_step("setup_profile")
    found.complete_onboarding_step("upload_avatar")
    found.mark_onboarding_completed()
    service.update(doc_id, found)
    print(f"[✓] Updated: onboarding completed")

    # COUNT
    total = service.count()
    print(f"[✓] Total documents: {total}")
    print()


def demo_education_meta():
    """Demo CRUD cho education_meta."""
    print("=" * 60)
    print("DEMO: education_meta")
    print("=" * 60)

    service = MetadataService("education_meta")

    # Tạo index
    service.create_indexes([
        [("education_id", pymongo.ASCENDING)]
    ])
    print("[✓] Index education_id đã tạo")

    # CREATE
    meta = EducationMeta(
        education_id="E001",
        description=(
            "Học tại Trường THPT Nguyễn Du, TP.HCM.\n"
            "Chuyên ban Toán-Tin. GPA: 9.2/10."
        ),
        achievements=[
            "HSG Toán cấp tỉnh 2024",
            "Giải 3 Olympic Tin học sinh viên 2025",
            "Học bổng toàn phần ĐHBK"
        ],
        document_urls=[
            "https://storage.etechs.vn/certs/E001_bangcap.pdf",
            "https://storage.etechs.vn/certs/E001_hsg_toan.pdf"
        ]
    )
    doc_id = service.create(meta)
    print(f"[✓] Created: _id = {doc_id}")

    # READ
    found = service.find_by_ref_id(
        "education_id", "E001", EducationMeta
    )
    if found:
        print(f"[✓] Found: education_id={found.education_id}")
        print(f"    Status: {found.verification_status.value}")
        print(f"    Achievements: {found.achievements}")

    # UPDATE - Admin xác minh
    found.verify()
    service.update(doc_id, found)
    print(f"[✓] Verified at: {found.verified_at}")

    # Thêm thành tích mới
    found.add_achievement("Chứng chỉ IELTS 7.5")
    found.add_document_url(
        "https://storage.etechs.vn/certs/E001_ielts.pdf"
    )
    service.update(doc_id, found)
    print(f"[✓] Added achievement & document")

    # COUNT
    total = service.count()
    print(f"[✓] Total documents: {total}")
    print()


if __name__ == "__main__":
    try:
        demo_student_profile_meta()
        demo_education_meta()
        print("\n✅ DEMO HOÀN TẤT THÀNH CÔNG!")
    except Exception as e:
        print(f"\n❌ LỖI: {e}")
    finally:
        Database.close()
