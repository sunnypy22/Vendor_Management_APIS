from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    # Vendor's API
    path('vendors/',views.vendors,name='vendors'),
    path('vendors/<int:pid>',views.specific_vendor,name='get_vendor'),
    # PO's API
    path('purchase_orders/',views.purchase_orders,name='purchase_orders'),
    path('purchase_orders/<int:pid>/',views.specific_PO,name='specific_PO'),
    path('purchase_orders/<int:pid>/acknowledge/',views.update_purchase_acknowledge,
         name='specific_PO_acknowledge'),

    path('vendors/<int:pid>/performance',views.vendors_performance,name='vendors_performance'),
]
