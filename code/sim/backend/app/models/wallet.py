"""Wallet model for team identity."""
from sqlalchemy import Column, Integer, String
from app.database import Base


class Wallet(Base):
    """Wallet model for team identity."""
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    salt = Column(String, nullable=False)
    secret = Column(String, nullable=False)
    pubkey = Column(String, nullable=False)
