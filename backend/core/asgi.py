# =============================================================
# IoT Environmental Monitoring — ASGI Configuration
# Entry point for Daphne ASGI server.
# Routes WebSocket connections to Django Channels consumers
# and HTTP connections to standard Django request handling.
# =============================================================

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.local')

# Initialise Django's ASGI application early to ensure the app
# registry is populated before importing consumers or routing.
django_asgi_app = get_asgi_application()

# Import websocket URL patterns after Django is initialised
from core.routing import websocket_urlpatterns  # noqa: E402

application = ProtocolTypeRouter({

    # -------------------------------------------------------
    # HTTP → standard Django request/response handling.
    # Handles all REST API endpoints, admin, static files.
    # -------------------------------------------------------
    'http': django_asgi_app,

    # -------------------------------------------------------
    # WebSocket → Django Channels consumers.
    # AllowedHostsOriginValidator rejects connections from
    # origins not in ALLOWED_HOSTS — prevents cross-site
    # WebSocket hijacking.
    # AuthMiddlewareStack populates scope['user'] from the
    # session, making the authenticated user available inside
    # consumers.
    # -------------------------------------------------------
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})