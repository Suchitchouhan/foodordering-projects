from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
	path("see_pending_delivery/",see_pending_delivery),
	path("complete_order/", complete_order),
	path("see_complete_delivery/",see_complete_delivery),
	path("login/",login),
	path("see_cancel_delivery/",see_cancel_delivery),
	path("cancel_order/",cancel_order),
	path("items_in_order/<str:uid>/",items_in_order),
	path("update_emp_location/",update_emp_location),
	path("change_delivery_status",change_delivery_status),
	path("profile",profile),
	path("change_duty_status",change_duty_status),
	path("get_duty_status",get_duty_status),
	path("get_location",get_location),


    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
