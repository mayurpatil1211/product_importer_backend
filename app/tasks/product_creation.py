from celery import shared_task
from app.models import *
from app.serializers import *

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
	return 'saved'