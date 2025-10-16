"""API resources for Bitcoin Meatspace Simulator."""
import json
import random
import string
import socket
from datetime import datetime
from app.database import SessionLocal
from app.models import Entity, Transaction, Node, Message


class EntityResource:
    """Resource for managing entities."""

    def on_get(self, req, resp):
        """Get all entities."""
        db = SessionLocal()
        try:
            entities = db.query(Entity).all()
            resp.text = json.dumps([{
                'id': e.id,
                'type': e.type,
                'x': e.x,
                'y': e.y,
                'btc': e.btc,
                'vx': e.vx,
                'vy': e.vy
            } for e in entities])
            resp.status = '200 OK'
        finally:
            db.close()

    def on_post(self, req, resp):
        """Create a new entity."""
        db = SessionLocal()
        try:
            data = json.loads(req.bounded_stream.read())
            entity_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))
            
            entity = Entity(
                id=entity_id,
                type=data['type'],
                x=data['x'],
                y=data['y'],
                btc=data.get('btc', random.random() * 0.5),
                vx=data.get('vx', 0.0),
                vy=data.get('vy', 0.0)
            )
            
            db.add(entity)
            db.commit()
            db.refresh(entity)
            
            resp.text = json.dumps({
                'id': entity.id,
                'type': entity.type,
                'x': entity.x,
                'y': entity.y,
                'btc': entity.btc,
                'vx': entity.vx,
                'vy': entity.vy
            })
            resp.status = '201 Created'
        finally:
            db.close()

    def on_delete(self, req, resp):
        """Delete all entities."""
        db = SessionLocal()
        try:
            db.query(Transaction).delete()
            db.query(Entity).delete()
            db.commit()
            resp.text = json.dumps({'message': 'All entities deleted'})
            resp.status = '200 OK'
        finally:
            db.close()


class EntityDetailResource:
    """Resource for managing individual entities."""

    def on_get(self, req, resp, entity_id):
        """Get a specific entity."""
        db = SessionLocal()
        try:
            entity = db.query(Entity).filter(Entity.id == entity_id).first()
            if entity:
                resp.text = json.dumps({
                    'id': entity.id,
                    'type': entity.type,
                    'x': entity.x,
                    'y': entity.y,
                    'btc': entity.btc,
                    'vx': entity.vx,
                    'vy': entity.vy
                })
                resp.status = '200 OK'
            else:
                resp.status = '404 Not Found'
        finally:
            db.close()

    def on_put(self, req, resp, entity_id):
        """Update an entity."""
        db = SessionLocal()
        try:
            entity = db.query(Entity).filter(Entity.id == entity_id).first()
            if not entity:
                resp.status = '404 Not Found'
                return

            data = json.loads(req.bounded_stream.read())
            entity.x = data.get('x', entity.x)
            entity.y = data.get('y', entity.y)
            entity.btc = data.get('btc', entity.btc)
            entity.vx = data.get('vx', entity.vx)
            entity.vy = data.get('vy', entity.vy)
            
            db.commit()
            db.refresh(entity)
            
            resp.text = json.dumps({
                'id': entity.id,
                'type': entity.type,
                'x': entity.x,
                'y': entity.y,
                'btc': entity.btc,
                'vx': entity.vx,
                'vy': entity.vy
            })
            resp.status = '200 OK'
        finally:
            db.close()


class TransactionResource:
    """Resource for managing transactions."""

    def on_get(self, req, resp):
        """Get all transactions."""
        db = SessionLocal()
        try:
            transactions = db.query(Transaction).all()
            resp.text = json.dumps([{
                'id': t.id,
                'from_id': t.from_id,
                'to_id': t.to_id,
                'amount': t.amount,
                'timestamp': t.timestamp.isoformat()
            } for t in transactions])
            resp.status = '200 OK'
        finally:
            db.close()

    def on_post(self, req, resp):
        """Create a new transaction."""
        db = SessionLocal()
        try:
            data = json.loads(req.bounded_stream.read())
            
            from_entity = db.query(Entity).filter(Entity.id == data['from_id']).first()
            to_entity = db.query(Entity).filter(Entity.id == data['to_id']).first()
            
            if not from_entity or not to_entity:
                resp.status = '404 Not Found'
                resp.text = json.dumps({'error': 'Entity not found'})
                return
            
            amount = data['amount']
            if from_entity.btc < amount:
                resp.status = '400 Bad Request'
                resp.text = json.dumps({'error': 'Insufficient BTC'})
                return
            
            # Update balances
            from_entity.btc -= amount
            to_entity.btc += amount
            
            # Create transaction
            transaction = Transaction(
                from_id=data['from_id'],
                to_id=data['to_id'],
                amount=amount
            )
            
            db.add(transaction)
            db.commit()
            db.refresh(transaction)
            
            resp.text = json.dumps({
                'id': transaction.id,
                'from_id': transaction.from_id,
                'to_id': transaction.to_id,
                'amount': transaction.amount,
                'timestamp': transaction.timestamp.isoformat()
            })
            resp.status = '201 Created'
        finally:
            db.close()


class StatsResource:
    """Resource for getting simulation statistics."""

    def on_get(self, req, resp):
        """Get simulation statistics."""
        db = SessionLocal()
        try:
            people_count = db.query(Entity).filter(Entity.type == 'person').count()
            merchant_count = db.query(Entity).filter(Entity.type == 'merchant').count()
            transaction_count = db.query(Transaction).count()
            
            entities = db.query(Entity).all()
            total_btc = sum(e.btc for e in entities)
            
            resp.text = json.dumps({
                'people': people_count,
                'merchants': merchant_count,
                'transactions': transaction_count,
                'total_btc': total_btc
            })
            resp.status = '200 OK'
        finally:
            db.close()


