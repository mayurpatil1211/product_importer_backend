from django.db import models
from django.conf import settings

from django.db.models.signals import post_save as ps
from django.dispatch import receiver

from jsonfield import JSONField

import base64
import json
import random
import datetime
import pytz
import _thread

class Product(models.Model):
	name = models.CharField(max_length=240, null=False)
	sku = models.CharField(max_length=240, null=False, unique=True)
	description = models.TextField(null=True)

	class Meta:
		app_label = 'app'
		db_table = 'product'
		indexes = [
			models.Index(fields=['name', 'sku']),
			models.Index(fields=['sku']),
			models.Index(fields=['name']),
		]


class WebhookLinks(models.Model):
	link = models.URLField(max_length=200, null=False, blank=False)
	method = models.CharField(max_length=10, null=False, blank=False)

	class Meta:
		app_label = 'app'
		db_table = 'webhook_links'


class WebhookEventsLogs(models.Model):
	link = models.URLField(max_length=200, null=False, blank=False)
	event = models.CharField(max_length=100, blank=False, null=False)
	meta_data = JSONField(null=False)
	created_on = models.DateTimeField(auto_now_add=True)

	class Meta:
		app_label = 'app'
		db_table = 'webhook_event_logs'