from django.shortcuts import render
from django.contrib.gis.geos import Point
from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
import json
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from rest_framework.response import Response
from django.contrib.auth.models import User
import math, random
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from cms.models import *
from foodordering.models import *

# create your views here.

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username=request.data.get("username")
    password=request.data.get("password")
    print(username)
    print(password)
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        returnMessage = {'error': 'Invalid Credentials'}
        return HttpResponse(
        json.dumps(returnMessage),
        content_type = 'application/javascript; charset=utf8'
    )
    token, _ = Token.objects.get_or_create(user=user)
    returnToken = {'token':token.key}
    return HttpResponse(
        json.dumps(returnToken),
        content_type = 'application/javascript; charset=utf8'
    )

@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def see_pending_delivery(request):
	data=[]
	if delivery_employee.objects.filter(user=request.user).exists():
		context={}
		demp=delivery_employee.objects.get(user=request.user)
		d_emp=delivery_assign.objects.filter(employee=demp,status="pending").order_by("date")
		for x in d_emp:
			c=customer.objects.get(user=x.order.user)
			orderO={"order_id":x.order.uid,"status":x.order.status,"otp":x.order.opt,"order_type":x.order.order_type,"date":x.order.date,"username":x.order.user.username,'firstname':x.order.user.first_name,'lastname':x.order.user.last_name,"email":x.order.user.email,"mobile":c.mobile,"city":x.order.shipping_city,'state':x.order.shipping_state,"zipcode":x.order.shipping_zipcode,'address':x.order.shipping_address,'latitute':x.order.location.x,"longitue":x.order.location.y}
			if store.objects.filter(uid=x.order.rest).exists():
				orderO['store']=store.objects.get(uid=x.order.rest).as_dict()
			else:
				orderO['store']={}
			if resturent.objects.filter(uid=x.order.rest).exists():
				orderO['restaurant']=resturent.objects.get(uid=x.order.rest).as_dict()			#context['data']=data
			else:
				orderO['restaurant']={}
			data.append(orderO)
		return Response({'delivery':data},status=HTTP_200_OK)
	else:
		return Response({'delivery': "You are not allowed for this operation"},status=HTTP_200_OK)
			
