"""Service layer for blockchain operations."""
from typing import List, Dict, Optional
from app.database import SessionLocal
from app.models.settings import Settings
from app.models.peer import Peer
from app.models.message import Message
from app.models.wallet import Wallet
from app.models.transaction import Transaction
from app.models.block import Block
from app.models.mined_txn import MinedTxn
from app.models.pending_txn import PendingTxn


class SettingsService:
    """Service for settings operations."""
    
    @staticmethod
    def get_or_create_settings(db) -> Settings:
        """Get settings or create default if none exist."""
        settings = db.query(Settings).first()
        if not settings:
            settings = Settings(block_reward=50, difficulty_target=4)
            db.add(settings)
            db.commit()
            db.refresh(settings)
        return settings
    
    @staticmethod
    def update_settings(db, data: Dict) -> Settings:
        """Update settings."""
        settings = db.query(Settings).first()
        if not settings:
            settings = Settings()
            db.add(settings)
        
        if 'block_reward' in data:
            settings.block_reward = data['block_reward']
        if 'difficulty_target' in data:
            settings.difficulty_target = data['difficulty_target']
        
        db.commit()
        db.refresh(settings)
        return settings


class PeerService:
    """Service for peer operations."""
    
    @staticmethod
    def get_all_peers(db) -> List[Peer]:
        """Get all peers."""
        return db.query(Peer).all()
    
    @staticmethod
    def create_peer(db, name: str) -> Peer:
        """Create a new peer."""
        peer = Peer(name=name)
        db.add(peer)
        db.commit()
        db.refresh(peer)
        return peer


class MessageService:
    """Service for message operations."""
    
    @staticmethod
    def get_all_messages(db) -> List[Message]:
        """Get all messages ordered by timestamp."""
        return db.query(Message).order_by(Message.timestamp).all()
    
    @staticmethod
    def create_message(db, peer_id: int, content: str, read: bool = False, processed: bool = False) -> Message:
        """Create a new message."""
        message = Message(
            peer_id=peer_id,
            content=content,
            read=read,
            processed=processed
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message


class WalletService:
    """Service for wallet operations."""
    
    @staticmethod
    def get_all_wallets(db) -> List[Wallet]:
        """Get all wallets."""
        return db.query(Wallet).all()
    
    @staticmethod
    def create_wallet(db, name: str, salt: str, secret: str, pubkey: str) -> Wallet:
        """Create a new wallet."""
        wallet = Wallet(
            name=name,
            salt=salt,
            secret=secret,
            pubkey=pubkey
        )
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
        return wallet


class TransactionService:
    """Service for transaction operations."""
    
    @staticmethod
    def get_all_transactions(db) -> List[Transaction]:
        """Get all transactions."""
        return db.query(Transaction).all()
    
    @staticmethod
    def create_transaction(db, data: Dict) -> Transaction:
        """Create a new transaction."""
        transaction = Transaction(
            peer_id=data.get('peer_id'),
            name=data.get('name'),
            amount=data.get('amount'),
            input_txn_id_1=data.get('input_txn_id_1'),
            input_txn_sig_1=data.get('input_txn_sig_1'),
            input_txn_id_2=data.get('input_txn_id_2'),
            input_txn_sig_2=data.get('input_txn_sig_2'),
            output_amount_1=data.get('output_amount_1'),
            output_pk_1=data.get('output_pk_1'),
            output_amount_2=data.get('output_amount_2'),
            output_pk_2=data.get('output_pk_2'),
            output_amount_3=data.get('output_amount_3'),
            output_pk_3=data.get('output_pk_3'),
            output_amount_4=data.get('output_amount_4'),
            output_pk_4=data.get('output_pk_4'),
            output_amount_5=data.get('output_amount_5'),
            output_pk_5=data.get('output_pk_5')
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction


class BlockService:
    """Service for block operations."""
    
    @staticmethod
    def get_all_blocks(db) -> List[Block]:
        """Get all blocks ordered by timestamp."""
        return db.query(Block).order_by(Block.timestamp).all()
    
    @staticmethod
    def create_block(db, data: Dict) -> Block:
        """Create a new block."""
        block = Block(
            peer_id=data.get('peer_id'),
            commitment=data.get('commitment'),
            target=data.get('target'),
            nonce=data.get('nonce'),
            hash=data.get('hash')
        )
        db.add(block)
        db.commit()
        db.refresh(block)
        return block
