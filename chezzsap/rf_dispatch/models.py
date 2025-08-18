from django.db import models
from django.contrib.auth.models import User


YES_NO_CHOICES = [
    ('Yes', 'Yes'),
    ('No', 'No'),
]
class YardHdr(models.Model):
    yard_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    truck_no = models.CharField(primary_key=True, max_length=100)
    whs_no = models.CharField(max_length=5)
    truck_type = models.CharField(max_length=20)
    driver_name = models.CharField(max_length=50)
    driver_phn_no = models.CharField(max_length=10)
    po_no = models.CharField(max_length=10)
    truck_date = models.DateField()
    truck_time = models.TimeField()
    seal_no = models.CharField(max_length=10)
    yard_scan = models.CharField(max_length=20)
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
        return str(self.truck_no)
    
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


# class StockUpload(models.Model):
#     whs_no = models.CharField(max_length=20, primary_key=True)
#     product = models.CharField(max_length=20)
#     quantity = models.IntegerField()
#     batch = models.CharField(max_length=20)
#     bin = models.CharField(max_length=20)
#     pallet = models.CharField(max_length=20)
#     p_mat = models.CharField(max_length=20) 
#     inspection = models.CharField(max_length=20)
#     stock_type = models.CharField(max_length=20)
#     wps = models.CharField(max_length=20)
#     doc_no = models.CharField(max_length=20)
#     pallet_status = models.CharField(max_length=20, default='Not planned')

#     def __str__(self):
#         return f"StockUpload(whs_no={self.whs_no}, product={self.product})"

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         inventory, created = Inventory.objects.get_or_create(product=self.product)
#         inventory.total_quantity += self.quantity
#         inventory.save()


class Truck(models.Model):
    yard = models.ForeignKey(YardHdr, on_delete=models.CASCADE, default=None, null=True, blank=True)
    truck_no = models.CharField(max_length=100, unique=True)
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


class Category(models.Model):
    
    category = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.category 

class Bin(models.Model):
    whs_no = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="bins" 
    )
    bin_id = models.CharField(max_length=50, unique=True) 
    capacity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="bins") 
    shelves = models.CharField(null=True, blank=True, max_length=100) 
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    existing_quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"Bin {self.bin_id} in Warehouse {self.whs_no}"

# class Inventory(models.Model):
#     product = models.CharField(max_length=50, unique=True)
#     total_quantity = models.IntegerField(default=0)

#     def __str__(self):
#         return f"{self.product} - {self.total_quantity} units"


# class Product(models.Model):
#     product_id = models.CharField(max_length=50)
#     name = models.CharField(max_length=255)
#     quantity = models.IntegerField()
#     pallet_no = models.CharField(max_length=50)
#     sku = models.CharField(max_length=100)
#     description = models.TextField()
#     unit_of_measure = models.CharField(max_length=50)
#     category = models.CharField(max_length=100)
#     re_order_level = models.IntegerField()
#     images = models.ImageField(upload_to='product_images/', null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


#     # Only this is the primary key
#     id = models.AutoField(primary_key=True)

#     def __str__(self):
#         return self.name


import uuid

