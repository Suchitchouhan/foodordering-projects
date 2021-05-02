from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
import json
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from base64 import b64decode
from django.core.files.base import ContentFile
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
from delivery.models import *
#from foodordering.views import #send_notification

# Create your views here.
def rest_rating(uid):
	res=resturent.objects.get(uid=uid)
	rating=rating_for_restaurant.objects.filter(for_restaurant=res).count()
	data=[]
	for y in [1,2,3,4,5]:
		if rating_for_restaurant.objects.filter(for_restaurant=res,rate=y).exists():
			percent=0
			rating_star=rating_for_restaurant.objects.filter(for_restaurant=res,rate=y).count()
			percent=((rating/100)*rating_star)
			data.append(percent)
		else:
			data.append(3.2)
	return data	

def st_rating(uid):
	res=store.objects.get(uid=uid)
	rating=rating_for_store.objects.filter(for_store=res).count()
	data=[]
	for y in [1,2,3,4,5]:
		if rating_for_store.objects.filter(for_store=res,rate=y).exists():
			percent=0
			rating_star=rating_for_store.objects.filter(for_store=res,rate=y).count()
			percent=((rating/100)*rating_star)
			data.append(percent)
		else:
			data.append(3.2)
	return data


def custom_food_price(food):
	data=[]
	if food_sub_cat.objects.filter(for_food=food).exists():
		foo=food_sub_cat.objects.filter(for_food=food)
		for x in foo:
			data.append(x.as_dict())
		return data
	else:
		return data		



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    password = request.data.get("password")
    username= request.data.get("username")
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
    
    if store.objects.filter(user=user).exists():
    	returnToken = {'token':token.key,"store":"store"}
    elif resturent.objects.filter(user=user).exists():
    	returnToken = {'token':token.key,"resturent":"resturent"}
    else:
    	returnToken = {'token':token.key}	
    return HttpResponse(
        json.dumps(returnToken),
        content_type = 'application/javascript; charset=utf8'
    )



@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def orders_for_delivery(request,statusO):
	data=[]
	if store.objects.filter(user=request.user).exists():
		st=store.objects.get(user=request.user)
		oda=order.objects.filter(status=statusO,rest=st.uid)
		for x in oda:
			orderO={"order_uid":x.uid,"customer_firstname":x.user.first_name,"customer_lastname":x.user.last_name,"customer_email":x.user.email,"datetime":x.date,"total_amount":x.amount}
			z=delivery_assign.objects.get(order=x)
			orderO['delivery_employee_first_name']=z.employee.user.first_name
			orderO['delivery_employee_last_name']=z.employee.user.last_name
			orderO['delivery_employee_mobile']=z.employee.mobile
			orderO['delivery_employee_email']=z.employee.user.email
			orderO['delivery_employee_city']=z.employee.city
			item=[]
			for y in order_items.objects.filter(order=x,item_type="product"):
				item.append({"item_uid":y.item_uid,"quantity":y.quantity,"cost":y.cost,"name":store_product.objects.get(uid=y.item_uid).name})
			orderO['item']=item
			data.append(orderO)	
		if len(data) > 0:
			return Response({'data': data},status=HTTP_200_OK)
		else:
			return Response({'data': 'no data'},status=HTTP_200_OK)
	elif resturent.objects.filter(user=request.user).exists():
		st=resturent.objects.get(user=request.user)
		oda=order.objects.filter(status=statusO,rest=st.uid)
		for x in oda:
			orderO={"order_uid":x.uid,"customer_firstname":x.user.first_name,"customer_lastname":x.user.last_name,"customer_email":x.user.email,"datetime":x.date,"total_amount":x.amount}
			z=delivery_assign.objects.get(order=x)
			orderO['delivery_employee_first_name']=z.employee.user.first_name
			orderO['delivery_employee_last_name']=z.employee.user.last_name
			orderO['delivery_employee_mobile']=z.employee.mobile
			orderO['delivery_employee_email']=z.employee.user.email
			orderO['delivery_employee_city']=z.employee.city
			item=[]
			for y in order_items.objects.filter(order=x,item_type="food"):
				order_itemsx={"item_uid":y.item_uid,"quantity":y.quantity,"cost":y.cost}
				order_itemsx['food_name']=food.objects.get(uid=y.item_uid).name
				if order_sub_cat.objects.filter(order=x,for_order_item=y.item_uid).exists():
					order_itemsx['sub_cat']=order_sub_cat.objects.get(order=x,for_order_item=y.item_uid).as_dict()
				else:
					order_itemsx['sub_cat']={}
				if order_exra_item.objects.filter(for_order_item=y.item_uid,order=x):
					order_itemsx['extra_item_status']="exists"
					order_items_list=[]
					for z in  order_exra_item.objects.filter(for_order_item=y.item_uid,order=x):
						order_items_list.append(z.as_dict())
					order_itemsx['extra_item']=order_items_list
				else:
					order_itemsx['extra_item_status']="notexists"
					order_itemsx['extra_item']={}				
			item.append(order_itemsx)
			print(item)
			orderO['item']=item
			data.append(orderO)		#context['food']=data
		if len(data) > 0:
			return Response({'data': data},status=HTTP_200_OK)
		else:
			return Response({'data': 'no data'},status=HTTP_200_OK)
	else:
		return Response({'delivery': "not exists"},status=HTTP_200_OK)	




