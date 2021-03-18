from celery import shared_task
from app.models import *
from app.serializers import *
import requests

@shared_task
def webhook_logging(event, object_dict):
	links = WebhookLinks.objects.all()

	for link in links:
		data = {
					'link' : link.link,
					'event' : event,
					'meta_data' : object_dict
				}
		serializer = WebhookEventsLogSerializer(
				data=data
			)
		if serializer.is_valid():
			serializer.save()
		else:
			print(serializer.errors)

		try:
			requests.post(link.link, data=data)
		except(Exception)as e:
			pass

	return 'saved'