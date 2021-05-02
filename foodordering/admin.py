from django.contrib import admin
from .models import *
from django.contrib.gis.admin import OSMGeoAdmin
# Register your models here.
admin.site.register(customer)
admin.site.register(cart)
admin.site.register(order)
admin.site.register(order_items)
admin.site.register(shipping_address)
admin.site.register(cart_sub_cat)
admin.site.register(cart_exra_item)
admin.site.register(order_sub_cat)
admin.site.register(order_exra_item)
admin.site.register(donation)

# @admin.register(order_address)
class order_address(OSMGeoAdmin):
	list_display = ('shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_address', 'location','order')

