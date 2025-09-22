from django.db import models
from django.contrib.auth.models import User
from django.db.models import F, Sum
from django.utils import timezone
from django.utils.timezone import now
from django.utils.html import format_html
from django.shortcuts import render, redirect, get_object_or_404
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
import uuid
from decimal import Decimal


YES_NO_CHOICES = [
    ('Yes', 'Yes'),
    ('No', 'No'),
]
class YardHdr(models.Model):
    id = models.AutoField(primary_key=True)
    yard_id = models.CharField(max_length=100, null=True, blank=True)
    truck_no = models.CharField(max_length=100)
    whs_no = models.ForeignKey('Warehouse', on_delete=models.CASCADE, default=None, null=True, blank=True)
    truck_type = models.CharField(max_length=50, blank=True, null=True)
    driver_name = models.CharField(max_length=50)
    driver_phn_no = models.CharField(max_length=10)
    po_no = models.CharField(max_length=10)
    truck_date = models.DateField()
    truck_time = models.TimeField()
    truck_state = models.CharField(max_length=50, default='Unknown', blank=True, null=True)
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


class InspectionQuestion(models.Model):
    text = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class InspectionResponse(models.Model):
    yard = models.ForeignKey(YardHdr, on_delete=models.CASCADE, related_name="inspections")
    question = models.ForeignKey(InspectionQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=10, choices=YES_NO_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.yard.truck_no} - {self.question.text} - {self.answer}"


class TruckLog(models.Model):
    truck_no = models.ForeignKey(YardHdr, on_delete=models.CASCADE)
    truck_date = models.DateField(auto_now_add=True)
    truck_time = models.TimeField(auto_now_add=True)
    time_taken = models.CharField(max_length=20, default='-')
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='Not planned')
    status_changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.truck_no.truck_no} - {self.status} @ {self.truck_date} {self.truck_time}"




def log_truck_status(truck_instance, status, user=None, comment=''):
    TruckLog.objects.create(
        truck_no=truck_instance,
        status=status,
        status_changed_by=user,
        comment=comment
    )




class Truck(models.Model):
    yard = models.ForeignKey(YardHdr, on_delete=models.CASCADE, default=None, null=True, blank=True)
    truck_no = models.CharField(max_length=100, unique=True)
    driver_name = models.CharField(max_length=50)
    driver_phn_no = models.CharField(max_length=10)

    def __str__(self):
        return f"Truck(truck_no={self.truck_no}, driver_name={self.driver_name})"

    
class Warehouse(models.Model):
    whs_no = models.CharField(primary_key=True, max_length=50)
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
    
class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Bin(models.Model):
    whs_no = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="bins" 
    )
    bin_id = models.CharField(max_length=50, unique=True) 
    bin_type = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    location = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="bins") 
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="bins", null=True, blank=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    existing_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Bin {self.bin_id} in Warehouse {self.whs_no}"
    
    def remaining_capacity(self):
        return self.capacity - self.existing_quantity

    def __str__(self):
        return f"{self.bin_id} (Remaining: {self.remaining_capacity()}/{self.capacity})"


