# rf_dispatch/forms.py
from django import forms
from .models import YardHdr, YES_NO_CHOICES  # Make sure YES_NO_CHOICES is imported
from .models import Product
from .models import Warehouse
from .models import StockUpload
from .models import Customers
from .models import Vendor
from .models import Truck

class YardHdrForm(forms.ModelForm):
  
    class Meta:
        model = YardHdr
        fields = [
            'whs_no', 'truck_no', 'truck_type', 'driver_name',
            'driver_phn_no', 'po_no', 'truck_date', 'truck_time',
            'seal_no', 'yard_scan'
        ]
        widgets = {
            'truck_date': forms.DateInput(attrs={'type': 'date'}),
            'truck_time': forms.TimeInput(attrs={'type': 'time'}),
            
        }

from django import forms 


class TruckInspectionForm(forms.ModelForm):
    class Meta:
        model = YardHdr
        fields = [
          'truck_no', 'seal_no',
          'is_the_lock_secure', 'is_the_truck_clean', 'is_the_driver_safe', 'is_the_pallet_stable',
          'is_the_temperature_ideal', 'is_the_ac_working', 'does_the_truck_have_a_good_odor',
          'is_the_truck_dock_level_ok']

        widgets = {
            'truck_no': forms.TextInput(attrs={'class': 'form-control'}),
            'seal_no': forms.TextInput(attrs={'class': 'form-control'}),
            'is_the_lock_secure': forms.Select(choices=YES_NO_CHOICES, attrs={'class': 'form-select'}),
            'is_the_truck_clean': forms.Select(choices=YES_NO_CHOICES, attrs={'class': 'form-select'}),
            'is_the_driver_safe': forms.Select(choices=YES_NO_CHOICES, attrs={'class': 'form-select'}),
            'is_the_pallet_stable': forms.Select(choices=YES_NO_CHOICES, attrs={'class': 'form-select'}),
            'is_the_temperature_ideal': forms.Select(choices=YES_NO_CHOICES, attrs={'class': 'form-select'}),
            'is_the_ac_working': forms.Select(choices=YES_NO_CHOICES, attrs={'class': 'form-select'}),
            'does_the_truck_have_a_good_odor': forms.Select(choices=YES_NO_CHOICES, attrs={'class': 'form-select'}),
            'is_the_truck_dock_level_ok': forms.Select(choices=YES_NO_CHOICES, attrs={'class': 'form-select'}),
        }


from django import forms
class Trucksearchform(forms.Form):
      truck_no=forms.CharField(max_length=50)
      
      

      
class ProductForm(forms.ModelForm): 
    
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['created_at', 'updated_at']




class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = '__all__'
        
        
class CustomersForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields =  '__all__'
    
class VendorForm(forms.ModelForm):
    class Meta:
        model=Vendor
        fields='__all__'

from django.utils import timezone
from django import forms
from .models import Pallet

from django import forms
from .models import Pallet

from django import forms
from .models import Pallet

class PalletForm(forms.ModelForm):
    has_child_pallets = forms.BooleanField(
        required=False,
        label="Does this pallet have child pallets?",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    number_of_children = forms.IntegerField(
        required=False,
        min_value=1,
        label="Number of child pallets",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Pallet
        fields = '__all__'
        exclude = ['scanned_at', 'created_by', 'updated_by', 'parent_pallet','created_at']

    def __init__(self, *args, **kwargs):
        super(PalletForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # Skip boolean field so it uses 'form-check-input'
            if name != 'has_child_pallets':
                field.widget.attrs.update({'class': 'form-control'})

class PalletEditForm(forms.ModelForm):
    class Meta:
        model = Pallet
        # include only the fields you want to edit
        fields = ['product', 'p_mat', 'quantity', 'weight']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'p_mat': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }

from django import forms

from django import forms
from .models import PurchaseOrder

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'  # You can also manually list the fields if needed

    def __init__(self, *args, **kwargs):
        super(PurchaseOrderForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

from django import forms
from .models import Bin

class BinForm(forms.ModelForm):
    class Meta:
        model = Bin
        fields = '__all__'
        exclude = ['created_by', 'updated_by', 'existing_quantity']  # Exclude fields that are not needed in the form

from .models import Category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        exclude = ['created_by', 'created_at', 'updated_by', 'updated_at']  # Exclude fields that are not needed in the form
        
        
   
from .models import Putaway

class PutawayForm(forms.ModelForm):
    class Meta:
        model = Putaway
        exclude = ['created_at', 'confirmed_at']
        fields = '__all__'


# forms.py

from django import forms
from .models import Picking, Customer

class PickingForm(forms.ModelForm):
    class Meta:
        model = Picking
        fields = ['id', 'pallet', 'location', 'product', 'quantity','picking_type','status']
        exclude = ['created_at']

from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['created_by']  
        fields='__all__'
        
from django import forms
from .models import InboundDelivery

class InboundDeliveryForm(forms.ModelForm):
    class Meta:
        model = InboundDelivery
        fields = '__all__'
        exclude = ['inbound_delivery_number', 'batch_number']
        widgets = {
            'inbound_delivery_number': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'document_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gr_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'supplier': forms.TextInput(attrs={'class': 'form-control'}),
            'purchase_order_number': forms.TextInput(attrs={'class': 'form-control'}),
            'warehouse_no': forms.TextInput(attrs={'class': 'form-control'}),
            'material_code': forms.TextInput(attrs={'class': 'form-control'}),
            'product_description': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity_delivered': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity_received': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_of_measure': forms.TextInput(attrs={'class': 'form-control'}),
            'batch_number': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_status': forms.Select(attrs={'class': 'form-control'}),
            'storage_location': forms.TextInput(attrs={'class': 'form-control'}),
            'carrier_info': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control'}),
        }
        
from .models import SalesOrderCreation
class SalesOrderCreationForm(forms.ModelForm):
        class Meta:
            model=SalesOrderCreation
            fields = '__all__'
            widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from .models import OutboundDelivery, OutboundDeliveryItem, Product


class OutboundDeliveryForm(forms.ModelForm):
    class Meta:
        model = OutboundDelivery
        fields = '__all__'   # add other fields if required


class OutboundDeliveryItemForm(forms.ModelForm):
    product_id = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = OutboundDeliveryItem
        fields = '__all__'  # include fields you have in model
            
from django import forms
from django.forms import modelformset_factory
from .models import PackedItem, Packing

class PackingForm(forms.ModelForm):
    class Meta:
        model = Packing
        fields = ["pallet", "p_mat", "del_no", "gross_wt", "net_wt", "volume"]

class PackedItemForm(forms.ModelForm):
    class Meta:
        model = PackedItem
        fields = ["pallet", "p_mat", "batch_no", "serial_no", "quantity", "unit_price"]

PackedItemFormSet = modelformset_factory(PackedItem, form=PackedItemForm, extra=1, can_delete=True)
