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
from delivery.models import *
import random
from django.contrib.gis.db.models.functions import Distance
# from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
import razorpay
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


class signup(APIView):
	permission_classes = (AllowAny,)
	@csrf_exempt
	def post(self, request):
		username=request.data.get("username")
		firstname=request.data.get("firstname")
		lastname=request.data.get("lastname")
		email=request.data.get("email")
		password=request.data.get("password")
		mobile=request.data.get("mobile")
		billing_city=request.data.get("billing_city")
		billing_state=request.data.get("billing_state")
		billing_zipcode=request.data.get("billing_zipcode")
		billing_address=request.data.get("billing_address")
		# shipping_city=request.data.get("shipping_city")
		# shipping_state=request.data.get("shipping_state")
		# shipping_zipcode=request.data.get("shipping_zipcode")
		# shipping_address=request.data.get("shipping_address")		
		#image=request.data["image"]
		# print(image)
		# print(username)
		# print(email)
		# print(image)
		# return Response({"message": "Username already exists created",},status=HTTP_200_OK)
		# print(username)
		# print(image)
		if username!="" and firstname!="" and lastname!="" and email!="" and password!="" and mobile!="" and billing_city!="" and billing_state!="" and billing_zipcode!="" and billing_address!="" and username!=None and firstname!=None and lastname!=None and email!=None and password!=None and mobile!=None and billing_city!=None and billing_state!=None and billing_zipcode!=None and billing_address!=None:
			if User.objects.filter(username=username,email=email).exists():
				return Response({"message": "Username already exists created",},status=HTTP_200_OK)
			else:
				user=User.objects.create_user(username=username,first_name=firstname,last_name=lastname,email=email,password=password)
				user.save()
				custurmerO=customer.objects.create()
				custurmerO.uid=get_random_string(10)
				custurmerO.user=user
				custurmerO.mobile=mobile
				custurmerO.billing_city=billing_city
				print(billing_city)
				custurmerO.billing_state=billing_state
				custurmerO.billing_zipcode=billing_zipcode
				custurmerO.billing_address=billing_address
				# custurmerO.shipping_city=shipping_city
				# custurmerO.shipping_state=shipping_state
				# custurmerO.shipping_zipcode=shipping_zipcode
				# custurmerO.shipping_address=shipping_address
				#custurmerO.image=image
				custurmerO.save()
				data={"username":username,'firstname':lastname}
				return Response({"message": "Your profile sucessfully created",'data':data},status=HTTP_200_OK)
		else:
			return Response({"message": "all field must be filled"},status=HTTP_200_OK)		

@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def user_profile(request):
	cust=customer.objects.get(user=request.user)
	context={}
	context['username']=cust.user.username
	context['first_name']=cust.user.first_name
	context['last_name']=cust.user.last_name
	context['email']=cust.user.email
	context['mobile']=cust.mobile
	context['billing_city']=cust.billing_city
	context['billing_state']=cust.billing_state
	context['billing_zipcode']=cust.billing_zipcode
	context['billing_address']=cust.billing_address
	return HttpResponse(json.dumps({"data":context}), content_type='application/json')


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def get_store_category(request):
	context=[]
	store_cat=store_category.objects.all()
	for x in store_cat:
		context.append(x.as_dict())
	return HttpResponse(json.dumps({"data":context}), content_type='application/json')

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def get_product_category(request):
	store_cat=store_product_category.objects.all()
	data=[]
	for x in store_cat:
		data.append(x.as_dict())
	return HttpResponse(json.dumps({"data":data}), content_type='application/json')

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def get_resturent_category(request):
	store_cat=resturent_category.objects.all()
	data=[]
	for x in store_cat:
		data.append(x.as_dict())
	return HttpResponse(json.dumps({"data":data}), content_type='application/json')



@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def get_food_category(request):
	store_cat=food_category.objects.all()
	data=[]
	for x in store_cat:
		data.append(x.as_dict())
	return HttpResponse(json.dumps({"data":data}), content_type='application/json')


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def get_product_by_category(request,name):
	if store_product_category.objects.filter(name=name).exists():
		cat=store_product_category.objects.get(name=name)
		stp=store_product.objects.filter(product_category=cat)
		context=[]
		for x in stp:
			data={}
			data["product"]=x.as_dict()
			image=[]
			specification=[]
			des=[]
			p=store_product.objects.get(uid=x.uid)
			pO=product_image.objects.filter(product=p)
			for y in pO:
				image.append(y.image.url)
			POO=product_specification.objects.filter(product=p)
			for y in POO:
				specification.append(y.specification)
				des.append(y.des)
			data['image']=image
			data['specification']=specification
			data['des']=des
			context.append(data)
		return HttpResponse(json.dumps({"data":context}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"Category is not exists"}), content_type='application/json')


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def get_product_by_category_in_city(request,name):
	if store_product_category.objects.filter(name=name).exists():
		cust=customer.objects.get(user=request.user)
		cat=store_product_category.objects.get(name=name)
		context=[]
		for y in store.objects.filter(city=cust.city):
			st=store.objects.get(uid=y.uid)
			stp=store_product.objects.filter(store=st,product_category=cat)		
			for x in stp:
				data={}
				data["product"]=x.as_dict()
				image=[]
				specification=[]
				des=[]
				p=store_product.objects.get(uid=x.uid)
				pO=product_image.objects.filter(product=p)
				for y in pO:
					image.append(y.image.url)
				POO=product_specification.objects.filter(product=p)
				for y in POO:
					specification.append(y.specification)
					des.append(y.des)
				data['image']=image
				data['specification']=specification
				data['des']=des
				context.append(data)
		return HttpResponse(json.dumps({"data":context}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"Category is not exists"}), content_type='application/json')




@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def detail_product_view(request,uid):
	if store_product.objects.filter(uid=uid).exists():
		stp=store_product.objects.get(uid=uid)
		context={}
		context['product']=stp.as_dict()
		image=[]
		for x in product_image.objects.filter(product=stp):
			image.append(x.image.url)
		context['image']=image
		specification=[]
		des=[]
		for x in product_specification.objects.filter(product=stp):
			specification.append(x.specification)
			des.append(x.des)
		context['specification']=specification
		context['des']=des
		return HttpResponse(json.dumps({"data":context}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"Product Id is not exists"}),content_type='application/json')



@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def get_food_by_category(request,name):
	if food_category.objects.filter(name=name).exists():
		cat=food_category.objects.get(name=name)
		stp=food.objects.filter(food_category=cat)
		context=[]
		for x in stp:
			data={}
			print(x.as_dict())
			data["product"]=x.as_dict()
			image=[]
			specification=[]
			des=[]
			p=food.objects.get(uid=x.uid)
			pO=food_image.objects.filter(food=p)
			for x in pO:
				image.append(x.image.url)
			POO=food_specification.objects.filter(food=p)
			for x in POO:
				specification.append(x.specification)
				des.append(x.des)
			data['image']=image
			data['specification']=specification
			data['des']=des
			data['food_price_type']=custom_food_price(p)
			context.append(data)
		return HttpResponse(json.dumps({"data":context}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"Category is not exists"}), content_type='application/json')


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def get_food_by_category_in_city(request,name):
	if food_category.objects.filter(name=name).exists():
		cust=customer.objects.get(user=request.user)
		cat=food_category.objects.get(name=name)
		context=[]
		for x in resturent.objects.filter(city=cust.city):
			st=resturent.objects.get(uid=x.uid)
			stp=food.objects.filter(food_category=cat)
			for x in stp:
				data={}
				data["product"]=x.as_dict()
				image=[]
				specification=[]
				des=[]
				p=food.objects.get(uid=x.uid)
				pO=food_image.objects.filter(food=p)
				for x in pO:
					image.append(x.image.url)
				POO=food_specification.objects.filter(food=p)
				for x in POO:
					specification.append(x.specification)
					des.append(x.des)
				data['image']=image
				data['specification']=specification
				data['des']=des		
				data['food_price_type']=custom_food_price(p)
				context.append(data)
		return HttpResponse(json.dumps({"data":context}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"Category is not exists"}), content_type='application/json')






