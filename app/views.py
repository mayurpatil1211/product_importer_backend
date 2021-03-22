from django.shortcuts import render
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.http import HttpRequest
from django.contrib.auth import authenticate
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from datetime import timedelta

from django.db.models import Q as queue

from app.models import * 
from app.serializers import * 

import datetime
import math

import os

import base64
import json
import shutil 
import csv

import pandas as pd

from app.tasks.product_creation import adding_task
from app.tasks.delete_product_task import delete_task
from app.tasks.webhook_task import webhook_logging

from django_eventstream import send_event


class TestEvent(APIView):
	def get(self, request):
		send_event('test', 'message', {'text': 'hello world'})
		return JsonResponse({'message':'Event sent'}, status=200)



class UploadDocApiView(APIView):
	parser_classes = (JSONParser, MultiPartParser,)
	def post(self, request):
		response = []
		if request.data.get('file', None):
			data = pd.read_csv(request.data.get('file', None)) 
			data.set_index("sku", inplace = True)
			data.groupby(data.index).first()
			data.reset_index(level=0, inplace=True)
			data = data.to_dict(orient='records')

			lenght = len(data)

			ranges = math.ceil(lenght/1000)
			start = 0
			end = 1000

			for i in range(ranges):
				task = adding_task.delay(data[start:end])
				send_event('test', 'message', {'text': 'Processing {} records, added to queue. '.format(len(data[start:end]))})
				start = end
				end = end+1000
				
				

			return JsonResponse({'message':'File being uploaded', 'status':False, 'status_code':200}, status=200)
		return JsonResponse({'message':'Invalid request, User ID not found', 'status':False, 'status_code':400}, status=200)


class ProductListApiView(APIView):
	def get(self, request):
		page = request.GET.get('page', 1)

		end = int(page)*1000
		start = end-1000
		query = request.GET.get('query')

		if query:
			product = Product.objects.filter(queue(sku__icontains=query)| queue(name__contains=query)).order_by('-id')[start:end]
		else:
			product = Product.objects.all().order_by('-id')[start:end]
		serializer = ProductSerializer(product,many=True)
		return JsonResponse({'message':'Product List', 'status':True, 'status_code':200, 'products':serializer.data, 'total_count':Product.objects.count()}, status=200)

	def delete(self, request):
		task = delete_task.delay()
		return JsonResponse({'message':'Products are being deleted.', 'status':True, 'status_code':200}, status=200)

	def post(self, request):
		if request.data:
			sku = request.data.get('sku')

			product_exist = Product.objects.filter(sku=sku).last()
			if product_exist:
				serializer = ProductSerializer(product_exist, data=request.data)
				if serializer.is_valid():
					serializer.save()
					return JsonResponse({'message':'Product already exist, Updating existing product.', 'status':True, 'status_code':200}, status=200)
				return JsonResponse({'message':'Error during adding product, please check all the required fields.', 'status':False, 'status_code':400}, status=200)
			else:
				serializer = ProductSerializer(data=request.data)
				if serializer.is_valid():
					serializer.save()
					return JsonResponse({'message':'Product added successfully.', 'status':True, 'status_code':200}, status=200)
				return JsonResponse({'message':'Error during adding product, please check all the required fields.', 'status':False, 'status_code':400}, status=200)
		return JsonResponse({'message':'Bad request, empty request.', 'status':False, 'status_code':200}, status=200)




class UpdateProductDetails(APIView):
	def put(self, request):
		if request.data:
			product = Product.objects.filter(sku=request.data.get('sku')).last()
			if product:
				serializer = ProductSerializer(product, data=request.data)
				if serializer.is_valid():
					serializer.save()
					webhook_logging.delay('Product Updated', request.data)
					return JsonResponse({'message':'Product updated successfully', 'status':True, 'status_code':200}, status=200)
				return JsonResponse({'message':'Error during updating product.', 'status':False, 'status_code':400}, status=400)
			return JsonResponse({'message':'Invalid product key, Please provide valid Product ID.', 'status':False, 'status_code':400}, status=200)
		return JsonResponse({'message':'Bad Request.', 'status':False, 'status_code':200}, status=200)


class WebhookLinkApiView(APIView):
	def post(self, request):
		if request.data:
			serializer = WebhookLinkSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return JsonResponse({'message':'Webhook URL saved successfully', 'status':True, 'status_code':200}, status=200)
			return JsonResponse({'message':'Invalid data.', 'status':False, 'status_code':400,'errors':serializer.errors}, status=200)
		return JsonResponse({'message':'Bad Request.', 'status':False, 'status_code':400}, status=200)

	def get(self, request):
		webhook_links = WebhookLinks.objects.all()
		serializer = WebhookLinkSerializer(webhook_links, many=True)
		return JsonResponse({'message':'Webhook links', 'status':True, 'status_code':200, 'webhooks':serializer.data}, status=200)

	def delete(self, request):
		
		if request.GET.get('id'):
			WebhookLinks.objects.filter(id=request.GET.get('id')).delete()
			return JsonResponse({'message':'Webook deleted successfully', 'status':True, 'status_code':204}, status=200)
		return JsonResponse({'message':'Webhook ID required.', 'status':False, 'status_code':400}, status=200)
		

class WebhookLogApiView(APIView):
	def get(self, request):
		logs = WebhookEventsLogs.objects.all()
		serializer = WebhookEventsLogSerializer(logs, many=True)
		return JsonResponse({'message':'Webook Logs', 'status':True, 'status_code':200, 'webhook_logs':serializer.data}, status=200)