@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def cancel_order(request,order_uid):
	if store.objects.filter(user=request.user).exists():
		st=store.objects.get(user=request.user)
		if order.objects.filter(uid=order_uid).exists():
			o=order.objects.get(uid=order_uid)
			if order_items.objects.filter(order=o).exists():
				otm=order_items.objects.filter(order=o)
				for x in otm:
					x.status="cancel"
					x.save()
			o.status= 'cancel'
			o.save()
			w=wallet.objects.get(user=o.user)
			w.coin+=o.amount
			w.save()
		return Response({'delivery': "item has been cancel"},status=HTTP_200_OK)		
	elif resturent.objects.filter(user=request.user).exists():
		st=resturent.objects.get(user=request.user)
		if order.objects.filter(uid=order_uid).exists():
			o=order.objects.get(uid=order_uid)
			if order_items.objects.filter(order=o):
				otm=order_items.objects.filter(order=o)
				for x in otm:
					x.status="cancel"
					x.save()
			o.status= 'cancel'
			o.save()
			w=wallet.objects.get(user=o.user)
			w.coin+=o.amount
			w.save()
		return Response({'delivery': "item has been cancel"},status=HTTP_200_OK)		


def check_blank_or_null(data):
    status = True
    for x in data:
        if x == "" and x == None:
            status = True
        else:
            pass
    return status 


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def add_product(request):
	context={}
	name=request.data.get("name")
	brandname=request.data.get("brandname")
	cat_id=request.data.get("cat_id")
	price=request.data.get("price")
	des1=request.data.get("des1")
	highlight=request.data.get("highlight")
	overview=request.data.get("overview")
	gst=request.data.get("gst")
	specification=request.data.getlist("specification")
	des=request.data.getlist("des")
	image=request.data.getlist("image")
	if store.objects.filter(user=request.user).exists() and len(specification)>0 and len(des)>0  and len(specification)==len(des) and check_blank_or_null([name,brandname,cat_id,price,des,highlight,overview,gst]) == True:
		stp=store_product.objects.create()
		stp.uid=get_random_string(8)
		stp.name=name
		stp.brandname=brandname
		stp.store=store.objects.get(user=request.user)
		stp.product_category=store_product_category.objects.get(pk=cat_id)
		stp.price=price
		stp.des=des1
		stp.highlight=highlight
		stp.overview=overview
		stp.gst=gst
		ps_list=[]
		pi_list=[]
		if len(specification)>0 and len(des)>0:
			for x,y in zip(specification,des):
				ps=product_specification.objects.create()
				ps.product=stp
				ps.specification=x
				ps.des=y
				ps_list.append(ps)
		for x in image:
			try:
				image_data = b64decode(x)
				y = ContentFile(image_data)
			except:
				context['message']="image must be base64"
				return Response(context,status=HTTP_200_OK)		
			pi=product_image.objects.create(product=stp,)
			pi.image.save('category_image.jpg',y)
			pi_list.append(pi)
		stp.save()
		if len(specification)>0 and len(des)>0:
			for x in ps_list:
				x.save()
		for x in pi_list:
			x.save()	
		context['message']="product has been successfully added"		
	else:
		context['message']="something is not right"
	return Response(context,status=HTTP_200_OK)	

