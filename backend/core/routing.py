# =============================================================
# WebSocket URL Routing
# Maps WebSocket connection paths to Channels consumers.
# Consumers will be implemented in each app as we build them.
# =============================================================

from django.urls import re_path # noqa: F401

# Consumers imported here as they are built — placeholder for now.
# from apps.readings.consumers import ReadingsConsumer

websocket_urlpatterns = [
    # Pattern: ws://localhost:8000/ws/readings/{device_id}/
    # re_path(r'ws/readings/(?P<device_id>[^/]+)/$', ReadingsConsumer.as_asgi()),
]
