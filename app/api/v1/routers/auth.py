from fastapi import APIRouter, Body, Depends, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select
from datetime import datetime, timedelta

from models.login_history import LoginHistory
from utils.request_info import get_client_ip, get_user_agent
from core.login_otp import LoginOTP
from utils.otp import generate_otp, otp_expiry
from core.refresh_token import RefreshToken
from schemas.user_schema import UserCreate
from services.user_service import create_user, authenticate_user
from utils.dependencies import get_current_user, get_db
from fastapi.security import OAuth2PasswordRequestForm
from core.security import create_access_token, create_refresh_token, hash_password, verify_password

from models.user import User
from models.email_token import EmailToken
from models.token_blacklist import TokenBlacklist
from utils.token import generate_token
from utils.email import send_email, send_otp_email

MAX_FAILED_ATTEMPTS = 5
LOCK_TIME_MINUTES = 15

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    # 🔐 ALWAYS create normal user
    new_user = await create_user(
        db,
        user.name,
        user.email,
        user.password,
        user.role
    )

    # 🔑 Create verification token
    token, expiry = generate_token(minutes=15)

    db.add(EmailToken(
        user_id=new_user.id,
        token=token,
        expires_at=expiry
    ))
    await db.commit()

    # 📧 Send verification email (mock)
    send_email(
        new_user.email,
        "Verify your email",
        f"http://127.0.0.1:8000/auth/verify-email-page?token={token}"
    )

    return {"message": "Registration successful. Verify your email."}

@router.get("/verify-email")
async def verify_email(
    token: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(EmailToken).where(EmailToken.token == token)
    )
    record = result.scalar_one_or_none()

    if not record or record.expires_at < datetime.utcnow():
        raise HTTPException(400, "Invalid or expired token")

    user = await db.get(User, record.user_id)
    user.is_verified = True

    await db.delete(record)
    await db.commit()

    return {"message": "Email verified successfully"}

@router.get("/verify-email-page")
def verify_email_page():
    return FileResponse("templates/verify-email.html")


@router.post("/login")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == form_data.username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 🔒 Account lock check
    if user.locked_until and user.locked_until > datetime.utcnow():
        raise HTTPException(
            status_code=403,
            detail=f"Account locked until {user.locked_until}"
        )

    # ❌ Wrong password
    if not verify_password(form_data.password, user.password):
        user.failed_attempts += 1
        if user.failed_attempts >= 5:
            user.locked_until = datetime.utcnow() + timedelta(minutes=15)
            user.failed_attempts = 0
        await db.commit()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")

    # ✅ Reset lock counters
    user.failed_attempts = 0
    user.locked_until = None

    # 🔐 CREATE TOKENS
    access_token = create_access_token(
        {"sub": str(user.id), "role": user.role}
    )

    refresh_token = create_refresh_token()
    refresh_expires = datetime.utcnow() + timedelta(days=7)

    db.add(
        RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=refresh_expires
        )
    )

    # 🧾 SAVE LOGIN HISTORY
    db.add(
        LoginHistory(
            user_id=user.id,
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request)
        )
    )

    await db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get("/reset-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    return templates.TemplateResponse(
        "password.html",
        {"request": request}
    )

@router.post("/reset-password")
async def reset_password(
    email: str = Body(...),
    new_password: str = Body(...),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 🔐 Update password
    user.password = hash_password(new_password)
    await db.commit()

    return {"message": "Password reset successful"}


@router.post("/refresh-token")
async def refresh_access_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token == refresh_token
        )
    )
    token_obj = result.scalar_one_or_none()

    if not token_obj:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if token_obj.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expired")

    user = await db.get(User, token_obj.user_id)

    new_access_token = create_access_token(
        {"sub": str(user.id), "role": user.role}
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
@router.post("/login-otp")
async def login_with_otp(
    email: str,
    db: AsyncSession = Depends(get_db)
):
    # user validation code...

    otp = generate_otp()

    db.add(LoginOTP(
        email=email,
        otp=otp,
        expires_at=otp_expiry()
    ))
    await db.commit()

    # 🔥 Send OTP email
    send_otp_email(email, otp)

    return {"message": "OTP sent to your email"}


@router.post("/verify-otp")
async def verify_login_otp(
    email: str,
    otp: str,
    db: AsyncSession = Depends(get_db)
):
    # 🔍 Fetch OTP
    result = await db.execute(
        select(LoginOTP).where(
            LoginOTP.email == email,
            LoginOTP.otp == otp,
            LoginOTP.is_used == 0
        )
    )
    otp_entry = result.scalar_one_or_none()

    if not otp_entry:
        raise HTTPException(status_code=401, detail="Invalid OTP")

    if otp_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="OTP expired")

    # 🔐 Mark OTP as used
    otp_entry.is_used = 1
    await db.commit()

    # 👤 Fetch user
    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    # 🔑 Generate JWT
    access_token = create_access_token(
        {"sub": str(user.id), "role": user.role}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/logout")
async def logout(
    refresh_token: str,
    db: AsyncSession = Depends(get_db)
):
    await db.execute(
        delete(RefreshToken).where(
            RefreshToken.token == refresh_token
        )
    )
    await db.commit()

    return {"message": "Logged out successfully"}

@router.get("/login-history")
async def my_login_history(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(LoginHistory)
        .where(LoginHistory.user_id == user.id)
        .order_by(LoginHistory.logged_in_at.desc())
    )

    history = result.scalars().all()

    return [
        {
            "id": h.id,
            "logged_in_at": h.logged_in_at,
            "ip_address": h.ip_address,
            "user_agent": h.user_agent
        }
        for h in history
    ]

@router.get("/me")
async def me(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }
