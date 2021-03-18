from celery import shared_task
from app.models import *
from app.serializers import *

from django_eventstream import send_event


@shared_task
def adding_task(object_dict):
	for product in object_dict:
		prod = Product.objects.filter(sku=product.get('sku')).last()

		if prod:
			serializer = ProductSerializer(prod, data=product)
			if serializer.is_valid():
				serializer.save()
			else:
				pass
		else:
			serializer = ProductSerializer(data=product)
			if serializer.is_valid():
				serializer.save()

	send_event('test', 'message', {'text': 'Processed {} records'.format(len(object_dict))})
	return 'saved'