@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def add_food(request):
	context={}
	name=request.data.get("name")
	brandname=request.data.get("brandname")
	cat_id=request.data.get("cat_id")
	price=request.data.get("price")
	des1=request.data.get("des1")
	highlight=request.data.get("highlight")
	overview=request.data.get("overview")
	gst=request.data.get("gst")
	food_type=request.data.get("food_type")
	sub_cat_name=request.data.getlist("sub_cat_name")
	sub_cat_price=request.data.getlist("sub_cat_price")
	extra_item_name=request.data.getlist("extra_item_name")
	extra_item_price=request.data.getlist("extra_item_price")
	specification=request.data.getlist("specification")
	des=request.data.getlist("des")
	image=request.data.getlist("image")
	if food_type in ['Veg','Nveg','Egg'] and food_category.objects.filter(pk=cat_id).exists() and len(sub_cat_name)==len(sub_cat_price) and len(extra_item_price)==len(extra_item_name) and resturent.objects.filter(user=request.user).exists() and len(specification)>0 and len(des)>0 and len(specification)==len(des):
		rt=resturent.objects.get(user=request.user)
		f=food.objects.create()
		f.uid=get_random_string(8)
		f.name=name
		f.brandname=brandname
		f.resturent=rt
		f.food_category=food_category.objects.get(pk=cat_id)
		f.price=price
		f.des=des1
		f.highlight=highlight
		f.overview=overview
		f.gst=gst
		f.food_type=food_type
		sbc_list=[]
		fxi_list=[]
		fs_list=[]
		ps_list=[]
		if len(sub_cat_name)>0 and len(sub_cat_price)>0:
			for x,y in zip(sub_cat_name,sub_cat_price):
				sbc=food_sub_cat.objects.create()
				sbc.for_food=f
				sbc.cat_name=x
				sbc.price=y
				sbc_list.append(sbc)
		if len(extra_item_name)>0 and len(extra_item_price)>0:		
			for x,y in zip(extra_item_name,extra_item_price):
				fxi=food_extra_items.objects.create()
				fxi.for_food=f
				fxi.item_name=x
				fxi.price=y
				fxi_list.append(fxi)
		if len(specification)>0 and len(specification)>0:		
			for x,y in zip(specification,specification):
				fs=food_specification.objects.create()
				fs.food=f
				fs.specification=x
				fs.des=y
				fs_list.append(fs)		
		for x in image:
			try:
				image_data = b64decode(x)
				y = ContentFile(image_data)
			except:
				context['message']="image must be base64"
				return Response(context,status=HTTP_200_OK)		
			pi=food_image.objects.create(food=f)
			pi.image.save('category_image.jpg',y)
			ps_list.append(pi)
		# for x in image:
		# 	fi=food_image.objects.create()
		# 	fi.food=f
		# 	fi.image=x
		# 	fi.save()
		f.save()
		if len(sub_cat_name)>0 and len(sub_cat_price)>0:
			for x in sbc_list:
				x.save()
		if len(extra_item_name)>0 and len(extra_item_price)>0:		
			for x in fxi_list:
				x.save()
		if len(specification)>0 and len(specification)>0:
			for x in fs_list:
				x.save()
		for x in ps_list:
			x.save()			
		
		context['message']="food has been successfully added"
	else:
		context['message']="something is not right"
	return Response(context,status=HTTP_200_OK)				



