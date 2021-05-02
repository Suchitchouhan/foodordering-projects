from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
	path("login/",login),
	path("orders_for_delivery/<str:statusO>/",orders_for_delivery),
	path("cancel_order/<str:order_uid>/",cancel_order),

	path("add_product",add_product),
	path("add_food",add_food),
	path("get_product_category",get_product_category),
	path("get_food_category",get_food_category),
	path("add_product_category",add_product_category),
	path("add_food_category",add_food_category),
	path("get_all_store_product",get_all_store_product),
	path("get_all_food",get_all_food),
	path("change_opening_status",change_opening_status),
	path("update_store",update_store),
	path("get_store_details",get_store_details),
	path("update_resturent",update_resturent),
	path("get_resturent_details",get_resturent_details),
	path("delete_food/<str:uid>",delete_food),
	path("delete_product/<str:uid>",delete_product),
	path("update_food",update_food),
	path("update_product",update_product),
	path("add_store_image",add_store_image),
	path("add_resturent_image",add_resturent_image),
	path("change_order_status",change_order_status),


    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
