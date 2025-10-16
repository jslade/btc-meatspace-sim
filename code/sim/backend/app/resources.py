"""API resources for Bitcoin Meatspace Simulator."""
import json
import random
import string
from datetime import datetime
from app.database import SessionLocal
from app.models import Entity, Transaction


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
