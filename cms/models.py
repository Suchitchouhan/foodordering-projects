from django.db import models
from django.contrib.auth.models import User
from django_cryptography.fields import encrypt


# Create your models here.
class cms_user(models.Model):
	uid=models.CharField(default="",max_length=20)
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	mobile=models.CharField(default="9999999999",max_length=20)
	city=models.CharField(default='noida',max_length=50)
	state=models.CharField(default='Delhi',max_length=50)
	zipcode=models.CharField(default="666666",max_length=10)
	address = models.CharField(default='xyx', max_length=400)
	image=models.ImageField(upload_to='store_category',default='noimage.jpg', blank=True, null=True)
	def __str__(self):
		return self.uid



class store_category(models.Model):
	name=models.CharField(default="",max_length=100)
	des=models.CharField(default=" ",max_length=200)
	image=models.ImageField(upload_to='store_category',default='noimage.jpg', blank=True, null=True)
	def __str__(self):
		return self.name
	def as_dict(self):
		return {'name':self.name,'des':self.des,'image':self.image.url,'pk':str(self.pk)}	


class store(models.Model):
	uid=models.CharField(default="",max_length=20)
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	store_name=models.CharField(default="",max_length=100)
	mobile=models.CharField(default="9999999999",max_length=20)
	city=models.CharField(default='noida',max_length=50)
	state=models.CharField(default='Delhi',max_length=50)
	zipcode=models.CharField(default="666666",max_length=10)
	address = models.CharField(default='address', max_length=400)
	locality = models.CharField(default='', max_length=200)
	category=models.ForeignKey(store_category,on_delete=models.CASCADE,null=True)
	image=models.ImageField(upload_to='store',default='noimage.jpg', blank=True, null=True)
	image1=models.ImageField(upload_to='store',default='noimage.jpg', blank=True, null=True)	
	opening=models.CharField(default="close",max_length=50)
	def __str__(self):
		return self.uid
	def as_dict(self):
		return {"locality":self.locality,"pk":self.pk,"uid":self.uid,"store_name":self.store_name,"mobile":self.mobile,"city":self.city,"state":self.state,"zipcode":self.zipcode,'address':self.address,"category":self.category.name,'image':self.image.url,'image1':self.image1.url,"opening":self.opening}	
	

class store_product_category(models.Model):
	name=models.CharField(default="",max_length=100)
	des=models.CharField(default=" ",max_length=200)
	image=models.ImageField(upload_to='store_product_category',default='noimage.jpg', blank=True, null=True)
	def __str__(self):
		return self.name
	def as_dict(self):
		return {'name':self.name,'des':self.des,'image':self.image.url,'pk':str(self.pk)}	


class store_product(models.Model):
	uid=models.CharField(default="",max_length=20)
	name=models.CharField(default=" ",max_length=20)
	brandname=models.CharField(default=" ",max_length=20)
	store=models.ForeignKey(store,on_delete=models.CASCADE,null=True)
	product_category=models.ForeignKey(store_product_category,on_delete=models.CASCADE,null=True)
	price=models.IntegerField(default=0,null=True)
	des=models.CharField(default=" ",max_length=200)
	highlight=models.CharField(default=" ",max_length=500)
	overview=models.CharField(default=" ",max_length=500)
	gst=models.IntegerField(default=0,null=True)	
	def __str__(self):
		return self.name
	def as_dict(self):
		return {"pk":str(self.pk),'uid':self.uid,'name':self.name,"brandname":self.brandname,"store":self.store.store_name,"store_uid":self.store.uid,"category":self.product_category.name,"price":self.price,"des":self.des,"highlight":self.highlight,"overview":self.overview,"gst":self.gst,"opening_status":self.store.opening}		

class product_image(models.Model):
	product=models.ForeignKey(store_product,on_delete=models.CASCADE,null=True)
	image=models.ImageField(upload_to='product',default='noimage.jpg', blank=True, null=True)
	def __str__(self):
		return self.product.name+"->"+self.product.brandname


class product_specification(models.Model):
	product=models.ForeignKey(store_product,on_delete=models.CASCADE,null=True)
	specification=models.CharField(default=" ",max_length=200)
	des=models.CharField(default=" ",max_length=100)
	def __str__(self):
		return self.product.name+" - > "+self.product.uid+" - > "+self.specification+" - > "+self.des		



