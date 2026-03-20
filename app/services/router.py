from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# نموذج البيانات (Schema) لضمان صحة الإدخال
class Service(BaseModel):
    id: int
    name: str
    description: str
    type: str # 'individual' for technician, 'group' for workshop
    icon: Optional[str] = None

# بيانات وهمية للتجربة (سنربطها بـ Firebase لاحقاً)
fake_services_db = [
    {"id": 1, "name": "سباكة", "description": "إصلاح أعطال المياه والصرف", "type": "individual", "icon": "plumbing_icon.png"},
    {"id": 2, "name": "ورشة ترميم", "description": "بناء وإعادة هيكلة منازل", "type": "group", "icon": "construction_icon.png"},
]

@router.get("/", response_model=List[Service])
async def get_all_services():
    """جلب كافة الخدمات المتاحة في التطبيق (صيانة، ترحيل، تنظيف...)"""
    return fake_services_db

@router.post("/add", status_code=201)
async def add_new_service(service: Service):
    """إضافة خدمة جديدة للنظام (للمدير فقط مستقبلاً)"""
    fake_services_db.append(service.dict())
    return {"message": f"Service {service.name} added successfully!"}

@router.get("/{service_id}")
async def get_service_details(service_id: int):
    service = next((s for s in fake_services_db if s["id"] == service_id), None)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service