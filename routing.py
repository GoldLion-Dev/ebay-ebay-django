from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from myapp.consumers import MyConsumer

# application = ProtocolTypeRouter({
#     'http': get_asgi_application(),
#     'websocket': URLRouter([
#         path('ws/', consumer.MyConsumer.as_asgi()),
#     ]),
# })


# from django.urls import path
# from myapp.consumers import MyConsumer

websocket_urlpatterns = [
    path('ws/', MyConsumer.as_asgi()),
]