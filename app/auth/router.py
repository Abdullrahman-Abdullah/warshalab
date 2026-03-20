from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def test_auth():
    return {'status': 'Module auth is working'}
