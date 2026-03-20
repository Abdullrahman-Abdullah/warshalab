from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from database import get_db
import uuid

router = APIRouter()
db = get_db()

@router.post("/verify-technician/{tech_id}")
async def upload_documents(
    tech_id: str,
    full_name: str = Form(...),
    specialty: str = Form(...),
    identity_card: UploadFile = File(...)
):
    """رفع وثائق التوثيق للفني أو الورشة"""
    
    # في الإنتاج: سنقوم برفع الصورة إلى Firebase Storage والحصول على رابط
    # حالياً سنحفظ الرابط وهمياً ونحدث البيانات في Firestore
    file_extension = identity_card.filename.split(".")[-1]
    file_name = f"verify_{tech_id}_{uuid.uuid4()}.{file_extension}"
    
    doc_ref = db.collection("technicians").document(tech_id)
    doc_ref.set({
        "full_name": full_name,
        "specialty": specialty,
        "id_document_url": f"gs://warsha-lab/verification/{file_name}",
        "is_verified": False, # يبدأ بـ False حتى يوافق المدير
        "status": "pending_review"
    }, merge=True)
    
    return {"message": "تم رفع الوثائق بنجاح، وهي قيد المراجعة من قبل إدارة ورشة"}

@router.get("/pending-verifications")
async def get_pending_techs():
    """خاص بالمدير: عرض الفنيين الذين ينتظرون التوثيق"""
    techs = db.collection("technicians").where("is_verified", "==", False).stream()
    return [doc.to_dict() | {"id": doc.id} for doc in techs]

@router.patch("/approve-tech/{tech_id}")
async def approve_technician(tech_id: str):
    """موافقة المدير على الفني ليدخل سوق العمل"""
    db.collection("technicians").document(tech_id).update({"is_verified": True, "status": "active"})
    return {"message": "تم توثيق الفني بنجاح، يمكنه الآن استقبال الطلبات"}