from celery import shared_task
from app.models import *
from app.serializers import *

from django_eventstream import send_event


@shared_task
def delete_task():
	Product.objects.all().delete()
	return 'Deleted'