from database import Base
from sqlalchemy import Column, Integer, String, DateTime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, auto_increment=True, index=True)
    user_name = Column(String, unique=True, nullable=False)
    user_email = Column(String, unique=True, nullable=False)
    user_password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