@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def see_complete_delivery(request):
	if delivery_employee.objects.filter(user=request.user).exists():
		context={}
		data=[]
		demp=delivery_employee.objects.get(user=request.user)
		d_emp=delivery_assign.objects.filter(employee=demp,status="complete").order_by("date")
		for x in d_emp:
			c=customer.objects.get(user=x.order.user)
			data.append({"order_id":x.order.uid,"status":x.order.status,"order_type":x.order.order_type,"date":x.order.date,"username":x.order.user.username,'firstname':x.order.user.first_name,'lastname':x.order.user.last_name,"email":x.order.user.email,"mobile":c.mobile,"city":x.order.shipping_city,'state':x.order.shipping_state,"zipcode":x.order.shipping_zipcode,'address':x.order.shipping_address,'latitute':x.order.location.x,"longitue":x.order.location.y})
		return Response({'delivery':data},status=HTTP_200_OK)
	else:
		return Response({'delivery': "You are not allowed for this operation"},status=HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def see_cancel_delivery(request):
	if delivery_employee.objects.filter(user=request.user).exists():
		context={}
		data=[]
		demp=delivery_employee.objects.get(user=request.user)
		d_emp=delivery_assign.objects.filter(employee=demp,status="cancel").order_by("date")
		for x in d_emp:
			c=customer.objects.get(user=x.order.user)
			data.append({"order_id":x.order.uid,"status":x.order.status,"order_type":x.order.order_type,"date":x.order.date,"username":x.order.user.username,'firstname':x.order.user.first_name,'lastname':x.order.user.last_name,"email":x.order.user.email,"mobile":c.mobile,"city":x.order.shipping_city,'state':x.order.shipping_state,"zipcode":x.order.shipping_zipcode,'address':x.order.shipping_address,'latitute':x.order.location.x,"longitue":x.order.location.y})
			#context['data']=data
		return Response({'delivery':data},status=HTTP_200_OK)
	else:
		return Response({'delivery': "You are not allowed for this operation"},status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def complete_order(request):
	uid = request.data.get('uid')
	otp=request.data.get("otp")
	if delivery_employee.objects.filter(user=request.user).exists() and otp!="" and otp!=None and uid !=None and uid !="":
		context={}
		o=order.objects.get(uid=uid)
		if o.opt==otp:
			o.status="complete"
			o.save()
			oit=order_items.objects.filter(order=o)
			for x in oit:
				oitO=order_items.objects.filter(item_uid=x.item_uid)
				for q in oitO:
					q.status="complete"
					q.save()

			oo=delivery_assign.objects.get(order=o)
			oo.status="complete"
			oo.save()
			return Response({'status': "order has been completed"},status=HTTP_200_OK)
		else:
			return Response({'status': "otp has not matched"},status=HTTP_200_OK)
	else:
		return Response({'status': "not authorized"},status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def cancel_order(request):
	uid = request.data.get('uid')
	otp=request.data.get("otp")
	if delivery_employee.objects.filter(user=request.user).exists() and uid != "" and uid !=None and otp !=None and otp !="":
		context={}
		o=order.objects.get(uid=uid)
		if o.opt==otp:
			o.status="cancel"
			o.save()
			oo=delivery_assign.objects.get(order=o)
			oo.status="cancel"
			oo.save()
			w=wallet.objects.get(user=o.user)
			w.coin+=o.amount
			w.save()
			return Response({'status': "order has been cancel"},status=HTTP_200_OK)
		else:
			return Response({'status': "otp has not matched"},status=HTTP_200_OK)
	else:
		return Response({'status': "not authorized"},status=HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def items_in_order(request,uid):
	if order.objects.filter(uid=uid).exists():
		emp=delivery_employee.objects.get(user=request.user)
		orderO=order.objects.get(uid=uid)
		das=delivery_assign.objects.get(order=orderO,employee=emp)
		context={}
		od=order_items.objects.filter(order=orderO)
		i=1
		j=1
		for x in od:
			data={}
			data['item_uid']=x.item_uid
			data['quantity']=x.quantity
			if "product"==x.item_type:
				stp=store_product.objects.get(uid=x.item_uid)
				product={}
				product['product']=stp.as_dict()
				image=[]
				for y in product_image.objects.filter(product=stp):
					image.append(y.image.url)
				product['image']=image
				specification=[]
				des=[]
				for y in product_specification.objects.filter(product=stp):
					specification.append(y.specification)
					des.append(y.des)
				product['specification']=specification
				product['des']=des
				data['product']=product
				data['store']={"store_name":stp.store.store_name,'firstname':stp.store.user.first_name,"last_name":stp.store.user.last_name,"mobile":stp.store.mobile,"email":stp.store.user.email,"city":stp.store.city,'state':stp.store.state,'zipcode':stp.store.zipcode,"address":stp.store.address}
				context['data'+str(i)]=data

				i+=1
			elif "food"==x.item_type:
				foodO={}
				ftp=food.objects.get(uid=x.item_uid)
				foodO['food']=ftp.as_dict()
				image=[]
				for y in food_image.objects.filter(food=ftp):
					image.append(y.image.url)
				foodO['image']=image
				specification=[]
				des=[]
				for y in food_specification.objects.filter(food=ftp):
					specification.append(y.specification)
					des.append(y.des)
				foodO['specification']=specification
				foodO['des']=des
				data['food']=foodO
				data['resturent']={"resturent_name":ftp.resturent.resturent_name,'firstname':ftp.resturent.user.first_name,"last_name":ftp.resturent.user.last_name,"mobile":ftp.resturent.mobile,"email":ftp.resturent.user.email,"city":ftp.resturent.city,'state':ftp.resturent.state,'zipcode':ftp.resturent.zipcode,"address":ftp.resturent.address}
				context['data'+str(j)]=data
				j+=1
	else:
		context['data']="Data not found"			

	return HttpResponse(json.dumps({"data":context}), content_type='application/json')	


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_emp_location(request):
	context={}
	lat = request.data.get('latitute')
	lon = request.data.get('longitue')
	user = request.user
	if lat != '' and lon != '' and lat != None and lon != None:
		loc = Point(float(lat), float(lon))
		delivery_employeeO = delivery_employee.objects.get(user=user)
		delivery_employeeO.location = loc
		delivery_employeeO.save()
		context['data'] = 'saved'
	else:
		context['data'] = 'i won\'t do this'
	return HttpResponse(json.dumps(context), content_type='application/json')





@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def change_delivery_status(request):
	uid = request.data.get('uid')
	status=request.data.get("status")
	context={}
	if order.objects.filter(uid=uid).exist() and delivery_employee.objects.filter(user=request.user).exists() and uid != "" and uid !=None and status !=None and status !="" and status != 'cancel':
		o=order.objects.get(uid=uid)
		oo=delivery_assign.objects.get(order=o,employee=delivery_employee.objects.get(user=request.user))
		oo.status=status
		oo.save()
		o.status=status
		o.save()
		return Response({'status': "order has been cancel"},status=HTTP_200_OK)
	else:
		return Response({'status': "not authorized"},status=HTTP_200_OK)




@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def profile(request):
	context={}
	if delivery_employee.objects.filter(user=request.user).exists():
		context['profile']=delivery_employee.objects.get(user=request.user).as_dict()
		return Response(context,status=HTTP_200_OK)
	else:
		return Response({'status': "not authorized"},status=HTTP_200_OK)





@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def change_duty_status(request):
	context={}
	if delivery_employee.objects.filter(user=request.user,on_duty=False).exists():
		d=delivery_employee.objects.get(user=request.user)
		d.on_duty=True
		d.save()
		return Response({'status': "On duty"},status=HTTP_200_OK)
	elif delivery_employee.objects.filter(user=request.user,on_duty=True).exists():
		d=delivery_employee.objects.get(user=request.user)
		d.on_duty=False
		d.save()
		return Response({'status': "off duty"},status=HTTP_200_OK)




@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_duty_status(request):
	context={}
	if delivery_employee.objects.filter(user=request.user).exists():
		context['profile']=delivery_employee.objects.get(user=request.user).on_duty
		return Response(context,status=HTTP_200_OK)
	else:
		return Response({'status': "not authorized"},status=HTTP_200_OK)
		


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_location(request):
	context={}
	if delivery_employee.objects.filter(user=request.user).exists():
		demp=delivery_employee.objects.get(user=request.user)
		context['latitute']=demp.location.x
		context['longitue']=demp.location.y
	else:
		context['status']="not a delivery boy"	
	return HttpResponse(json.dumps(context), content_type='application/json')

