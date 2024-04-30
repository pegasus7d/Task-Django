from django.urls import path
from .views import *

urlpatterns = [
    path('api/test/', test, name='test-endpoint'),
    path('api/vendors/', vendor_list, name='vendor-list'),
    path('api/vendors/<int:vendor_id>/', vendor_detail, name='vendor-detail'),
    path('api/vendors/<int:vendor_id>/performance/', vendor_performance, name='vendor-performance'), 
    path('api/purchase_orders/', create_purchase_order, name='create-purchase-order'),
    path('api/purchase_orders/<str:po_id>/', purchase_order_detail, name='purchase-order-detail'),
    path('api/purchase_orders/<str:po_id>/acknowledge', acknowledge_purchase_order, name='acknowledge-purchase-order'),
]
