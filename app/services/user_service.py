from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from core.security import hash_password, verify_password

async def create_user(
        db: AsyncSession,
        name : str,
        email: str,
        password: str,
        role: str
):
    user = User(
        name=name,
        email=email,
        password=hash_password(password),
        role=role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user 

async def authenticate_user(
        db: AsyncSession,
        email: str,
        password: str
):
    result = await db.execute(
        select(User).where(User.email == email)
    )

    user = result.scalar_one_or_none()

    if not user:
        return None
    if not verify_password(password, user.password):
        return None 

    return user 

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()
