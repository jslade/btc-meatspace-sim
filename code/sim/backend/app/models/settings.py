"""Settings model for blockchain configuration."""
from sqlalchemy import Column, Integer
from app.database import Base


class Settings(Base):
    """Settings model for blockchain configuration."""
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, index=True)
    block_reward = Column(Integer, nullable=False, default=50)
    difficulty_target = Column(Integer, nullable=False, default=4)
