# models/login_history.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from core.database import Base

class LoginHistory(Base):
    __tablename__ = "login_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    logged_in_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
