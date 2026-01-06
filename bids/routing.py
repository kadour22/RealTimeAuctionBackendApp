from django.urls import re_path
from . import consumers
from notifications.consumers import notifications_consumer

websocket_urlpatterns = [
    re_path(r'ws/auction/(?P<auction_id>\w+)/$', consumers.auction_consumer.as_asgi()),
    re_path(r'^ws/notifications/$', notifications_consumer.as_asgi()),
]