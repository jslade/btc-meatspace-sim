"""Main Falcon application."""
import falcon
from falcon_cors import CORS
from app.database import init_db
from app.resources_new import (
    SettingsResource,
    PeerResource,
    MessageResource,
    WalletResource,
    TransactionResource,
    BlockResource
)

# Initialize database
init_db()

# Configure CORS
cors = CORS(allow_all_origins=True, allow_all_methods=True, allow_all_headers=True)

# Create Falcon app
app = falcon.App(middleware=[cors.middleware])

# Routes
settings_resource = SettingsResource()
peer_resource = PeerResource()
message_resource = MessageResource()
wallet_resource = WalletResource()
transaction_resource = TransactionResource()
block_resource = BlockResource()

app.add_route('/api/settings', settings_resource)
app.add_route('/api/peers', peer_resource)
app.add_route('/api/messages', message_resource)
app.add_route('/api/wallets', wallet_resource)
app.add_route('/api/transactions', transaction_resource)
app.add_route('/api/blocks', block_resource)


# Health check
class HealthResource:
    def on_get(self, req, resp):
        resp.text = '{"status": "ok"}'
        resp.status = falcon.HTTP_200


app.add_route('/health', HealthResource())