@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def update_food(request):
	context={}
	food_id=request.data.get("food_id")
	name=request.data.get("name")
	brandname=request.data.get("brandname")
	cat_id=request.data.get("cat_id")
	price=request.data.get("price")
	des1=request.data.get("des1")
	highlight=request.data.get("highlight")
	overview=request.data.get("overview")
	gst=request.data.get("gst")
	food_type=request.data.get("food_type")
	sub_cat_name=request.data.getlist("sub_cat_name")
	sub_cat_price=request.data.getlist("sub_cat_price")
	extra_item_name=request.data.getlist("extra_item_name")
	extra_item_price=request.data.getlist("extra_item_price")
	specification=request.data.getlist("specification")
	des=request.data.getlist("des")
	image=request.data.getlist("image")
	check=True
	if food.objects.filter(pk=food_id).exists() == False:
		check=False
	if check==True and food_type in ['Veg','Nveg','Egg'] and food_category.objects.filter(pk=cat_id).exists() and  len(sub_cat_name)==len(sub_cat_price) and len(extra_item_price)==len(extra_item_name) and resturent.objects.filter(user=request.user).exists() and len(specification)>0 and len(des)>0 and len(specification)==len(des):
		rt=resturent.objects.get(user=request.user)
		f=food.objects.create()
		f.uid=get_random_string(8)
		f.name=name
		f.brandname=brandname
		f.resturent=rt
		f.food_category=food_category.objects.get(pk=cat_id)
		f.price=price
		f.des=des1
		f.highlight=highlight
		f.overview=overview
		f.gst=gst
		f.food_type=food_type
		sbc_list=[]
		fxi_list=[]
		fs_list=[]
		ps_list=[]
		if len(sub_cat_name)>0 and len(sub_cat_price)>0:
			for x,y in zip(sub_cat_name,sub_cat_price):
				sbc=food_sub_cat.objects.create()
				sbc.for_food=f
				sbc.cat_name=x
				sbc.price=y
				sbc_list.append(sbc)
		if len(extra_item_name)>0 and len(extra_item_price)>0:		
			for x,y in zip(extra_item_name,extra_item_price):
				fxi=food_extra_items.objects.create()
				fxi.for_food=f
				fxi.item_name=x
				fxi.price=y
				fxi_list.append(fxi)
		if len(specification)>0 and len(specification)>0:		
			for x,y in zip(specification,specification):
				fs=food_specification.objects.create()
				fs.food=f
				fs.specification=x
				fs.des=y
				fs_list.append(fs)		
		for x in image:
			try:
				image_data = b64decode(x)
				y = ContentFile(image_data)
			except:
				context['message']="image must be base64"
				return Response(context,status=HTTP_200_OK)		
			pi=food_image.objects.create(food=f)
			pi.image.save('category_image.jpg',y)
			ps_list.append(pi)
		# for x in image:
		# 	fi=food_image.objects.create()
		# 	fi.food=f
		# 	fi.image=x
		# 	fi.save()
		f.save()
		if len(sub_cat_name)>0 and len(sub_cat_price)>0:
			for x in sbc_list:
				x.save()
		if len(extra_item_name)>0 and len(extra_item_price)>0:		
			for x in fxi_list:
				x.save()
		if len(specification)>0 and len(specification)>0:
			for x in fs_list:
				x.save()
		for x in ps_list:
			x.save()			
		fd=food.objects.get(pk=food_id)
		fd.delete()
		context['message']="food has been successfully added"
	else:
		context['message']="something is not right"
	return Response(context,status=HTTP_200_OK)				


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def update_product(request):
	context={}
	product_id=request.data.get("product_id")
	name=request.data.get("name")
	brandname=request.data.get("brandname")
	cat_id=request.data.get("cat_id")
	price=request.data.get("price")
	des1=request.data.get("des1")
	highlight=request.data.get("highlight")
	overview=request.data.get("overview")
	gst=request.data.get("gst")
	specification=request.data.getlist("specification")
	des=request.data.getlist("des")
	image=request.data.getlist("image")
	check=True
	if store_product.objects.filter(pk=product_id).exists() == False:
		check=False
	if check==True and store.objects.filter(user=request.user).exists() and len(specification)>0 and len(des)>0  and len(specification)==len(des) and check_blank_or_null([name,brandname,cat_id,price,des,highlight,overview,gst]) == True:
		stp=store_product.objects.create()
		stp.uid=get_random_string(8)
		stp.name=name
		stp.brandname=brandname
		stp.store=store.objects.get(user=request.user)
		stp.product_category=store_product_category.objects.get(pk=cat_id)
		stp.price=price
		stp.des=des1
		stp.highlight=highlight
		stp.overview=overview
		stp.gst=gst
		ps_list=[]
		pi_list=[]
		if len(specification)>0 and len(specification)>0:
			for x,y in zip(specification,des):
				ps=product_specification.objects.create()
				ps.product=stp
				ps.specification=x
				ps.des=y
				ps_list.append(ps)
		for x in image:
			try:
				image_data = b64decode(x)
				y = ContentFile(image_data)
			except:
				context['message']="image must be base64"
				return Response(context,status=HTTP_200_OK)		
			pi=product_image.objects.create(product=stp,)
			pi.image.save('category_image.jpg',y)
			pi_list.append(pi)
		stp.save()
		for x in ps_list:
			x.save()
		for x in pi_list:
			x.save()
		stpO=store_product.objects.get(pk=product_id)
		stpO.delete()	
		context['message']="product has been successfully added"		
	else:
		context['message']="something is not right"
	return Response(context,status=HTTP_200_OK)	



