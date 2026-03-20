from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# استيراد الـ Routers من المجلدات الفرعية
# ملاحظة: سنفترض وجود ملف router.py داخل كل مجلد
# من المهم استخدام المسار الكامل لـ Vercel
try:
    from app.auth import router as auth_router
    from app.services import router as services_router
    from app.orders import router as orders_router
    from app.subscriptions import router as subs_router
    from app.finance import router as finance_router
    from app.users import router as users_router
    from app.notifications import router as notifications_router
    from app.reviews import router as reviews_router
except ImportError:
    # هذا للتوافق إذا كنت تشغل السيرفر من داخل مجلد server مباشرة
    from app.auth import router as auth_router
    from app.services import router as services_router
    from app.orders import router as orders_router
    from app.subscriptions import router as subs_router
    from app.finance import router as finance_router    
    from app.users import router as users_router
    from app.notifications import router as notifications_router
    from app.reviews import router as reviews_router




app = FastAPI(
    title="Warsha Lab API",
    description="Backend for Technician and Workshop services in Syria",
    version="1.0.0"
)

# إعدادات الـ CORS للسماح لتطبيق Flutter والويب بالاتصال بالباك أند
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # في الإنتاج يفضل تحديد الدومين الخاص بك
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ربط الأقسام (Routes) بالسيرفر الأساسي
app.include_router(auth_router.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(services_router.router, prefix="/api/services", tags=["Services & Categories"])
app.include_router(orders_router.router, prefix="/api/orders", tags=["Orders & Workshops"])
app.include_router(subs_router.router, prefix="/api/subscriptions", tags=["Corporate Subscriptions"])
app.include_router(finance_router.router, prefix="/api/finance", tags=["Finance & Commissions"])
app.include_router(users_router.router, prefix="/api/users", tags=["Users & Verifiyng"])
app.include_router(notifications_router.router, prefix="/api/notifications", tags=["Notifications"])
app.include_router(reviews_router.router, prefix="/api/reviews", tags=["Reviews & Complaints"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Warsha Lab API",
        "status": "Running",
        "docs": "/docs"
    }