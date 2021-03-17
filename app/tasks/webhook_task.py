from celery import shared_task
from app.models import *
from app.serializers import *

@shared_task
def webhook_logging(event, object_dict):
	links = WebhookLinks.objects.all()

	for link in links:
		serializer = WebhookEventsLogSerializer(
				data={
					'link' : link.link,
					'event' : event,
					'meta_data' : object_dict
				}
			)
		if serializer.is_valid():
			serializer.save()
		else:
			print(serializer.errors)
	return 'saved'