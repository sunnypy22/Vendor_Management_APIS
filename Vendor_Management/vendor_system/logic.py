import django

# Set up Django
django.setup()

from vendor_system.models import PurchaseOrder
from django.db.models import Q,F, ExpressionWrapper, fields, Sum, Count
from django.db.models.functions import Extract

from datetime import date, timedelta
import datetime
 
today = date.today()
current_time = datetime.datetime.now()


def calculate_on_time_delivery_rate(vendor_id):
    # Calculate on-time delivery rate logic
    try:
        vendor = PurchaseOrder.objects.filter(Q(vendor=vendor_id) & 
                                              Q(status="Completed") & Q(delivery_date__lte=current_time))
        total_completed_vendor = PurchaseOrder.objects.filter(Q(vendor=vendor_id) & Q(status="Completed"))
        on_time_delivery_rate = (len(vendor)/len(total_completed_vendor))*100
        return on_time_delivery_rate
    except ZeroDivisionError:
        return 00.00


def calculate_quality_rating_avg(vendor_id):
    # Calculate quality rating average logic
    try:
        vendor = PurchaseOrder.objects.filter(Q(vendor=vendor_id) &
                                               Q(status="Completed")).values('quality_rating')
        # Use a list comprehension to extract the 'quality_rating' values
        quality_ratings = [item['quality_rating'] for item in vendor]
        sum_of_ratings = sum(quality_ratings)
        avg_of_rating = sum_of_ratings/len(vendor)
        return avg_of_rating

    except ZeroDivisionError:
        return 00.00

def calculate_average_response_time(vendor_id):
    # Calculate average response time logic
    try:
        pos = PurchaseOrder.objects.filter(vendor=vendor_id).values('issue_date','acknowledgment_date')
        result = PurchaseOrder.objects.filter(vendor=vendor_id).annotate(
                time_difference=ExpressionWrapper(
                    F('acknowledgment_date') - F('issue_date'),
                    output_field=fields.DurationField()
                )
            ).aggregate(
                total_time=Sum('time_difference'),
                count=Count('id')
            )
        average_time_days = result['total_time'] / result['count']

        average_percentage = (average_time_days / timedelta(days=1))
        return average_percentage
    except:
        return 00.00

def calculate_fulfillment_rate(vendor_id):
    # Calculate fulfillment rate logic
    try:
        total_completed_vendor = PurchaseOrder.objects.filter(Q(vendor=vendor_id) & Q(status="Completed"))
        total_vendor = PurchaseOrder.objects.filter(vendor=vendor_id)
        fulfillment_rate = (len(total_completed_vendor)/len(total_vendor))*100
        return fulfillment_rate
    except ZeroDivisionError:
        return 00.00

# if __name__ == '__main__':
#     calculate_average_response_time(2)