class Product(models.Model):
    product_id = models.CharField(
        primary_key=True,
        max_length=50,
        unique=True,
        editable=False   # prevents showing in admin form
    )
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)   
    pallet_no = models.CharField(max_length=50, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    unit_of_measure = models.CharField(max_length=50, default="pcs")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="products", null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="products",null=True, blank=True) 
    re_order_level = models.IntegerField(default=10)
    images = models.ImageField(upload_to='product_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        is_new = self._state.adding  

        # 🔹 Auto-generate product_id only for new products
        if is_new and not self.product_id:
            last = Product.objects.order_by("-created_at").first()
            if last and last.product_id.startswith("P"):
                next_num = int(last.product_id[1:]) + 1
            else:
                next_num = 1
            self.product_id = f"P{next_num:05d}"   # Example: P00001, P00002...

        # 🔹 Track old quantity for inventory sync
        old_quantity = None
        if not is_new:
            old_quantity = Product.objects.get(pk=self.pk).quantity

        super().save(*args, **kwargs)

        # 🔹 Update Inventory after save
        if is_new or (old_quantity != self.quantity):
            inventory, created = Inventory.objects.get_or_create(product=self)
            inventory.total_quantity = self.quantity
            inventory.save()

    def __str__(self):
        return f"{self.name} ({self.product_id})"



# -----------------------------
# POST SAVE SIGNAL
# -----------------------------
@receiver(post_save, sender=Product)
def create_or_update_inventory(sender, instance, **kwargs):
    """
    Ensure every Product always has an Inventory,
    and sync total_quantity automatically.
    """
    inventory, created = Inventory.objects.get_or_create(product=instance)
    if inventory.total_quantity != instance.quantity:
        inventory.total_quantity = instance.quantity
        inventory.save()



class PackingMaterial(models.Model):
    material = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.material

class Pallet(models.Model):
    pallet_no = models.CharField(max_length=100, unique=True, editable=False, default='') 
    parent_pallet = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_pallets')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True)
    p_mat = models.ForeignKey(PackingMaterial, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    scanned_at = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.CharField(max_length=100, default=None, null=True, blank=True)
    updated_by = models.CharField(max_length=100, default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pallet_no:
            last_pallet = Pallet.objects.order_by('-id').first()
            if last_pallet and last_pallet.pallet_no.startswith("PLT-") and last_pallet.pallet_no[4:].isdigit():
                next_id = int(last_pallet.pallet_no[4:]) + 1
            else:
                next_id = 1
            self.pallet_no = f"PLT-{next_id:03d}"   # 👉 PLT-001, PLT-002, PLT-003
        super().save(*args, **kwargs)
    def __str__(self):
          return f"PLT {self.id}"

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
    customer_id = models.CharField(max_length=10, blank=True, null=True) 
    customer_code = models.CharField(max_length=50)
    email = models.EmailField()
    phone_no = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


  

class StockUpload(models.Model):
    id = models.AutoField(primary_key=True)
    whs_no = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, blank=True, null=True)   
    sub_category = models.CharField(max_length=100, blank=True, null=True) 
    description = models.TextField(blank=True, null=True)   
    quantity = models.PositiveIntegerField()
    batch = models.CharField(max_length=100, null=True, blank=True)
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE , null=True, blank=True)
    pallet = models.CharField(max_length=50, default='Not assigned', blank=True, null=True)
    p_mat = models.ForeignKey(PackingMaterial, on_delete=models.CASCADE, null=True, blank=True)
    inspection = models.CharField(max_length=50)
    stock_type = models.CharField(max_length=50)
    item_number = models.CharField(max_length=50)
    doc_no = models.CharField(max_length=50)
    pallet_status = models.CharField(max_length=50, default='Not planned')


    def __str__(self):
        return f"{self.product} in {self.bin} - {self.quantity}"
    
    def clean(self):
        """Ensure quantity does not exceed bin remaining capacity"""
        if self.bin and self.quantity > self.bin.remaining_capacity():
            raise ValidationError(
                f"Cannot assign {self.quantity} items to {self.bin.bin_id}. "
                f"Only {self.bin.remaining_capacity()} remaining."
            )

    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)

        # Update total quantity in Inventory
        total_quantity = StockUpload.objects.filter(product=self.product).aggregate(
            total=Sum('quantity')
        )['total'] or 0
        inventory, _ = Inventory.objects.get_or_create(product=self.product)
        inventory.total_quantity = total_quantity
        inventory.save()

        # Update quantity in Product
        self.product.quantity = total_quantity
        self.product.save()

        # Update Bin existing quantity
        if self.bin:
            total_in_bin = StockUpload.objects.filter(bin=self.bin).aggregate(
                total=Sum('quantity')
            )['total'] or 0
            self.bin.existing_quantity = total_in_bin
            self.bin.save()

    def delete(self, *args, **kwargs):
        product = self.product
        bin_obj = self.bin
        super().delete(*args, **kwargs)

        # Update Inventory
        total_quantity = StockUpload.objects.filter(product=product).aggregate(
            total=Sum('quantity')
        )['total'] or 0
        inventory, _ = Inventory.objects.get_or_create(product=product)
        inventory.total_quantity = total_quantity
        inventory.save()

        # Update Product quantity
        product.quantity = total_quantity
        product.save()

        # Update Bin existing quantity
        if bin_obj:
            bin_obj.existing_quantity = StockUpload.objects.filter(bin=bin_obj).aggregate(
                total=Sum('quantity')
            )['total'] or 0
            bin_obj.save()        # Update Bin existing quantity
            
        if bin_obj:
            total_in_bin = StockUpload.objects.filter(bin=bin_obj).aggregate(
                total=Sum('quantity')
            )['total'] or 0
            bin_obj.existing_quantity = total_in_bin
            bin_obj.save()


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_quantity = models.IntegerField(default=0)
    min_quantity = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_low_stock(self):
        return self.total_quantity < self.min_quantity

    def is_medium_stock(self):
        return self.total_quantity >= self.min_quantity and self.total_quantity < self.min_quantity * 2

    def stock_status_badge(self):
        if self.is_low_stock():
            color = "danger"
            text = "Low"
        elif self.is_medium_stock():
            color = "warning"
            text = "Medium"
        else:
            color = "success"
            text = "Sufficient"
        return format_html('<span class="badge bg-{}">{}</span>', color, text)


   
