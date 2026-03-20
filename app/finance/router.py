from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

# نموذج المعاملة المالية
class Transaction(BaseModel):
    order_id: int
    tech_id: int
    total_amount: float
    commission_rate: float = 0.05  # الـ 5% التي اتفقنا عليها
    net_commission: float = 0.0

# سجل العمليات المالية
finance_log = []

@router.post("/calculate-commission")
async def process_payment(transaction: Transaction):
    """حساب واقتطاع العمولة عند انتهاء الطلب"""
    # حساب قيمة الـ 5%
    transaction.net_commission = transaction.total_amount * transaction.commission_rate
    
    # إضافة العملية للسجل
    finance_log.append(transaction.dict())
    
    return {
        "status": "success",
        "tech_id": transaction.tech_id,
        "total_collected": transaction.total_amount,
        "our_cut": transaction.net_commission,
        "message": f"تم تسجيل عمولة بقيمة {transaction.net_commission} ليرة"
    }

@router.get("/total-earnings")
async def get_total_earnings():
    """عرض إجمالي أرباح التطبيق من العمولات"""
    total = sum(item['net_commission'] for item in finance_log)
    return {"total_app_revenue": total, "transactions_count": len(finance_log)}

@router.get("/tech-debt/{tech_id}")
async def get_tech_debt(tech_id: int):
    """معرفة المبالغ التي يجب على الفني دفعها للتطبيق"""
    debt = sum(item['net_commission'] for item in finance_log if item['tech_id'] == tech_id)
    return {"tech_id": tech_id, "total_debt": debt}