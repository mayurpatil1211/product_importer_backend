from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from app.consumers import EventConsumer


# application = ProtocolTypeRouter({
# 	'websocket':AllowedHostsOriginValidator(
# 		URLRouter(
# 				[
# 					url(r"^event$", EventConsumer),
# 				]
# 			)
# 		),
# 	'channel': ChannelNameRouter({"game_engine": EventConsumer}),
# 	},
# 	)


# from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
# from django.conf.urls import url
# from channels.auth import AuthMiddlewareStack
# from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

# from app.consumers import EventConsumer




# application = ProtocolTypeRouter({
# 	'websocket':AllowedHostsOriginValidator(
# 		URLRouter(
# 				[
# 					url(r"^event/(?P<imei>[\w.@+-]+)/$", EventConsumer),
# 					# url(r"^event/$", EventConsumer),
# 				]
# 			)
# 		),
# 	'channel': ChannelNameRouter({"game_engine": EventConsumer}),
# 	},
# 	)