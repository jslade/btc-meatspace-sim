"""Main Falcon application."""
import falcon
from falcon_cors import CORS
from app.database import init_db
from app.resources import (
    EntityResource,
    EntityDetailResource,
    TransactionResource,
    StatsResource,
    NodeResource,
    MessageResource,
    MessageDetailResource
)

# Initialize database
init_db()

# Configure CORS
cors = CORS(allow_all_origins=True, allow_all_methods=True, allow_all_headers=True)

# Create Falcon app
app = falcon.App(middleware=[cors.middleware])

# Legacy routes (backward compatibility)
entity_resource = EntityResource()
entity_detail_resource = EntityDetailResource()
transaction_resource = TransactionResource()
stats_resource = StatsResource()

app.add_route('/api/entities', entity_resource)
app.add_route('/api/entities/{entity_id}', entity_detail_resource)
app.add_route('/api/transactions', transaction_resource)
app.add_route('/api/stats', stats_resource)

# New routes for network node functionality
node_resource = NodeResource()
message_resource = MessageResource()
message_detail_resource = MessageDetailResource()

app.add_route('/api/nodes', node_resource)
app.add_route('/api/messages', message_resource)
app.add_route('/api/messages/{message_id}', message_detail_resource)


# Health check
class HealthResource:
    def on_get(self, req, resp):
        resp.text = '{"status": "ok"}'
        resp.status = falcon.HTTP_200


app.add_route('/health', HealthResource())