class PurchaseOrder(models.Model):
    company_name = models.CharField(max_length=255)
    company_address = models.TextField()
    company_phone = models.CharField(max_length=15, null=True, blank=True)
    company_email = models.EmailField()
    company_website = models.URLField(blank=True, null=True)
    po_date = models.DateField(null=True, blank=True)
    po_number = models.CharField(max_length=50, unique=True)
    invoice_number = models.CharField(max_length=50, null=True, blank=True)
    vendor_company_name = models.CharField(max_length=255, null=True, blank=True)
    vendor_contact_name = models.CharField(max_length=255, null=True, blank=True)
    vendor_phone = models.CharField(max_length=15, null=True, blank=True)
    vendor_address = models.TextField(null=True, blank=True)
    vendor_website = models.URLField(blank=True, null=True)
    vendor_email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="purchase_orders"
    )

    def __str__(self):
        return f"PO-{self.po_number}"



class Putaway(models.Model):
    putaway_id = models.CharField(max_length=50, unique=True, editable=False)
    pallet = models.ForeignKey(Pallet, on_delete=models.SET_NULL, null=True, blank=True)
    source_location = models.CharField(max_length=100)
    destination_location = models.CharField(max_length=100)
    PUTAWAY_TASK_TYPE_CHOICES = [
        ("Putaway by HU", "Putaway by HU"),
        ("Putaway by Warehouse", "Putaway by Warehouse"),
        ("Putaway by Product", "Putaway by Product"),
        ("Putaway by Bin", "Putaway by Bin"),
    ]
    putaway_task_type = models.CharField(
        max_length=100, null=True, blank=True, choices=PUTAWAY_TASK_TYPE_CHOICES
    )

    STATUS_CHOICES = [
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="In Progress")

    # ✅ Tracking fields
    created_by = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    confirmed_at = models.CharField(max_length=100,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)


    warehouse = models.ForeignKey(
        "Warehouse", on_delete=models.SET_NULL, null=True, blank=True
    )
    product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, blank=True
    )
    bin = models.ForeignKey(
        "Bin", on_delete=models.SET_NULL, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.putaway_id:
            date_str = now().strftime("%Y%m%d")
            last_id = Putaway.objects.filter(
                putaway_id__startswith=f"PUT{date_str}"
            ).order_by("-putaway_id").first()
            if last_id:
                last_number = int(last_id.putaway_id[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            self.putaway_id = f"PUT{date_str}{new_number:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.putaway_id} - {self.pallet} ({self.status})"



from django.db import models
from django.utils import timezone

class Picking(models.Model):
    picking_id = models.CharField(max_length=10, null=True, blank=True, unique=True) 
    pallet = models.ForeignKey('Pallet', on_delete=models.CASCADE)  
    product = models.ForeignKey('Product', on_delete=models.CASCADE) 
    source_location = models.CharField(max_length=100)
    destination_location = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

    created_by = models.CharField(max_length=100, default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    updated_by = models.CharField(max_length=100, default=None, null=True, blank=True)
    confirmed_at = models.CharField(max_length=100, null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    PICKING_TYPE_CHOICES = [
        ('INBOUND', 'Inbound'),
        ('OUTBOUND', 'Outbound'),
    ]
    picking_type = models.CharField(max_length=50, choices=PICKING_TYPE_CHOICES, default="Inbound")

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
            self.picking_id = f"P{next_id:03d}" 

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
    supplier = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    purchase_order_number = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE,null=True,  blank=True)
    esn= models.CharField(max_length=100, blank=True, null=True)
    whs_no = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='inbound_deliveries', null=True, blank=True)
   
    
    DELIVERY_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='Pending')
    remarks = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.inbound_delivery_number:
            self.inbound_delivery_number = f"IDN-{uuid.uuid4().hex[:8].upper()}"
    
        
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
    delivery = models.ForeignKey(InboundDelivery, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inbound_deliveries')
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

   

from decimal import Decimal
from django.db import models

class PurchaseItem(models.Model):
    purchase_order = models.ForeignKey(
        "PurchaseOrder",
        on_delete=models.CASCADE,
        related_name="purchase_items"
    )
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    warehouse = models.ForeignKey(
        "Warehouse",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="purchase_items"
    )

    def save(self, *args, **kwargs):
        # calculate total price before saving
        if self.quantity and self.unit_price:
            self.total_price = Decimal(self.quantity) * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) in PO-{self.purchase_order.po_number}"




STATUS_CHOICES = [
    ('Draft', 'Draft'),
    ('Confirm', 'Confirm'),
    ('Cancel', 'Cancel'),
    ('Edit', 'Edit'),
    ('Delivery', 'Delivery')
]

class SalesOrderCreation(models.Model):
    so_no = models.CharField(max_length=50, editable=False, unique=True)
    whs_no = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="sales_orders")
    whs_address = models.TextField(default="Unknown")
    customer_id = models.CharField(max_length=50)
    customer_code = models.CharField(max_length=50)
    order_date = models.DateField()
    delivery_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Draft')
    remarks = models.TextField(blank=True, null=True)
    net_total_price = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.so_no} - {self.status}"

    def save(self, *args, **kwargs):
        if not self.so_no:
            last_so = SalesOrderCreation.objects.all().order_by('id').last()
            if last_so and last_so.so_no.startswith('SO'):
                last_no = int(last_so.so_no.split('SO')[-1])
                self.so_no = f"SO{last_no + 1:05d}"
            else:
                self.so_no = "SO00001"
        super().save(*args, **kwargs)




