from django.shortcuts import render
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
import numpy as np
from datetime import datetime

@api_view(['GET'])
def test(request):
    return Response({'message': 'This is a test endpoint!'})

@api_view(['GET', 'POST'])
def vendor_list(request):
    # Handling GET request
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Handling POST request
    elif request.method == 'POST':
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def vendor_detail(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VendorSerializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = VendorSerializer(vendor, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['GET', 'POST'])
def create_purchase_order(request):
    # Handle GET request: List all purchase orders or filter by vendor
    if request.method == 'GET':
        vendor_id = request.query_params.get('vendor_id')
        if vendor_id is not None:
            vendor = Vendor.objects.filter(id=vendor_id).first()
            purchase_orders = PurchaseOrder.objects.filter(vendor=vendor)
        else:
            purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Handle POST request: Create a new purchase order
    elif request.method == 'POST':
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'PUT', 'DELETE'])
def purchase_order_detail(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response({'error': 'Purchase order not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




def calculate_on_time_delivery_rate(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_count = completed_pos.filter(delivery_date__gte=datetime.now()).count()
    total_completed = completed_pos.count()
    return (on_time_count / total_completed) if total_completed > 0 else 0

def calculate_quality_rating_avg(vendor):
    ratings = PurchaseOrder.objects.filter(vendor=vendor, quality_rating__isnull=False).values_list('quality_rating', flat=True)
    return np.mean(ratings) if ratings else 0

def calculate_average_response_time(vendor):
    response_times = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
    total_time = sum((po.acknowledgment_date - po.issue_date).total_seconds() for po in response_times)
    count = response_times.count()
    return (total_time / count) / 3600 if count > 0 else 0  # Convert seconds to hours

def calculate_fulfillment_rate(vendor):
    total_pos = PurchaseOrder.objects.filter(vendor=vendor).count()
    fulfilled_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
    return (fulfilled_pos / total_pos) if total_pos > 0 else 0
def update_average_response_time(vendor):
    response_times = PurchaseOrder.objects.filter(
        vendor=vendor,
        acknowledgment_date__isnull=False
    )
    total_time = sum((po.acknowledgment_date - po.issue_date).total_seconds() for po in response_times)
    count = response_times.count()
    if count > 0:
        vendor.average_response_time = (total_time / count) / 3600  # Convert seconds to hours
        vendor.save(update_fields=['average_response_time'])

@api_view(['GET'])
def vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

    on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
    quality_rating_avg = calculate_quality_rating_avg(vendor)
    average_response_time = calculate_average_response_time(vendor)
    fulfillment_rate = calculate_fulfillment_rate(vendor)

    performance_metrics = {
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_avg': quality_rating_avg,
        'average_response_time': average_response_time,
        'fulfillment_rate': fulfillment_rate
    }

    historical_data = {
        'vendor': vendor.id,
        'date': timezone.now(),
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_avg': quality_rating_avg,
        'average_response_time': average_response_time,
        'fulfillment_rate': fulfillment_rate
    }

    # Serialize and save historical performance
    historical_serializer = HistoricalPerformanceSerializer(data=historical_data)
    if historical_serializer.is_valid():
        historical_serializer.save()
    else:
        return Response(historical_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(performance_metrics, status=status.HTTP_200_OK)

@api_view(['POST'])
def acknowledge_purchase_order(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response({'error': 'Purchase order not found'}, status=status.HTTP_404_NOT_FOUND)

    
    purchase_order.acknowledgment_date = timezone.now()
    purchase_order.save(update_fields=['acknowledgment_date'])

    # Recalculate the average response time for the vendor
    vendor = purchase_order.vendor
    update_average_response_time(vendor)

    return Response({'message': 'Purchase order acknowledged successfully'}, status=status.HTTP_200_OK)
    