@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def get_product_category(request):
	store_cat=store_product_category.objects.all()
	data=[]
	for x in store_cat:
		data.append(x.as_dict())
	return HttpResponse(json.dumps({"data":data}), content_type='application/json')


csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def get_food_category(request):
	store_cat=food_category.objects.all()
	data=[]
	for x in store_cat:
		data.append(x.as_dict())
	return HttpResponse(json.dumps({"data":data}), content_type='application/json')



@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def add_product_category(request):
	context={}
	name=request.data.get("name")
	des=request.data.get("des")
	image=request.data.get('image')
	#image=request.FILES['image']
	if store.objects.filter(user=request.user).exists() and name!=None and name!="" and des!=None and des!="" and image!="" and image!=None:
		if store_product_category.objects.filter(name=name).exists():
			context['message']="its already exists"
		else:
			storeO=store_product_category.objects.create()
			storeO.name=name
			storeO.des=des
			try:
				image_data = b64decode(image)
				x= ContentFile(image_data)
			except:
				context['message']="image must be base64"
				return Response(context,status=HTTP_200_OK)
			storeO.image.save('category_image.jpg',x)		
			storeO.save()
			context['message']="store category successfully addd"
	else:
		context['message']="all Filled must be filled"	
	return Response(context,status=HTTP_200_OK)	



@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def add_food_category(request):
	context={}
	name=request.data.get("name")
	des=request.data.get("des")
	image=request.data.get('image')
	#image=request.FILES['image']
	if resturent.objects.filter(user=request.user).exists() and name!=None and name!="" and des!=None and des!="" and image!="" and image!=None:
		if food_category.objects.filter(name=name).exists():
			context['message']="its already exists"
		else:
			store=food_category.objects.create()
			store.name=name
			store.des=des
			try:
				image_data = b64decode(image)
				x= ContentFile(image_data)
				#store.image.save('category_image.jpg',x)
			except:
				context['message']="image must be base64"
				return Response(context,status=HTTP_200_OK)	
			#store.image=image
			store.image.save('category_image.jpg',x)
			store.save()
			context['message']="store category successfully addd"
	else:
		context['message']="all Filled must be filled"	
	return Response(context,status=HTTP_200_OK)	



