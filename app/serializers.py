from rest_framework import serializers
from app.models import *
from django.conf import settings

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__all__'


class WebhookLinkSerializer(serializers.ModelSerializer):
	class Meta:
		model = WebhookLinks
		fields = '__all__'


class WebhookEventsLogSerializer(serializers.ModelSerializer):
	class Meta:
		model = WebhookEventsLogs
		fields = '__all__'