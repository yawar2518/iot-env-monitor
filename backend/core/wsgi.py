# =============================================================
# WSGI Configuration — kept for compatibility.
# The application runs under ASGI (Daphne) in all environments.
# This file is referenced by some Django management commands.
# =============================================================

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.local')

application = get_wsgi_application()