@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_all_food(request):
	if resturent.objects.filter(user=request.user).exists():
		rt=resturent.objects.get(user=request.user)
		context=[]
		resturent_d={}
		resturent_d['resturent_name']= rt.resturent_name
		resturent_d['category_name'] = rt.category.name
		resturent_d['locality'] = rt.locality
		# resturent_d['rating']=rest_rating(uid)
		resturent_d['average_price']=rt.average_price
		rest_cat=[]
		for z in food_category.objects.all():
			cat={}
			cat['name'] = z.name
			cat['des'] =z.des
			cat['image'] = z.image.url
			food_i=[]
			for x in food.objects.filter(resturent=rt,food_category=z):
				data={}
				data["food"]=x.as_dict()
				image=[]
				specification=[]
				des=[]
				p=food.objects.get(uid=x.uid)
				pO=food_image.objects.filter(food=p)
				for y in pO:
					image.append(y.image.url)
				POO=food_specification.objects.filter(food=p)
				for y in POO:
					specification.append(y.specification)
					des.append(y.des)
				data['image']=image
				data['specification']=specification
				data['des']=des
				data['food_price_type']=custom_food_price(p)
				data['food_type'] = x.food_type
				food_i.append(data)
			cat['food']=food_i	
			context.append(cat)
		return HttpResponse(json.dumps({"data":context,"rest":resturent_d}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"Category is not exists"}), content_type='application/json')



@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def get_all_store_product(request):
	context = {}
	dataL= []
	storeO=store.objects.get(user=request.user)
	for x in store_product_category.objects.all():
		cat={}
		cat['name'] = x.name
		cat['des'] =x.des
		cat['image'] = x.image.url
		product_i=[]
		for y in store_product.objects.filter(store=storeO,product_category=x):
			data={}
			data['product']=y.as_dict()
			image=[]
			for z in product_image.objects.filter(product=y):
				image.append(z.image.url)
			data['image']=image
			specification=[]
			des=[]
			for z in product_specification.objects.filter(product=y):
				specification.append(z.specification)
				des.append(z.des)
			data['specification']=specification
			data['des']=des
			product_i.append(data)
		cat['product']=product_i
		dataL.append(cat)
	if len(dataL) > 0:
		context['data'] = dataL
	else:
		context['data'] = 'no_records'
	return HttpResponse(json.dumps(context), content_type='application/json')






@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def change_opening_status(request):
	context={}
	if store.objects.filter(user=request.user,opening="open").exists():
		st=store.objects.get(user=request.user)
		st.opening="close"
		st.save()
		context['message']="Store has been closed"
	elif store.objects.filter(user=request.user,opening="close").exists():
		st=store.objects.get(user=request.user)
		st.opening="open"
		st.save()
		context['message']="Store has been open"		
	elif resturent.objects.filter(user=request.user,opening="close").exists():
		st=resturent.objects.get(user=request.user)
		st.opening="open"
		st.save()
		context['message']="Restaurant has been open"
	elif resturent.objects.filter(user=request.user,opening="open").exists():
		st=resturent.objects.get(user=request.user)
		st.opening="close"
		st.save()			
		context['message']="Restaurant has been close"
	else:
		context['message']="Sorry not Authorized"
	return HttpResponse(json.dumps(context), content_type='application/json')
	


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_store(request):
	context={}
	store_name=request.data.get("store_name")
	mobile=request.data.get("mobile")
	city=request.data.get("city")
	state=request.data.get("state")
	zipcode=request.data.get("zipcode")
	address=request.data.get("address")
	locality=request.data.get("locality")
	cat_id=request.data.get("cat_id")
	# image=request.data['image']
	# image1=request.data['image1']
	if check_blank_or_null([store_name,mobile,city,state,zipcode,address,locality,cat_id]) == True and store_category.objects.filter(pk=cat_id).exists() and store.objects.filter(user=request.user).exists():
		st=store.objects.get(user=request.user)
		st.store_name=store_name
		st.mobile=mobile
		st.city=city
		st.state=state
		st.zipcode=zipcode
		st.address=address
		st.locality=locality
		st.category=store_category.objects.get(pk=cat_id)
		# try:
		# 	image_data = b64decode(image)
		# 	y = ContentFile(image_data)
		# except:
		# 	context['message']="image must be base64"
		# 	return Response(context,status=HTTP_200_OK)
		# st.image.save('store.jpg',y)
		# try:
		# 	image_dataO = b64decode(image1)
		# 	yO = ContentFile(image_dataO)
		# except:
		# 	context['message']="image1 must be base64"
		# 	return Response(context,status=HTTP_200_OK)
		# st.image1.save('store1.jpg',y0)
		st.save()
		context['message']="successfully Updated"
	else:
		context['message']="All field must be filled"	
	return HttpResponse(json.dumps(context), content_type='application/json')





