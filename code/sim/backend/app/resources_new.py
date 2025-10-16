"""API resources for Bitcoin Blockchain Simulator."""
import json
from datetime import datetime
from app.database import SessionLocal
from app.models import Settings, Peer, Message, Wallet, Transaction, MinedTxn, PendingTxn, Block


class SettingsResource:
    """Resource for blockchain settings."""

    def on_get(self, req, resp):
        """Get settings."""
        db = SessionLocal()
        try:
            settings = db.query(Settings).first()
            if not settings:
                # Create default settings
                settings = Settings(block_reward=50, difficulty_target=4)
                db.add(settings)
                db.commit()
                db.refresh(settings)
            
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
            settings = db.query(Settings).first()
            if not settings:
                settings = Settings()
                db.add(settings)
            
            data = json.loads(req.bounded_stream.read())
            if 'block_reward' in data:
                settings.block_reward = data['block_reward']
            if 'difficulty_target' in data:
                settings.difficulty_target = data['difficulty_target']
            
            db.commit()
            db.refresh(settings)
            
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
            peers = db.query(Peer).all()
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
            peer = Peer(name=data['name'])
            db.add(peer)
            db.commit()
            db.refresh(peer)
            
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
            messages = db.query(Message).order_by(Message.timestamp).all()
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
            message = Message(
                peer_id=data['peer_id'],
                content=data['content'],
                read=data.get('read', False),
                processed=data.get('processed', False)
            )
            db.add(message)
            db.commit()
            db.refresh(message)
            
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
            wallets = db.query(Wallet).all()
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
            wallet = Wallet(
                name=data['name'],
                salt=data['salt'],
                secret=data['secret'],
                pubkey=data['pubkey']
            )
            db.add(wallet)
            db.commit()
            db.refresh(wallet)
            
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
            transactions = db.query(Transaction).all()
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
            blocks = db.query(Block).order_by(Block.timestamp).all()
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
            
            resp.text = json.dumps({
                'id': block.id,
                'hash': block.hash
            })
            resp.status = '201 Created'
        finally:
            db.close()