@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def detail_food_view(request,uid):
	if food.objects.filter(uid=uid).exists():
		stp=food.objects.get(uid=uid)
		context={}
		context['food']=stp.as_dict()
		image=[]
		for x in food_image.objects.filter(food=stp):
			image.append(x.image.url)
		context['image']=image
		specification=[]
		des=[]
		for x in food_specification.objects.filter(food=stp):
			specification.append(x.specification)
			des.append(x.des)
		context['specification']=specification
		context['des']=des
		context['food_price_type']=custom_food_price(stp)
		return HttpResponse(json.dumps({"data":context}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"Product Id is not exists"}),content_type='application/json')


# @csrf_exempt
# @api_view(["GET"])
# @permission_classes((IsAuthenticated,))
# def detail_food_view(request,uid):
# 	if food.objects.filter(uid=uid).exists():
# 		stp=food.objects.get(uid=uid)custom_food_price
# 		context={}
# 		context['product']=stp.as_dict()
# 		image=[]
# 		for x in food_image.objects.filter(food=stp):
# 			image.append(x.image.url)
# 		context['image']=image
# 		specification=[]
# 		des=[]
# 		for x in food_specification.objects.filter(food=stp):
# 			specification.append(x.specification)
# 			des.append(x.des)
# 		context['specification']=specification
# 		context['des']=des
# 		return HttpResponse(json.dumps({"data":context}), content_type='application/json')
# 	else:
# 		return HttpResponse(json.dumps({"data":"food Id is not exists"}),content_type='application/json')


@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def store_list(request):
	storeO=store.objects.all()
	context=[]
	for x in storeO:
		context.append([x.as_dict(),st_rating(x.uid)])
	return HttpResponse(json.dumps({"data":context}), content_type='application/json')	


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def store_list_in_city(request):
	cust=customer.objects.get(user=request.user)
	storeO=store.objects.filter(city=cust.billing_city)
	context=[]
	for x in storeO:
		context.append([x.as_dict(),st_rating(x.uid)])
	return HttpResponse(json.dumps({"data":context}), content_type='application/json')	




@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def resturent_list(request):
	storeO=resturent.objects.all()
	context=[]
	for x in storeO:
		context.append([x.as_dict(),rest_rating(x.uid)])
	return HttpResponse(json.dumps({"data":context}), content_type='application/json')	



@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def resturent_list_in_city(request):
	cust=customer.objects.get(user=request.user)
	storeO=resturent.objects.filter(city=cust.billing_city)
	context=[]
	for x in storeO:
		context.append([x.as_dict(),rest_rating(x.uid)])
	return HttpResponse(json.dumps({"data":context}), content_type='application/json')	



@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def store_products(request,uid):
	if store.objects.filter(uid=uid).exists():
		st=store.objects.get(uid=uid)
		stp=store_product.objects.filter(store=st)
		context=[]
		for x in stp:
			data={}
			data["product"]=x.as_dict()
			image=[]
			specification=[]
			des=[]
			p=store_product.objects.get(uid=x.uid)
			pO=product_image.objects.filter(product=p)
			for y in pO:
				image.append(y.image.url)
			POO=product_specification.objects.filter(product=p)
			for y in POO:
				specification.append(y.specification)
				des.append(y.des)
			data['image']=image
			data['specification']=specification
			data['des']=des
			context.append(data)
		return HttpResponse(json.dumps({"data":context}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"Category is not exists"}), content_type='application/json')


@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def resturent_foods(request,uid):
	if resturent.objects.filter(uid=uid).exists():
		rt=resturent.objects.get(uid=uid)
		rtf=food.objects.filter(resturent=rt)
		context=[]
		for x in rtf:
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
			context.append(data)
		return HttpResponse(json.dumps({"data":context}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"Category is not exists"}), content_type='application/json')

@csrf_exempt
@api_view(['GET'])
def get_food_extra_items(request,uid):
	context = []
	if uid != '' and uid != None and food.objects.filter(uid=uid).exists():
		foodO = food.objects.get(uid=uid)
		food_extra_itemsO = food_extra_items.objects.filter(for_food=foodO)
		for x in food_extra_itemsO:
			tmp={}
			tmp['id'] = x.id
			tmp['item_name'] = x.item_name
			tmp['price'] = x.price
			context.append(tmp)
		return HttpResponse(json.dumps({'data': context}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({'data': 'invalid uid'}), content_type='application/json')

@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_to_cart(request):
	uid = request.POST.get('uid')
	if store_product.objects.filter(uid=uid).exists():
		c,__=cart.objects.get_or_create(item_uid=uid,item_type="product",user=request.user)
		c.save()
		return HttpResponse(json.dumps({"data":"Product has been added to cart"}), content_type='application/json')		
	elif food.objects.filter(uid=uid).exists():
		c,__=cart.objects.get_or_create(item_uid=uid,item_type="food",user=request.user)
		c.save()

		return HttpResponse(json.dumps({"data":"food has been added to cart"}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"uid is not exists"}), content_type='application/json')

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def remove_to_cart(request,uid):
	if store_product.objects.filter(uid=uid).exists():
		c=cart.objects.get(item_uid=uid,item_type="product",user=request.user)
		c.delete()
		return HttpResponse(json.dumps({"data":"Product has been deleted form cart"}), content_type='application/json')		
	elif food.objects.filter(uid=uid).exists():
		c=cart.objects.get(item_uid=uid,item_type="food",user=request.user)
		############changed_here#########
		# food_sub_cat.objects.get(pk=food_cat_id).exists():	
		if cart_sub_cat.objects.filter(for_cart_item=c.item_uid,user=request.user).exists():
			ct=cart_sub_cat.objects.get(for_cart_item=c.item_uid,user=request.user)
			ct.delete()
			# c.delete()
		if cart_exra_item.objects.filter(for_cart_item=c.item_uid,user=request.user).exists():
			cart_exra_itemO = cart_exra_item.objects.filter(for_cart_item=c.item_uid,user=request.user)
			for q in cart_exra_itemO:
				q.delete()
		c.delete()
		return HttpResponse(json.dumps({"data":"food has been deleted form cart"}), content_type='application/json')

		# else:
		# 	c.delete()
		# 	return HttpResponse(json.dumps({"data":"food has been deleted form cart"}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"uid is not exists"}), content_type='application/json')


# @csrf_exempt
# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# def update_cart(request):
# 	uid = request.data.get('uid')
# 	quantity=request.data.get("quantity")
# 	if quantity!="":
# 		if cart.objects.filter(item_uid=uid, user=request.user).exists():
# 			c=cart.objects.get(item_uid=uid, user=request.user)
# 			c.quantity=quantity
# 			c.save()
# 			return HttpResponse(json.dumps({"data":"cart has been updated"}), content_type='application/json')
# 		else:
# 			return HttpResponse(json.dumps({"data":"uid is not exists"}), content_type='application/json')
# 	else:
# 		return HttpResponse(json.dumps({"data":"quantity must not ve"}), content_type='application/json')



@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_cart(request):
	uid = request.data.get('uid')
	quantity=request.data.get("quantity")
	###########changed_here################
	extra_item = request.POST.getlist('extra_item')
	food_cat_id = request.data.get('food_cat_id')
	if quantity!="" and uid != "" :
		if cart.objects.filter(item_uid=uid, user=request.user).exists():
			c=cart.objects.get(item_uid=uid, user=request.user)
			c.quantity=quantity
			if food_cat_id != None and food_cat_id != "" and food_sub_cat.objects.filter(pk=food_cat_id).exists():
				food_sub_catO = food_sub_cat.objects.get(pk=food_cat_id)
				ct,__=cart_sub_cat.objects.get_or_create(for_cart_item=c.item_uid,user=request.user)
				ct.cat_name = food_sub_catO.cat_name
				ct.price = food_sub_catO.price
				ct.save()
			else:
				pass
			c.save()
			if len(extra_item) > 0:
				for i in extra_item:
					# if cart_exra_item.objects.filter(for_cart_item=c.item_uid,user=request.user).exists():
					# 	cart_exra_itemO = cart_exra_item.objects.filter(for_cart_item=c.item_uid,user=request.user)
					# for cart_extra in cart_exra_itemO:
					# cart_extra.delete()
					if i!="":
						food_extra_itemsO = food_extra_items.objects.get(pk=i)
						cart_exra_item1 = cart_exra_item.objects.create(for_cart_item=c.item_uid, cat_name=food_extra_itemsO.item_name, price=food_extra_itemsO.price)
						cart_exra_item1.save()
					else:
						pass
			else:
				pass
			return HttpResponse(json.dumps({"data":"cart has been updated"}), content_type='application/json')
		else:
			return HttpResponse(json.dumps({"data":"uid is not exists"}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"quantity must not ve"}), content_type='application/json')



