"""Resource controllers for API endpoints."""
import json
from app.database import SessionLocal
from app.services import (
    SettingsService,
    PeerService,
    MessageService,
    WalletService,
    TransactionService,
    BlockService
)


class SettingsResource:
    """Resource for blockchain settings."""

    def on_get(self, req, resp):
        """Get settings."""
        db = SessionLocal()
        try:
            settings = SettingsService.get_or_create_settings(db)
            resp.text = json.dumps({
                'block_reward': settings.block_reward,
                'difficulty_target': settings.difficulty_target
            })
            resp.status = '200 OK'
        finally:
            db.close()

    def on_put(self, req, resp):
        """Update settings."""
        db = SessionLocal()
        try:
            data = json.loads(req.bounded_stream.read())
            settings = SettingsService.update_settings(db, data)
            
            resp.text = json.dumps({
                'block_reward': settings.block_reward,
                'difficulty_target': settings.difficulty_target
            })
            resp.status = '200 OK'
        finally:
            db.close()


class PeerResource:
    """Resource for peers."""

    def on_get(self, req, resp):
        """Get all peers."""
        db = SessionLocal()
        try:
            peers = PeerService.get_all_peers(db)
            resp.text = json.dumps([{
                'id': p.id,
                'name': p.name,
                'heartbeat': p.heartbeat.isoformat() if p.heartbeat else None
            } for p in peers])
            resp.status = '200 OK'
        finally:
            db.close()

    def on_post(self, req, resp):
        """Create a peer."""
        db = SessionLocal()
        try:
            data = json.loads(req.bounded_stream.read())
            peer = PeerService.create_peer(db, data['name'])
            
            resp.text = json.dumps({
                'id': peer.id,
                'name': peer.name,
                'heartbeat': peer.heartbeat.isoformat() if peer.heartbeat else None
            })
            resp.status = '201 Created'
        finally:
            db.close()


class MessageResource:
    """Resource for messages."""

    def on_get(self, req, resp):
        """Get all messages."""
        db = SessionLocal()
        try:
            messages = MessageService.get_all_messages(db)
            resp.text = json.dumps([{
                'id': m.id,
                'peer_id': m.peer_id,
                'timestamp': m.timestamp.isoformat(),
                'content': m.content,
                'read': m.read,
                'processed': m.processed
            } for m in messages])
            resp.status = '200 OK'
        finally:
            db.close()

    def on_post(self, req, resp):
        """Create a message."""
        db = SessionLocal()
        try:
            data = json.loads(req.bounded_stream.read())
            message = MessageService.create_message(
                db,
                data['peer_id'],
                data['content'],
                data.get('read', False),
                data.get('processed', False)
            )
            
            resp.text = json.dumps({
                'id': message.id,
                'peer_id': message.peer_id,
                'timestamp': message.timestamp.isoformat(),
                'content': message.content,
                'read': message.read,
                'processed': message.processed
            })
            resp.status = '201 Created'
        finally:
            db.close()


class WalletResource:
    """Resource for wallets."""

    def on_get(self, req, resp):
        """Get all wallets."""
        db = SessionLocal()
        try:
            wallets = WalletService.get_all_wallets(db)
            resp.text = json.dumps([{
                'id': w.id,
                'name': w.name,
                'salt': w.salt,
                'pubkey': w.pubkey
            } for w in wallets])
            resp.status = '200 OK'
        finally:
            db.close()

    def on_post(self, req, resp):
        """Create a wallet."""
        db = SessionLocal()
        try:
            data = json.loads(req.bounded_stream.read())
            wallet = WalletService.create_wallet(
                db,
                data['name'],
                data['salt'],
                data['secret'],
                data['pubkey']
            )
            
            resp.text = json.dumps({
                'id': wallet.id,
                'name': wallet.name,
                'salt': wallet.salt,
                'pubkey': wallet.pubkey
            })
            resp.status = '201 Created'
        finally:
            db.close()


class TransactionResource:
    """Resource for transactions."""

    def on_get(self, req, resp):
        """Get all transactions."""
        db = SessionLocal()
        try:
            transactions = TransactionService.get_all_transactions(db)
            resp.text = json.dumps([{
                'id': t.id,
                'peer_id': t.peer_id,
                'name': t.name,
                'amount': t.amount,
                'input_txn_id_1': t.input_txn_id_1,
                'input_txn_id_2': t.input_txn_id_2,
                'output_amount_1': t.output_amount_1,
                'output_pk_1': t.output_pk_1,
                'output_amount_2': t.output_amount_2,
                'output_pk_2': t.output_pk_2
            } for t in transactions])
            resp.status = '200 OK'
        finally:
            db.close()

    def on_post(self, req, resp):
        """Create a transaction."""
        db = SessionLocal()
        try:
            data = json.loads(req.bounded_stream.read())
            transaction = TransactionService.create_transaction(db, data)
            
            resp.text = json.dumps({'id': transaction.id})
            resp.status = '201 Created'
        finally:
            db.close()


class BlockResource:
    """Resource for blocks."""

    def on_get(self, req, resp):
        """Get all blocks."""
        db = SessionLocal()
        try:
            blocks = BlockService.get_all_blocks(db)
            resp.text = json.dumps([{
                'id': b.id,
                'peer_id': b.peer_id,
                'commitment': b.commitment,
                'timestamp': b.timestamp.isoformat(),
                'target': b.target,
                'nonce': b.nonce,
                'hash': b.hash
            } for b in blocks])
            resp.status = '200 OK'
        finally:
            db.close()

    def on_post(self, req, resp):
        """Create a block."""
        db = SessionLocal()
        try:
            data = json.loads(req.bounded_stream.read())
            block = BlockService.create_block(db, data)
            
            resp.text = json.dumps({
                'id': block.id,
                'hash': block.hash
            })
            resp.status = '201 Created'
        finally:
            db.close()
