from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.shortcuts import render,redirect
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from .models import *
from django.core.paginator import Paginator
from foodordering.models import *
import random
from delivery.models import *
# Create your views here.


@login_required()
@permission_required("is_staff")
def add_cms_employee(request):
	context={}
	if request.method=="POST":
		username=request.POST.get("username")
		first_name=request.POST.get("first_name")
		last_name=request.POST.get("last_name")
		email=request.POST.get("email")
		password=request.POST.get("password")
		mobile=request.POST.get("mobile")
		city=request.POST.get("city")
		state=request.POST.get("state")
		zipcode=request.POST.get("zipcode")
		address=request.POST.get("address")
		image=request.FILES['image']
		if username!="" and username!=None and first_name!="" and first_name!=None and last_name!=None and last_name!="" and email!="" and email!=None and password!="" and password!=None and mobile!="" and mobile!=None and city!="" and city!=None and state!=None and state!="" and zipcode!="" and zipcode!=None and address!=None and address!="" and image!="" and image!=None:
			if User.objects.filter(username=username,email=email).exists():
				context['message']="username is already exists"
			else:
				user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
				user.save()
				cms=cms_user.objects.create()
				cms.uid=get_random_string(10)
				cms.user=user
				cms.mobile=mobile
				cms.city=city
				cms.state=state
				cms.zipcode=zipcode
				cms.address=address
				cms.image=image
				cms.save()
				context['message']="user is successfully created "
		else:
			context['message']="all Filled must be filled"		
		return render(request,'cms/add_cms_employee.html',context)
	else:
		return render(request,'cms/add_cms_employee.html',context)		


@login_required()
def add_store_category(request):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			name=request.POST.get("name")
			des=request.POST.get("des")
			image=request.FILES['image']
			if name!=None and name!="" and des!=None and des!="" and image!="" and image!=None:
				if store_category.objects.filter(name=name).exists():
					context['message']="its already exists"
				else:
					store=store_category.objects.create()
					store.name=name
					store.des=des
					store.image=image
					store.save()
					return redirect("/view_store_category/")
			else:
				context['message']="all Filled must be filled"	
			return render(request,'cms/add_store_category.html',context)
		else:
			return render(request,'cms/add_store_category.html',context)
	else:
		context['message']="not authorized"
	return render(request,'cms/add_store_category.html',context)


@login_required()
def update_store_category(request,pk):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			name=request.POST.get("name")
			des=request.POST.get("des")
			image=request.FILES['image']
			if des!=None and des!="" and image!="" and image!=None:
				if store_category.objects.filter(pk=pk).exists():
					store=store_category.objects.get(pk=pk)
					store.name=name
					store.des=des
					store.image=image
					store.save()
					return redirect("/view_store_category")
					context['message']="store_category has been successfully delete"
				else:
					context['message']="category is not exists"
			else:
				context['message']="All filled must be filled"			
		else:
			context['pk']=pk
			context['des']=store_category.objects.get(pk=pk)
	else:
		context['message']="not authorized"
	return render(request,'cms/update_store_category.html',context)

	


@login_required()
def view_store_category(request):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="GET":
			context['des']=store_category.objects.all()
	else:
		context['message']="not authorized"
	return render(request,'cms/view_store_category.html',context)		



@login_required()
def add_store(request):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			first_name=request.POST.get("first_name")
			last_name=request.POST.get("last_name")
			username=request.POST.get("username")
			email=request.POST.get("email")
			password=request.POST.get("password")
			mobile=request.POST.get("mobile")
			store_name=request.POST.get("store_name")
			city=request.POST.get("city")
			state=request.POST.get("state")
			zipcode=request.POST.get("zipcode")
			address=request.POST.get("address")
			locality=request.POST.get("locality")
			image=request.FILES['image']
			image1=request.FILES['image1']
			pk=request.POST.get("pk")
			if locality!=None and locality!="" and store_name!=None and store_name!="" and username!="" and username!=None and first_name!="" and first_name!=None and last_name!=None and last_name!="" and email!="" and email!=None and password!="" and password!=None and mobile!="" and mobile!=None and city!="" and city!=None and state!=None and state!="" and zipcode!="" and zipcode!=None and address!=None and address!="" and image!="" and image1!="" and image!=None and image1!=None:
				if User.objects.filter(username=username,email=email).exists():
					context['message']="user is already exists"
				elif store_category.objects.filter(pk=pk).exists():
					store_cat=store_category.objects.get(pk=pk)
					user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
					user.save()
					storeO=store.objects.create()
					storeO.uid=get_random_string(10)
					storeO.store_name=store_name
					storeO.mobile=mobile
					storeO.city=city
					storeO.state=state
					storeO.zipcode=zipcode
					storeO.address=address
					storeO.category=store_cat
					storeO.user=user
					storeO.image=image
					storeO.image1=image1
					storeO.locality=locality
					storeO.save()
					return redirect("/view_store/")
					# context['message']="store has been successfully created"
			else:
				context['message']="all Field must be filled"		
		else:
			context['category']=store_category.objects.all()
	else:
		context['message']="not authorized"
	return render(request,'cms/add_store.html',context)


@login_required
def view_resturent_spotlight(request):
	context = {}
	if cms_user.objects.filter(user=request.user).exists():
		rt=inSpotlight_restaurant.objects.all()
		return render(request,'cms/view_resturent_spotlight.html',{"resturent":rt})
	else:
		return redirect("/not_authorized/")	
	

@login_required
def remove_from_spotlight_restaurant(request,pk):
	context = {}
	if cms_user.objects.filter(user=request.user).exists():
		spt=inSpotlight_restaurant.objects.get(pk=pk)
		spt.delete()
		return redirect("/view_resturent_spotlight/")
	else:
		return redirect("/not_authorized/")	


@login_required
def remove_from_spotlight_store(request):
	context = {	}
	if request.method == 'POST':
		store_idL = request.POST.getlist('id')
		if len(store_idL) > 0:
			for x in store_idL:
				storeO = store.objects.get(uid=x)
				if storeO.exists():
					inSpotlight_storeO = inSpotlight_store.objects.get(storeK=storeO)
					inSpotlight_storeO.delete()
					# storeO.delete()
				else:
					pass
			context['message'] = 'store removed'
		else:
			context['message'] = 'error occured'
	else:
		dataL = []
		storeO = store.objects.all()
		for x in storeO:
			tmp = {}
			tmp['id'] = x.uid
			tmp['store_name'] = x.store_name
			dataL.append(tmp)
		context['data'] = dataL
	return render(request, 'cms/add_to_spotlight_store.html', context)
			

@login_required
def add_to_spotlight_store(request):
	context = {}
	if request.method == 'POST':
		store_idL = request.POST.getlist('id')
		if len(store_idL) > 0:
			for x in store_idL:
				storeO = store.objects.get(uid=x)
				if storeO.exists():
					inSpotlightO = inSpotlight_store.objects.create()
					inSpotlightO.storeK = storeO
					inSpotlightO.save()
			context['message'] = 'spotlight saved!'
		else:
			context['message'] = 'error occured!'
	else:
		dataL = []
		storeO = store.objects.all()
		for x in storeO:
			tmp = {}
			tmp['id'] = x.uid
			tmp['store_name'] = x.store_name
			dataL.append(tmp)
		context['data'] = dataL
	return render(request, 'cms/add_to_spotlight_store.html', context)


@login_required
def add_to_spotlight_restaurant(request):
	context = {}
	if request.method == 'POST':
		store_idL = request.POST.getlist('id')
		if len(store_idL) > 0:
			for x in store_idL:
				storeO = resturent.objects.get(uid=x)
				if storeO.exists():
					inSpotlightO = inSpotlight_restaurant.objects.create()
					inSpotlightO.storeK = storeO
					inSpotlightO.save()
			context['message'] = 'spotlight saved!'
		else:
			context['message'] = 'error occured!'
	else:
		dataL = []
		storeO = resturent.objects.all()
		for x in storeO:
			tmp = {}
			tmp['id'] = x.uid
			tmp['store_name'] = x.store_name
			dataL.append(tmp)
		context['data'] = dataL
	return render(request, 'cms/add_to_spotlight_store.html', context)


@login_required()
def view_store(request):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			mobile=request.POST.get("mobile")
			if mobile!=None and mobile!="":
				if store.objects.filter(mobile=mobile).exists():
					context['store']=store.objects.filter(mobile=mobile)
				else:
					context['message']="there is not store in our database"
			else:
				context['message']="all filled must be filled"		
		else:
			st=store.objects.all().reverse()
			page = request.GET.get('page', 1)
			paginator = Paginator(st, 1)
			try:
				users = paginator.page(page)
			except PageNotAnInteger:
				users = paginator.page(1)
			except EmptyPage:
				users = paginator.page(paginator.num_pages)    
			context['store']=users
	else:
		context['message']="not authorized"
	return render(request,'cms/view_store.html',context)