@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def get_restaurant_by_cat(request, catId):
	context = {}
	if catId != '' and catId != None:
		if resturent_category.objects.filter(pk=catId).exists():
			dataL = []
			restCat = resturent_category.objects.get(pk=catId)
			restaurantO = resturent.objects.filter(category=restCat)
			for rest in restaurantO:
				tmp = {}
				tmp['resturent'] = rest.as_dict()
				tmp['rating']=rest_rating(rest.uid)
				dataL.append(tmp)
			if len(dataL) > 0:
				context['data'] = dataL
			else:
				context['data'] = 'no_records'
		else:
			context['data'] = 'no_records'
	else:
		context['data'] = 'supply full details'
	return HttpResponse(json.dumps(context), content_type='application/json')


		





@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def get_store_by_cat(request, catId):
	context = {}
	if catId != '' and catId != None:
		if store_category.objects.filter(pk=catId).exists():
			dataL = []
			store_catO = store_category.objects.get(pk=catId)
			storeO = store.objects.filter(category=store_catO)
			for st in storeO:
				tmp = {}
				tmp['store'] = st.as_dict()
				tmp['rating']= st_rating(st.uid)
				dataL.append(tmp)
			if len(dataL) > 0:
				context['data'] = dataL
			else:
				context['data'] = 'no_records'
		else:
			context['data'] = 'no_records'
	else:
		context['data'] = 'supply full details'
	return HttpResponse(json.dumps(context), content_type='application/json')


@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def get_resturent_by_food_cat(request, cat):
	context={}
	if cat != '' and cat != None:
		restL = []
		storeL = []
		uid=[]
		if food_category.objects.filter(name=cat).exists():
			food_categoryO = food_category.objects.get(name=cat)
			if food.objects.filter(food_category=food_categoryO):
				foodO = food.objects.filter(food_category=food_categoryO)
				for x in foodO:
					if x.resturent.uid not in uid:
						restCat = resturent.objects.get(pk=x.resturent.pk)
						tmp = {}
						tmp['restaurant'] = restCat.as_dict()
						tmp['rating'] = rest_rating(restCat.uid)
						restL.append(tmp)
						uid.append(x.resturent.uid)
				if len(restL) > 0:
					context['data'] = restL
			else:
				context['data']="not exists"		
		elif store_product_category.objects.filter(name=cat).exists():
			catO = store_product_category.objects.get(name=cat)
			if store_product.objects.filter(product_category=catO).exists():
				store_productO = store_product.objects.filter(product_category=catO)
				for x in store_productO:
					if x.store.uid not in uid:
						st=store.objects.get(pk=x.store.pk)
						tmp = {}
						tmp['store'] = st.as_dict()
						tmp['rating']= st_rating(st.uid)
						storeL.append(tmp)
				if len(storeL) > 0:
					context['data'] = storeL
			else:
				context['data']="not exists"		
		else:
			context['data'] = 'no records found'
	else:
		context['data'] = 'server will not give any results for these type of queries'
	return HttpResponse(json.dumps(context), content_type='application/json')


@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def get_all_store_product(request):
	context = {}
	dataL= []
	# if store_product.objects.all().exists():
	store_productO = store_product.objects.all()
	for x in store_productO:
		stp=store_product.objects.get(uid=x.uid)
		tmp = {}
		tmp['product'] = stp.as_dict()
		image=[]
		for y in product_image.objects.filter(product=stp):
			image.append(y.image.url)
		tmp['image']=image
		specification=[]
		des=[]
		for y in product_specification.objects.filter(product=stp):
			specification.append(y.specification)
			des.append(y.des)
		tmp['specification']=specification
		tmp['des']=des
		dataL.append(tmp)
	if len(dataL) > 0:
		context['data'] = dataL
	else:
		context['data'] = 'no_records'
	return HttpResponse(json.dumps(context), content_type='application/json')


@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def get_all_food(request):
	context = {}
	dataL = []
	foodO = food.objects.all()
	for x in foodO:
		stp=food.objects.get(uid=x.uid)
		tmp = {}
		tmp['food'] = x.as_dict()
		image=[]
		for y in food_image.objects.filter(food=stp):
			image.append(y.image.url)
		tmp['image']=image
		specification=[]
		des=[]
		for y in food_specification.objects.filter(food=stp):
			specification.append(y.specification)
			des.append(y.des)
		tmp['specification']=specification
		tmp['des']=des
		tmp['custom_food_price']=custom_food_price(stp)
		dataL.append(tmp)
	if len(dataL) > 0:
		context['data'] = dataL
	else:
		context['data'] = 'no records found'
	return HttpResponse(json.dumps(context), content_type='application/json')


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def all_cart(request):
	context=[]
	cart_value = 0
	i=1
	j=1
	for x in cart.objects.filter(user=request.user):
		if x.item_type=="food":
			data={}
			stp=food.objects.get(uid=x.item_uid)
			data['food']=stp.as_dict()
			data['uid']=stp.uid
			data['price']=stp.price
			data['name']=stp.name
			image=[]
			for y in food_image.objects.filter(food=stp):
				image.append(y.image.url)
			data['image']=image
			specification=[]
			des=[]
			for y in food_specification.objects.filter(food=stp):
				specification.append(y.specification)
				des.append(y.des)

			data['specification']=specification
			data['des']=des
			data['quantity'] = x.quantity

			if cart_sub_cat.objects.filter(for_cart_item=stp.uid,user=request.user).exists():
				sub_c=cart_sub_cat.objects.get(for_cart_item=stp.uid,user=request.user)	
				data['sub_details'] = sub_c.as_dict()
				cart_value += int(x.quantity)*int(sub_c.price)
			else:
				cart_value += int(x.quantity)*int(stp.price)

			if cart_exra_item.objects.filter(for_cart_item=stp.uid,user=request.user).exists():
				cart_exra_itemO = cart_exra_item.objects.filter(for_cart_item=stp.uid,user=request.user)
				tmp=[]
				for q in cart_exra_itemO:
					cart_value += int(x.quantity)*int(q.price)
					tmp.append(q.as_dict())
				data['extra_item'] = tmp

			context.append(data)
			i+=1
		elif x.item_type=="product":
			stp=store_product.objects.get(uid=x.item_uid)
			data={}
			data['product']=stp.as_dict()
			data['uid']=stp.uid
			data['price']=stp.price
			data['name']=stp.name

			image=[]
			for y in product_image.objects.filter(product=stp):
				image.append(y.image.url)
			data['image']=image
			specification=[]
			des=[]
			for y in product_specification.objects.filter(product=stp):
				specification.append(y.specification)
				des.append(y.des)
			data['specification']=specification
			data['des']=des
			data['quantity'] = x.quantity
			cart_value += int(x.quantity)*int(stp.price)
			context.append(data)
			j+=1
	return HttpResponse(json.dumps({"data":context,"cart_value":cart_value}), content_type='application/json')


# # def create_order(amount, currency='INR', receipt, notes={}):
# # 	client = razorpay.client(auth=("rzp_live_kly6Kq05ZPRWsm", "MsdmVDWZqL0rl24kVmDEXO1I"))

# # 	client.order.create(amount=amount, currency=currency, receipt=receipt, notes=notes)


