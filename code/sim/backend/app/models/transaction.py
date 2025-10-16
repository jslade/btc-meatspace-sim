"""Transaction model with multiple inputs and outputs."""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


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