@login_required()
def update_store(request,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			mobile=request.POST.get("mobile")
			store_name=request.POST.get("store_name")
			city=request.POST.get("city")
			state=request.POST.get("state")
			zipcode=request.POST.get("zipcode")
			address=request.POST.get("address")
			image=request.FILES['image']
			image1=request.FILES['image1']
			if store_name!=None and store_name!="" and mobile!="" and mobile!=None and city!="" and city!=None and state!=None and state!="" and zipcode!="" and zipcode!=None and address!=None and address!="" and image!="" and image1!="" and image!=None and image1!=None:
				if store.objects.filter(uid=uid).exists():
					st=store.objects.get(uid=uid)
					st.mobile=mobile
					st.store_name=store_name
					st.city=city
					st.state=state
					st.zipcode=zipcode
					st.address=address
					st.image=image
					st.image1=image1				
					st.save()
					return redirect("/view_store/")
					context['message']="store details has been successfully update"
				else:
					context['message']="uid does not exists"
			else:
				context['message']="All field must be filled"		
		else:
			context['uid']=uid
			context['store']=store.objects.get(uid=uid)
	else:
		context['message']="not authorized"
	return render(request,'cms/update_store.html',context)
						
@login_required()
def delete_store(request,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="GET":
			if store.objects.filter(uid=uid).exists():
				st=store.objects.get(uid=uid)
				user=User.objects.get(username=st.user.username)
				user.delete()
				return redirect("/view_store/")
			else:
				context['message']="uid is not exists"	
			
	else:	
		context['message']="not authorized"
	return render(request,'cart/create_seller.html',context)		



@login_required()
def add_store_product_category(request):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			name=request.POST.get("name")
			des=request.POST.get("des")
			image=request.FILES['image']
			if des!=None and des!="" and image!="" and image!=None:
				if store_product_category.objects.filter(name=name).exists():
					context['message']="its already exists"
				else:
					store=store_product_category.objects.create()
					store.name=name
					store.des=des
					store.image=image
					store.save()
					context['message']="store_category has been successfully created"
					return redirect("/view_store_product_category/")
			else:
				context['message']="all filled must be filled"		
		else:
			return render(request,'cms/add_store_product_category.html',context)
	else:
		context['message']="not authorized"
	return render(request,'cms/add_store_product_category.html',context)

@login_required()
def update_store_product_category(request,pk):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			name=request.POST.get("name")
			des=request.POST.get("des")
			image=request.FILES['image']
			if des!=None and des!="" and image!="" and image!=None:
				if store_product_category.objects.filter(pk=pk).exists():
					store=store_product_category.objects.get(pk=pk)
					store.des=des
					store.image=image
					store.name=name
					store.save()
					return redirect("/view_store_product_category/")
				else:
					context['message']="category is not exists"
			else:
				context['message']="all filled must be filled"					
		else:
			context['pk']=pk
			context['des']=store_product_category.objects.get(name=name)
			return render(request,'cms/update_store_product_category.html',context)				
	else:
		context['message']="not authorized"
		context['name']=name
	return render(request,'cms/update_store_product_category.html',context)


@login_required()
def view_store_product_category(request):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="GET":
			context['des']=store_product_category.objects.all()
	else:
		context['message']="not authorized"
	return render(request,'cms/view_store_product_category.html',context)

@login_required()
def view_store_product(request,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="GET":
			if store.objects.filter(uid=uid).exists():
				st=store.objects.get(uid=uid)
				context['st_uid']=uid
				st=store.objects.get(uid=uid)
				page = request.GET.get('page', 1)

				paginator = Paginator(store_product.objects.filter(store=st), 1)
				try:
					users = paginator.page(page)
				except PageNotAnInteger:
					users = paginator.page(1)
				except EmptyPage:
					users = paginator.page(paginator.num_pages)
				context['product']=users
			else:
				context['message']="Store ID is not exists"	
		else:
			name=request.POST.get("name")
			if store.objects.filter(uid=uid).exists() and name!="" and name!=None:
				st=store.objects.get(uid=uid)
				stO=store_product.objects.filter(store=st,name__startswith=name)
				page = request.GET.get('page', 1)

				paginator = Paginator(stO, 1)
				try:
					users = paginator.page(page)
				except PageNotAnInteger:
					users = paginator.page(1)
				except EmptyPage:
					users = paginator.page(paginator.num_pages)
				context['product']=users
				context['st_uid']=uid
			else:
				context['message']="Store ID is not exists"		
		return render(request,'cms/view_store_product.html',context)
	else:
		context['message']="not authorized"
	return render(request,'cms/view_store_product.html',context)	

	

@login_required()
def add_store_product(request,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			name=request.POST.get("name")
			price=request.POST.get("price")
			des=request.POST.get("des")
			category_name=request.POST.get("category_name")
			brandname=request.POST.get("brandname")
			highlight=request.POST.get("highlight")
			overview=request.POST.get("overview")
			gst=request.POST.get("gst")
			if gst!="" and gst!=None and name!="" and name!=None and price!="" and price!=None and des!="" and des!=None and category_name!=None and category_name!="" and category_name!=None and brandname!=None and brandname!="" and highlight!="" and highlight!=None and overview!=None and overview!="":
				if store.objects.filter(uid=uid).exists() and store_product_category.objects.filter(name=category_name).exists():
					st=store.objects.get(uid=uid)
					cat=store_product_category.objects.get(name=category_name)
					product=store_product.objects.create()
					product.uid=get_random_string(10)
					product.name=name
					product.store=st
					product.product_category=cat
					product.des=des
					product.price=int(price)
					product.brandname=brandname
					product.highlight=highlight
					product.overview=overview
					product.gst=int(gst)
					product.save()
					return redirect("/view_store_product/"+uid)
				else:
					context['message']="uid deos not exists or may be category is not exists"
			else:
				context['message']="all field must be filled"		
		else:
			context['category']=store_product_category.objects.all()
			context['uid']=uid
			return render(request,'cms/add_store_product.html',context)
	else:
				
		context['message']="not authorized"
	return render(request,'cms/add_store_product.html',context)				
					
@login_required()
def add_product_image(request,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			# uid=request.POST.get("uid")
			# image=[]
			# for key,value in request.POST.lists():
			# 	if "image" in key:
			# 		for x in value:
			# 			image.append(x)
			image=request.FILES.getlist("image")
			if len(image)!=0:
				if store_product.objects.filter(uid=uid).exists():
					pro=store_product.objects.get(uid=uid)
					for x in image:
						pro_img=product_image.objects.create()
						pro_img.product=pro
						pro_img.image=x
						pro_img.save()
						return redirect("/view_product_image/"+uid+"/")
				else:
					context['message']="Store uid is not exists"
			else:
				context['message']="add same image"			
			# return redirect("/view_product_image/"+uid+"/")
		else:
			context['uid']=uid
		return render(request,"cms/add_product_image.html",context)

@login_required()
def view_product_image(request,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists() and store_product.objects.filter(uid=uid).exists():
		if request.method=="GET":
			pro=store_product.objects.get(uid=uid)
			pro_img=product_image.objects.filter(product=pro)
			context['pro_img']=pro_img
			context['uid']=uid
			context['st_uid']=pro.store.uid
			return render(request,"cms/view_product_image.html",context)
	else:
		context['message']="not authorized"
		return render(request,"cms/view_product_image.html",context)	

@login_required()
def delete_product_image(request,uid,pk):
	context={}
	if cms_user.objects.filter(user=request.user).exists() and store_product.objects.filter(uid=uid).exists():
		pro=store_product.objects.get(uid=uid)
		pro_img=product_image.objects.get(product=pro,pk=pk)
		pro_img.delete()
		return redirect("/view_product_image/"+uid+"/")	




@login_required()
def add_product_specification(request,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists() and store_product.objects.filter(uid=uid).exists():
		if request.method=="POST":
			des=[]
			specification=[]
			for key,value in request.POST.lists():
				if 'des' in key:
					for x in value:
						des.append(x)
				elif 'specification' in key:
					for x in value:
						specification.append(x)      
			pro=store_product.objects.get(uid=uid)
			for x,y in zip(des,specification):
				ps=product_specification.objects.create(product=pro,specification=y,des=x)
				ps.save()
			context['uid']=uid
			return redirect("/view_product_specification/"+uid+"/")
		else:
			context['uid']=uid
	else:
		context['message']="not authorized"
	return render(request,'cms/add_product_specification.html',context)				

@login_required()
def view_product_specification(request,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists() and store_product.objects.filter(uid=uid).exists():
		if request.method=="GET":
			pro=store_product.objects.get(uid=uid)
			ps=product_specification.objects.filter(product=pro)
			context['specification']=ps
			context['uid']=uid
			context['st_uid']=pro.store.uid
			return render(request,"cms/view_product_specification.html",context)

@login_required()
def delete_product_specification(request,uid,pk):
	context={}
	if cms_user.objects.filter(user=request.user).exists() and store_product.objects.filter(uid=uid).exists():
		if request.method=="GET":
			pro=store_product.objects.get(uid=uid)
			ps=product_specification.objects.get(product=pro,pk=pk)
			ps.delete()
			return redirect("/view_product_specification/"+uid+"/")			


@login_required()
def update_store_product(request,uid,st_uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			name=request.POST.get("name")
			price=request.POST.get("price")
			des=request.POST.get("des")
			category_name=request.POST.get("category_name")
			# image1=request.FILES['image1']
			# image2=request.FILES['image2']
			# image3=request.FILES['image3']
			# image4=request.FILES['image4']
			brandname=request.POST.get("brandname")
			highlight=request.POST.get("highlight")
			overview=request.POST.get("overview")
			gst=request.POST.get("gst") 
			if store_product.objects.filter(uid=uid).exists() and store_product_category.objects.filter(name=category_name).exists() and name!="" and price!="" and des!="" and category_name!="" and brandname!="" and highlight!="" and overview!="" and gst!="" and name!=None and price!=None and des!=None and category_name!=None and brandname!=None and highlight!=None and overview!=None and gst!=None:
				st=store.objects.get(uid=st_uid)
				cat=store_product_category.objects.get(name=category_name)
				product=store_product.objects.get(uid=uid,store=st)
				product.name=name
				product.product_category=cat
				product.des=des
				product.price=price
				# product.image1=image1
				# product.image2=image2
				# product.image3=image3
				# product.image4=image4
				product.brandname=brandname
				product.highlight=highlight
				product.overview=overview
				product.gst=gst				
				product.save()
				return redirect("/view_store_product/"+st_uid)
			else:
				context['message']="uid deos not exists or may be category is not exists"
		else:
			st=store.objects.get(uid=st_uid)
			product=store_product.objects.get(uid=uid,store=st)
			context['st_uid']=st_uid
			context['uid']=uid
			context['product']=product
			context['product_cat']=product.product_category.name
			context['category']=store_product_category.objects.all()
		return render(request,'cms/update_store_product.html',context)
	else:	
		context['message']="not authorized"
	return render(request,'cms/update_store_product.html',context)				
		

@login_required()
def delete_product(request,uid,st_uid):
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="GET":
			if store_product.objects.filter(uid=uid).exists():
				product=store_product.objects.get(uid=uid)
				product.delete()
				return redirect("/view_store_product/"+st_uid)

# @login_required()
# def delete_store_product(request,uid):
# 	context={}
# 	print("ASFA")
# 	if request.method=="GET":
# 		if cms_user.objects.filter(user=request.user).exists():
# 			if store_product.objects.filter(uid=uid).exists():
# 				product=store_product.objects.get(uid=uid)
# 				st=product.store.uid
# 				product.delete()
# 				return redirect("/view_store_product/"+st)



@login_required()
def add_resturent_category(request):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			name=request.POST.get("name")
			des=request.POST.get("des")
			image=request.FILES['image']
			if resturent_category.objects.filter(name=name).exists():
				context['message']="its already exists"
			else:
				store=resturent_category.objects.create()
				store.name=name
				store.des=des
				store.image=image
				store.save()
				context['message']="resturent_category has been successfully created"
			return render(request,'cms/add_resturent_category.html',context)
		else:
			return render(request,'cms/add_resturent_category.html',context)
	else:
		context['message']="not authorized"
	return render(request,'cart/create_seller.html',context)


@login_required()
def update_resturent_category(request,pk):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			name=request.POST.get("name")
			des=request.POST.get("des")
			image=request.FILES['image']
			if resturent_category.objects.filter(pk=pk).exists() and name!="" and des!="" and image!="" and name!=None and name!=None and image!=None:
				resturent=resturent_category.objects.get(pk=pk)
				resturent.name=name
				resturent.des=des
				resturent.image=image
				resturent.save()
				return redirect("/view_resturent_category/")
			return render(request,'cart/create_seller.html',context)
		else:
			context['pk']=pk
			context['des']=resturent_category.objects.get(pk=pk)
			return render(request,'cms/update_resturent_category.html',context)				
	else:
		context['message']="not authorized"
	return render(request,'cms/update_resturent_category.html',context)


@login_required()
def view_resturent_category(request):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="GET":
			context['cat']=resturent_category.objects.all()
	else:
		context['message']="not authorized"
	return render(request,'cms/view_resturent_category.html',context)		



@login_required()
def add_resturent(request):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			username=request.POST.get("username")
			first_name=request.POST.get("first_name")
			last_name=request.POST.get("last_name")
			email=request.POST.get("email")
			password=request.POST.get("password")
			mobile=request.POST.get("mobile")
			resturent_name=request.POST.get("resturent_name")
			city=request.POST.get("city")
			state=request.POST.get("state")
			zipcode=request.POST.get("zipcode")
			address=request.POST.get("address")
			image=request.FILES['image']
			image1=request.FILES['image1']
			locality=request.POST.get("locality")
			average_price=request.POST.get("average_price")
			resturent_categoryO=request.POST.get("resturent_category")
			if average_price!="" and average_price!=None and locality!=None and locality!="" and resturent_name!=None and resturent_name!="" and username!="" and username!=None and first_name!="" and first_name!=None and last_name!=None and last_name!="" and email!="" and email!=None and password!="" and password!=None and mobile!="" and mobile!=None and city!="" and city!=None and state!=None and state!="" and zipcode!="" and zipcode!=None and address!=None and address!="" and image!="" and image1!="" and image!=None and image1!=None and resturent_category.objects.filter(name=resturent_categoryO).exists():
				if User.objects.filter(username=username).exists():
					context['message']="user is already exists"
				elif resturent.objects.filter(resturent_name=resturent_name).exists():
					context['message']="resturent is already exists"
				else:
					user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
					user.save()
					storeO=resturent.objects.create()
					storeO.uid=get_random_string(10)
					storeO.user=user
					storeO.resturent_name=resturent_name
					storeO.mobile=mobile
					storeO.city=city
					storeO.state=state
					storeO.zipcode=zipcode
					storeO.address=address
					storeO.category=resturent_category.objects.get(name=resturent_categoryO)
					storeO.image=image
					storeO.image1=image1
					storeO.locality=locality
					storeO.average_price=int(average_price)
					storeO.save()
					return redirect("/view_resturent/")
			else:
				context['message']="All filled must be filled"				
		else:
			context['category']=resturent_category.objects.all()
	else:
		context['message']="not authorized"
	return render(request,'cms/add_resturent.html',context)
		

@login_required()
def view_resturent(request):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			mobile=request.POST.get("mobile")
			if resturent.objects.filter(mobile=mobile).exists():
				context['resturent']=store.objects.filter(mobile=mobile)
			else:
				context['message']="there is not store in our database"
		else:
			st=resturent.objects.all().reverse()
			page = request.GET.get('page', 1)
			paginator = Paginator(st, 50)
			try:
				users = paginator.page(page)
			except PageNotAnInteger:
				users = paginator.page(1)
			except EmptyPage:
				users = paginator.page(paginator.num_pages)    
			context['resturent']=users
	else:
		context['message']="not authorized"
	return render(request,'cms/view_resturent.html',context)



@login_required()
def update_resturent(request,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			mobile=request.POST.get("mobile")
			resturent_name=request.POST.get("resturent_name")
			city=request.POST.get("city")
			state=request.POST.get("state")
			zipcode=request.POST.get("zipcode")
			address=request.POST.get("address")
			locality=request.POST.get("locality")
			average_price=request.POST.get("average_price")
			image=request.FILES['image']
			image1=request.FILES['image1']
			if average_price!="" and average_price!=None and locality!=None and locality!="" and resturent_name!=None and resturent_name!="" and mobile!="" and mobile!=None and city!="" and city!=None and state!=None and state!="" and zipcode!="" and zipcode!=None and address!=None and address!="" and image!="" and image1!="" and image!=None and image1!=None:
				if resturent.objects.filter(uid=uid).exists():
					st=resturent.objects.get(uid=uid)
					st.mobile=mobile
					st.resturent_name=resturent_name
					st.city=city
					st.state=state
					st.zipcode=zipcode
					st.address=address
					st.image=image
					st.image1=image1
					st.average_price=average_price
					st.locality=locality
					st.save()
					return redirect("/view_resturent/")
				else:
					context['message']="uid does not exists"
		else:
			context['uid']=uid
			context['resturent']=resturent.objects.get(uid=uid)
	else:
		context['message']="not authorized"
	return render(request,'cms/update_resturent.html',context)
						
@login_required()
def delete_resturent(request,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="GET":
			st=resturent.objects.get(uid=uid)
			user=User.objects.get(username=st.user.username)
			user.delete()
			return redirect("/view_resturen/")


@login_required()
def add_food_category(request):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			name=request.POST.get("name")
			des=request.POST.get("des")
			image=request.FILES['image']
			if name!=None and des!=None and image!=None and name!="" and des!="" and image!="":
				if food_category.objects.filter(name=name).exists():
					context['message']="its already exists"
				else:
					store=food_category.objects.create()
					store.name=name
					store.des=des
					store.image=image
					store.save()
					return redirect("/view_food_category/")
			else:
				context['message']="all filled must be filled"		
			return render(request,'cms/add_food_category.html',context)
		else:
			return render(request,'cms/add_food_category.html',context)
	else:
		context['message']="not authorized"
	return render(request,'cms/add_food_category.html',context)

@login_required()
def update_food_category(request,pk):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			name=request.POST.get("name")
			des=request.POST.get("des")
			image=request.FILES['image']
			if name!=None and des!=None and image!=None and name!="" and des!="" and image!="":
				if food_category.objects.filter(pk=pk).exists():
					store=food_category.objects.get(pk=pk)
					store.name=name
					store.des=des
					store.image=image
					store.save()
					return redirect("/view_food_category/")
				else:
					context['message']="category Is not exists"	
			else:
				context['message']="all filled must be filled"						
		else:
			context['pk']=pk
			context['des']=food_category.objects.get(pk=pk)
			return render(request,'cms/update_food_category.html',context)				
	else:
		context['message']="not authorized"
	return render(request,'cms/update_food_category.html',context)


@login_required()
def view_food_category(request):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="GET":
			context['cat']=food_category.objects.all()
	else:
		context['message']="not authorized"
	return render(request,'cms/view_food_category.html',context)

@login_required()
def view_food(request,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="GET":
			st=resturent.objects.get(uid=uid)
			context['uid']=uid
			context['food']=food.objects.filter(resturent=st)
		else:
			name=request.POST.get("name")
			st=resturent.objects.get(uid=uid)
			context['food']=food.objects.filter(resturent=st,name__startswith=name)
	else:
		context['message']="not authorized"
	return render(request,'cms/view_food.html',context)	

	

@login_required()
def add_food(request,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			name=request.POST.get("name")
			price=request.POST.get("price")
			des=request.POST.get("des")
			category_name=request.POST.get("category_name")

			brandname=request.POST.get("brandname")
			highlight=request.POST.get("highlight")
			overview=request.POST.get("overview")
			gst=request.POST.get("gst")
			food_type=request.POST.get("food_type")

			sub_cat_name = request.POST.getlist('sub_cat_name')
			sub_cat_price = request.POST.getlist('sub_cat_price')
			item_name = request.POST.getlist('item_name')
			item_price = request.POST.getlist('item_price')
			if name!="" and len(sub_cat_price) == len(sub_cat_name) and len(sub_cat_price) >= 0 and name!=None and price!=None and price!="" and des!="" and des!=None and category_name!="" and category_name!=None and brandname!=None and brandname!="" and overview!="" and overview!=None and gst!="" and gst!=None and food_type!=None and food_type!="" and food_type in ['Veg','Nveg']:
				if resturent.objects.filter(uid=uid).exists() and food_category.objects.filter(name=category_name).exists():
					st=resturent.objects.get(uid=uid)
					cat=food_category.objects.get(name=category_name)
					product=food.objects.create()
					product.uid=get_random_string(10)
					product.name=name
					product.resturent=st
					product.food_category=cat
					product.des=des
					product.price=price
					# product.image1=image1
					# product.image2=image2
					# product.image3=image3
					# product.image4=image4
					product.brandname=brandname
					product.highlight=highlight
					product.overview=overview
					product.gst=gst
					product.food_type=food_type
					product.save()
					# food_sub_catO = food_sub_cat
					# if len(sub_cat_name) == len(sub_cat_price):
					if len(sub_cat_price) > 0:
						for cat_n, cat_y in zip(sub_cat_name, sub_cat_price):
							food_sub_catO = food_sub_cat.objects.create()
							food_sub_catO.for_food = product
							food_sub_catO.cat_name = cat_n
							food_sub_catO.price = cat_y
							food_sub_catO.save()
					
					if len(item_price) > 0:
						for itm_name, itm_prce in zip(item_name, item_price):
							food_extra_itemsO = food_extra_items.objects.create()
							food_extra_itemsO.item_name = itm_name
							food_extra_itemsO.price = itm_prce
							food_extra_itemsO.save()
					return redirect("/view_food/"+uid+"/")
				else:
					context['message']="uid deos not exists or may be category is not exists"
			else:
				context['message']="uid deos not exists or may be category is not exists"					
		else:
			context['category']=food_category.objects.all()
			context['uid']=uid
			return render(request,'cms/add_food.html',context)	
	else:				
		context['message']="not authorized"
	return render(request,'cms/add_food.html',context)		


@login_required()
def add_food_image(request,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			# uid=request.POST.get("uid")
			# image=[]
			# for key,value in request.POST.lists():
			# 	if "image" in key:
			# 		for x in value:
			# 			image.append(x)
			image=request.FILES.getlist("image")
			if len(image)!=0:
				pro=food.objects.get(uid=uid)
				for x in image:
					pro_img=food_image.objects.create()
					pro_img.food=pro
					pro_img.image=x
					pro_img.save()
				return redirect("/view_food_image/"+uid+"/")	
				
			else:
				context['uid']=uid
				context['message']="Image must be something"	
			return render(request,"cms/add_food_image.html",context)	
			# return redirect("/view_product_image/"+uid+"/")
		else:
			context['uid']=uid
			return render(request,"cms/add_food_image.html",context)

@login_required()
def view_food_image(request,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="GET":
			pro=food.objects.get(uid=uid)
			pro_img=food_image.objects.filter(food=pro)
			context['pro_img']=pro_img
			context['uid']=uid
			context['p_uid']=food.objects.get(uid=uid).resturent.uid
			return render(request,"cms/view_food_image.html",context)

@login_required()
def delete_food_image(request,uid,pk):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		pro=food.objects.get(uid=uid)
		pro_img=food_image.objects.get(food=pro,pk=pk)
		pro_img.delete()
		return redirect("/view_food_image/"+uid+"/")	




@login_required()
def add_food_specification(request,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			des=[]
			specification=[]
			for key,value in request.POST.lists():
				if 'des' in key:
					for x in value:
						des.append(x)
				elif 'specification' in key:
					for x in value:
						specification.append(x)      
			if len(des)!=0 and len(specification)!=0:
				pro=food.objects.get(uid=uid)
				for x,y in zip(des,specification):

					ps=food_specification.objects.create(food=pro,specification=y,des=x)
					ps.save()
				context['uid']=uid
				return redirect("/view_food_specification/"+uid+"/")
			else:
				context['message']="specification must be something"	
		else:
			context['uid']=uid
		return render(request,'cms/add_food_specification.html',context)	

@login_required()
def view_food_specification(request,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="GET":
			pro=food.objects.get(uid=uid)
			ps=food_specification.objects.filter(food=pro)
			context['specification']=ps
			context['uid']=uid
			context['p_uid']=pro.resturent.uid
			return render(request,"cms/view_food_specification.html",context)

@login_required()
def delete_food_specification(request,uid,pk):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="GET":
			pro=food.objects.get(uid=uid)
			ps=food_specification.objects.get(food=pro,pk=pk)
			ps.delete()
			return redirect("/view_food_specification/"+uid+"/")			

					

@login_required()
def update_food(request,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			name=request.POST.get("name")
			price=request.POST.get("price")
			des=request.POST.get("des")
			category_name=request.POST.get("category_name")
			# image1=request.FILES['image1']
			# image2=request.FILES['image2']
			# image3=request.FILES['image3']
			# image4=request.FILES['image4']
			brandname=request.POST.get("brandname")
			highlight=request.POST.get("highlight")
			overview=request.POST.get("overview")
			food_type=request.POST.get("food_type")
			gst=request.POST.get("gst")
			# if food.objects.filter(uid=uid).exists():
			if name!="" and name!=None and price!=None and price!="" and des!="" and des!=None and category_name!="" and category_name!=None and brandname!=None and brandname!="" and overview!="" and overview!=None and gst!="" and gst!=None and food_type!=None and food_type!="" and food_type in ['Veg','Nveg'] and food_category.objects.filter(name=category_name).exists():
				cat=food_category.objects.get(name=category_name)
				product=food.objects.get(uid=uid)
				product.name=name
				product.des=des
				product.price=price
				product.food_category=cat
				# product.image1=image1
				# product.image2=image2
				# product.image3=image3
				# product.image4=image4
				product.brandname=brandname
				product.highlight=highlight
				product.overview=overview
				product.food_type=food_type
				product.gst=gst
				product.save()
				return redirect("/view_food/"+product.resturent.uid+"/")
			else:
				context['message']="all field must be filled "
				context['st_uid']=food.objects.get(uid=uid).resturent.uid	
			# else:
			# 	context['message']="uid deos not exists or may be category is not exists"
		else:
			# context['rt_uid']=rt_uid
			context['uid']=uid
			context['category']=food_category.objects.all()
			context['food']=food.objects.get(uid=uid)
			context['st_uid']=food.objects.get(uid=uid).resturent.uid
	else:	
		context['message']="not authorized"
	return render(request,'cms/update_food.html',context)				
		

@login_required()
def delete_food(request,uid,rt_uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if food.objects.filter(uid=uid).exists():
			product=food.objects.get(uid=uid)
			product.delete()
			return redirect("/view_food/"+rt_uid+"/")
	else:
		return redirect("/logout_view/")		

@login_required
def add_social_cause(request):
	context = {}
	if request.method == 'POST':
		name = request.POST.get('name')
		des = request.POST.get('des')
		if name != '' and name != None and des != '' and des != None:
			donateO = donate.objects.create()
			donateO.name = name
			donateO.des = des
			donateO.save()
			context['message'] = 'social cause saved'
		else:
			context['message'] = 'invalid data supplied'
	return render(request, 'cms/add_social_cause.html', context)


@login_required
def add_inspotlight_product_cat(request):
	context = {}
	res = []
	if request.method == 'POST':
		uid = request.POST.getlist('uid')
		if len(uid) > 0:
			for i in range(0, len(uid)-1):
				if store_product_category.objects.filter(pk=uid[i]).exists():
					store_product_categoryO = store_product_category.objects.get(pk=uid[i])
					insplotlight_product_categoryO = insplotlight_product_category.objects.create()
					insplotlight_product_categoryO.category = store_product_categoryO
					insplotlight_product_categoryO.save()
					context['message'] = 'data saved'
				else:
					context['message'] = 'invalid data supplied'
		else:
			pass
	else:
		store_product_categoryO = store_product_category.objects.all()
		for x in store_product_categoryO:
			tmp['id'] = x.pk
			tmp['name'] = x.name
			res.append(tmp)
		context['data'] = res
	return render(request, 'cms/add_inspotlight_food_cat.html', context)


@login_required
def add_inspotlight_food_cat(request):
	context = {}
	res = []
	if request.method == 'POST':
		uid = request.POST.getlist('uid')
		if len(uid) > 0:
			for i in range(0, len(uid)-1):
				if food.objects.filter(pk=uid[i]).exists():
					foodO = food.objects.get(pk=uid[i])
					insplotlight_food_categoryO = insplotlight_food_category.objects.create()
					insplotlight_food_categoryO.category = foodO
					insplotlight_food_categoryO.save()
					context['message'] = 'data saved'
				else:
					context['message'] = 'invalid data supplied'
		else:
			pass
	else:
		foodO = food.objects.all()
		for x in foodO:
			tmp['id'] = x.pk
			tmp['name'] = x.name
			res.append(tmp)
		context['data'] = res
	return render(request, 'cms/add_inspotlight_food_cat.html', context)


@login_required
def add_insplotlight_food(request):
	context = {}
	res
	if request.method == 'POST':
		uid = request.POST.getlist('uid')
		if len(uid) > 0:
			for i in range(0, len(uid)-1):
				if food.objects.filter(uid=uid[i]).exists():
					foodO = food.objects.get(uid=uid[i])
					insplotlight_productO = insplotlight_product.objects.create()
					insplotlight_productO.product = foodO
					insplotlight_productO.save()
					context['message'] = 'saved'
				else:
					context['message'] = 'invalid data supplied'
		else:
			pass
	else:
		foodO = food.objects.all()
		for x in foodO:
			tmp = {}
			tmp['uid'] = x.uid
			tmp['name'] = x.name
			res.append(tmp)
		context['data'] = res
	return render(request, 'cms/add_insplotlight_product.html', context)


@login_required
def add_insplotlight_product(request):
	context = {}
	res
	if request.method == 'POST':
		uid = request.POST.getlist('uid')
		if len(uid) > 0:
			for i in range(0, len(uid)-1):
				if store_product.objects.filter(uid=uid[i]).exists():
					store_productO = store_product.objects.get(uid=uid[i])
					insplotlight_productO = insplotlight_product.objects.create()
					insplotlight_productO.product = store_productO
					insplotlight_productO.save()
					context['message'] = 'saved'
				else:
					context['message'] = 'invalid data supplied'
		else:
			pass
	else:
		store_productO = store_product.objects.all()
		for x in store_productO:
			tmp = {}
			tmp['uid'] = x.uid
			tmp['name'] = x.name
			res.append(tmp)
		context['data'] = res
	return render(request, 'cms/add_insplotlight_product.html', context)


@login_required
def add_banner(request):
	context = {}
	res = []
	if request.method == 'POST':
		resturent_uid = request.POST.get('uid')
		image = request.FILES.getlist('image')
		if resturent_uid != '' and resturent_uid != None and len(image) > 0:
			bannerO = banner.objects.create()
			bannerO.resturent_uid = resturent_uid
			bannerO.image = image[0]
			bannerO.save()
			context['message'] = 'banner saved'
		else:
			context['message'] = 'invalid data supplied'
	else:
		resturentO = resturent.objects.all()
		for x in resturentO:
			tmp = {}
			tmp['uid'] = x.uid
			tmp['name'] = x.resturent_name
			res.append(tmp)
		context['data'] = res
	return render(request, 'cms/add_banner.html', context)


@login_required()
def logout_view(request):
    logout(request)
    return redirect("/")


def login_view(request):
	context={}
	if request.method=="POST":
		username=request.POST.get("username")
		password=request.POST.get("password")
		user=authenticate(username=username,password=password)
		if user is not None:
			login(request, user)
			if cms_user.objects.filter(user=user).exists():
				return redirect("/index/")

			context['status']="login successfully"
		else:
			context['status']="email and password is not exists" 
		return render(request,"cms/login.html",context)
	else:
		return render(request,"cms/login.html",context)      

@login_required()
def index(request):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="GET":
			context['username']=request.user.username
			context['image']=cms_user.objects.get(user=request.user).image.url
			context['message']='Adfad'
			return render(request,"cms/index.html",context)
	else:
		context['message']="not authorized"
	return render(request,'cms/index.html',context)	




					

# @login_required()
# def upload_image(request):
# 	context={}
# 	if request.method=="POST":
# 		image=
	

@login_required
def manage_customer(request):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			mobile=request.POST.get("mobile")
			if mobile!="" and mobile!=None:
				if customer.objects.filter(mobile=mobile).exists():
					context['customer']=customer.objects.filter(mobile__startswith=mobile)
				else:
					context['message']="mobile number is not exists"
			else:
				context['message']="mobile must not be empty don 't play with your work"		
		else:
			context['customer']=customer.objects.all()
		return render(request,'cms/manage_customer.html',context)



@login_required()
def single_customer_panel(request,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="GET":
			cust=customer.objects.get(uid=uid)
			context['customer']=cust
			return render(request,'cms/single_customer_panel.html',context)


@login_required()
def product_for_order(request,c_uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="GET":
			uid=[]
			name=[]
			brandname=[]
			store_name=[]
			category=[]
			price=[]
			des=[]
			itme_type=[]
			p=store_product.objects.all()
			for x in p:
				uid.append(x.uid)
				name.append(x.name)
				brandname.append(x.brandname)
				store_name.append(x.store.store_name)
				category.append(x.product_category.name)
				price.append(x.price)
				des.append(x.des)
				itme_type.append("product")
			f=food.objects.all()
			for x in f:
				uid.append(x.uid)
				name.append(x.name)
				brandname.append(x.brandname)
				store_name.append(x.resturent.resturent_name)
				category.append(x.food_category.name)
				price.append(x.price)
				des.append(x.des)
				itme_type.append("food")
			z=list(zip(uid,name,brandname,store_name,category,price,des,itme_type))
			random.shuffle(z)	
			context['item']=z
			context['c_uid']=c_uid
			context['product_type']=["product","food"]
			context['store_name']=store.objects.all()
			context['resturent_name']=resturent.objects.all()
			return render(request,'cms/product_for_order.html',context)
		else:
			product_type=request.POST.get("product_type")
			product_name=request.POST.get("product_name")
			# resturent_name=request.POST.get("resturent_name")
			# store_name=request.POST.get("store_name")
			# print(product_name)
			# print(product_type)
			uid=[]
			name=[]
			brandname=[]
			store_name=[]
			category=[]
			price=[]
			des=[]
			itme_type=[]
			if product_type!="" and product_name!="":
				if product_type=="food":
					f=food.objects.filter(name__startswith=product_name)
					for x in f:
						uid.append(x.uid)
						name.append(x.name)
						brandname.append(x.brandname)
						store_name.append(x.resturent.resturent_name)
						category.append(x.food_category.name)
						price.append(x.price)
						des.append(x.des)
						itme_type.append("food")
				elif product_type=="product":
					p=store_product.objects.filter(name__startswith=product_name)
					for x in p:
						uid.append(x.uid)
						name.append(x.name)
						brandname.append(x.brandname)
						store_name.append(x.store.store_name)
						category.append(x.product_category.name)
						price.append(x.price)
						des.append(x.des)
						itme_type.append("product")
				else:
					p=store_product.objects.all()
					for x in p:
						uid.append(x.uid)
						name.append(x.name)
						brandname.append(x.brandname)
						store_name.append(x.store.store_name)
						category.append(x.product_category.name)
						price.append(x.price)
						des.append(x.des)
						itme_type.append("product")
					f=food.objects.all()
					for x in f:
						uid.append(x.uid)
						name.append(x.name)
						brandname.append(x.brandname)
						store_name.append(x.resturent.resturent_name)
						category.append(x.food_category.name)
						price.append(x.price)
						des.append(x.des)
						itme_type.append("food")
			if product_type=="" and product_name!="":
					p=store_product.objects.filter(name__startswith=product_name)
					for x in p:
						uid.append(x.uid)
						name.append(x.name)
						brandname.append(x.brandname)
						store_name.append(x.store.store_name)
						category.append(x.product_category.name)
						price.append(x.price)
						des.append(x.des)
						itme_type.append("product")
					f=food.objects.filter(name__startswith=product_name)
					for x in f:
						uid.append(x.uid)
						name.append(x.name)
						brandname.append(x.brandname)
						store_name.append(x.resturent.resturent_name)
						category.append(x.food_category.name)
						price.append(x.price)
						des.append(x.des)
						itme_type.append("food")			
			# if store_name!="" and product_type=="" and product_name=="" and resturent_name=="":
			# 	st=store.objects.get(store_name=store_name)
			# 	p=store_product.objects.filter(store=st)
			# 	for x in p:
			# 		uid.append(x.uid)
			# 		name.append(x.name)
			# 		brandname.append(x.brandname)
			# 		store_name.append(x.store.store_name)
			# 		category.append(x.product_category.name)
			# 		price.append(x.price)
			# 		des.append(x.des)
			# 		itme_type.append("product")
			# # if store_name!="" and product_type=="" and product_name!="" and resturent_name=="":
			# # 	st=store.objects.get(store_name=store_name)
			# # 	p=store_product.objects.filter(store=st,name__startswith=product_name)
			# # 	for x in p:
			# # 		uid.append(x.uid)
			# # 		name.append(x.name)
			# # 		brandname.append(x.brandname)
			# # 		store_name.append(x.store.store_name)
			# # 		category.append(x.product_category.name)
			# # 		price.append(x.price)
			# # 		des.append(x.des)
			# # 		itme_type.append("product")		
			# if resturent_name!="" and product_type=="" and product_name=="" and store_name=="":
			# 	st=resturent.objects.get(resturent_name=resturent_name)
			# 	f=food.objects.filter(resturent=st)
			# 	for x in f:
			# 		uid.append(x.uid)
			# 		name.append(x.name)
			# 		brandname.append(x.brandname)
			# 		store_name.append(x.resturent.resturent_name)
			# 		category.append(x.food_category.name)
			# 		price.append(x.price)
			# 		des.append(x.des)
			# 		itme_type.append("food")
			# # if resturent_name!="" and product_type=="" and product_name!="" and store_name=="":
			# # 	st=resturent.objects.get(resturent_name=resturent_name)
			# # 	f=food.objects.filter(resturent=st,name__startswith=product_name)
			# # 	for x in f:
			# # 		uid.append(x.uid)
			# # 		name.append(x.name)
			# # 		brandname.append(x.brandname)
			# # 		store_name.append(x.resturent.resturent_name)
			# # 		category.append(x.food_category.name)
			# # 		price.append(x.price)
			# # 		des.append(x.des)
			# # 		itme_type.append("food")
			# if product_type=="" and product_name!="" and resturent_name=="" and store_name=="":
			# 	f=food.objects.filter(name__startswith=product_name)
			# 	print(f)
			# 	for x in f:
			# 		uid.append(x.uid)
			# 		name.append(x.name)
			# 		brandname.append(x.brandname)
			# 		store_name.append(x.resturent.resturent_name)
			# 		category.append(x.food_category.name)
			# 		price.append(x.price)
			# 		des.append(x.des)
			# 		itme_type.append("food")
			# 	p=store_product.objects.filter(name__startswith=product_name)
			# 	for x in p:
			# 		uid.append(x.uid)
			# 		name.append(x.name)
			# 		brandname.append(x.brandname)
			# 		store_name.append(x.store.store_name)
			# 		category.append(x.product_category.name)
			# 		price.append(x.price)
			# 		des.append(x.des)
			# 		itme_type.append("product")	

			z=list(zip(uid,name,brandname,store_name,category,price,des,itme_type))
			random.shuffle(z)	
			context['item']=z
			context['c_uid']=c_uid
			context['product_type']=["product","food"]
			context['store_name']=store.objects.all()
			context['resturent_name']=resturent.objects.all()			
			return render(request,'cms/product_for_order.html',context)			

							


@login_required()
def single_product_for_cms(request,c_uid,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="GET":
			if store_product.objects.filter(uid=uid).exists():
				f=store_product.objects.get(uid=uid)
				f_img=product_image.objects.filter(product=f)
				f_spc=product_specification.objects.filter(product=f)
				context['product']=f
				context['image']=f_img
				context['specification']=f_spc
				context['c_uid']=c_uid
				context['type']='product'
			if food.objects.filter(uid=uid).exists():
				f=food.objects.get(uid=uid)
				f_img=food_image.objects.filter(food=f)
				f_spc=food_specification.objects.filter(food=f)
				context['product']=f
				context['image']=f_img
				context['specification']=f_spc
				context['c_uid']=c_uid
				context['type']='food'
			return render(request,'cms/single_product_for_cms.html',context)


# @login_required()
# def food_for_order(request,c_uid):
# 	context={}
# 	if cms_user.objects.filter(user=request.user).exists():
# 		if request.method=="GET":
# 			f=food.objects.all()
# 			context['food']=f
# 			context['c_uid']=c_uid
# 			return render(request,'cms/product_for_order.html',context)


@login_required
def add_to_cart_for_product(request,c_uid,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			quantity=request.POST.get("quantity")
			cust=customer.objects.get(uid=c_uid)
			if store_product.objects.filter(uid=uid).exists():
				c,__=cart.objects.get_or_create(item_uid=uid)
				c.quantity=quantity
				c.item_type="product"
				c.user=cust.user
				c.save()
			if food.objects.filter(uid=uid).exists():
				c,__=cart.objects.get_or_create(item_uid=uid)
				c.quantity=quantity
				c.item_type="food"
				c.user=cust.user
				c.save()
					
			return redirect("/product_for_order"+"/"+c_uid+"/")			
	else:
		context['message']="not authorized"	
	return render(request,'cms/manage_customer.html',context)



@login_required()	
def see_cart(request,c_uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists() and customer.objects.filter(uid=c_uid).exists():
		cust=customer.objects.get(uid=c_uid)
		c=cart.objects.filter(user=cust.user,item_type="product")
		uid=[]
		name=[]
		brandname=[]
		store_name=[]
		category=[]
		price=[]
		des=[]
		itme_type=[]
		quantity=[]
		for y in c:
			x=store_product.objects.get(uid=y.item_uid)
			uid.append(x.uid)
			name.append(x.name)
			brandname.append(x.brandname)
			store_name.append(x.store.store_name)
			category.append(x.product_category.name)
			price.append(x.price)
			des.append(x.des)
			itme_type.append("product")
			quantity.append(y.quantity)
		p=cart.objects.filter(user=cust.user,item_type="food")
		for y in p:
			x=food.objects.get(uid=y.item_uid)
			uid.append(x.uid)
			name.append(x.name)
			brandname.append(x.brandname)
			store_name.append(x.resturent.resturent_name)
			category.append(x.food_category.name)
			price.append(x.price)
			des.append(x.des)
			itme_type.append("food")
			quantity.append(y.quantity)
		z=list(zip(uid,name,brandname,store_name,category,price,des,itme_type,quantity))
	
		context['item']=z
		context['c_uid']=c_uid
		context['product_type']=["product","food"]
		return render(request,'cms/see_cart.html',context)



@login_required()
def update_cart(request,c_uid,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			quantity=request.POST.get("quantity")
			if quantity!="" and quantity!=None:
				cust=customer.objects.get(uid=c_uid)
				c=cart.objects.get(item_uid=uid,user=cust.user)
				c.quantity=quantity
				c.save()
				return redirect("/see_cart/"+c_uid+"/")
			else:
				return redirect("/see_cart/"+c_uid+"/")	
		else:
			return redirect("/see_cart/"+c_uid+"/")
				

# @login_required()
# def place_order_on_same_address(request,c_uid):
# 	context={}
# 	if cms_user.objects.filter(user=request.user).exists():
# 		if request.method=="GET":
# 			cust=customer.objects.get(uid=c_uid)
# 			orderO=order.objects.create()
# 			orderO.uid=get_random_string(10)
# 			orderO.user=cust.user
# 			orderO.save()
# 			for x in cart.objects.filter(user=cust.user):
# 				order_itemsO=order_items.objects.create()
# 				order_itemsO.item_uid=x.item_uid
# 				order_itemsO.item_type=x.item_type
# 				order_itemsO.order=orderO
# 				order_itemsO.quantity=x.quantity
# 				order_itemsO.save()
# 				cartO=cart.objects.get(item_uid=x.item_uid)
# 				cartO.delete()
# 			return redirect("/see_cart/"+c_uid+"/")	

@login_required()
def place_order_on_different_address(request,c_uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			shipping_city=request.POST.get("shipping_city")
			shipping_state=request.POST.get("shipping_state")
			shipping_zipcode=request.POST.get("shipping_zipcode")
			shipping_address=request.POST.get("shipping_address")
			code=request.POST.get("code")
			delivery_employee_uid=request.POST.get("delivery_employee_uid")
			cust=customer.objects.get(uid=c_uid)
			price=[]
			if delivery_employee_uid!=None and delivery_employee_uid!="" and shipping_city != "" and shipping_state !="" and shipping_zipcode !="" and shipping_address!="" and shipping_city !=None and shipping_zipcode!=None and shipping_address!=None and promo_code.objects.filter(code=code).exists() and cart.objects.filter(user=cust.user).exists():
				for x in cart.objects.filter(user=cust.user):
					if store_product.objects.filter(uid=x.item_uid).exists():
						st=store_product.objects.get(uid=x.item_uid)
						price.append(st.price*x.quantity)
						total_price=sum(price)
						total_price=(((total_price/100)*18)+total_price)
					elif food.objects.filter(uid=x.item_uid).exists():
						st=food.objects.get(uid=x.item_uid)
						price.append(st.price*x.quantity)
						total_price=sum(price)
						total_price=(((total_price/100)*18)+total_price)
					else:
						context['message']="something Worng please call the developer who mode this project"
						break

				if code!="" and code!=None and promo_code.objects.filter(code=code).exists():
					c_code=promo_code.objects.get(code=code)
					orderO=order.objects.create()
					orderO.opt=get_random_string(5)
					orderO.uid=get_random_string(10)
					orderO.user=request.user
					orderO.shipping_city=shipping_city
					orderO.shipping_state=shipping_state
					orderO.shipping_zipcode=shipping_zipcode
					orderO.shipping_address=shipping_address
					orderO.promo_code=code
					orderO.amount=total_price-c_code.price
					orderO.order_type="cod"
					orderO.save()
				else:
					orderO=order.objects.create()
					orderO.opt=get_random_string(5)
					orderO.uid=get_random_string(10)
					orderO.user=request.user
					orderO.shipping_city=shipping_city
					orderO.shipping_state=shipping_state
					orderO.shipping_zipcode=shipping_zipcode
					orderO.shipping_address=shipping_address
					orderO.amount=total_price-c_code.price
					orderO.order_type="cod"
					orderO.save()
				delivery_employeeO=delivery_employee.objects.get(uid=delivery_employee_uid)
				d_asign=delivery_assign.objects.create()
				d_asign.order=orderO
				d_asign.employee=delivery_employeeO
				d_asign.save()						
				price=[]
				for x in cart.objects.filter(user=request.user):
					order_itemsO=order_items.objects.create()
					order_itemsO.item_uid=x.item_uid
					order_itemsO.item_type=x.item_type
					order_itemsO.order=orderO
					order_itemsO.quantity=x.quantity
					order_itemsO.save()
					cartO=cart.objects.get(item_uid=x.item_uid)
					cartO.delete()
				return redirect("/single_customer_panel/"+c_uid+"/")
			else:
				context['context']="ALl filled must be filled"
				return render(request,"cms/place_order_on_different_address.html",context)

		else:
			context['c_uid']=c_uid
			context['customer']=customer.objects.get(uid=c_uid)
			context['delivery_employee']=delivery_employee.objects.all()
			return render(request,"cms/place_order_on_different_address.html",context)

				

@login_required()
def previous_order_complete(request,c_uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists() and customer.objects.filter(uid=c_uid).exists():
		cust=customer.objects.get(uid=c_uid)
		orderO=order.objects.filter(user=cust.user,status="complete")
		uid=[]
		date=[]
		city=[]
		state=[]
		zipcode=[]
		address=[]
		order_type=[]
		amount=[]
		for x in orderO:
			uid.append(x.uid)
			date.append(str(x.date))
			orde=order.objects.get(uid=x.uid)
			city.append(orde.shipping_city)
			state.append(orde.shipping_state)
			zipcode.append(orde.shipping_zipcode)
			address.append(orde.shipping_address)
			order_type.append(orde.order_type)
			amount.append(orde.amount)
		context['previous_order']=list(zip(uid,date,city,state,zipcode,address,order_type,amount))
		context['c_uid']=c_uid
		return render(request,"cms/previous_order_complete.html",context)


@login_required()
def previous_order_pending(request,c_uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists() and customer.objects.filter(uid=c_uid).exists():
		cust=customer.objects.get(uid=c_uid)
		orderO=order.objects.filter(user=cust.user,status="pending")
		uid=[]
		date=[]
		city=[]
		state=[]
		zipcode=[]
		address=[]
		order_type=[]
		amount=[]
		for x in orderO:
			uid.append(x.uid)
			date.append(str(x.date))
			orde=order.objects.get(uid=x.uid)
			city.append(orde.shipping_city)
			state.append(orde.shipping_state)
			zipcode.append(orde.shipping_zipcode)
			address.append(orde.shipping_address)
			order_type.append(orde.order_type)
			amount.append(orde.amount)
		context['previous_order']=list(zip(uid,date,city,state,zipcode,address,order_type,amount))
		context['c_uid']=c_uid
		return render(request,"cms/previous_order_pending.html",context)

@login_required()
def cancel_order_pending(request,c_uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists() and customer.objects.filter(uid=c_uid).exists():
		cust=customer.objects.get(uid=c_uid)
		orderO=order.objects.filter(user=cust.user,status="pending")
		uid=[]
		date=[]
		city=[]
		state=[]
		zipcode=[]
		address=[]
		order_type=[]
		amount=[]
		for x in orderO:
			uid.append(x.uid)
			date.append(str(x.date))
			orde=order.objects.get(uid=x.uid)
			city.append(orde.shipping_city)
			state.append(orde.shipping_state)
			zipcode.append(orde.shipping_zipcode)
			address.append(orde.shipping_address)
			order_type.append(orde.order_type)
			amount.append(orde.amount)
		context['previous_order']=list(zip(uid,date,city,state,zipcode,address,order_type,amount))
		context['c_uid']=c_uid
		return render(request,"cms/previous_order_complete.html",context)



@login_required()
def ordered_items(request,o_uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		oo=order.objects.get(uid=o_uid)
		ooo=order_items.objects.filter(order=oo)
		uid=[]
		name=[]
		brandname=[]
		store_name=[]
		category=[]
		price=[]
		des=[]
		itme_type=[]
		for y in ooo:
			if store_product.objects.filter(uid=y.item_uid).exists():
				x=store_product.objects.get(uid=y.item_uid)
				uid.append(x.uid)
				name.append(x.name)
				brandname.append(x.brandname)
				store_name.append(x.store.store_name)
				category.append(x.product_category.name)
				price.append(x.price)
				des.append(x.des)
				itme_type.append("product")
			elif food.objects.filter(uid=y.item_uid).exists():
				x=food.objects.get(uid=y.item_uid)
				uid.append(x.uid)
				name.append(x.name)
				brandname.append(x.brandname)
				store_name.append(x.resturent.resturent_name)
				category.append(x.food_category.name)
				price.append(x.price)
				des.append(x.des)
				itme_type.append("food")
		z=list(zip(uid,name,brandname,store_name,category,price,des,itme_type))
		context['item']=z
		context['c_uid']=o_uid
		return render(request,"cms/ordered_items.html",context)




@login_required()
def cancel_order(request,o_uid,c_uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		oo=order.objects.get(uid=o_uid)
		oo.status="cancel"
		order_itemsO=order_items.objects.filter(order=oo)
		for x in order_itemsO:
			ooo=order_items.objects.get(pk=x.pk)
			ooo.status='cancel'
		oo.save()
		return redirect("/previous_order_pending/"+c_uid+"/")




@login_required()
def delivery_details(request):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			mobile=request.POST.get('mobile')
			if mobile!="" and mobile!=None:
				demp=delivery_employee.objects.filter(mobile=mobile)
				context['employee']=demp
			else:
				context['message']="mobile must be exists"	
			return render(request,'cms/delivery_details.html',context)
		else:
			demp=delivery_employee.objects.all()
			context['employee']=demp
			return render(request,'cms/delivery_details.html',context)


@login_required()
def delivery_assigned(request,uid,status):
	context={}
	#cancel pending complete
	if cms_user.objects.filter(user=request.user).exists():
		demp=delivery_employee.objects.get(uid=uid)
		delivery_assignO=delivery_assign.objects.filter(employee=demp,status=status)
		context['delivery']=delivery_assignO
		context['status']=status
		return render(request,'cms/delivery_assigned.html',context)

@login_required()
def add_delivery_employee(request):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST" :
			username=request.POST.get("username")
			first_name=request.POST.get("first_name")
			last_name=request.POST.get("last_name")
			email=request.POST.get("email")
			password=request.POST.get("password")
			mobile=request.POST.get("mobile")
			city=request.POST.get("city")
			state=request.POST.get("state")
			zipcode=request.POST.get("zipcode")
			address=request.POST.get("address")
			package=request.POST.get("package")
			if username!="" and username!=None and first_name!="" and first_name!=None and last_name!=None and last_name!="" and email!="" and email!=None and password!="" and password!=None and mobile!="" and mobile!=None and city!="" and city!=None and state!=None and state!="" and zipcode!="" and zipcode!=None and address!=None and address!="" and package!=None and package!="":
				if User.objects.filter(username=username,email=email).exists():
					context['message']="user is already exists"
				else:
					user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
					user.save()
					delivery_emp=delivery_employee.objects.create()
					delivery_emp.uid=get_random_string(10)
					delivery_emp.user=user
					delivery_emp.name=first_name+" "+last_name
					delivery_emp.mobile=mobile
					delivery_emp.city=city
					delivery_emp.state=state
					delivery_emp.zipcode=zipcode
					delivery_emp.address=address
					delivery_emp.package=package
					delivery_emp.save()
					return redirect("/delivery_details/")
			else:
				context['message']="all Field must be filled"
			return render(request,'cms/add_delivery_employee.html',context)	
		else:
			return render(request,'cms/add_delivery_employee.html',context)		


@login_required()
def update_delivery_employee(request,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			first_name=request.POST.get("first_name")
			last_name=request.POST.get("last_name")
			email=request.POST.get("email")
			password=request.POST.get("password")
			mobile=request.POST.get("mobile")
			city=request.POST.get("city")
			state=request.POST.get("state")
			zipcode=request.POST.get("zipcode")
			address=request.POST.get("address")
			package=request.POST.get("package")
			if first_name!="" and first_name!=None and last_name!=None and last_name!="" and email!="" and email!=None and password!="" and password!=None and mobile!="" and mobile!=None and city!="" and city!=None and state!=None and state!="" and zipcode!="" and zipcode!=None and address!=None and address!="" and package!=None and package!="":
				de=delivery_employee.objects.get(uid=uid)
				user=User.objects.get(username=de.user.username)
				user.first_name=first_name
				user.last_name=last_name
				user.email=email
				user.password=password
				user.save()
				de.mobile=mobile
				de.name=first_name+" "+last_name
				de.city=city
				de.state=state
				de.zipcode=zipcode
				de.address=address
				de.package=package
				de.save()
				return redirect("/delivery_details/")
			else:
				context['message']="you must need fill all field"
		else:
			context['uid']=uid
			context['employee']=delivery_employee.objects.get(uid=uid)
		return render(request,'cms/update_delivery_employee.html',context)
	else:
		return redirect("/not_authorized/")	
		


@login_required()
def add_promo_code(request):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":
			code=request.POST.get("code")
			price=request.POST.get("price")
			des=request.POST.get("des")
			if code!="" and code!=None and price!="" and price!=None and des!="" and des!=None and price.isdigit():	
				pc,__=promo_code.objects.get_or_create(code=code)
				pc.price=int(price)
				pc.des=des
				pc.save()
				return redirect("/view_promo_code/")
			else:
				context['message']="hey please Insert all Requied information ,otherwise do your job honestly"	
		else:
			return render(request,"cms/add_promo_code.html",context)
	else:
		return redirect("/not_authorized/")	
	
# @login_required()
# def delivery_employee(request,uid):
# 	context={}
# 	if cms_user.objects.filter(user=request.user).exists():
# 		if delivery_employee.objects.filter(uid=uid).exists():
# 			context['employee']=delivery_employee.objects.get(uid=uid)
# 		else:
# 			context['message']="employee uid is not exists"





@login_required()
def update_promo_code(request,pk):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="POST":	
			code=request.POST.get("code")
			price=request.POST.get("price")
			des=request.POST.get("des")
			if code!="" and code!=None and price!="" and price!=None and des!="" and des!=None and price.isdigit():	
				pc=promo_code.objects.get(pk=pk)
				pc.price=price
				pc.des=des
				pc.save()
				return render(request,"cms/add_promo_code.html",context)
			else:
				context['message']="hey please Insert all Requied information ,otherwise do your job honestly"		
		else:
			context['pk']=pk
			context['code']=promo_code.objects.get(pk=pk)
		return render(request,"cms/add_promo_code.html",context)
	else:
		return redirect("/not_authorized/")		


@login_required()
def view_promo_code(request):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		context['promo_code']=promo_code.objects.all()
		return render(request,"cms/view_promo_code.html",context)
	else:
		return redirect("/not_authorized/")	


				

@login_required()
def delete_promo_code(request,pk):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		p=promo_code.objects.get(pk=pk)
		p.delete()
		return redirect("/view_promo_code/")
	else:
		return redirect("/not_authorized/")	



def not_authorized(request):
	return render(request,'cms/not_authorized.html',{})




@login_required()
def single_product_details(request,uid):
	context={}
	if cms_user.objects.filter(user=request.user).exists():
		if request.method=="GET":
			if store_product.objects.filter(uid=uid).exists():
				f=store_product.objects.get(uid=uid)
				f_img=product_image.objects.filter(product=f)
				f_spc=product_specification.objects.filter(product=f)
				context['product']=f
				context['image']=f_img
				context['specification']=f_spc
				context['type']='product'
			if food.objects.filter(uid=uid).exists():
				f=food.objects.get(uid=uid)
				f_img=food_image.objects.filter(food=f)
				f_spc=food_specification.objects.filter(food=f)
				context['product']=f
				context['image']=f_img
				context['specification']=f_spc
				context['type']='food'
			return render(request,'cms/single_product_for_cms.html',context)
			






