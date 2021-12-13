"""
ASGI config for imahima_mura project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from .token_auth import TokenAuthMiddleware
import imahima.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imahima_mura.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),

    "websocket": TokenAuthMiddleware(
        URLRouter(
            imahima.routing.websocket_urlpatterns
        )
    ),
})
