"""Mined transaction model."""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class MinedTxn(Base):
    """Mined transaction model."""
    __tablename__ = 'mined_txns'

    id = Column(Integer, primary_key=True, index=True)
    block_id = Column(Integer, ForeignKey('blocks.id'), nullable=False)
    txn_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    output = Column(Integer, nullable=True)
    spent_txn_id = Column(Integer, nullable=True)

    block = relationship('Block', back_populates='mined_txns')
    transaction = relationship('Transaction', back_populates='mined_txns')
