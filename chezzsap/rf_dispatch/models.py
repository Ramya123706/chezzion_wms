from django.db import models

YES_NO_CHOICES = [
    ('Yes', 'Yes'),
    ('No', 'No'),
]
class YardHdr(models.Model):
    whs_no = models.CharField(max_length=10, primary_key=True)
    truck_no = models.CharField(max_length=5, unique=True)
    truck_type = models.CharField(max_length=10)
    driver_name = models.CharField(max_length=50)
    driver_phn_no = models.CharField(max_length=15)
    po_no = models.CharField(max_length=20)
    truck_date = models.DateField()
    truck_time = models.TimeField()
    seal_no = models.CharField(max_length=20)
    yard_scan = models.CharField(max_length=20)
    truck_status = models.CharField(max_length=20, editable=False, default='Not planned')
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
    truck_no= models.ForeignKey(YardHdr, to_field='truck_no', on_delete=models.CASCADE)
    truck_date = models.DateField()
    truck_time = models.TimeField()
    comment = models.TextField()
    status = models.CharField(max_length=20, default='Not planned')
   

    def __str__(self):
        return f"TruckLog(truck_no={self.truck_no}, truck_date={self.truck_date}, truck_time={self.truck_time})"

