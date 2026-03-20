from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta

router = APIRouter()

# نموذج عقد الصيانة للشركة
class CompanySubscription(BaseModel):
    id: int
    company_name: str
    plan_name: str  # مثال: Basic, Premium, Gold
    start_date: datetime
    next_visit: datetime
    status: str  # active, expired, pending

# قاعدة بيانات تجريبية للعقود
subscriptions_db = [
    {
        "id": 1,
        "company_name": "شركة الهندسية للمقاولات",
        "plan_name": "الذهبية (صيانة أسبوعية)",
        "start_date": datetime.now(),
        "next_visit": datetime.now() + timedelta(days=7),
        "status": "active"
    }
]

@router.get("/")
async def get_active_subscriptions():
    """عرض كافة عقود الشركات النشطة حالياً"""
    return [sub for sub in subscriptions_db if sub["status"] == "active"]

@router.post("/subscribe")
async def create_subscription(sub: CompanySubscription):
    """إضافة عقد صيانة جديد لشركة"""
    subscriptions_db.append(sub.dict())
    return {"message": f"Subscription for {sub.company_name} created successfully!"}

@router.get("/schedule/{company_id}")
async def get_maintenance_schedule(company_id: int):
    """جلب موعد الزيارة الدورية القادمة لشركة معينة"""
    sub = next((s for s in subscriptions_db if s["id"] == company_id), None)
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return {"company": sub["company_name"], "next_visit": sub["next_visit"]}