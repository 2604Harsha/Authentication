from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timedelta

from core.database import Base

class LoginOTP(Base):
    __tablename__ = "login_otps"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    otp = Column(String)
    expires_at = Column(DateTime)
    is_used = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)