# @csrf_exempt
# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# def checkout(request):
# 	if request.method == 'POST':
# 		if cart.objects.filter(user=request.user).exists():
# 			shipping_city=request.data.get("shipping_city")
# 			shipping_state=request.data.get("shipping_state")
# 			shipping_zipcode=request.data.get("shipping_zipcode")
# 			shipping_address=request.data.get("shipping_address")
# 			longitude=request.data.get("longitude")
# 			latitude=request.data.get("latitude")
# 			promo_code=request.data.get("promo_code")

# 			if promo_code.objects.filter(code=promo_code).exists() and promo_code!=None or promo_code=="" :
# 				if shipping_city!="" and shipping_state!="" and shipping_zipcode!="" and shipping_address!="" and latitude!="" and longitude!="":

# 					if promo_code!="" and order.objects.filter(code=promo_code).exists==False:
# 						price = []

# 						for x in cart.objects.filter(user=request.user):
# 							pid = x.item_uid
# 							gstVal = 0
# 							if store_product.objects.filter(uid=x.uid).exists():

# 								stoo=store_product.objects.get(uid=x.uid)
# 								gstVal = (int(stoo.gst)*int(stoo.price))/100
# 								priceN = (gstVal+stoo.price)*x.quantity

# 							elif food.objects.filter(uid=x.uid).exists():
# 								stoo=food.objects.get(uid=x.uid)
# 								gstVal = (int(stoo.gst)*int(stoo.price))/100
# 								priceN = (gstVal+stoo.price)*x.quantity
# 							price.append(priceN)
# 						total_price = price.sum()
# 						total_discounted_price = 0
# 						if promo_code!="" and order.objects.filter(code=promo_code).exists()==False:
# 							pc=promo_code.objects.get(code=promo_code)
# 							total_discounted_price=price.sum()-pc.price



# @csrf_exempt
# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# def order_placed_by_address(request):
# 	if cart.objects.filter(user=request.user).exists():
# 		shipping_city=request.data.get("shipping_city")
# 		shipping_state=request.data.get("shipping_state")
# 		shipping_zipcode=request.data.get("shipping_zipcode")
# 		shipping_address=request.data.get("shipping_address")
# 		longitude=request.data.get("longitude")
# 		latitude=request.data.get("latitude")
# 		promo_code=request.data.get("promo_code")
# 		if promo_code.objects.filter(code=promo_code).exists() and promo_code!=None or promo_code=="" :
# 			if shipping_city!="" and shipping_state!="" and shipping_zipcode!="" and shipping_address!="" and latitude!="" and longitude!="":

# 				if promo_code!="" and order.objects.filter(code=promo_code).exists()==False:
# 					orderO=order.objects.create()
# 					orderO.uid=get_random_string(10)
# 					orderO.user=request.user
# 					orderO.opt=get_random_string(5)
# 					orderO.promo_code=promo_code
# 					orderO.shipping_city=shipping_city
# 					orderO.shipping_state=shipping_state
# 					orderO.shipping_zipcode=shipping_zipcode
# 					orderO.shipping_address=shipping_address
# 					orderO.location=Point(float(latitude),float(longitude), srid=4326)
# 					# custurmerO.save()
# 					orderO.save()
# 				elif promo_code=="":
# 					orderO=order.objects.create()
# 					orderO.uid=get_random_string(10)
# 					orderO.user=request.user
# 					orderO.opt=get_random_string(5)
# 					orderO.shipping_city=shipping_city
# 					orderO.shipping_state=shipping_state
# 					orderO.shipping_zipcode=shipping_zipcode
# 					orderO.shipping_address=shipping_address
# 					orderO.location=Point(float(latitude),float(longitude), srid=4326)
# 					# custurmerO.save()
# 					orderO.save()					 	
# 				else:
# 					return HttpResponse(json.dumps({"data":"promo_code is all ready used"}), content_type='application/json')						
# 				# custurmerO=order_address.objects.create()
# 				# custurmerO.order=orderO
# 				# custurmerO.shipping_city=shipping_city
# 				# custurmerO.shipping_state=shipping_state
# 				# custurmerO.shipping_zipcode=shipping_zipcode
# 				# custurmerO.shipping_address=shipping_address
# 				# custurmerO.location=Point(float(latitude),float(longitude), srid=4326)
# 				# custurmerO.save()
# 				de=delivery_employee.objects.annotate(distance=Distance('location',Point(float(latitude), float(longitude), srid=4326))).order_by('distance')[0:6]
# 				random.shuffle(de)
# 				# print(de)
# 				for x in de:
# 					print(x)
# 					emp=delivery_employee.objects.get(uid=x.uid)
# 					del_assign=delivery_assign.objects.filter(employee=emp).count()
# 					if x.package>del_assign:
# 						del_assignO,__=delivery_assign.objects.get_or_create(order=orderO,employee=emp)
# 						del_assignO.status="pending"
# 						del_assignO.des="waiting for delivery"
# 						del_assignO.save()
# 				if cart.objects.filter(user=request.user).exists():
# 					price=[]
# 					for x in cart.objects.filter(user=request.user):
# 						print(x)
# 						order_itemsO=order_items.objects.create()
# 						order_itemsO.item_uid=x.item_uid
# 						order_itemsO.item_type=x.item_type
# 						order_itemsO.order=orderO
# 						order_itemsO.quantity=x.quantity
# 						# order_itemsO.save()
# 						if store_product.objects.filter(uid=x.uid).exists():
# 							stoo=store_product.objects.get(uid=x.uid)
# 							priceN = stoo.price*x.quantity

# 						elif food.objects.filter(uid=x.uid).exists():
# 							stoo=food.objects.get(uid=x.uid)
# 							priceN = stoo.price*x.quantity
# 						price.append(priceN)	
# 						order_itemsO.cost = priceN
# 						order_itemsO.save()
# 						cartO=cart.objects.get(item_uid=x.item_uid)
# 						cartO.delete()
# 					if promo_code.objects.filter(code=promo_code).exists() or promo_code!="":	
# 						pc=promo_code.objects.get(code=promo_code)
# 						total_price=price.sum()-pc.price
# 						total_price=(((total_price/100)*18)+total_price)
# 					else:
# 						total_price=price.sum()
# 						total_price=(((total_price/100)*18)+total_price)
# 					return HttpResponse(json.dumps({"data":"Your order has been placed","total_price":total_price}), content_type='application/json')	
# 				else:
# 					return HttpResponse(json.dumps({"data":"cart is empty"}), content_type='application/json')
# 		return HttpResponse(json.dumps({"data":"cart is empty"}), content_type='application/json')		


# @csrf_exempt
# @api_view(['GET'])
# @permission_classes((IsAuthenticated,))
# def order_placed_same_address(request):
# 	cust=customer.objects.get(user=request.user)
# 	orderO=order.objects.create()
# 	orderO.uid=get_random_string(10)
# 	orderO.user=request.user
# 	orderO.save()
# 	for x in cart.objects.filter(user=request.user):
# 		order_itemsO=order_items.objects.create()
# 		order_itemsO.item_uid=x.item_uid
# 		order_itemsO.item_type=x.item_type
# 		order_itemsO.order=orderO
# 		order_itemsO.quantity=x.quantity
# 		order_itemsO.save()
# 		cartO=cart.objects.get(item_uid=x.item_uid)
# 		cartO.delete()
# 	return HttpResponse(json.dumps({"data":"Your order has been placed"}), content_type='application/json')	

# def login_to_pay(request, code):
# 	context = {}
# 	promo = 0
# 	price=[]
# 	total_price=0
# 	amount=0
# 	if request.method == 'POST':
# 		username = request.POST.get('username')
# 		password = request.POST.get('password')
# 		if username is None or password is None:
# 			context['data'] = 'both feilds are compulsary'
# 			return render(request, 'foodordering/login.html', context)
# 		else:
# 			user = authenticate(username=username, password=password)
# 			if not user:
# 				context['data'] = 'Invalid creds!'
# 				return render(request, 'foodordering/login.html', context)
# 			else:
# 				if promo_code.objects.filter(code=code).exists() and code != None or code == "":
# 					promo=1
# 					if cart.objects.filter(user=user).exists():
# 						for x in cart.objects.filter(user=user):
# 							priceN = 0
# 							if store_product.objects.filter(uid=x.item_uid).exists():
# 								stoo=store_product.objects.get(uid=x.item_uid)
# 								priceN = stoo.price*x.quantity
# 							elif food.objects.filter(uid=x.item_uid).exists():
# 								stoo=food.objects.get(uid=x.item_uid)
# 								priceN = stoo.price*x.quantity
# 							price.append(priceN)
# 					else:
# 						return render(request, 'foodordering/pay.html',{'error':'cart empty'})

