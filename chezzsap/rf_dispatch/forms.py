# rf_dispatch/forms.py
from django import forms
from .models import YardHdr, YES_NO_CHOICES  # Make sure YES_NO_CHOICES is imported
from .models import Product


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

class EditProduct(forms.ModelForm):
    class Meta:
        model =Product
        fields = '__all__'