"""
ASGI config for djangosocket project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter,get_default_application
from django.urls import path, re_path
from register.consumers import ChatConsumer
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangosocket.settings')

application = get_asgi_application()
ws_patterns=[path('user/<id>/',ChatConsumer.as_asgi())]





application = ProtocolTypeRouter({
	'websocket': 
		AllowedHostsOriginValidator(AuthMiddlewareStack(
			URLRouter(ws_patterns)
		)
		),
	})