# 				elif promo_code.objects.filter(code=code).exists() == False:
# 					if cart.objects.filter(user=user).exists():
# 						for x in cart.objects.filter(user=user):
# 							priceN = 0
# 							if store_product.objects.filter(uid=x.item_uid).exists():
# 								stoo=store_product.objects.get(uid=x.item_uid)
# 								priceN = stoo.price*x.quantity
# 							elif food.objects.filter(uid=x.item_uid).exists():
# 								stoo=food.objects.get(uid=x.item_uid)
# 								priceN = stoo.price*x.quantity
# 							price.append(priceN)
# 					else:
# 						return render(request, 'foodordering/pay.html', {'error':'cart empty'})
# 				if promo == 1 and promo_code.objects.filter(code=code).exists():
# 					pc=promo_code.objects.get(code=code)
# 					total_price=sum(price)-pc.price
# 					amount=(((total_price/100)*18)+total_price)
# 				else:
# 					total_price=sum(price)
# 					amount=(((total_price/100)*18)+total_price)

# 				client = razorpay.Client(auth=("rzp_live_kly6Kq05ZPRWsm", "MsdmVDWZqL0rl24kVmDEXO1I"))
# 				q = client.order.create(dict(amount=int(amount)*100, currency='INR', notes={}))
# 				if not q:
# 					return render(request, 'foodordering/pay.html', {'error': 'oops something went wrong'})
# 				orderO = order.objects.create()
# 				orderO.uid = q['id']
# 				orderO.user = user
# 				orderO.amount = q['amount']
# 				orderO.save()

# 				return render(request, 'foodordering/pay.html', {'payment':q})


# 	else:
# 		return render(request, 'foodordering/login.html', context)


@permission_classes((IsAuthenticated,))
def create_order(request):
	if request.method == 'POST':
		promo = 0
		price=[]
		total_price=0
		amount=0
		code=request.POST.get("promo_code")
		if promo_code.objects.filter(code=code).exists() and code != None or code == "":
			promo=1
			if cart.objects.filter(user=request.user).exists():
				for x in cart.objects.filter(user=request.user):
					priceN = 0
					if store_product.objects.filter(uid=x.item_uid).exists():
						stoo=store_product.objects.get(uid=x.item_uid)
						priceN = stoo.price*x.quantity
					elif food.objects.filter(uid=x.item_uid).exists():
						stoo=food.objects.get(uid=x.item_uid)
						if cart_sub_cat.objects.filter(for_cart_item=x.item_uid,user=request.user).exists():
							csc=cart_sub_cat.objects.get(for_cart_item=x.item_uid,user=request.user)
							priceN = csc.price*x.quantity
						else:	
							priceN = stoo.price*x.quantity
					price.append(priceN)
			else:
				return HttpResponse({'data':'cart empty'}, content_type='application/json')

		elif promo_code.objects.filter(code=code).exists() == False:
			if cart.objects.filter(user=request.user).exists():
				for x in cart.objects.filter(user=request.user):
					priceN = 0
					if store_product.objects.filter(uid=x.item_uid).exists():
						stoo=store_product.objects.get(uid=x.item_uid)
						priceN = stoo.price*x.quantity
					elif food.objects.filter(uid=x.item_uid).exists():
						stoo=food.objects.get(uid=x.item_uid)
						if cart_sub_cat.objects.filter(for_cart_item=x.item_uid,user=request.user).exists():
							csc=cart_sub_cat.objects.get(for_cart_item=x.item_uid,user=request.user)
							priceN = csc.price*x.quantity
						else:	
							priceN = stoo.price*x.quantity
						# priceN = stoo.price*x.quantity
					price.append(priceN)
			else:
				return HttpResponse({'data':'cart empty'}, content_type='application/json')
		if promo == 1 and promo_code.objects.filter(code=code).exists():
			pc=promo_code.objects.get(code=code)
			total_price=sum(price)-pc.price
			amount=(((total_price/100)*18)+total_price)
		else:
			total_price=sum(price)
			amount=(((total_price/100)*18)+total_price)

		client = razorpay.Client(auth=("rzp_live_kly6Kq05ZPRWsm", "MsdmVDWZqL0rl24kVmDEXO1I"))
		q = client.order.create(dict(amount=int(amount)*100, currency='INR', notes={}))
		if not q:
			return HttpResponse({'data':'error occured'}, content_type='application/json')
		else:
			return HttpResponse(json.dumps(q), content_type='application/json')

