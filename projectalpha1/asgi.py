"""
ASGI config for projectalpha1 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from . import routing
from projectalpha1.token_auth import TokenAuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectalpha1.settings')


# application = get_asgi_application()
application = ProtocolTypeRouter({
	'http':get_asgi_application(),
	"websocket": TokenAuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})

