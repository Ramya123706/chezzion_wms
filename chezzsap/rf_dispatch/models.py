from django.db import models
from django.contrib.auth.models import User

YES_NO_CHOICES = [
    ('Yes', 'Yes'),
    ('No', 'No'),
]
class YardHdr(models.Model):
    truck_no = models.CharField(max_length=10, primary_key=True)
    whs_no = models.CharField(max_length=5, unique=True)
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        inventory, created = Inventory.objects.get_or_create(product=self.product)
        inventory.total_quantity += self.quantity
        inventory.save()


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
    image = models.ImageField(upload_to='warehouse_images/', blank=True, null=True)
    


    def __str__(self):
        return f"Warehouse(whs_no={self.whs_no}, whs_name={self.whs_name})"




class Inventory(models.Model):
    product = models.CharField(max_length=50, unique=True)
    total_quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product} - {self.total_quantity} units"





from django.db import models

class Product(models.Model):
    product_id = models.CharField(max_length=50, unique=True)  
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    pallet_no = models.CharField(max_length=50)
    sku = models.CharField(max_length=100)
    description = models.TextField()
    unit_of_measure = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    re_order_level = models.IntegerField()
    images = models.ImageField(upload_to='product_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    action= models.CharField(max_length=20, choices=[
        ('Modify', 'Modify'),
        ('Delete', 'Delete')
    ], default='Modify')

    # Only this is the primary key
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.name
    
    
# ....................
# customer_details
# ....................

from django.utils import timezone

class Pallet(models.Model):
    pallet_no = models.CharField(max_length=100, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    capacity = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_scanned = models.BooleanField(default=False)
    scanned_at = models.DateTimeField(default=timezone.now, blank=True)
    created_by = models.CharField(max_length=100, default=None, null=True, blank=True)
    updated_by = models.CharField(max_length=100, default=None, null=True, blank=True)

    def __str__(self):
        return f"Pallet {self.pallet_no} - Product: {self.product.name if self.product else 'None'}"

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    id=models.IntegerField(primary_key=True)
    vendor_code = models.CharField(max_length=50, unique=True)
    email = models.EmailField()  
    phone_no = models.CharField(max_length=10)
    address = models.TextField(null=True,blank=True )
    location = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='vendor_images/', default='vendor_images/default.jpg', null=True, blank=True)
   
    def __str__(self):
        return self.name
   
class Customers(models.Model):
    name = models.CharField(max_length=255)
    vendor_id = models.CharField(max_length=100, unique=True)
    customer_code = models.CharField(max_length=50)
    email = models.EmailField()  
    phone_no = models.CharField(max_length=10)
    address = models.CharField()
    location = models.CharField(max_length=255, blank=True, null=True)



    def __str__(self):
        return self.name