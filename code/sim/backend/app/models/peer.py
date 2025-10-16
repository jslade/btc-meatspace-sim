"""Peer model for network nodes."""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Peer(Base):
    """Peer model for network nodes."""
    __tablename__ = 'peers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    heartbeat = Column(DateTime, default=datetime.utcnow)

    messages = relationship('Message', back_populates='peer')
    transactions = relationship('Transaction', back_populates='peer')
    blocks = relationship('Block', back_populates='peer')
