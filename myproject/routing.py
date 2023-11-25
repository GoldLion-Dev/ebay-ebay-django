from django.urls import path
from myapp.consumers import MyConsumer

websocket_urlpatterns = [
    path('ws/', MyConsumer.as_asgi()),
]