from django.contrib.auth.models import User
from django.contrib.gis.db import models
from foodordering.models import *
# Create your models here.
class delivery_employee(models.Model):
	uid=models.CharField(default="",max_length=20)
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	name=models.CharField(default="",max_length=100)
	mobile=models.CharField(default="9999999999",max_length=20)
	city=models.CharField(default='noida',max_length=50)
	state=models.CharField(default='Delhi',max_length=50)
	zipcode=models.CharField(default="666666",max_length=10)
	address = models.CharField(default='First Name', max_length=400)
	location = models.PointField(null=True)
	package=models.IntegerField(default=10)
	on_duty=models.BooleanField(default=False)
	def __str__(self):
		return self.uid+"-->"+self.user.username
	def as_dict(self):
		return {"name":self.name,"mobile":self.mobile,"city":self.city,"state":self.state,"zipcode":self.zipcode,"address":self.address,"latitude":self.location.x,"longitude":self.location.y,"package":self.package,"on_duty":self.on_duty}	


# class current_loaction(models.Model):
# 	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
# 	location = models.PointField(null=True)
# 	def __str__(self):
# 		return self.location


class delivery_assign(models.Model):
	order=models.ForeignKey(order,on_delete=models.CASCADE,null=True)
	employee=models.ForeignKey(delivery_employee,on_delete=models.CASCADE,null=True)
	status=models.CharField(default="pending",max_length=100)
	des=models.CharField(default="pending",max_length=400)
	date=models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.order.uid+"-->"+self.employee.uid+"-->"+self.employee.user.username


class rating_for_delivery(models.Model):
	for_emp = models.ForeignKey(delivery_employee, on_delete=models.CASCADE)
	#by_user = models.ForeignKey(User, on_delete=models.CASCADE)
	rate = models.IntegerField(default=0)

	def __str__(self):
		return str(self.rate)
