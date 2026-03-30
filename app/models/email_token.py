from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from core.database import Base

class EmailToken(Base):
    __tablename__ = "email_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),  # 👈 users MUST exist
        nullable=False
    )
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)
