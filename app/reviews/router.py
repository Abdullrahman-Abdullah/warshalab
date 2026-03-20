from fastapi import APIRouter, HTTPException
from database import get_db
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter()
db = get_db()

# نموذج التقييم الشامل
class Review(BaseModel):
    order_id: str
    client_id: str
    tech_id: str
    rating_tech: int  # من 1 إلى 5
    rating_service: int
    rating_app: int
    comment: Optional[str] = None

# نموذج الشكوى
class Complaint(BaseModel):
    order_id: str
    user_id: str
    reason: str
    details: str

@router.post("/submit")
async def submit_review(review: Review):
    """تسجيل تقييم ثلاثي (فني، خدمة، تطبيق)"""
    review_data = review.dict()
    review_data["created_at"] = datetime.now()
    
    # حفظ في Firebase
    db.collection("reviews").add(review_data)
    
    # تحديث متوسط تقييم الفني تلقائياً (منطق برمجي بسيط)
    # سنضيفه لاحقاً لرفع رتبة الفنيين المتميزين
    return {"message": "شكرًا لتقييمك، رأيك يساعدنا على التحسن!"}

@router.post("/report-issue")
async def file_complaint(complaint: Complaint):
    """نظام الشكاوى والإلغاء مع مراجعة من قبل الإدارة"""
    complaint_data = complaint.dict()
    complaint_data["status"] = "open" # مفتوحة للمراجعة
    complaint_data["created_at"] = datetime.now()
    
    doc_ref = db.collection("complaints").add(complaint_data)
    return {"complaint_id": doc_ref[1].id, "message": "تم استلام شكواك، سيتواصل معك فريق الدعم فوراً"}