def success(request, payment_id):
	if payment_id != "":
		return HttpResponse(json.dumps({'success':'complete', 'payment_id': payment_id}), content_type='application/json')
	else:
		pass


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def order_placed_by_address(request):
	tmp = ''
	avg_time = 0
	loc = ''
	p_code=0
	total_price=0

	shipping_city=request.data.get("shipping_city")
	shipping_state=request.data.get("shipping_state")
	shipping_zipcode=request.data.get("shipping_zipcode")
	shipping_address=request.data.get("shipping_address")
	longitude=request.data.get("longitude")
	latitude=request.data.get("latitude")
	code=request.data.get("promo_code")
	order_id = request.data.get("order_id")
	if cart.objects.filter(user=request.user).exists():
		if promo_code.objects.filter(code=code).exists() and code!=None or code=="" :
			if shipping_city!="" and shipping_state!="" and shipping_zipcode!="" and shipping_address!="" and latitude!="" and longitude!="":
				if code!="" and order.objects.filter(code=code).exists()==False:
					orderO=order.objects.get(uid=order_id)
					orderO.uid=order_id
					orderO.user=request.user
					orderO.opt=get_random_string(5)
					orderO.promo_code=code
					orderO.shipping_city=shipping_city
					orderO.shipping_state=shipping_state
					orderO.shipping_zipcode=shipping_zipcode
					orderO.order_type = 'online'
					orderO.shipping_address=shipping_address
					orderO.location=Point(float(latitude),float(longitude), srid=4326)
					# custurmerO.save()
					loc = Point(float(latitude),float(longitude), srid=4326)
					orderO.save()
					p_code=1
				elif code=="":
					orderO=order.objects.get(uid=order_id)
					orderO.uid=order_id
					orderO.user=request.user
					orderO.opt=get_random_string(5)
					orderO.shipping_city=shipping_city
					orderO.shipping_state=shipping_state
					orderO.shipping_zipcode=shipping_zipcode
					orderO.order_type = 'online'
					orderO.shipping_address=shipping_address
					orderO.location=Point(float(latitude),float(longitude), srid=4326)
					# custurmerO.save()
					loc = Point(float(latitude),float(longitude), srid=4326)
					orderO.save()					 	
				else:
					return HttpResponse(json.dumps({"data":"promo_code is all ready used"}), content_type='application/json')						
				# custurmerO=order_address.objects.create()
				# custurmerO.order=orderO
				# custurmerO.shipping_city=shipping_city
				# custurmerO.shipping_state=shipping_state
				# custurmerO.shipping_zipcode=shipping_zipcode
				# custurmerO.shipping_address=shipping_address
				# custurmerO.location=Point(float(latitude),float(longitude), srid=4326)
				# custurmerO.save()
				de=delivery_employee.objects.annotate(distance=Distance('location',Point(float(latitude), float(longitude), srid=4326))).order_by('distance')
				random.shuffle(de)
				# print(de)
				for x in de:
					emp=delivery_employee.objects.get(uid=x.uid)
					del_assign=delivery_assign.objects.filter(employee=emp).count()
					if x.package>del_assign:
						del_assignO,__=delivery_assign.objects.get_or_create(order=orderO,employee=emp)
						del_assignO.status="pending"
						del_assignO.des="waiting for delivery"
						del_assignO.save()
						tmp = emp.location
						break
				
				price=[]
				for x in cart.objects.filter(user=request.user):
					order_itemsO=order_items.objects.create()
					order_itemsO.item_uid=x.item_uid
					order_itemsO.item_type=x.item_type
					order_itemsO.order=orderO
					order_itemsO.quantity=x.quantity
					# order_itemsO.save()
					if store_product.objects.filter(uid=x.item_uid).exists():
						stoo=store_product.objects.get(uid=x.item_uid)
						priceN = stoo.price*x.quantity

					elif food.objects.filter(uid=x.item_uid).exists():
						stoo=food.objects.get(uid=x.item_uid)
						if cart_sub_cat.objects.filter(for_cart_item=x.item_uid,user=request.user).exists():
							csc=cart_sub_cat.objects.get(for_cart_item=x.item_uid,user=request.user)
							priceN = csc.price*x.quantity
							csc.delete()
						else:	
							priceN = stoo.price*x.quantity
						if cart_exra_item.objects.filter(user=request.user, for_cart_item=x.item_uid).exists():
							cat_ex=cart_exra_item.objects.filter(user=request.user, for_cart_item=x.item_uid)
							for x in cat_ex:
								priceN+=x.price*x.quantity
								x.delete()
						# priceN = stoo.price*x.quantity
					price.append(priceN)	
					order_itemsO.cost = priceN
					order_itemsO.save()
					cartO=cart.objects.get(item_uid=x.item_uid,user=request.user)
					cartO.delete()
				if p_code==1:	
					pc=promo_code.objects.get(code=code)
					total_price=sum(price)-pc.price
					total_price=(((total_price/100)*18)+total_price)
				else:
					total_price=sum(price)
					total_price=(((total_price/100)*18)+total_price)
				avg_time=(tmp.distance(loc)*100)/45
				return HttpResponse(json.dumps({"data":"Your order has been placed", "total_price":total_price,'employee_location_latitude':tmp.x, 'employee_location_longitude':tmp.y,'average_time': avg_time}), content_type='application/json')	
			else:
				return HttpResponse(json.dumps({"data":"must need to filled field1"}), content_type='application/json')
		else:
			return HttpResponse(json.dumps({"data":"promo code not exists"}), content_type='application/json')		
	else:				
		return HttpResponse(json.dumps({"data":"cart is empty"}), content_type='application/json')		


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def order_placed_by_address_cod(request):
	tmp = ''
	avg_time = 0
	loc = ''
	p_code=0
	total_price=0
	shipping_city=request.data.get("shipping_city")
	shipping_state=request.data.get("shipping_state")
	shipping_zipcode=request.data.get("shipping_zipcode")
	shipping_address=request.data.get("shipping_address")
	longitude=request.data.get("longitude")
	latitude=request.data.get("latitude")
	code=request.data.get("promo_code")
	order_id = get_random_string(10)
	if cart.objects.filter(user=request.user).exists():
		if promo_code.objects.filter(code=code).exists() and code!=None or code=="" :
			if shipping_city!="" and shipping_state!="" and shipping_zipcode!="" and shipping_address!="" and latitude!="" and longitude!="":

				if code!="" and order.objects.filter(code=code).exists()==False:
					orderO=order.objects.create()
					orderO.uid=order_id
					orderO.user=request.user
					orderO.opt=get_random_string(5)
					orderO.promo_code=code
					orderO.shipping_city=shipping_city
					orderO.shipping_state=shipping_state
					orderO.shipping_zipcode=shipping_zipcode
					orderO.order_type = 'cod'
					orderO.shipping_address=shipping_address
					orderO.location=Point(float(latitude),float(longitude), srid=4326)
					# custurmerO.save()
					loc = Point(float(latitude),float(longitude), srid=4326)
					orderO.save()
					p_code=1
				elif code=="":
					orderO=order.objects.create()
					orderO.uid=order_id
					orderO.user=request.user
					orderO.opt=get_random_string(5)
					orderO.shipping_city=shipping_city
					orderO.shipping_state=shipping_state
					orderO.shipping_zipcode=shipping_zipcode
					orderO.order_type = 'cod'
					orderO.shipping_address=shipping_address
					orderO.location=Point(float(latitude),float(longitude), srid=4326)
					# custurmerO.save()
					loc = Point(float(latitude),float(longitude), srid=4326)
					orderO.save()					 	
				else:
					return HttpResponse(json.dumps({"data":"promo_code is all ready used"}), content_type='application/json')						
				# custurmerO=order_address.objects.create()
				# custurmerO.order=orderO
				# custurmerO.shipping_city=shipping_city
				# custurmerO.shipping_state=shipping_state
				# custurmerO.shipping_zipcode=shipping_zipcode
				# custurmerO.shipping_address=shipping_address
				# custurmerO.location=Point(float(latitude),float(longitude), srid=4326)
				# custurmerO.save()
				de=delivery_employee.objects.annotate(distance=Distance('location',Point(float(latitude), float(longitude), srid=4326))).order_by('distance')
				random.shuffle(de)
				# print(de)
				for x in de:
					emp=delivery_employee.objects.get(uid=x.uid)
					del_assign=delivery_assign.objects.filter(employee=emp).count()
					if x.package>del_assign:
						del_assignO,__=delivery_assign.objects.get_or_create(order=orderO,employee=emp)
						del_assignO.status="pending"
						del_assignO.des="waiting for delivery"
						del_assignO.save()
						tmp = emp.location
						break
				
				price=[]
				for x in cart.objects.filter(user=request.user):
					print(x)
					order_itemsO=order_items.objects.create()
					order_itemsO.item_uid=x.item_uid
					order_itemsO.item_type=x.item_type
					order_itemsO.order=orderO
					order_itemsO.quantity=x.quantity
					# order_itemsO.save()
					if store_product.objects.filter(uid=x.item_uid).exists():
						stoo=store_product.objects.get(uid=x.item_uid)
						priceN = stoo.price*x.quantity

					elif food.objects.filter(uid=x.item_uid).exists():
						stoo=food.objects.get(uid=x.item_uid)
						if cart_sub_cat.objects.filter(for_cart_item=x.item_uid,user=request.user).exists():
							csc=cart_sub_cat.objects.get(for_cart_item=x.item_uid,user=request.user)
							priceN = csc.price*x.quantity
							csc.delete()
						else:	
							priceN = stoo.price*x.quantity
						if cart_exra_item.objects.filter(user=request.user, for_cart_item=x.item_uid).exists():
							cat_ex=cart_exra_item.objects.filter(user=request.user, for_cart_item=x.item_uid)
							for x in cat_ex:
								priceN+=x.price*x.quantity
					price.append(priceN)	
					order_itemsO.cost = priceN
					order_itemsO.save()
					cartO=cart.objects.get(item_uid=x.item_uid,user=request.user)
					cartO.delete()
				if p_code==1:	
					pc=promo_code.objects.get(code=code)
					total_price=sum(price)-pc.price
					total_price=(((total_price/100)*18)+total_price)
				else:
					total_price=sum(price)
					total_price=(((total_price/100)*18)+total_price)
				avg_time=(tmp.distance(loc)*100)/45
				return HttpResponse(json.dumps({"data":"Your order has been placed", "total_price":total_price,'employee_location_latitude':tmp.x, 'employee_location_longitude':tmp.y,'average_time': avg_time}), content_type='application/json')	
			else:
				return HttpResponse(json.dumps({"data":"must need to filled field1"}), content_type='application/json')
		else:
			return HttpResponse(json.dumps({"data":"promo code not exists"}), content_type='application/json')		
	else:				
		return HttpResponse(json.dumps({"data":"cart is empty"}), content_type='application/json')		

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def previous_order_complete(request):
	orderO=order.objects.filter(user=request.user,status="complete")
	context=[]
	for x in orderO:
		context.append(x.as_dict())
	return HttpResponse(json.dumps({"data":context}), content_type='application/json')	
	

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def previous_order_pending(request):
	orderO=order.objects.filter(user=request.user,status="pending")
	context=[]
	for x in orderO:
		context.append(x.as_dict())
	return HttpResponse(json.dumps({"data":context}), content_type='application/json')	
	

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def items_in_order(request,uid):
	orderO=order.objects.get(user=request.user,uid=uid)
	productl=[]
	foodl=[]
	od=order_items.objects.filter(order=orderO)
	i=1
	j=1
	for x in od:
		# data={}
		# data['quantity']=x.quantity
		if "product"==x.item_type:
			stp=store_product.objects.get(uid=x.item_uid)
			product={}
			product['product']=stp.as_dict()
			product['item_uid']=x.item_uid
			product['quantity']=x.quantity
			product['price']=x.cost
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
			# data['product']=product
			productl.append(product)
			i+=1
		elif "food"==x.item_type:
			foodO={}
			ftp=food.objects.get(uid=x.item_uid)
			foodO['food']=ftp.as_dict()
			foodO['item_uid']=x.item_uid
			foodO['quantity']=x.quantity
			foodO['price']=x.cost
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
			# data['food']=foodO
			foodl.append(foodO)
			j+=1

	return HttpResponse(json.dumps({"food":foodl,"product":productl}), content_type='application/json')	
	