class SalesOrderItem(models.Model):
    so_no = models.ForeignKey(SalesOrderCreation, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None) 
    product_name = models.CharField(max_length=200)
    existing_quantity = models.IntegerField(default=0)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.product_name} ({self.quantity}) - {self.so_no.so_no}"

    def save(self, *args, **kwargs):
        self.unit_total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

# outbound delivery
class OutboundDelivery(models.Model):
    dlv_no = models.CharField(max_length=200, unique=True, blank=True, null=True)
    so_no = models.ForeignKey(
        SalesOrderCreation,
        on_delete=models.CASCADE,
        related_name='outbound_deliveries'
    )
    whs_no = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='outbound_deliveries',
        default=None,
        null=True,
        blank=True
    )
    whs_address = models.CharField(max_length=300, blank=True, null=True)

    sold_to = models.CharField(max_length=200, blank=True, null=True)
    ship_to = models.CharField(max_length=200, blank=True, null=True)
    cust_ref = models.CharField(max_length=200, blank=True, null=True)
    ord_date = models.DateField(blank=True, null=True)
    del_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Delivery {self.dlv_no}"


class OutboundDeliveryItem(models.Model):
    delivery = models.ForeignKey(
        OutboundDelivery,
        on_delete=models.CASCADE,
        related_name='items'
    )
    dlv_it_no = models.CharField(max_length=50)  

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="outbound_items"
    )
    product_name = models.CharField(max_length=200)
    serial_no = models.CharField(max_length=100, blank=True, null=True)
    batch_no = models.CharField(max_length=100, blank=True, null=True)
    qty_order = models.DecimalField(max_digits=100, decimal_places=2)
    qty_issued = models.DecimalField(max_digits=100, decimal_places=2)
    unit_price = models.DecimalField(max_digits=100, decimal_places=2)
    unit_total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    net_total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    vol_per_item  = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        unique_together = ('delivery', 'dlv_it_no')

    def __str__(self):
        return f"{self.product.name} - Item {self.dlv_it_no}"



