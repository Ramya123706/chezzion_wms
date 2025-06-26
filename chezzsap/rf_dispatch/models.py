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