class Product(models.Model):
#     id= models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    pallet_no = models.CharField(max_length=50)
    sku = models.CharField(max_length=100)
    description = models.TextField()
    unit_of_measure = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", null=True, blank=True)
    re_order_level = models.IntegerField()
    images = models.ImageField(upload_to='product_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Sync with inventory
        from .models import Inventory
        inventory, created = Inventory.objects.get_or_create(product=self)
        inventory.total_quantity = self.quantity
        inventory.save()

    def __str__(self):
        return self.name




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
    name = models.CharField(max_length=100)
    vendor_id = models.CharField(max_length=10, primary_key=True, editable=False) 
    vendor_code = models.CharField(max_length=100)
    email = models.EmailField()
    phone_no = models.CharField(max_length=15)
    address = models.TextField()
    

    profile_image = models.ImageField(upload_to='vendor_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.vendor_id:
            last_vendor = Vendor.objects.order_by('-vendor_id').first()
            if last_vendor and last_vendor.vendor_id[1:].isdigit():
                next_id = int(last_vendor.vendor_id[1:]) + 1
            else:
                next_id = 1
            self.vendor_id = f"V{next_id:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Customers(models.Model):
    name = models.CharField(max_length=255)
    customer_id = models.CharField(max_length=10, primary_key=True, editable=False) 
    customer_code = models.CharField(max_length=50)
    email = models.EmailField()
    phone_no = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

from django.db import models
from django.db.models import F
from .models import Product
from django.db.models import Sum


  

class StockUpload(models.Model):
    id = models.AutoField(primary_key=True)
    whs_no = models.CharField(max_length=20)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)   
    quantity = models.IntegerField()
    batch = models.CharField(max_length=20)
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE)
    pallet = models.CharField(max_length=20)
    p_mat = models.CharField(max_length=20)
    inspection = models.CharField(max_length=20)
    stock_type = models.CharField(max_length=20)
    wps = models.CharField(max_length=20)
    doc_no = models.CharField(max_length=20)
    pallet_status = models.CharField(max_length=20, default='Not planned')

    def __str__(self):
        return f"StockUpload(whs_no={self.whs_no}, product={self.product.name})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Update Inventory after save
        total_quantity = StockUpload.objects.filter(product=self.product).aggregate(
            total=Sum('quantity')
        )['total'] or 0

        inventory, _ = Inventory.objects.get_or_create(product=self.product)
        inventory.total_quantity = total_quantity
        inventory.save()

        # Sync Product quanti ty
        self.product.quantity = total_quantity
        self.product.save()

    def delete(self, *args, **kwargs):
        product = self.product  
        super().delete(*args, **kwargs)

        total_quantity = StockUpload.objects.filter(product=product).aggregate(
            total=Sum('quantity')
        )['total'] or 0

        inventory, _ = Inventory.objects.get_or_create(product=product)
        inventory.total_quantity = total_quantity
        inventory.save()

        # Sync Product quantity
        product.quantity = total_quantity
        product.save()



class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    total_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.product.name} - {self.total_quantity} units"
    
class PurchaseOrder(models.Model):
    company_name = models.CharField(max_length=255)
    company_address = models.TextField()
    company_phone = models.CharField(max_length=15)
    company_email = models.EmailField()
    company_website = models.URLField(blank=True, null=True)
    po_date = models.DateField(auto_now_add=True)
    po_number = models.CharField(max_length=50, unique=True)
    customer_number = models.CharField(max_length=50)
    vendor_company_name = models.CharField(max_length=255)
    vendor_contact_name = models.CharField(max_length=255)
    vendor_phone = models.CharField(max_length=15)
    vendor_address = models.TextField()
    vendor_website = models.URLField(blank=True, null=True)
    vendor_email = models.EmailField()
    ship_to_name = models.CharField(max_length=255)
    ship_to_company_name = models.CharField(max_length=255)
    ship_to_address = models.TextField()
    ship_to_phone = models.CharField(max_length=15)
    ship_to_email = models.EmailField()
    ship_to_website = models.URLField(blank=True, null=True)
    item_number = models.CharField(max_length=50)
    product_name = models.CharField(max_length=255)
    product_quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

# class Bin(models.Model):
#     whs_no = models.ForeignKey(
#         Warehouse,
#         on_delete=models.CASCADE,
#         related_name="bins"  # use plural for clarity
#     )
#     bin_id = models.CharField(max_length=50, unique=True)  # Add max_length and make it unique if applicable
#     capacity = models.IntegerField()
#     category = models.CharField(max_length=100)  # Add max_length
#     shelves = models.CharField(null=True, blank=True, max_length=100)  # Add max_length
#     created_by = models.CharField(max_length=100, null=True, blank=True)
#     updated_by = models.CharField(max_length=100, null=True, blank=True)
#     existing_quantity = models.IntegerField(default=0)  # Add default value

#     def __str__(self):
#         return f"Bin {self.bin_id} in Warehouse {self.whs_no}"

#    
    


class Putaway(models.Model):
    putaway_id = models.CharField(max_length=50)
    pallet = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    putaway_task_type = models.CharField(max_length=100, null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
   

    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.pallet} - {self.status}"

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from .models import Putaway

