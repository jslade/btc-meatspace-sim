"""Database models for Bitcoin Blockchain Simulator."""
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Settings(Base):
    """Settings model for blockchain configuration."""
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, index=True)
    block_reward = Column(Integer, nullable=False, default=50)
    difficulty_target = Column(Integer, nullable=False, default=4)


class Peer(Base):
    """Peer model for network nodes."""
    __tablename__ = 'peers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    heartbeat = Column(DateTime, default=datetime.utcnow)

    messages = relationship('Message', back_populates='peer')
    transactions = relationship('Transaction', back_populates='peer')
    blocks = relationship('Block', back_populates='peer')


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


class Wallet(Base):
    """Wallet model for team identity."""
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    salt = Column(String, nullable=False)
    secret = Column(String, nullable=False)
    pubkey = Column(String, nullable=False)


class Transaction(Base):
    """Transaction model with multiple inputs and outputs."""
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    peer_id = Column(Integer, ForeignKey('peers.id'), nullable=True)
    name = Column(String, nullable=True)
    amount = Column(Integer, nullable=True)
    
    # Inputs (up to 2)
    input_txn_id_1 = Column(String, nullable=True)
    input_txn_sig_1 = Column(String, nullable=True)
    input_txn_id_2 = Column(String, nullable=True)
    input_txn_sig_2 = Column(String, nullable=True)
    
    # Outputs (up to 5)
    output_amount_1 = Column(Integer, nullable=True)
    output_pk_1 = Column(String, nullable=True)
    output_amount_2 = Column(Integer, nullable=True)
    output_pk_2 = Column(String, nullable=True)
    output_amount_3 = Column(Integer, nullable=True)
    output_pk_3 = Column(String, nullable=True)
    output_amount_4 = Column(Integer, nullable=True)
    output_pk_4 = Column(String, nullable=True)
    output_amount_5 = Column(Integer, nullable=True)
    output_pk_5 = Column(String, nullable=True)

    peer = relationship('Peer', back_populates='transactions')
    mined_txns = relationship('MinedTxn', back_populates='transaction')
    pending_txns = relationship('PendingTxn', back_populates='transaction')


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


class PendingTxn(Base):
    """Pending transaction model."""
    __tablename__ = 'pending_txns'

    id = Column(Integer, primary_key=True, index=True)
    txn_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    transaction = relationship('Transaction', back_populates='pending_txns')


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
