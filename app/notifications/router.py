from fastapi import APIRouter, HTTPException
from firebase_admin import messaging
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class NotificationPayload(BaseModel):
    token: str  # Token الخاص بجهاز الفني (يأتي من Flutter)
    title: str
    body: str
    data: Optional[dict] = None # لبيانات إضافية مثل رقم الطلب

@router.post("/send")
async def send_push_notification(payload: NotificationPayload):
    """إرسال إشعار لجهاز محدد (فني أو عميل)"""
    message = messaging.Message(
        notification=messaging.Notification(
            title=payload.title,
            body=payload.body,
        ),
        data=payload.data,
        token=payload.token,
    )
    
    try:
        response = messaging.send(message)
        return {"status": "success", "message_id": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/broadcast")
async def broadcast_to_topic(topic: str, title: str, body: str):
    """إرسال إشعار لكل الفنيين في تخصص معين (مثلاً: سباكة)"""
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        topic=topic,
    )
    messaging.send(message)
    return {"message": f"تم إرسال التنبيه لجميع المشتركين في {topic}"}