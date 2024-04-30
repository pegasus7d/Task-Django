from django.urls import path
from .views import test, vendor_list, vendor_detail, purchase_order_detail, create_purchase_order

urlpatterns = [
    path('api/test/', test, name='test-endpoint'),
    path('api/vendors/', vendor_list, name='vendor-list'),
    path('api/vendors/<int:vendor_id>/', vendor_detail, name='vendor-detail'),
    path('api/purchase_orders/', create_purchase_order, name='create-purchase-order'),
    path('api/purchase_orders/<str:po_id>/', purchase_order_detail, name='purchase-order-detail'),
]