class resturent_category(models.Model):
	name=models.CharField(default="",max_length=100)
	des=models.CharField(default=" ",max_length=200)
	image=models.ImageField(upload_to='resturent_category',default='noimage.jpg', blank=True, null=True)
	def __str__(self):
		return self.name+" "+str(self.pk)
	def as_dict(self):
		return {'name':self.name,'des':self.des,'image':self.image.url,'pk':str(self.pk)}	


class spotlight(models.Model):
	spotId = models.CharField(default='', max_length=20)

	def __str__(self):
		self.spotId

class resturent(models.Model):
	uid=models.CharField(default="",max_length=20)
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	resturent_name=models.CharField(default="",max_length=100)
	mobile=models.CharField(default="9999999999",max_length=20)
	city=models.CharField(default='noida',max_length=50)
	state=models.CharField(default='Delhi',max_length=50)
	zipcode=models.CharField(default="666666",max_length=10)
	address = models.CharField(default='First Name', max_length=400)
	category=models.ForeignKey(resturent_category,on_delete=models.CASCADE,null=True)
	locality = models.CharField(default='', max_length=220)
	average_price=models.IntegerField(default=1)
	image=models.ImageField(upload_to='resturent',default='noimage.jpg', blank=True, null=True)
	image1=models.ImageField(upload_to='resturent',default='noimage.jpg', blank=True, null=True)
	opening=models.CharField(default="close",max_length=100)
	# closing=models.CharField(default="07:00",max_length=100)
	def __str__(self):
		return self.uid+" "+self.user.username
	def as_dict(self):
		return {"pk":self.pk,"locality":self.locality,"average_price":self.average_price,"uid":self.uid,"resturent_name":self.resturent_name,"mobile":self.mobile,"city":self.city,"state":self.state,"zipcode":self.zipcode,'address':self.address,"category":self.category.name,'image':self.image.url,'image1':self.image1.url,"opening_status":self.opening}		
	
class food_category(models.Model):
	name=models.CharField(default="",max_length=100)
	des=models.CharField(default=" ",max_length=200)
	image=models.ImageField(upload_to='food_category',default='noimage.jpg', blank=True, null=True)		
	def __str__(self):
		return self.name
	def as_dict(self):
		return {'name':self.name,'des':self.des,'image':self.image.url,'pk':str(self.pk)}	
	

class food(models.Model):
	uid=models.CharField(default="",max_length=20)	
	name=models.CharField(default=" ",max_length=20)
	brandname=models.CharField(default=" ",max_length=20)
	resturent=models.ForeignKey(resturent,on_delete=models.CASCADE,null=True)
	food_category=models.ForeignKey(food_category,on_delete=models.CASCADE,null=True)
	price=models.IntegerField(default=0,null=True)
	des=models.CharField(default=" ",max_length=200)
	highlight=models.CharField(default=" ",max_length=500)
	overview=models.CharField(default=" ",max_length=500)
	gst=models.IntegerField(default=0,null=True)
	food_type = models.CharField(default='Veg', max_length=10)	

	def __str__(self):
		return self.name+" "+self.uid
	def as_dict(self):
		return {"pk":str(self.pk),"food_type":self.food_type,'uid':self.uid,'name':self.name,"brandname":self.brandname,"resturent":self.resturent.resturent_name,"resturent_uid":self.resturent.uid,"category":self.food_category.name,"base_price":self.price,"des":self.des,"highlight":self.highlight,"overview":self.overview,"gst":self.gst,"opening_status":self.resturent.opening}		
		

class food_sub_cat(models.Model):
	for_food = models.ForeignKey(food, on_delete=models.CASCADE, null=True)
	cat_name = models.CharField(default='cat name', max_length=30)
	price = models.IntegerField(default=0)

	def __str__(self):
		return self.cat_name
	def as_dict(self):
		return {"cat_name":self.cat_name,"price":self.price,"pk":self.pk}


class food_extra_items(models.Model):
	for_food = models.ForeignKey(food, on_delete=models.CASCADE ,null=True)
	item_name = models.CharField(default='', max_length=30)
	price = models.IntegerField(default=0)

	def __str__(self):
		return self.item_name


class food_image(models.Model):
	food=models.ForeignKey(food,on_delete=models.CASCADE,null=True)
	image=models.ImageField(upload_to='food',default='noimage.jpg', blank=True, null=True)
	def __str__(self):
		return self.food.name+"->"+self.food.brandname