def pending_putaway(request):
    pending_tasks = Putaway.objects.filter(status="In Progress")
    return render(request, 'pending_task.html', {'pending_tasks': pending_tasks})

def edit_putaway(request, pk):
    putaway = get_object_or_404(Putaway, pk=pk)

    if request.method == 'POST':
        putaway.pallet = request.POST.get('pallet')
        putaway.location = request.POST.get('location')
        putaway.putaway_task_type = request.POST.get('putaway_task_type')
        putaway.status = request.POST.get('status')

        if putaway.status == "Completed":
            putaway.confirmed_at = now()

        putaway.save()
        return redirect('pending_putaway')

    return render(request, 'edit_putaway.html', {'putaway': putaway})

class PutawayTask(models.Model):
    PUTAWAY_TASK_CHOICES = [
        ("Putaway by HU", "Putaway by HU"),
        ("Putaway by Warehouse", "Putaway by Warehouse"),
        ("Putaway by Product", "Putaway by Product"),
        ("Putaway by Storage Bin", "Putaway by Storage Bin"),
    ]

    putaway_id = models.CharField(max_length=50)
    pallet = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    putaway_task_type = models.CharField(
        max_length=50,
        choices=PUTAWAY_TASK_CHOICES,
        default="Putaway by HU"
    )
    status = models.CharField(max_length=20, choices=[
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ], default="In Progress")

    def __str__(self):
        return f"{self.putaway_id} - {self.putaway_task_type}"



from django.db import models
from django.contrib.auth.models import User

class Picking(models.Model):
    picking_id = models.CharField(max_length=10, null=True, blank=True, unique=True) 
    pallet = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100, default=None, null=True, blank=True)
    location = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

    STATUS_CHOICES = [
       
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Progress')
    def save(self, *args, **kwargs):
        if not self.picking_id:
            last_picking = Picking.objects.order_by('-picking_id').first()
            if last_picking and last_picking.picking_id[1:].isdigit():
                next_id = int(last_picking.picking_id[1:]) + 1
            else:
                next_id = 1

            self.picking_id = f"P{next_id:03d}"  # Example: P001, P002
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.picking_id} - {self.product}"
    

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    product = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class InboundDelivery(models.Model):
    inbound_delivery_number = models.CharField(max_length=50, unique=True, editable=False)
    delivery_date = models.DateField()
    document_date = models.DateField(blank=True, null=True)
    gr_date = models.DateField()
    supplier = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    purchase_order_number = models.ForeignKey(PurchaseOrder,on_delete=models.CASCADE,null=True,  blank=True)
    whs_no = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='inbound_deliveries', null=True, blank=True)

    
    DELIVERY_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='Pending')
    storage_location = models.CharField(max_length=100)
    carrier_info = models.CharField(max_length=100)
    remarks = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.inbound_delivery_number:
            self.inbound_delivery_number = f"IDN-{uuid.uuid4().hex[:8].upper()}"
        
        # if not self.batch_number:
        #     self.batch_number = f"BATCH-{uuid.uuid4().hex[:6].upper()}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Delivery #{self.inbound_delivery_number}"
    def warehouse_number(self):
        """Fetches the warehouse number from related Warehouse"""
        return self.whs_no.whs_no
    def vendor_number(self):
        return self.supplier.supplier_id if self.supplier else None
    def vendor_number(self):
        """Fetches the vendor number from related Vendor"""
        return f"{self.supplier.supplier_id} - {self.supplier.name}" if self.supplier else None

    def po_number(self):
        return self.purchase_order_number.po_number if self.purchase_order_number else None

    def product(self):
        """Fetches product ID and name from related Product"""
        return f"{self.product.product_id} - {self.product.name}" if self.product else None

class InboundDeliveryproduct(models.Model):
    delivery = models.ForeignKey(InboundDelivery, on_delete=models.CASCADE, related_name='product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    product_description = models.CharField(max_length=255)
    quantity_delivered = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_received = models.DecimalField(max_digits=10, decimal_places=2)
    unit_of_measure = models.CharField(max_length=20)
    batch_number = models.CharField(max_length=50, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.batch_number:
           self.batch_number = f"BATCH-{uuid.uuid4().hex[:6].upper()}"
        
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Delivery #{self.batch_number}"

   