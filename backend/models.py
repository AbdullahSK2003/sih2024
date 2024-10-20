from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String, index=True)
    ai_response = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())