class Packing(models.Model):
    pallet = models.ForeignKey(Pallet, on_delete=models.CASCADE, related_name="packings")
    p_mat = models.ForeignKey(PackingMaterial, on_delete=models.CASCADE, null=True, blank=True)
    del_no = models.CharField(max_length=50)   
    gross_wt = models.DecimalField(max_digits=10, decimal_places=2)
    net_wt = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pallet {self.pallet} - Delivery {self.del_no}"


class PackedItem(models.Model):
    packing = models.ForeignKey(Packing, on_delete=models.CASCADE, related_name="items")
    pallet = models.ForeignKey(Pallet, on_delete=models.CASCADE, related_name="items")
    p_mat = models.ForeignKey(PackingMaterial, on_delete=models.CASCADE, null=True, blank=True)
    batch_no = models.CharField(max_length=50)
    serial_no = models.CharField(max_length=50)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-fill pallet and p_mat from parent Packing
        if self.packing:
            self.pallet = self.packing.pallet
            self.p_mat = self.packing.p_mat
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Item {self.serial_no} (Pallet {self.pallet})"


class PostGoodsIssue(models.Model):
    pgi_no = models.CharField(max_length=50, unique=True)  
    delivery = models.OneToOneField(  
        "rf_dispatch.OutboundDelivery",
        on_delete=models.CASCADE,
        related_name="pgi"
    )
    shipment = models.ForeignKey(
        "rf_dispatch.Shipment",
        on_delete=models.CASCADE,
        related_name="pgis",
        default=None,
        null=True,
        blank=True
    )
    posting_date = models.DateField(auto_now_add=True)
    posted_by = models.CharField(max_length=100)  
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Post Goods Issue"
        verbose_name_plural = "Post Goods Issues"
        ordering = ['-posting_date']

    def __str__(self):
        return f"PGI {self.pgi_no} for Delivery {self.delivery.dlv_no}"



class GoodsReceipt(models.Model):
    gr_no = models.CharField(max_length=50, unique=True, editable=False)
    inbound_delivery = models.OneToOneField(
        InboundDelivery,
        on_delete=models.CASCADE,
        related_name="gr"
    )
    posting_date = models.DateField(auto_now_add=True)
    posted_by = models.CharField(max_length=100)
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.gr_no:
            last_gr = GoodsReceipt.objects.order_by("-id").first()
            if last_gr and last_gr.gr_no.startswith("GR"):
                number = int(last_gr.gr_no.replace("GR", "")) + 1
            else:
                number = 1
            self.gr_no = f"GR{number:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.gr_no} - {self.inbound_delivery.inbound_delivery_number}"



