from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .serializers import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from .logic import *
from datetime import date
import datetime
 
today = date.today()

current_time = datetime.datetime.now()
time_stamp = current_time.timestamp()

# Vendors

@api_view(['GET','POST'])
@permission_classes([AllowAny])
def vendors(request):
    # Get all vendor details
    if request.method == 'GET':

        vend = Vendor.objects.all()   # model object
        serializer = Vendor_Serializer(vend,many=True)  #  convert into the serializer
        json_data = JSONRenderer().render(serializer.data) # convert into the Json render
        # return HttpResponse(json_data,content_type='application/json')
        return Response(serializer.data)
    # Create New Vendor
    if request.method == 'POST':
        data = request.data
        serializer = Vendor_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            res = {
                'msg' : "Data has been created successfully",
                'status' : status.HTTP_201_CREATED
            }
            return Response(res)
        return Response({
                'msg': serializer.errors,
                'status' : status.HTTP_400_BAD_REQUEST
            })



@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def specific_vendor(request,pid):
    # Get specific vendor's details
    if request.method == 'GET':
        try:
            data = request.data

            on_time_delivery_rate = calculate_on_time_delivery_rate(pid)
            quality_rating_avg = calculate_quality_rating_avg(pid)
            average_response_time = calculate_average_response_time(pid)
            fulfillment_rate = calculate_fulfillment_rate(pid)

            data['on_time_delivery_rate'] = on_time_delivery_rate
            data['quality_rating_avg'] = quality_rating_avg
            data['average_response_time'] = average_response_time
            data['fulfillment_rate'] = fulfillment_rate
            
            """
                Whenever we hit this API then this will call the 
                business logic and update the Vendors table
            """
            vend_model = Vendor.objects.get(id=pid) 
            vend_model.on_time_delivery_rate = data['on_time_delivery_rate']
            vend_model.quality_rating_avg = data['quality_rating_avg']
            vend_model.average_response_time = data['average_response_time']
            vend_model.fulfillment_rate = data['fulfillment_rate']
                
            vend_model.save()
            vend = Vendor.objects.get(id=pid)   # model object
            serializer = Vendor_Serializer(vend)  #  convert into the serializer
            json_data = JSONRenderer().render(serializer.data) # convert into the Json render
            
            return HttpResponse(json_data,content_type='application/json')
        except:
            return Response({
                    'msg' : "Vendor not exist or Vendor Id is not correct!"
                })
    # Update specific vendor's details
    if request.method == 'PUT':
        try:
            vend = Vendor.objects.get(id=pid)
            serializer = Vendor_Serializer(vend,data=request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
                data = request.data

                on_time_delivery_rate = calculate_on_time_delivery_rate(pid)
                quality_rating_avg = calculate_quality_rating_avg(pid)
                average_response_time = calculate_average_response_time(pid)
                fulfillment_rate = calculate_fulfillment_rate(pid)

                data['on_time_delivery_rate'] = on_time_delivery_rate
                data['quality_rating_avg'] = quality_rating_avg
                data['average_response_time'] = average_response_time
                data['fulfillment_rate'] = fulfillment_rate
                
                """
                    Whenever we hit this API then this will call the 
                    business logic and update the Vendors table
                """

                vend_model = Vendor.objects.get(id=pid)
                vend_model.on_time_delivery_rate = data['on_time_delivery_rate']
                vend_model.quality_rating_avg = data['quality_rating_avg']
                vend_model.average_response_time = data['average_response_time']
                vend_model.fulfillment_rate = data['fulfillment_rate']
                    
                vend_model.save()
                return Response({
                        'msg' : "Data Updated!!"
                    })
            return Response({
                        'msg' : serializer.errors,
                        'status': status.HTTP_400_BAD_REQUEST
                    })
        except:
            return Response({
                    'msg' : "Vendor not exist or Vendor Id is not correct!",
                    'status' : status.HTTP_400_BAD_REQUEST
                })
    # Delete specific vendor's details
    if request.method == 'DELETE':
        try:
            vend = Vendor.objects.get(id=pid)
            vend.delete()
            return Response({
                        'msg' : "Data Deleted!!"
                    })
        except:
            return Response({
                    'msg' : "Vendor not exist or Vendor Id is not correct!",
                    "status" : status.HTTP_404_NOT_FOUND
                })
        

# Purchase ORDERS

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def purchase_orders(request):
    # Get all the POs details
    if request.method == 'GET':
        vendor = request.query_params.get('vendor', None)
        if vendor != None:
            po = PurchaseOrder.objects.filter(vendor=vendor) # model object
            serializer = PurchaseOrder_Serializer(po,many=True) #  convert into the serializer
            json_data = JSONRenderer().render(serializer.data) # convert into the Json render
            # return HttpResponse(json_data,content_type='application/json')
            return Response(serializer.data)

        po = PurchaseOrder.objects.all() # model object
        serializer = PurchaseOrder_Serializer(po,many=True) #  convert into the serializer
        json_data = JSONRenderer().render(serializer.data) # convert into the Json render
        # return HttpResponse(json_data,content_type='application/json')
        return Response(serializer.data)
    # Insert New PO Detail
    if request.method == 'POST':
        data = request.data
        data['order_date'] = current_time
        data['issue_date'] = current_time
        serializer = PurchaseOrder_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            res = {
                'msg' : "Data has been created successfully",
                'status' : status.HTTP_201_CREATED
            }
            return Response(res)
        return Response({
                'msg': serializer.errors
            })


@api_view(['GET','DELETE','PUT'])
@permission_classes([IsAuthenticated])
def specific_PO(request,pid):

    # Get Specific PO
    if request.method == 'GET':
        try:
            po = PurchaseOrder.objects.get(id=pid)
            serializer = PurchaseOrder_Serializer(po)
            json_data = JSONRenderer().render(serializer.data) # convert into the Json render    
            # return HttpResponse(json_data,content_type='application/json')
            return Response(serializer.data)
        except:
            return Response({
                    'msg' : "PO ID not exist or PO Id is not correct!"
                })
    # Delete Specific PO
        
    if request.method == 'DELETE':
        try:
            po = PurchaseOrder.objects.get(id=pid)
            po.delete()
            return Response({
                        'msg' : "Purchase Order Deleted!!"
                    })
        except:
            return Response({
                    'msg' : "Purchase ID not exist or Purchase Id is not correct!"
                })

    # Update Specific PO 

    if request.method == 'PUT':
        try:

            status = request.query_params.get('status', None)
            acknowledgment_date = request.query_params.get('acknowledgment_date', None)
            po = PurchaseOrder.objects.get(id=pid)
            data = request.data
            if status != None:
                data['status'] = status
            serializer = PurchaseOrder_Serializer(po,data=data,partial = True)
            if serializer.is_valid():
                serializer.save()
                count = HistoricalPerformance.objects.filter(vendor=po.vendor.id)
                if len(count) != 0: 
                    data = request.data                        
                    on_time_delivery_rate = calculate_on_time_delivery_rate(po.vendor.id)
                    quality_rating_avg = calculate_quality_rating_avg(po.vendor.id)
                    average_response_time = calculate_average_response_time(po.vendor.id)
                    fulfillment_rate = calculate_fulfillment_rate(po.vendor.id)
                    data = request.data
                    data['vendor'] = po.vendor.id
                    data['date'] = current_time
                    data['on_time_delivery_rate'] = on_time_delivery_rate
                    data['quality_rating_avg'] = quality_rating_avg
                    data['average_response_time'] = average_response_time
                    data['fulfillment_rate'] = fulfillment_rate
                    vend = HistoricalPerformance.objects.get(vendor=po.vendor.id)
                    serializer = HistoricalPerformance_Serializer(vend,data=data,partial = True)
                    if serializer.is_valid():
                        serializer.save() 
                        vend_model = Vendor.objects.get(id=po.vendor.id)
                        vend_model.on_time_delivery_rate = data['on_time_delivery_rate']
                        vend_model.quality_rating_avg = data['quality_rating_avg']
                        vend_model.average_response_time = data['average_response_time']
                        vend_model.fulfillment_rate = data['fulfillment_rate']

                        vend_model.save()

                    return Response({
                        'msg' : "Data Updated!!"
                    }) 
                else:
                    on_time_delivery_rate = calculate_on_time_delivery_rate(po.vendor.id)
                    quality_rating_avg = calculate_quality_rating_avg(po.vendor.id)
                    average_response_time = calculate_average_response_time(po.vendor.id)
                    fulfillment_rate = calculate_fulfillment_rate(po.vendor.id)
                    data = request.data
                    data['vendor'] = po.vendor.id
                    data['date'] = current_time
                    data['on_time_delivery_rate'] = on_time_delivery_rate
                    data['quality_rating_avg'] = quality_rating_avg
                    data['average_response_time'] = average_response_time
                    data['fulfillment_rate'] = fulfillment_rate
                    
                    serializer = HistoricalPerformance_Serializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        vend_model = Vendor.objects.get(id=po.vendor.id)
                        vend_model.on_time_delivery_rate = data['on_time_delivery_rate']
                        vend_model.quality_rating_avg = data['quality_rating_avg']
                        vend_model.average_response_time = data['average_response_time']
                        vend_model.fulfillment_rate = data['fulfillment_rate']
                            
                        vend_model.save()
                return Response({
                        'msg' : "Data Updated!!"
                    })
            return Response({
                        'msg' : serializer.errors
                    })
        except:
            return Response({
                    'msg' : "Purchase ID not exist or Purchase Id is not correct!"
                })
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_purchase_acknowledge(request,pid):
    if request.method == "POST":
        if len(PurchaseOrder.objects.filter(id=pid)) != 0:
            acknowledgment_date = request.query_params.get('acknowledgment_date', None)
            po = PurchaseOrder.objects.get(id=pid)
            if acknowledgment_date != None:
                data = request.data
                data['acknowledgment_date'] = acknowledgment_date
                serializer = PurchaseOrder_Serializer(po,data=data,partial = True)
                if serializer.is_valid():
                    serializer.save()
                    count = HistoricalPerformance.objects.filter(vendor=po.vendor.id)
                    if len(count) != 0: 
                        data = request.data                        
                        average_response_time = calculate_average_response_time(po.vendor.id)
                        data['average_response_time'] = average_response_time
                        vend = HistoricalPerformance.objects.get(vendor=po.vendor.id)
                        serializer = HistoricalPerformance_Serializer(vend,data=data,partial = True)
                        if serializer.is_valid():
                            serializer.save() 
                        return Response({
                            'msg' : "Data Updated!!"
                        }) 
                    else:
                        on_time_delivery_rate = calculate_on_time_delivery_rate(po.vendor.id)
                        quality_rating_avg = calculate_quality_rating_avg(po.vendor.id)
                        average_response_time = calculate_average_response_time(po.vendor.id)
                        fulfillment_rate = calculate_fulfillment_rate(po.vendor.id)
                        data = request.data
                        data['vendor'] = po.vendor.id
                        data['date'] = current_time
                        data['on_time_delivery_rate'] = on_time_delivery_rate
                        data['quality_rating_avg'] = quality_rating_avg
                        data['average_response_time'] = average_response_time
                        data['fulfillment_rate'] = fulfillment_rate
                        
                        serializer = HistoricalPerformance_Serializer(data=data)
                        if serializer.is_valid():
                            serializer.save()
                       
                    return Response({
                            'msg' : "Data Updated!!"
                        }) 
                
            return Response({
                            'msg' : "acknowledgment date not provided!"
                        })
        else:
            return Response({
                    'msg' : "Purchase ID not exist or Purchase Id is not correct!"
                })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendors_performance(request,pid):
    # Get specific vendor's details
    if request.method == 'GET':

        count = HistoricalPerformance.objects.filter(vendor=pid)
        if len(count) != 0:
            on_time_delivery_rate = calculate_on_time_delivery_rate(pid)
            quality_rating_avg = calculate_quality_rating_avg(pid)
            average_response_time = calculate_average_response_time(pid)
            fulfillment_rate = calculate_fulfillment_rate(pid)
            data = request.data
            data['date'] = current_time
            data['on_time_delivery_rate'] = on_time_delivery_rate
            data['quality_rating_avg'] = quality_rating_avg
            data['average_response_time'] = average_response_time
            data['fulfillment_rate'] = fulfillment_rate
            vend = HistoricalPerformance.objects.get(vendor=pid)
            serializer = HistoricalPerformance_Serializer(vend,data=data,partial = True) 
            if serializer.is_valid():
                serializer.save()
                vend_model = Vendor.objects.get(id=pid)
                vend_model.on_time_delivery_rate = data['on_time_delivery_rate']
                vend_model.quality_rating_avg = data['quality_rating_avg']
                vend_model.average_response_time = data['average_response_time']
                vend_model.fulfillment_rate = data['fulfillment_rate']
                    
                vend_model.save()

                json_data = JSONRenderer().render(serializer.data) # convert into the Json render
                return HttpResponse(json_data,content_type='application/json')
                            
            return Response({
                    'msg': serializer.errors
                })
            
        else:
            count = PurchaseOrder.objects.filter(vendor=pid)
            if len(count) != 0:
                on_time_delivery_rate = calculate_on_time_delivery_rate(pid)
                quality_rating_avg = calculate_quality_rating_avg(pid)
                average_response_time = calculate_average_response_time(pid)
                fulfillment_rate = calculate_fulfillment_rate(pid)
                data = request.data
                data['vendor'] = pid
                data['date'] = current_time
                data['on_time_delivery_rate'] = on_time_delivery_rate
                data['quality_rating_avg'] = quality_rating_avg
                data['average_response_time'] = average_response_time
                data['fulfillment_rate'] = fulfillment_rate
                serializer = HistoricalPerformance_Serializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    vend_model = Vendor.objects.get(id=pid)
                    vend_model.on_time_delivery_rate = data['on_time_delivery_rate']
                    vend_model.quality_rating_avg = data['quality_rating_avg']
                    vend_model.average_response_time = data['average_response_time']
                    vend_model.fulfillment_rate = data['fulfillment_rate']
                        
                    vend_model.save()
                    json_data = JSONRenderer().render(serializer.data) # convert into the Json render
                
                    return HttpResponse(json_data,content_type='application/json')
                return Response({
                        'msg': serializer.errors
                    })
            return Response({
                    'msg' : "Vendor ID not exist or Vendor has no historical performance records or purchase orders!!!"
                })
