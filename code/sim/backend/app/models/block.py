"""Block model for blockchain."""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Block(Base):
    """Block model for blockchain."""
    __tablename__ = 'blocks'

    id = Column(Integer, primary_key=True, index=True)
    peer_id = Column(Integer, ForeignKey('peers.id'), nullable=True)
    commitment = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    target = Column(Integer, nullable=True)
    nonce = Column(String, nullable=True)
    hash = Column(String, nullable=True)

    peer = relationship('Peer', back_populates='blocks')
    mined_txns = relationship('MinedTxn', back_populates='block')