@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
#context={}
def add_store_image(request):
	context={}
	if store.objects.filter(user=request.user).exists():
		image=request.data.get("image")
		image1=request.data.get("image")
		try:
			image_data = b64decode(image)
			x= ContentFile(image_data)
		except:
			context['message']="image must be base64"
			return Response(context,status=HTTP_200_OK)
		try:
			image_data1 = b64decode(image1)
			y = ContentFile(image_data1)
		except:
			context['message']="image must be base64"
			return Response(context,status=HTTP_200_OK)	
		st=store.objects.get(user=request.user)
		st.image.save('image.jpg',x)
		st.image1.save("image1.jpg",y)
		st.save()
		context['status']="success"
		return HttpResponse(json.dumps(context), content_type='application/json')
	else:
		context['status']="Restaurant not exists"
		return HttpResponse(json.dumps({"status","Not exists"}), content_type='application/json')			



@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_resturent_image(request):
	context={}
	if resturent.objects.filter(user=request.user).exists():
		image=request.data.get("image")
		image1=request.data.get("image")
		try:
			image_data = b64decode(image)
			x= ContentFile(image_data)
		except:
			context['message']="image must be base64"
			return Response(context,status=HTTP_200_OK)
		try:
			image_data1 = b64decode(image1)
			y = ContentFile(image_data1)
		except:
			context['message']="image must be base64"
			return Response(context,status=HTTP_200_OK)	
		st=resturent.objects.get(user=request.user)
		st.image.save('image.jpg',x)
		st.image1.save("image1.jpg",y)
		st.save()
		context['status']="success"
		return HttpResponse(json.dumps(context), content_type='application/json')
	else:
		context['status']="Restaurant not exists"
		return HttpResponse(json.dumps({"status","Not exists"}), content_type='application/json')
	

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_store_details(request):
	context={}
	context['store']=store.objects.get(user=request.user).as_dict()
	return HttpResponse(json.dumps(context), content_type='application/json')
	

