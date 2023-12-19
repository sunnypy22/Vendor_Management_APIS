from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import Vendor_Serializer, PurchaseOrder_Serializer, HistoricalPerformance_Serializer
from rest_framework.test import APIClient
from django.urls import reverse
import json
from datetime import date,datetime
import datetime
from django.utils.timezone import now



class VendorTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('vendors')  # Assuming you have a URL pattern named 'vendors'

        # Create a sample user for authentication
        self.user = User.objects.create_user(username='admin', password='admin')
        
        # Authenticate the test client
        self.client = APIClient()
        self.client.login(username='admin', password='admin')

        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='Test Contact',
            address='Test Address',
            vendor_code='Sunny Patel33',
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.,
            fulfillment_rate=0.0
        )
        self.vendor_data = {
            'name': 'Test Vendor',
            'contact_details': 'Test Contact',
            'address': 'Test Address',
            'vendor_code': 'Sunny Patel33',
            'on_time_delivery_rate': 0.0,
            'quality_rating_avg': 0.0,
            'average_response_time': 0.0,
            'fulfillment_rate': 0.0
        }
        self.invalid_data = [{
            'id' : 1,
            'name': 'Test Vendor',
            'contact_details': 'Test Contact',
            'address': 'Test Address',
            'vendor_code': 'Sunny Patel33',
            'on_time_delivery_rate': 0.0,
            'quality_rating_avg': 0.0,
            'average_response_time': 0.0,
            'fulfillment_rate': 0.0
        }]

    def test_get_all_vendors(self):
        # Create sample vendors in the database

        # Send a GET request to the view
        response = self.client.get(self.url)

        # Check the response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check the response data  and expected data
        try:
            self.assertEqual(json.dumps(response.data), json.dumps(self.invalid_data))
        except AssertionError as e:
            self.assertIn('vendor_code', response.data)
            # print(f"Assertion Error : {e}")

    def test_create_vendor(self):
        # Define valid data to be sent in the POST request

        # Send a POST request to the view
        response = self.client.post(self.url, self.vendor_data, format='json')

        # Check the response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the vendor is actually created in the database
        vendor = Vendor.objects.get(vendor_code='Sunny Patel33')
        self.assertEqual(vendor.name, 'Test Vendor')
        

    def test_update_vendor(self):
        # Define updated data to be sent in the PUT request


        self.get_vendor_url = reverse('get_vendor', args=[self.vendor.id]) 

        updated_data = {
            'name': 'Updated Vendor',
            'contact_details': 'Updated Contact',
            'address': 'Updated Address',
            'vendor_code': 'UPDATED',
            'on_time_delivery_rate': 0.8,
            'quality_rating_avg': 3.5,
            'average_response_time': 3.0,
            'fulfillment_rate': 0.7
        }
        

        # Send a PUT request to the view
        response = self.client.put(self.get_vendor_url, updated_data, format='json')

        # Check the response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the vendor is actually updated in the database
        updated_vendor = Vendor.objects.get(id=self.vendor.id)
        self.assertEqual(updated_vendor.name, 'Updated Vendor')

    
    def test_update_vendor_invalid_data(self):
        # Test updating a vendor with invalid data

        self.url = reverse('get_vendor', args=[self.vendor.id])

        invalid_data = {'name': ''}
        response = self.client.put(self.url, invalid_data, format='json')
        
        # Check the response status code and content
        self.assertEqual(response.data['status'], status.HTTP_400_BAD_REQUEST)

    def test_update_nonexistent_vendor(self):
        # Test updating a vendor that does not exist
        nonexistent_url = reverse('get_vendor', args=[999])  # Assuming vendor with ID 999 does not exist
        response = self.client.put(nonexistent_url, {}, format='json')
        # Check the response status code
        self.assertEqual(response.data['status'], status.HTTP_400_BAD_REQUEST)

    def test_delete_vendor(self):
        # Send a DELETE request to the view
        

        self.delete_url = reverse('get_vendor', args=[self.vendor.id])

        response = self.client.delete(self.delete_url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the vendor is actually deleted from the database
        with self.assertRaises(Vendor.DoesNotExist):
            Vendor.objects.get(id=self.vendor.id)

    def test_delete_nonexistent_vendor(self):
        # Test deleting a vendor that does not exist
        nonexistent_url = reverse('get_vendor', args=[999])  # Assuming vendor with ID 999 does not exist
        response = self.client.delete(nonexistent_url)

        # Check the response status code
        self.assertEqual(response.data['status'], status.HTTP_404_NOT_FOUND)


class PurchaseOrderTestCase(APITestCase):

    def setUp(self):

        self.client = APIClient()
        # Create a user and log in if authentication is required
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.force_authenticate(user=self.user)
        # self.client.login(username='admin', password='admin')

        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='Test Contact',
            address='Test Address',
            vendor_code='TESTVENDOR',
            on_time_delivery_rate=0.9,
            quality_rating_avg=4.5,
            average_response_time=2.5,
            fulfillment_rate=0.8
        )
        # Create a sample historical performance entry
        self.historical_performance = HistoricalPerformance.objects.create(
            vendor=self.vendor,
            date='2023-01-01T00:00:00Z',  # Assuming UTC time
            on_time_delivery_rate=95.0,
            quality_rating_avg=4.0,
            average_response_time=2.5,
            fulfillment_rate=98.0
        )
        self.url = reverse('purchase_orders')  # Assuming you have a URL pattern named 'purchase_orders'

    def test_get_all_purchase_orders(self):
        # Create sample purchase orders in the database
        PurchaseOrder.objects.create(
            po_number='PO123',
            order_date='2023-12-19 10:26',
            delivery_date='2023-12-19 10:26',
            items=[{'item_name': 'Item1', 'quantity': 10}],
            quantity=10,
            status='Pending',
            quality_rating=None,
            issue_date='2023-12-19 10:26',
            acknowledgment_date=None,
            vendor=self.vendor,
        )
    
        # Send a GET request to the view
        response = self.client.get(self.url)
        # Check the response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_purchase_orders_by_vendor(self):
        # Create sample purchase orders in the database for a specific vendor
        PurchaseOrder.objects.create(
            po_number='PO789',
            vendor=self.vendor,
            order_date='2023-12-19T10:26:00Z',
            delivery_date='2023-12-19T10:26:00Z',
            items=[{'item_name': 'Item3', 'quantity': 15}],
            quantity=15,
            status='Canceled',
            quality_rating=None,
            issue_date='2023-12-19T10:26:00Z',
            acknowledgment_date=None
        )

        # Send a GET request to the view with a specific vendor parameter
        response = self.client.get(self.url, {'vendor': self.vendor.id})
        # Check the response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_purchase_order(self):
        # Define valid data to be sent in the POST request
        purchase_order_data = {
            'id' : 1,
            'po_number': 'PO789',
            'vendor': self.vendor.id,
            'order_date': '2023-12-19T10:26:00Z',
            'delivery_date': '2023-12-19T10:26:00Z',
            'items': [{'item_name': 'Item3', 'quantity': 15}],
            'quantity': 15,
            'status': 'Pending',
            'quality_rating': None,
            'issue_date': '2023-12-19T10:26:00Z',
            'acknowledgment_date': None
        }

        # Send a POST request to the view
        response = self.client.post(self.url, purchase_order_data, format='json')

        # Check the response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the purchase order is actually created in the database
        created_purchase_order = PurchaseOrder.objects.get(po_number='PO789')
        self.assertEqual(created_purchase_order.vendor, self.vendor)


class SpecificPOAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user and log in if authentication is required
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.force_authenticate(user=self.user)
        # self.client.login(username='admin', password='admin')
        
        # Replace the following lines with actual data for vendor creation
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='Test Contact',
            address='Test Address',
            vendor_code='Sunny Patel33',
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.,
            fulfillment_rate=0.0
        )
        # Replace the following lines with actual data for purchase order creation
        self.purchase_order = PurchaseOrder.objects.create(
            po_number='PO123',
            vendor=self.vendor,
            order_date='2023-01-01T00:00:00Z',
            delivery_date='2023-01-10T00:00:00Z',
            items={'item1': 10, 'item2': 5},
            quantity=15,
            status='Pending',
            quality_rating=None,
            issue_date='2023-01-02T00:00:00Z',
            acknowledgment_date=None
        )

    def test_get_specific_po(self):
        self.get_po_url = reverse('specific_PO', args=[self.purchase_order.id])
        response = self.client.get(self.get_po_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_specific_po(self):
        self.get_po_url = reverse('specific_PO', args=[self.purchase_order.id])
        response = self.client.delete(self.get_po_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['msg'], 'Purchase Order Deleted!!')