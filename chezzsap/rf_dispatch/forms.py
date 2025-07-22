# rf_dispatch/forms.py
from django import forms
from .models import YardHdr, YES_NO_CHOICES  # Make sure YES_NO_CHOICES is imported
from .models import Product
from .models import Warehouse
from .models import StockUpload
from .models import Customers
from .models import Vendor

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



class StockUploadForm(forms.ModelForm):
    class Meta:
        model = StockUpload
        fields = [
            'whs_no', 'product', 'quantity', 'batch', 'bin', 'pallet',
            'p_mat', 'inspection', 'stock_type', 'wps', 'doc_no', 'pallet_status'
        ] 
        widgets = {
            'whs_no': forms.TextInput(attrs={'class': 'form-control'}),
            'product': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'batch': forms.TextInput(attrs={'class': 'form-control'}),
            'bin': forms.TextInput(attrs={'class': 'form-control'}),
            'pallet': forms.TextInput(attrs={'class': 'form-control'}),
            'p_mat': forms.TextInput(attrs={'class': 'form-control'}),
            'inspection': forms.TextInput(attrs={'class': 'form-control'}),
            'stock_type': forms.TextInput(attrs={'class': 'form-control'}),
            'wps': forms.TextInput(attrs={'class': 'form-control'}),
            'doc_no': forms.TextInput(attrs={'class': 'form-control'}),
            'pallet_status': forms.TextInput(attrs={'class': 'form-control'})
        }

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = '__all__'
        
        
class CustomersForm(forms.ModelForm):
    class Meta:
        model=Customers
        fields='__all__'
    
class VendorForm(forms.ModelForm):
    class Meta:
        model=Vendor
        fields='__all__'        

from django.utils import timezone
from django import forms
from .models import Pallet

class PalletForm(forms.ModelForm):
    class Meta:
        model = Pallet
        exclude = ['created_by', 'updated_by']  
        widgets = {
            'pallet_no': forms.TextInput(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-select'}),  
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_scanned': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'scanned_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
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