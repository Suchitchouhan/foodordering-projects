from cms.models import *
from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from cms.models import resturent
# Create your models here.


class customer(models.Model):
	uid=models.CharField(default="",max_length=20)
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	mobile=models.CharField(default="9999999999",max_length=20)
	billing_city=models.CharField(default='noida',max_length=100)
	billing_state=models.CharField(default='Delhi',max_length=100)
	billing_zipcode=models.CharField(default="666666",max_length=10)
	billing_address = models.CharField(default='xyx', max_length=400)
	image=models.ImageField(upload_to='customer',default='product/linux_2-wallpaper-1366x768.jpg', blank=True, null=True)
	def __str__(self):
		return self.uid+" -> "

class cart_sub_cat(models.Model):
	#cart item uid
	for_cart_item = models.CharField(default=" ",max_length=50)
	cat_name = models.CharField(default='cat name', max_length=30)
	price = models.IntegerField(default=0)
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

	def __str__(self):
		return self.for_cart_item
	def as_dict(self):
		return {'cat_name':self.cat_name,'item_uid':self.for_cart_item,'price':self.price}	

# class cart_exra_item(models.Model):
# 	#cart item uid
# 	for_cart_item = models.CharField(default=" ",max_length=50)
# 	cat_name = models.CharField(default='cat name', max_length=30)
# 	price = models.IntegerField(default=0)
# 	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

# 	def __str__(self):
# 		return self.for_cart_item
# 	def as_dict(self):
# 		return {'item_name':self.cat_name,'item_uid':self.for_cart_item,'price':self.price}	


class cart_exra_item(models.Model):
	#cart item uid
	for_cart_item = models.CharField(default=" ",max_length=50)
	cat_name = models.CharField(default='cat name', max_length=30)
	price = models.IntegerField(default=0)
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

	def __str__(self):
		return self.for_cart_item
	def as_dict(self):
		return {'item_name':self.cat_name,'item_uid':self.for_cart_item,'price':self.price}	


class cart(models.Model):
	item_uid=models.CharField(default=" ",max_length=20)
	item_type=models.CharField(default=" ",max_length=20)
	quantity=models.IntegerField(default=1)
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	def __str__(self):
		return self.item_uid+" -> "+self.item_type



class order(models.Model):
	uid=models.CharField(default=" ",max_length=50)
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	status=models.CharField(default="pending",max_length=50)
	opt=models.CharField(default="",max_length=10)
	date=models.DateTimeField(auto_now_add=True)
	promo_code=models.CharField(default="",max_length=50)
	# cust = models.ForeignKey(customer, on_delete=models.CASCADE)
	shipping_city=models.CharField(default='noida',max_length=100)
	shipping_state=models.CharField(default='Delhi',max_length=100)
	shipping_zipcode=models.CharField(default="666666",max_length=10)
	shipping_address = models.CharField(default='xyx', max_length=400)
	location = models.PointField(null=True)
	order_type = models.CharField(default='', max_length=50)
	amount = models.IntegerField(default=0)
	tip=models.IntegerField(default=0)
	rest = models.CharField(default=" ",max_length=30)
	# order=models.ForeignKey(order,on_delete=models.CASCADE,null=True)
	def __str__(self):
		return self.uid+" -> "
	def as_dict(self):
		return {'uid':self.uid,'status':self.status,"time":str(self.date),"otp":self.opt,"promo_code":self.promo_code,"shipping_address":self.shipping_address,"shipping_state":self.shipping_state,"shipping_zipcode":self.shipping_zipcode,"shipping_address":self.shipping_address,"order_type":self.order_type,"amount":self.amount,"latitude":self.location.x,"longitude":self.location.y}	


class donation(models.Model):
	donate=models.ForeignKey(donate,on_delete=models.PROTECT,null=True)
	amount=models.IntegerField(default=0)
	order=models.ForeignKey(order,on_delete=models.CASCADE,null=True)
	def __str__(self):
		return self.amount



class order_sub_cat(models.Model):
	#cart item uid
	for_order_item = models.CharField(default=" ",max_length=50)
	cat_name = models.CharField(default='cat name', max_length=30)
	price = models.IntegerField(default=0)
	order=models.ForeignKey(order,on_delete=models.CASCADE,null=True)
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

	def __str__(self):
		return self.cat_name
	def as_dict(self):
		return {'cat_name':self.cat_name,'item_uid':self.for_order_item,'price':self.price}	



class order_exra_item(models.Model):
	#cart item uid
	for_order_item = models.CharField(default=" ",max_length=50)
	cat_name = models.CharField(default='cat name', max_length=30)
	price = models.IntegerField(default=0)
	order=models.ForeignKey(order,on_delete=models.CASCADE,null=True)
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

	def __str__(self):
		return self.cat_name
	def as_dict(self):
		return {'item_name':self.cat_name,'item_uid':self.for_order_item,'price':self.price}	


class order_items(models.Model):
	item_uid=models.CharField(default=" ",max_length=20)
	item_type=models.CharField(default=" ",max_length=20)
	quantity=models.IntegerField(default=1)	
	order=models.ForeignKey(order,on_delete=models.CASCADE,null=True)
	status=models.CharField(default="pending",max_length=20)
	cost = models.IntegerField(default=0)
	def __str__(self):
		return self.status
			

class shipping_address(models.Model):
	name=models.CharField(default=" ",max_length=200)
	user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	city=models.CharField(default='noida',max_length=50)
	state=models.CharField(default='Delhi',max_length=50)
	zipcode=models.CharField(default="666666",max_length=10)
	address = models.CharField(default='address', max_length=500)
	location = models.PointField(null=True)
	def __str__(self):
		return self.user.username
	def as_dict(self):
		return {"city":self.city,"state":self.state,'zipcode':self.zipcode,'address':self.address,'latitude':self.location.x,'longitude':self.location.y,"name":self.name,"pk":str(self.pk)}	


class wallet(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	coin=models.IntegerField(default=0)
	def __str__(self):
		return self.wallet