@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_resturent(request):
	context={}
	resturent_name=request.data.get("resturent_name")
	mobile=request.data.get("mobile")
	city=request.data.get("city")
	state=request.data.get("state")
	zipcode=request.data.get("zipcode")
	address=request.data.get("address")
	locality=request.data.get("locality")
	cat_id=request.data.get("cat_id")
	average_price=request.data.get("average_price")
	# image=request.data.getlist('image')
	#image1=request.data.get('image1')
	if check_blank_or_null([resturent_name,mobile,city,state,zipcode,address,locality,cat_id,average_price]) == True and resturent_category.objects.filter(pk=cat_id).exists() and resturent.objects.filter(user=request.user).exists():
		st,_=resturent.objects.get_or_create(user=request.user)
		st.resturent_name=resturent_name
		st.mobile=mobile
		st.city=city
		st.state=state
		st.zipcode=zipcode
		st.address=address
		st.locality=locality
		st.category=resturent_category.objects.get(pk=cat_id)
		st.average_price=average_price
		# try:
		# 	print(image)
		# 	image_data = b64decode(image[0])
		# 	#print(image_data)
		# 	x= ContentFile(image_data)
		# 	#print(x)
		# 	st.image.save('categore.jpg',x)
		# except:
		# 	context['message']="image must be base64"
		# 	return Response(context,status=HTTP_200_OK)	
		# try:
		# 	image_data = b64decode(image[1])
		# 	x= ContentFile(image_data)
		# 	st.image1.save('category_image.jpg',x)
		# except:
		# 	context['message']="image1 must be base64"
		# 	return Response(context,status=HTTP_200_OK)
		#st.image.save('category_image.jpg',x)
		#st.image1.save('category_image.jpg',x)
		st.save()
		context['message']="successfully Updated"
	else:
		context['message']="All field must be filled"	
	return HttpResponse(json.dumps(context), content_type='application/json')


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_resturent_details(request):
	context={}
	context['resturent']=resturent.objects.get(user=request.user).as_dict()
	return HttpResponse(json.dumps(context), content_type='application/json')
	
	

	
@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def delete_food(request,uid):
	context={}
	if resturent.objects.filter(user=request.user).exists():
		rest=resturent.objects.get(user=request.user)
		if food.objects.filter(resturent=rest,uid=uid).exists():
			f=food.objects.get(resturent=rest,uid=uid)
			f.delete()
			context['message']="Food has been successfully deleted"
		else:
			context['message']="Food is not exists"
	else:
		context['message']="Not Authorized"
	return HttpResponse(json.dumps(context), content_type='application/json')
				

	
@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def delete_product(request,uid):
	context={}
	if store.objects.filter(user=request.user).exists():
		st=store.objects.get(user=request.user)
		if store_product.objects.filter(store=st).exists():
			stp=store_product.objects.get(store=st,uid=uid)
			stp.delete()
			context['message']="product has been successfully deleted"
		else:
			context['message']="product is not exists"
	else:
		context['message']="Not Authorized"
	return HttpResponse(json.dumps(context), content_type='application/json')



@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def change_order_status(request):
	order_uid=request.data.get("order_uid")
	status=request.data.get("status")
	if store.objects.filter(user=request.user).exists() and status != 'cancel':
		st=store.objects.get(user=request.user)
		if order.objects.filter(uid=order_uid,rest=st.uid).exists():
			o=order.objects.get(uid=order_uid)
			if order_items.objects.filter(order=o).exists():
				otm=order_items.objects.filter(order=o)
				for x in otm:
					x.status=status
					x.save()
			o.status= status
			o.save()
			#send_notification(o.user,"Order status has changed "+status+" . Order ID "+o.uid)
			#send_notification(delivery_assign.objects.get(order=o).employee.user,"Order status has changed "+status+" . Order ID "+o.uid)
		return Response({'delivery': "item has been cancel"},status=HTTP_200_OK)		
	elif resturent.objects.filter(user=request.user).exists() and status != 'cancel':
		st=resturent.objects.get(user=request.user)
		if order.objects.filter(uid=order_uid,rest=st.uid).exists():
			o=order.objects.get(uid=order_uid)
			if order_items.objects.filter(order=o):
				otm=order_items.objects.filter(order=o)
				for x in otm:
					x.status=status
					x.save()
			o.status= status
			o.save()
			#send_notification(o.user,"Order status has changed "+status+" . Order ID "+o.uid)
			#send_notification(delivery_assign.objects.get(order=o).employee.user,"Order status has changed "+status+" . Order ID "+o.uid)
		return Response({'delivery': "item has been cancel"},status=HTTP_200_OK)
	else:
		return Response({"message":"You can not able to cancel this order"})		






