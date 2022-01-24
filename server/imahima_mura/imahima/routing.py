from django.urls import path

from . import consumers
# websocketルーティング設定
websocket_urlpatterns = [
    path('ws/imahima/<houseId>/', consumers.ImahimaConsumer.as_asgi()),
]