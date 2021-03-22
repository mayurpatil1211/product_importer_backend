import asyncio
import json
from datetime import datetime, timedelta
import time
import _thread

from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from django.db import connections, close_old_connections
from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync

