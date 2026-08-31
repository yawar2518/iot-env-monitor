# =============================================================
# IoT Environmental Monitoring — Root URL Configuration
# =============================================================

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


# =============================================================
# HEALTH CHECK
# Called by Docker healthcheck and load balancers.
# No authentication required.
# =============================================================

def health_check(request):
    return JsonResponse({'status': 'ok'})


# =============================================================
# URL PATTERNS
# =============================================================

urlpatterns = [

    # -----------------------------------------------------------
    # Admin — database inspection during development
    # -----------------------------------------------------------
    path('admin/', admin.site.urls),

    # -----------------------------------------------------------
    # Health check — unauthenticated, used by infrastructure
    # -----------------------------------------------------------
    path('health/', health_check),

    # -----------------------------------------------------------
    # JWT Authentication
    # POST /api/token/          → obtain access + refresh tokens
    # POST /api/token/refresh/  → exchange refresh for new access token
    # -----------------------------------------------------------
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # -----------------------------------------------------------
    # Application API endpoints
    # Each app manages its own URL patterns in apps/{name}/urls.py
    # Included here under the /api/ namespace.
    # -----------------------------------------------------------
    path('api/devices/', include('apps.devices.urls')),
    path('api/readings/', include('apps.readings.urls')),
    path('api/alerts/', include('apps.alerts.urls')),
    path('api/commands/', include('apps.commands.urls')),
]


# =============================================================
# DEBUG TOOLBAR
# Only active when DEBUG=True (local development).
# Must be appended after main patterns.
# =============================================================

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
