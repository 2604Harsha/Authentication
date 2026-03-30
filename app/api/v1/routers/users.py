from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from utils.dependencies import get_current_user, admin_required, get_db
from services.user_service import get_all_users

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
async def get_me(user=Depends(get_current_user)):
    return user

@router.get("/all")
async def get_users(
    admin=Depends(admin_required),
    db: AsyncSession = Depends(get_db)
):
    return await get_all_users(db)
