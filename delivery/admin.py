from django.contrib import admin
from .models import *
from django.contrib.gis.admin import OSMGeoAdmin

# Register your models here.
@admin.register(delivery_employee)
class current_location(OSMGeoAdmin):
    list_display = ('uid', 'user', 'name', 'mobile', 'city', 'state', 'zipcode', 'address' ,'location')

admin.site.register(delivery_assign)