@csrf_exempt
@api_view(['POST'])
def get_veg_noveg(request):
	food_type = request.data.get('food_type')
	foodL = []
	if food_type == 'Veg' or food_type == 'Nveg' and food_type in ['Veg','Nveg']:
		foodO = food.objects.filter(food_type=food_type)
		for x in foodO:
			tmp = {}
			tmp['food'] = x.as_dict()
			tmp['food_price_type']=custom_food_price(x)
			foodL.append(tmp)
		context['data'] = foodL
	else:
		context['message'] = 'error occured'
	return HttpResponse(json.dumps({"data":context}), content_type='application/json')


@csrf_exempt
@api_view(['POST'])
def get_veg_noveg_by_resturent(request):
	food_type = request.data.get('food_type')
	resturent_uid = request.data.get("resturent_uid")
	foodL = []
	if food_type == 'Veg' or food_type == 'Nveg' and food_type in ['Veg','Nveg']:
		res=resturent.objects.get(uid=resturent_uid)
		foodO = food.objects.filter(food_type=food_type,resturent=res)
		for x in foodO:
			tmp = {}
			tmp['food'] = x.as_dict()
			tmp['food_price_type']=custom_food_price(x)
			foodL.append(tmp)
		context['data'] = foodL
	else:
		context['message'] = 'error occured'
	return HttpResponse(json.dumps({"data":context}), content_type='application/json')

				


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_rating(request):
	uid = request.data.get('uid')
	rate = request.data.get('rate')
	user = request.user
	if uid != '' and uid != None and rate != '' and rate != None and rate.isdigit():
		if store.objects.filter(uid=uid).exists() and int(rate)>0 and int(rate)<6:
			storeO = store.objects.get(uid=uid)
			if rating_for_store.objects.filter(by_user=user).exists():
				rating_for_storeO = rating_for_store.objects.get(by_user=user)
				rating_for_storeO.rate = int(rate)
				rating_for_store.save()
			else:
				ratingO = rating_for_store.objects.create(for_store=storeO, by_user=user, rate=int(rate))
				ratingO.save()
				context['message'] = 'success'


		elif resturent.objects.filter(uid=uid).exists() and int(rate)>0 and int(rate)<6:
			storeO = resturent.objects.get(uid=uid)
			if rating_for_restaurant.objects.filter(by_user=user).exists():
				rating_for_restaurantO = rating_for_restaurant.objects.get(by_user=user)
				rating_for_storeO.rate = int(rate)
				rating_for_store.save()
			else:
				ratingO = rating_for_restaurant.objects.create(for_store=storeO, by_user=user, rate=int(rate))
				ratingO.save()
				context['message'] = 'success'
		else:
			context['message']="rate must be greater then "		
	else:
		context['message'] = 'no records found'
	return HttpResponse(json.dumps({"data":context}), content_type='application/json')

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def promo_code_price(request):
	promocode=request.data.get("promocode")
	if promo_code.objects.filter(code=promocode).exists():
		return HttpResponse(json.dumps({'price':promo_code.objects.get(code=promo_code).price}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({'price':"promo code not exists"}), content_type='application/json')
			


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def search_food(request):
	name=request.data.get("name")
	context=[]
	foodO=food.objects.filter(name__startswith=name)
	for x in foodO:
		data={}
		data['food']=x.as_dict()
		f=food.objects.get(uid=x.uid)
		image=[]
		for y in food_image.objects.filter(food=f):
			image.append(y.image.url)
		data['image']=image
		specification=[]
		des=[]
		for y in food_specification.objects.filter(food=f):
			specification.append(y.specification)
			des.append(y.des)
		data['specification']=specification
		data['des']=des
		data['food_price_type']=custom_food_price(x)
		context.append(data)
	return HttpResponse(json.dumps({'data':context}), content_type='application/json')


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def search_product(request):
	name=request.data.get("name")
	context=[]
	product=store_product.objects.filter(name__startswith=name)
	for x in product:
		data={}
		data['product']=x.as_dict()
		f=store_product.objects.get(uid=x.uid)
		image=[]
		for y in product_image.objects.filter(product=f):
			image.append(y.image.url)
		data['image']=image
		specification=[]
		des=[]
		for y in product_specification.objects.filter(food=f):
			specification.append(y.specification)
			des.append(y.des)
		data['specification']=specification
		data['des']=des
		context.append(data)
	return HttpResponse(json.dumps({'data':context}), content_type='application/json')



@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def items_exists_in_cart(request,uid):
	if cart.objects.filter(item_uid=uid,user=request.user).exists():
		return HttpResponse(json.dumps({'data':cart.objects.get(item_uid=uid,user=request.user).quantity}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({'data':"Not exists"}), content_type='application/json')



@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def resrturent_banner(request):
	if banner.objects.all().count()>0:
		ban=banner.objects.all()
		bann=[]
		for x in ban:
			bann.append(x.as_dict())
		return HttpResponse(json.dumps({'data':bann}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({'data':"ther is no data"}), content_type='application/json')
			


@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def donate_for_cause(request):
	if donate.objects.all().count()>0:
		d=donate.objects.all()
		data=[]
		for x in d:
			data.append(x.as_dict())
		return HttpResponse(json.dumps({'data':data}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({'data':"there is no data"}), content_type='application/json')




@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def resturent_list_by_zipcode(request,zipcode):
	if resturent.objects.filter(zipcode=zipcode).exists():
		resturentO=resturent.objects.filter(zipcode=zipcode)
		context=[]
		for x in resturentO:
			res=resturent.objects.get(uid=x.uid)
			rating=rating_for_restaurant.objects.filter(for_restaurant=res).count()
			data={}
			data['rating']=rest_rating(x.uid)
			data['resturent']=x.as_dict()
			context.append(data)
		return HttpResponse(json.dumps({"data":context}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"there is no data"}), content_type='application/json')
			
@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def store_list_by_zipcode(request,zipcode):
	if store.objects.filter(zipcode=zipcode).exists():
		storeO=store.objects.filter(zipcode=zipcode)
		context=[]
		for x in storeO:
			res=store.objects.get(uid=x.uid)
			rating=rating_for_store.objects.filter(for_store=res).count()
			data={}
			data['store']=x.as_dict()
			data['rating']=st_rating(x.uid)
			context.append(data)
		return HttpResponse(json.dumps({"data":context}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"there is no data"}), content_type='application/json')


@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_shipping_address(request):
	name=request.data.get("name")
	city=request.data.get("city")
	state=request.data.get("state")
	zipcode=request.data.get("zipcode")
	address=request.data.get("address")
	longitude=request.data.get("longitude")
	latitude=request.data.get("latitude")
	if city!="" and state!="" and zipcode!="" and address!="" and latitude!="" and longitude!="" and city!=None and state!=None and zipcode!=None and address!=None and latitude!=None and longitude!=None:
		location=Point(float(latitude),float(longitude), srid=4326)
		sha=shipping_address.objects.create()
		sha.user=request.user
		sha.city=city
		sha.state=state
		sha.zipcode=zipcode
		sha.address=address
		sha.location=location
		sha.name=name
		sha.save()
		return HttpResponse(json.dumps({"data":"shipping loactionn has been sucessfully added"}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"All Feild must be filled"}), content_type='application/json')
			


@csrf_exempt
@api_view(['GET'])
@permission_classes(IsAuthenticated,)
def view_shipping_address(request):
	if shipping_address.objects.filter(user=request.user).exists():
		s=shipping_address.objects.filter(user=request.user)
		context=[]
		for x in s:
			context.append(x.as_dict())

		return HttpResponse(json.dumps({"data":context}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"there is no data"}), content_type='application/json')
	


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def delete_shipping_address(request,pk):
	if shipping_address.objects.filter(pk=pk).exists():
		sh=shipping_address.objects.get(pk=pk)
		sh.delete()
		return HttpResponse(json.dumps({"data":"address has been successfully"}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"Id does not exists"}), content_type='application/json')
			

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def resturent_rating(request):
	uid=request.POST.get("uid")
	if uid!=None and uid!="" and resturent.objects.filter(uid=uid).exists():
		res=resturent.objects.get(uid=uid)
		rating=rating_for_restaurant.objects.filter(for_restaurant=res).count()
		context={}
		for x in [1,2,3,4,5]:
			percent=0
			rating_star=rating_for_restaurant.objects.filter(for_restaurant=res,rate=x).count()
			percent=((rating/100)*rating_star)
			context['rate'+x]
		return HttpResponse(json.dumps({"data": context}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"uid is not exists"}), content_type='application/json')



 

