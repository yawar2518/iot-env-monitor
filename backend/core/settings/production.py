# =============================================================
# Local Development Settings
# Overrides and extends base.py for the development environment.
# =============================================================

from .base import *  # noqa: F401, F403

# =============================================================
# DEVELOPMENT OVERRIDES
# =============================================================

DEBUG = True

# Allow all hosts in local dev — Docker internal hostnames vary
ALLOWED_HOSTS = ['*']

# =============================================================
# DEBUG TOOLBAR
# =============================================================

INSTALLED_APPS += ['debug_toolbar']  # noqa: F405

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']  # noqa: F405

# Debug toolbar only shows for these IPs
INTERNAL_IPS = ['127.0.0.1']
