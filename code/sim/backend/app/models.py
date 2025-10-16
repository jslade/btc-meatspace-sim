"""Database models for Bitcoin Meatspace Simulator."""
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Entity(Base):
    """Entity model (person or merchant)."""
    __tablename__ = 'entities'

    id = Column(String, primary_key=True, index=True)
    type = Column(String, nullable=False)  # 'person' or 'merchant'
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    btc = Column(Float, nullable=False, default=0.0)
    vx = Column(Float, default=0.0)
    vy = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    transactions_sent = relationship('Transaction', foreign_keys='Transaction.from_id', back_populates='sender')
    transactions_received = relationship('Transaction', foreign_keys='Transaction.to_id', back_populates='receiver')


class Transaction(Base):
    """Transaction model."""
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    from_id = Column(String, ForeignKey('entities.id'), nullable=False)
    to_id = Column(String, ForeignKey('entities.id'), nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship('Entity', foreign_keys=[from_id], back_populates='transactions_sent')
    receiver = relationship('Entity', foreign_keys=[to_id], back_populates='transactions_received')