@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def promo_code_list(request):
	p=promo_code.objects.all()
	promo=[]
	for x in p:
		promo.append(x.as_dict())
	return HttpResponse(json.dumps({"data":promo}), content_type='application/json')

@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def list_special_foog_category(request):
	sfc=special_category.objects.all()
	context=[]
	for x in sfc:
		context.append({"pk":x.pk,"name":x.name,"image":x.image.url})
	return HttpResponse(json.dumps({"data":context}), content_type='application/json')


@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def list_special_foog_category_by_name(request,name):
	if special_category.objects.filter(name=name).exists():
		sppp=special_category.objects.get(name=name)
		sfc=special_foog_category.objects.filter(special=sppp)
		data=[]
		for x in sfc:
			data.append(x.as_dict())
		return HttpResponse(json.dumps({"data":data}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"there is no data"}), content_type='application/json')
			



@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def list_speacial_dish(request):
	if special_dish.objects.all().count()>0:
		sfc=special_dish.objects.all()
		context={}
		name=[]
		for x in sfc:
			if x.name not in name:
				name.append(x.name)
		context['name']=name
		return HttpResponse(json.dumps(context), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"there is no data"}), content_type='application/json')
			



@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def list_speacial_dish_food(request,name):
	if special_dish.objects.filter(name=name).exists():
		context=[]
		f=[]
		
		sfc=special_dish.objects.filter(name=name)
		for x in sfc:
			data={}
			image=[]
			specification=[]
			des=[]
			foodO = food.objects.get(uid=x.food.uid)
			f.append(food.as_dict())
			for y in food_image.objects.filter(food=foodO):
				image.append(x.image.url)
			for y in specification.objects.filter(food=food):
				specification.append(x.specification)
				des.append(x.des)
			data['food']=f
			data['image']=image
			data['specification']=specification
			data['des']=des
			data['custom_food_price']=custom_food_price(foodO)
			context.append(data)
		return HttpResponse(json.dumps({"data":context}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"there is no data"}), content_type='application/json')
			
@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def view_resturent_spotlight(request):
	if inSpotlight_restaurant.objects.all().count()>0:
		rest=inSpotlight_restaurant.objects.all()
		context=[]
		for x in rest:
			data={}
			res = resturent.objects.get(uid=x.resturentK.uid)
			data['resturent']=res.as_dict()
			data['rating']=rest_rating(x.resturentK.uid)
			context.append(data)
		return HttpResponse(json.dumps({"data":context}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"No data exists"}), content_type='application/json')		


@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def view_store_spotlight(request):
	if inSpotlight_store.objects.all().count()>0:
		rest=inSpotlight_store.objects.all()
		context=[]
		for x in rest:
			data={}
			foodO = store.objects.get(uid=x.storeK.uid)
			data['store']=foodO.as_dict()
			data['rating']=st_rating(x.storeK.uid)
			context.append(data)
		return HttpResponse(json.dumps({"data":context}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"No data exists"}), content_type='application/json')		



@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def view_food_spotlight(request):
	if inspotlight_food.objects.all().count()>0:
		sp=inspotlight_food.objects.all()
		context=[]
		for x in sp:
			data={}
			image=[]
			specificationO=[]
			des=[]
			foodO = food.objects.get(uid=x.food.uid)
			
			for y in food_image.objects.filter(food=foodO):
				image.append(x.image.url)
			for y in food_specification.objects.filter(food=foodO):
				specificationO.append(x.specification)
				des.append(x.des)
			data['food']=foodO.as_dict()
			data['image']=image
			data['specification']=specificationO
			data['des']=des
			data['custom_food_price']=custom_food_price(foodO)
			context.append(data)
		return HttpResponse(json.dumps({"data":context}), content_type='application/json')
	else:
		return HttpResponse(json.dumps({"data":"No data exists"}), content_type='application/json')		
		

@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def view_product_spotlight(request):
	if insplotlight_product.objects.all().count()>0:
		sp=insplotlight_product.objects.all()
		context=[]
		for x in sp:
			f=store_product.objects.get(uid=x.product.uid)
			data={}
			data['product']=f.as_dict()
			image=[]
			for y in product_image.objects.filter(product=f):
				image.append(y.image.url)
			data['image']=image
			specification=[]
			des=[]
			for y in product_specification.objects.filter(product=f):
				specification.append(y.specification)
				des.append(y.des)
			data['specification']=specification
			data['des']=des
			context.append(data)
		return HttpResponse(json.dumps({"data":context}), content_type='application/json')	
	else:
		return HttpResponse(json.dumps({"data":"No data exists"}), content_type='application/json')		


@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def spotlight_product_category(request):
	if insplotlight_product_category.objects.all().count()>0:
		sr=insplotlight_product_category.objects.all()
		name=[]
		for x in sr:
			name.append(x.category.as_dict())	
		return HttpResponse(json.dumps({"names":name}), content_type='application/json')				
	else:
		return HttpResponse(json.dumps({"data":"No data exists"}), content_type='application/json')	



@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def all_name_special_resturent(request):
	if special_resturent.objects.all().count()>0:
		sr=special_resturent.objects.all()
		name=[]
		for x in sr:
			if x.name not in name:
				name.append(x.name)	
		return HttpResponse(json.dumps({"names":name}), content_type='application/json')				
	else:
		return HttpResponse(json.dumps({"data":"No data exists"}), content_type='application/json')		


@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def special_resturent_name(request,name):
	if special_resturent.objects.all().count()>0:
		sr=special_resturent.objects.filter(name=name)
		context=[]
		for x in sr:
			data={}
			data['resturent']=x.resturent.as_dict()
			data['rating']=rest_rating(x.resturent.uid)
			context.append(data)
		return HttpResponse(json.dumps({"names":name}), content_type='application/json')				
	else:
		return HttpResponse(json.dumps({"data":"No data exists"}), content_type='application/json')		




@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def cancel_order(request):
	uid = request.data.get('uid')
	if order.objects.filter(uid=uid).exists():
		o=order.objects.get(uid=uid)
		o.status="cancel"
		o.save()
		oo=delivery_assign.objects.get(order=o)
		oo.status="cancel"
		oo.save()
		return Response({'status': "order has been cancel"},status=HTTP_200_OK)
	else:
		return Response({'status': "order not found"},status=HTTP_200_OK)
	

