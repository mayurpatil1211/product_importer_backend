from django.urls import path, re_path
from django.conf.urls import url


from .views import *


# from app.events import trips as trip_event

urlpatterns = [
	url(r'^upload/file$', UploadDocApiView.as_view(), name='upload_file'),
	url(r'^update/product$', UpdateProductDetails.as_view(), name='update_product'),

	url(r'^product$', ProductListApiView.as_view(), name='product'),

	url(r'^webhook/log$', WebhookLogApiView.as_view(), name='webhook_logs'),
	url(r'^webhook$', WebhookLinkApiView.as_view(), name='webhook_crud'),

	url(r'^test$', TestEvent.as_view(), name='test_evnet'),
]