class food_specification(models.Model):
	food=models.ForeignKey(food,on_delete=models.CASCADE,null=True)
	specification=models.CharField(default=" ",max_length=200)
	des=models.CharField(default=" ",max_length=100)
	def __str__(self):
		return self.specification+" "+self.des
	# def __str__(self):
	# 	return self.food.name+" - > "+self.food.uid+" - > "+self.specification+" - > "+self.des			


class promo_code(models.Model):
	code=models.CharField(default="",max_length=50)
	price=models.IntegerField(default=0,null=True)
	des=models.CharField(default=" ",max_length=50)
	def __str__(self):
		return self.code
	def as_dict(self):
		return {'pk':self.pk,'code':self.code,'price':self.price,'des':self.des}	
		

class inSpotlight_store(models.Model):
	storeK = models.ForeignKey(store, blank=True, null=True, on_delete=models.CASCADE)
	
	def __str__(self):
		return str(self.pk)

class inSpotlight_restaurant(models.Model):
	resturentK = models.ForeignKey(resturent, blank=True, null=True, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.pk)

# class delivery_employee(models.Model):
	

class rating_for_store(models.Model):
	for_store = models.ForeignKey(store, on_delete=models.CASCADE)
	by_user = models.ForeignKey(User, on_delete=models.CASCADE)
	rate = models.IntegerField(default=0)

	def __str__(self):
		return (self.rate)


class rating_for_restaurant(models.Model):
	for_restaurant = models.ForeignKey(resturent, on_delete=models.CASCADE)
	by_user = models.ForeignKey(User, on_delete=models.CASCADE)
	rate = models.IntegerField(default=1)

	def __str__(self):
		return str(self.rate)



class donate(models.Model):
	name=models.CharField(default=" ",max_length=800)
	des=models.CharField(default=" ",max_length=200)
	def __str__(self):
		return self.name
	def as_dict(self):
		return {'name':self.name, 'des':self.des}	


class banner(models.Model):
	resturent_uid=models.CharField(default=" ",max_length=20)
	image=models.ImageField(upload_to='food',default='noimage.jpg', blank=True, null=True)
	def __str__(self):
		return self.resturent_uid

	def as_dict(self):
		return {'pk':self.pk,'resturent':self.resturent_uid,'image':self.image.url}		


class special_category(models.Model):
	image=models.ImageField(upload_to='food',default='noimage.jpg', blank=True, null=True)
	name=models.CharField(default=" ",max_length=200)
	def __str__(self):
		return self.name



class special_foog_category(models.Model):
	special=models.ForeignKey(special_category,on_delete=models.CASCADE,null=True)
	category=models.ForeignKey(food_category, on_delete=models.CASCADE, null=True)
	def __str__(self):
		return self.special.name
	def as_dict(self):
		return {"pk":self.category.pk,'name':self.special.name,'category_name':self.category.name,'category_des':self.category.des,'category_image':self.category.image.url}	




class inspotlight_food(models.Model):
	food=models.ForeignKey(food, on_delete=models.CASCADE,null=True)


class insplotlight_product(models.Model):
	product=models.ForeignKey(store_product, on_delete=models.CASCADE,null=True)


class insplotlight_product_category(models.Model):
	category=models.ForeignKey(store_product_category, on_delete=models.CASCADE,null=True)


class insplotlight_food_category(models.Model):
	category=models.ForeignKey(food_category, on_delete=models.CASCADE,null=True)




class special_resturent(models.Model):
	name=models.CharField(default=" ",max_length=160)
	resturent=models.ForeignKey(resturent,on_delete=models.CASCADE,null=True)
	def __str__(self):
		return str(self.pk)+" "+self.resturent.uid


class special_dish(models.Model):
	name=models.CharField(default=" ",max_length=200)
	food=models.ForeignKey(food, on_delete=models.CASCADE,null=True)
	def __str__(self):
		return self.name



class store_log(models.Model):
	username=encrypt(models.CharField(default=" ",max_length=100))
	password=encrypt(models.CharField(default=" ",max_length=100))
	store=models.ForeignKey(store,on_delete=models.CASCADE,null=True)
	def __str__(self):
		return self.username+" - >"+self.password


class resturent_log(models.Model):
	username=encrypt(models.CharField(default=" ",max_length=100))
	password=encrypt(models.CharField(default=" ",max_length=100))
	resturent=models.ForeignKey(resturent,on_delete=models.CASCADE,null=True)
	def __str__(self):
		return self.username+" - >"+self.password