class GoodsReceiptItem(models.Model):
    goods_receipt = models.ForeignKey(
        GoodsReceipt,
        on_delete=models.CASCADE,
        related_name="items"
    )
    inbound_delivery_product = models.ForeignKey(
        InboundDeliveryproduct,
        on_delete=models.CASCADE,
        related_name="gr_items"
    )
    quantity_received = models.DecimalField(max_digits=10, decimal_places=2)
    batch_number = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.batch_number and self.inbound_delivery_product.batch_number:
            self.batch_number = self.inbound_delivery_product.batch_number
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.goods_receipt.gr_no} - {self.inbound_delivery_product.product.name}"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    warehouse = models.ForeignKey('Warehouse',on_delete=models.SET_NULL,blank=True,null=True,related_name="profiles" )    
    image = models.ImageField(upload_to='profiles/', default='profiles/default.png')

    def __str__(self):
        return f"{self.user.username}'s Profile"

# ---------------
# Shipment Model
# ---------------
from django.db import models

class Shipment(models.Model):
    shipment_no = models.CharField(max_length=100, unique=True)
    truck = models.ForeignKey(Truck, null=True, blank=True, on_delete=models.SET_NULL)
    yard_hdr = models.ForeignKey(YardHdr, null=True, blank=True, on_delete=models.SET_NULL)
    planned_dispatch_date = models.DateField()
    shipment_status = models.CharField(max_length=50, default='Planned')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
     
    def __str__(self):
        return f"Shipment {self.shipment_no} - {self.shipment_status}"

class SortStatus(models.TextChoices):
    PENDING = "Pending", "Pending"
    SORTED = "Sorted", "Sorted"
    
class Sorting(models.Model):
    outbound = models.ForeignKey("OutboundDelivery",on_delete=models.CASCADE, related_name="sortings" )
    pallet = models.ForeignKey("Pallet",on_delete=models.CASCADE, related_name="sortings")
    so_no = models.ForeignKey("SalesOrderCreation",on_delete=models.CASCADE, related_name="sortings" )
    product = models.ForeignKey("Product", on_delete=models.CASCADE,related_name="sortings" )
    quantity = models.PositiveIntegerField()
    warehouse = models.ForeignKey("Warehouse",on_delete=models.CASCADE,related_name="sortings", null=True, blank=True, default=None )
    status = models.CharField( max_length=50,choices=SortStatus.choices,default=SortStatus.PENDING )
    sorted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, null=True, blank=True, default=None)
    updated_by = models.CharField(max_length=100, null=True, blank=True, default=None)
    class Meta:
        ordering = ["-sorted_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["outbound"]),
        ]
    def __str__(self):
        return f"Sorting #{self.id} | {self.product} x {self.quantity} ({self.get_status_display()})"

    def __str__(self):
        return f"{self.shipment.shipment_no} - {self.pgi.pgi_no}"

class SortStatus(models.TextChoices):
    PENDING = "Pending", "Pending"
    SORTED = "Sorted", "Sorted"
   

class Sorting(models.Model):
    outbound = models.ForeignKey("OutboundDelivery",on_delete=models.CASCADE, related_name="sortings" )
    pallet = models.ForeignKey("Pallet",on_delete=models.CASCADE, related_name="sortings")
    so_no = models.ForeignKey("SalesOrderCreation",on_delete=models.CASCADE,null=True, blank=True )
    product = models.ForeignKey("Product", on_delete=models.CASCADE,related_name="sortings" )
    quantity = models.PositiveIntegerField()
    location = models.CharField(max_length=100, null=True, blank=True, default=None)
    warehouse = models.ForeignKey("Warehouse",on_delete=models.CASCADE,related_name="sortings", null=True, blank=True, default=None )
    status = models.CharField( max_length=50,choices=SortStatus.choices,default=SortStatus.PENDING )
    sorted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, null=True, blank=True, default=None)
    updated_by = models.CharField(max_length=100, null=True, blank=True, default=None)
    class Meta:
        ordering = ["location"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["outbound"]),
        ]
    def __str__(self):
        return f"Sorting #{self.id} | {self.product} x {self.quantity} ({self.get_status_display()})"

from django.db import models
from django.contrib.auth.models import User

class BinLog(models.Model):
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=100)  
    whs_no = models.CharField(max_length=50)
    remarks = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bin.bin_code} - {self.action} at {self.created_at}"
