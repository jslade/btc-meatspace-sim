"""Database models for Bitcoin Meatspace Simulator."""
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Node(Base):
    """Network node model (represents a team/device)."""
    __tablename__ = 'nodes'

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    last_seen = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages_sent = relationship('Message', foreign_keys='Message.from_node_id', back_populates='sender')
    messages_received = relationship('Message', foreign_keys='Message.to_node_id', back_populates='receiver')


class Message(Base):
    """Message model for network communication."""
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    from_node_id = Column(String, ForeignKey('nodes.id'), nullable=False)
    to_node_id = Column(String, ForeignKey('nodes.id'), nullable=True)  # None for broadcast
    message_type = Column(String, nullable=False)  # 'transaction', 'broadcast', etc.
    content = Column(Text, nullable=False)  # JSON-encoded message content
    qr_data = Column(Text, nullable=True)  # QR code data if scanned
    status = Column(String, default='pending')  # 'pending', 'processed', 'archived'
    is_broadcast = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)

    sender = relationship('Node', foreign_keys=[from_node_id], back_populates='messages_sent')
    receiver = relationship('Node', foreign_keys=[to_node_id], back_populates='messages_received')


# Keep legacy models for backward compatibility
class Entity(Base):
    """Entity model (person or merchant) - legacy."""
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
    """Transaction model - legacy."""
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    from_id = Column(String, ForeignKey('entities.id'), nullable=False)
    to_id = Column(String, ForeignKey('entities.id'), nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship('Entity', foreign_keys=[from_id], back_populates='transactions_sent')
    receiver = relationship('Entity', foreign_keys=[to_id], back_populates='transactions_received')
