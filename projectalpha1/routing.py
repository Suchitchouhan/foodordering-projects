from django.urls import re_path
from foodordering.consumers import *

websocket_urlpatterns = [
	re_path(r'ws/chat/$', ChatConsumer.as_asgi()),
]


