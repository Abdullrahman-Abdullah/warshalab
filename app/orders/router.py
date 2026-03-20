from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def test_orders():
    return {'status': 'Module orders is working'}
