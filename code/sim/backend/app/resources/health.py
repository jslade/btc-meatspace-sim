"""Health check resource."""
import falcon


class HealthResource:
    """Health check endpoint."""
    
    def on_get(self, req, resp):
        """Get health status."""
        resp.text = '{"status": "ok"}'
        resp.status = falcon.HTTP_200
