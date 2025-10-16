"""Message model for peer communication."""
from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Message(Base):
    """Message model for peer communication."""
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    peer_id = Column(Integer, ForeignKey('peers.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    content = Column(Text, nullable=False)
    read = Column(Boolean, default=False)
    processed = Column(Boolean, default=False)

    peer = relationship('Peer', back_populates='messages')