class NodeResource:
    """Resource for managing network nodes."""

    def on_get(self, req, resp):
        """Get all nodes."""
        db = SessionLocal()
        try:
            nodes = db.query(Node).all()
            resp.text = json.dumps([{
                'id': n.id,
                'name': n.name,
                'ip_address': n.ip_address,
                'is_active': n.is_active,
                'last_seen': n.last_seen.isoformat() if n.last_seen else None
            } for n in nodes])
            resp.status = '200 OK'
        finally:
            db.close()

    def on_post(self, req, resp):
        """Register or update a node."""
        db = SessionLocal()
        try:
            data = json.loads(req.bounded_stream.read())
            node_id = data.get('id', ''.join(random.choices(string.ascii_lowercase + string.digits, k=9)))
            
            # Check if node exists
            node = db.query(Node).filter(Node.id == node_id).first()
            
            if node:
                # Update existing node
                node.name = data.get('name', node.name)
                node.ip_address = data.get('ip_address', node.ip_address)
                node.is_active = data.get('is_active', True)
                node.last_seen = datetime.utcnow()
            else:
                # Create new node
                node = Node(
                    id=node_id,
                    name=data.get('name', f'Node-{node_id[:6]}'),
                    ip_address=data.get('ip_address'),
                    is_active=True
                )
                db.add(node)
            
            db.commit()
            db.refresh(node)
            
            resp.text = json.dumps({
                'id': node.id,
                'name': node.name,
                'ip_address': node.ip_address,
                'is_active': node.is_active
            })
            resp.status = '201 Created' if not node else '200 OK'
        finally:
            db.close()


class MessageResource:
    """Resource for managing messages."""

    def on_get(self, req, resp):
        """Get messages for a node."""
        node_id = req.get_param('node_id')
        status = req.get_param('status', default='pending')
        
        db = SessionLocal()
        try:
            query = db.query(Message)
            
            if node_id:
                # Get messages for specific node (received or broadcast)
                query = query.filter(
                    (Message.to_node_id == node_id) | (Message.is_broadcast == True)
                )
            
            if status != 'all':
                query = query.filter(Message.status == status)
            
            messages = query.order_by(Message.timestamp).all()
            
            resp.text = json.dumps([{
                'id': m.id,
                'from_node_id': m.from_node_id,
                'to_node_id': m.to_node_id,
                'message_type': m.message_type,
                'content': m.content,
                'qr_data': m.qr_data,
                'status': m.status,
                'is_broadcast': m.is_broadcast,
                'timestamp': m.timestamp.isoformat(),
                'processed_at': m.processed_at.isoformat() if m.processed_at else None
            } for m in messages])
            resp.status = '200 OK'
        finally:
            db.close()

    def on_post(self, req, resp):
        """Create and send a message."""
        db = SessionLocal()
        try:
            data = json.loads(req.bounded_stream.read())
            
            # Verify sender node exists
            from_node = db.query(Node).filter(Node.id == data['from_node_id']).first()
            if not from_node:
                resp.status = '404 Not Found'
                resp.text = json.dumps({'error': 'Sender node not found'})
                return
            
            is_broadcast = data.get('is_broadcast', False)
            to_node_id = None if is_broadcast else data.get('to_node_id')
            
            # Verify receiver node exists if not broadcast
            if not is_broadcast and to_node_id:
                to_node = db.query(Node).filter(Node.id == to_node_id).first()
                if not to_node:
                    resp.status = '404 Not Found'
                    resp.text = json.dumps({'error': 'Receiver node not found'})
                    return
            
            # Create message
            message = Message(
                from_node_id=data['from_node_id'],
                to_node_id=to_node_id,
                message_type=data.get('message_type', 'transaction'),
                content=json.dumps(data.get('content', {})),
                qr_data=data.get('qr_data'),
                is_broadcast=is_broadcast,
                status='pending'
            )
            
            db.add(message)
            db.commit()
            db.refresh(message)
            
            resp.text = json.dumps({
                'id': message.id,
                'from_node_id': message.from_node_id,
                'to_node_id': message.to_node_id,
                'message_type': message.message_type,
                'content': message.content,
                'is_broadcast': message.is_broadcast,
                'timestamp': message.timestamp.isoformat()
            })
            resp.status = '201 Created'
        finally:
            db.close()


class MessageDetailResource:
    """Resource for individual message operations."""

    def on_put(self, req, resp, message_id):
        """Update message status (mark as processed, etc.)."""
        db = SessionLocal()
        try:
            message = db.query(Message).filter(Message.id == int(message_id)).first()
            if not message:
                resp.status = '404 Not Found'
                return
            
            data = json.loads(req.bounded_stream.read())
            
            if 'status' in data:
                message.status = data['status']
                if data['status'] == 'processed' and not message.processed_at:
                    message.processed_at = datetime.utcnow()
            
            db.commit()
            db.refresh(message)
            
            resp.text = json.dumps({
                'id': message.id,
                'status': message.status,
                'processed_at': message.processed_at.isoformat() if message.processed_at else None
            })
            resp.status = '200 OK'
        finally:
            db.close()
