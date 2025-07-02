from django.db import models
from django.contrib.auth.models import User

YES_NO_CHOICES = [
    ('Yes', 'Yes'),
    ('No', 'No'),
]
class YardHdr(models.Model):
    truck_no = models.CharField(max_length=10, primary_key=True)
    whs_no = models.CharField(max_length=5, unique=True)
    truck_type = models.CharField(max_length=20)
    driver_name = models.CharField(max_length=50)
    driver_phn_no = models.CharField(max_length=10)
    po_no = models.CharField(max_length=10)
    truck_date = models.DateField()
    truck_time = models.TimeField()
    seal_no = models.CharField(max_length=10)
    yard_scan = models.CharField(max_length=10)
    truck_status = models.CharField(max_length=10, editable=False, default='Not planned')
    is_the_lock_secure = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    is_the_truck_clean = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    is_the_driver_safe = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    is_the_pallet_stable = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    is_the_temperature_ideal = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    is_the_ac_working = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    does_the_truck_have_a_good_odor = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    is_the_truck_dock_level_ok = models.CharField(max_length=3, choices=YES_NO_CHOICES)  
     

    def __str__(self):
        return f"YardHdr(whs_no={self.whs_no}, truck_no={self.truck_no})"

class TruckLog(models.Model):
    truck_no = models.ForeignKey(YardHdr, on_delete=models.CASCADE)
    truck_date = models.DateField(auto_now_add=True)
    truck_time = models.TimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='Not planned')
    status_changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.truck_no.truck_no} - {self.status} @ {self.truck_date} {self.truck_time}"


from .models import TruckLog

def log_truck_status(truck_instance, status, user=None, comment=''):
    TruckLog.objects.create(
        truck_no=truck_instance,
        status=status,
        status_changed_by=user,
        comment=comment
    )

class StockUpload(models.Model):
    whs_no = models.CharField(max_length=20, primary_key=True)
    product = models.CharField(max_length=20)
    quantity = models.IntegerField()
    batch = models.CharField(max_length=20)
    bin = models.CharField(max_length=20)
    pallet = models.CharField(max_length=20)
    p_mat = models.CharField(max_length=20)
    inspection = models.CharField(max_length=20)
    stock_type = models.CharField(max_length=20)
    wps = models.CharField(max_length=20)
    doc_no = models.CharField(max_length=20)
    pallet_status = models.CharField(max_length=20, default='Not planned')

    def __str__(self):
        return f"StockUpload(whs_no={self.whs_no}, product={self.product})"

class Truck(models.Model):
    truck_no = models.ForeignKey(YardHdr, to_field='truck_no', on_delete=models.CASCADE)
    driver_name = models.CharField(max_length=50)
    driver_phn_no = models.CharField(max_length=10)
    
    def __str__(self):
        return f"Truck(truck_no={self.truck_no}, driver_name={self.driver_name})"
    
class Warehouse(models.Model):
    whs_no = models.IntegerField(primary_key=True)
    whs_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phn_no = models.CharField(max_length=10)  
    email = models.EmailField(max_length=100)
    manager = models.CharField(max_length=50)
    


    def __str__(self):
        return f"Warehouse(whs_no={self.whs_no}, whs_name={self.whs_name})"


