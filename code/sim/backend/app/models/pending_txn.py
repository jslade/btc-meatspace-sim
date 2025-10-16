"""Pending transaction model."""
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class PendingTxn(Base):
    """Pending transaction model."""
    __tablename__ = 'pending_txns'

    id = Column(Integer, primary_key=True, index=True)
    txn_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    transaction = relationship('Transaction', back_populates='pending_txns')
