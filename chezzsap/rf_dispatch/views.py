from django.shortcuts import render

def index(request):
    return render(request, 'home.html')

def home(request):
    return render(request, 'home.html')

def outbound3(request):
    return render(request, 'outbound3.html')

def sixth(request):
    return render(request, 'sixth.html')

def first(request):
    return render(request, 'first.html')

def hu1(request):
    return render(request, 'hu1.html')
def hu12(request):
    return render(request, 'hu12.html')
def hu123(request):
    return render(request, 'hu123.html')
def new1(request):  
    return render(request, 'new1.html')
def new2(request):
    return render(request, 'new2.html')
def new3(request):
    return render(request, 'new3.html')
def new4(request):
    return render(request, 'new4.html')
# def one(request):
#     return render(request, 'truck_screen/one.html')
# rf_dispatch/views.py
from django.shortcuts import render, redirect
from .forms import YardHdrForm


def yard_checkin_view(request):
    if request.method == 'POST':
        form = YardHdrForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            scan = instance.yard_scan.lower()   
            if 'door' in scan:
                instance.truck_status = 'door'
            elif 'parking' in scan:
                instance.truck_status = 'parking'
            elif 'Checkin' in scan:
                instance.truck_status = 'Checkin'
            elif 'gate' in scan:
                instance.truck_status = 'gate'
            elif 'checkout' in scan:
                instance.truck_status = 'checkout'
            else:
                instance.truck_status = 'not planned'

            instance.save()

            # ✅ Redirect to truck_inspection_view with truck_no
            return redirect('truck_inspection', truck_no=instance.truck_no)

    else:
        form = YardHdrForm()

    return render(request, 'truck_screen/one.html', {'form': form})




# def two(request):
#     return render(request, 'truck_screen/two.html')

# from django.shortcuts import render, redirect
# from .forms import TruckInspectionForm

# def truck_inspection_view(request):
#     truck= request.GET.objects.all()
#     if truck:
#         truck_no = truck[0].truck_no
#     else:
#         truck_no = None
#     if request.method == 'POST':
#         form = TruckInspectionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('two')  
#     else:
#         form = TruckInspectionForm()
#     return render(request, 'truck_screen/two.html', {'form': form})
from django.shortcuts import render, redirect
from .forms import TruckInspectionForm
from .models import Pallet, YardHdr, TruckLog
from .utils import log_truck_status  # create this helper

def truck_inspection_view(request, truck_no):
    try:
        existing_truck = YardHdr.objects.get(truck_no=truck_no)
        seal_no = existing_truck.seal_no
    except YardHdr.DoesNotExist:
        existing_truck = None
        seal_no = ''

    if request.method == 'POST':
        form = TruckInspectionForm(request.POST, instance=existing_truck)
        if form.is_valid():
            instance = form.save(commit=False)

            # 🔍 Capture previous status before saving
            old_status = existing_truck.truck_status if existing_truck else None

            instance.truck_no = truck_no
            if not instance.seal_no:
                instance.seal_no = seal_no
            instance.save()

            if old_status != instance.truck_status:
                log_truck_status(instance, instance.truck_status, user=request.user)

            return redirect('one')
        else:
            print(form.errors)
    elif existing_truck:
        form = TruckInspectionForm(instance=existing_truck)
    else:
        form = TruckInspectionForm(initial={'truck_no': truck_no, 'seal_no': seal_no})

    return render(request, 'truck_screen/two.html', {
        'form': form,
        'truck_no': truck_no,
        'seal_no': seal_no,
    })


from django.shortcuts import render
from .models import YardHdr

def inspection_summary_view(request):
    inspections = YardHdr.objects.all().order_by('-truck_date', '-truck_time')  # latest first
    return render(request, 'truck_screen/summary.html', {'inspections': inspections})


def three(request):
    return render(request, 'truck_screen/three.html')
def four(request):  
    return render(request, 'truck_screen/four.html')
def five1(request):
    return render(request, 'truck_screen/five1.html')
def six1(request):
    return render(request, 'truck_screen/six.html')
def seven1(request):
    return render(request, 'truck_screen/seven.html')
def eight1(request):    
    return render(request, 'truck_screen/eight.html')
def nine1(request):
    return render(request, 'truck_screen/nine.html')
def outbound1(request):
    return render(request, 'outbound1.html')
def outbound2(request):
    return render(request, 'outbound2.html')
def outbound3(request):
    return render(request, 'outbound3.html')
def outbound4(request):
    return render(request, 'outbound4.html')
def outbound5(request):
    return render(request, 'outbound5.html')
def outbound6(request):
    return render(request, 'outbound6.html')
def outbound7(request):
    return render(request, 'outbound7.html')


def truck_landing(request):
    return render(request, 'truck_screen/truck_landing_page.html')



def status_log_view(request, truck_no):
    logs = TruckLog.objects.filter(truck_no__truck_no=truck_no).order_by('-truck_date', '-truck_time')
    return render(request, 'truck_screen/status_log.html', {'logs': logs, 'truck_no': truck_no})


from django.shortcuts import render, get_object_or_404
from .models import TruckLog, YardHdr

def truck_log_view(request):
    truck_no_query = request.GET.get('truck_no')
    logs = []
    truck_details = None
    error_message = ""

    if truck_no_query:
        logs = TruckLog.objects.filter(truck_no__truck_no__icontains=truck_no_query).order_by('-truck_date', '-truck_time')
        try:
            truck_details = YardHdr.objects.get(truck_no=truck_no_query)
        except YardHdr.DoesNotExist:
            error_message = f"No truck found with number: {truck_no_query}"

    return render(request, 'truck_screen/truck_log.html', {
        'logs': logs,
        'truck_no_query': truck_no_query,
        'truck_details': truck_details,
        'error_message': error_message,
    })


from .models import YardHdr
from .forms import Trucksearchform

# View 1: Truck Status (Search by exact truck number using POST)
def truck_status_view(request, truck_no):
    truck = None
    not_found = False

    if request.method == 'POST':
        form = Trucksearchform(request.POST)
        if form.is_valid():
            truck_no = form.cleaned_data['truck_no']
            try:
                truck = YardHdr.objects.get(truck_no=truck_no)
            except YardHdr.DoesNotExist:
                not_found = True
    else:
        form = Trucksearchform()

    return render(request, 'truck_screen/truck_status.html', {
        'form': form,
        'truck': truck,
        'not_found': not_found,
    })

# View 2: Truck List (Search using GET, shows list)
def truck_list(request):
    query = request.GET.get('search')
    if query:
        trucks = YardHdr.objects.filter(truck_no__icontains=query)
    else:
        trucks = YardHdr.objects.all()

    return render(request, 'truck_screen/truck_list.html', {'trucks': trucks, 'query': query})

# View 3: Truck Detail (View single truck by whs_no)
from .models import YardHdr, TruckLog
from .utils import log_truck_status  # Assuming your log function is in utils.py

from .models import YardHdr, TruckLog
from .utils import log_truck_status  # Assuming your log function is in utils.py

def truck_detail(request, truck_no):
    try:
        truck = YardHdr.objects.get(truck_no=truck_no)

        # Log status only on POST
        if request.method == 'POST':
            new_status = request.POST.get('status', 'Viewed')
            comment = request.POST.get('comment', '')
            log_truck_status(truck_instance=truck, status=new_status, comment=comment)

        # Fetch logs related to this truck
        logs = TruckLog.objects.filter(truck_no=truck).order_by('-truck_date', '-truck_time')

        return render(request, 'truck_screen/truck_detail.html', {
            'truck': truck,
            'logs': logs
        })


    except YardHdr.DoesNotExist:
        return render(request, 'truck_screen/truck_detail.html', {'error': 'Truck not found'})




# views.py

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import YardHdr
from .utils import log_truck_status  # Ensure this utility function is defined

def update_truck_status(request, truck_no):
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        truck = get_object_or_404(YardHdr, truck_no=truck_no)
        old_status = truck.truck_status

        if new_status and new_status != old_status:
            truck.truck_status = new_status
            truck.save()

        comment = request.POST.get('comment', '')

        log_truck_status(truck_instance=truck, status=new_status,  comment=comment)

        return redirect('truck_detail', truck_no=truck_no)  

def stock_upload_login(request):
    return render(request, 'stock_upload/login_in_RFUI.html')

def stock_menu(request):
    return render(request, 'stock_upload/stock_menu.html')

# views.py
from django.shortcuts import render, redirect
from .models import StockUpload

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import StockUpload

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, StockUpload

def batch_product_view(request):
    if request.method == 'POST':
        whs_no = request.POST.get('whs_no')
        product_id = request.POST.get('product')  # Product ID
        quantity = request.POST.get('quantity')
        batch = request.POST.get('batch')
        bin_ = request.POST.get('bin')
        pallet = request.POST.get('pallet')
        p_mat = request.POST.get('p_mat')
        inspection = request.POST.get('inspection')
        stock_type = request.POST.get('stock_type')
        wps = request.POST.get('wps')
        doc_no = request.POST.get('doc_no')
        pallet_status = request.POST.get('pallet_status')

        try:
            product_instance = get_object_or_404(Product, id=product_id)

            StockUpload.objects.create(
                whs_no=whs_no,
                product=product_instance,
                quantity=int(quantity),
                batch=batch,
                bin=bin_,
                pallet=pallet,
                p_mat=p_mat,
                inspection=inspection,
                stock_type=stock_type,
                wps=wps,
                doc_no=doc_no,
                pallet_status=pallet_status
            )

            # Render with success flag
            products = Product.objects.all()
            return render(request, 'stock_upload/batch_product.html', {
                'products': products,
                'success': True
            })

        except Exception as e:
            print("❌ Error during StockUpload creation:", e)
            products = Product.objects.all()
            return render(request, 'stock_upload/batch_product.html', {
                'products': products,
                'error': str(e)
            })

    # GET request
    products = Product.objects.all()
    return render(request, 'stock_upload/batch_product.html', {'products': products})




def stock_detail_view(request, pallet):
    stock = get_object_or_404(StockUpload, pallet=pallet)
    return render(request, 'stock_upload/stock_detail.html', {'stock': stock})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Warehouse
from .forms import WarehouseForm

# Create or update a warehouse
# def warehouse_view(request):
#     if request.method == 'POST':
#         form = WarehouseForm(request.POST)
#         if form.is_valid():
#             warehouse = form.save()
#             # ✅ Correct redirect to the detail view using the proper URL name
#             return redirect('warehouse_detail', whs_no=warehouse.whs_no)
#     else:
#         form = WarehouseForm()
#     return render(request, 'warehouse/warehouse.html', {'form': form})


# # Display warehouse details
# def warehouse_detail_view(request, whs_no):
#     warehouse = get_object_or_404(Warehouse, whs_no=whs_no)
#     return render(request, 'warehouse/warehouse_details.html', {'warehouse': warehouse})


# def warehouse_list(request):
#     query = request.GET.get('search')
#     if query:
#         warehouses = Warehouse.objects.filter(whs_no__icontains=query)
#     else:
#         warehouses = Warehouse.objects.all()
#     return render(request, 'warehouse/warehouse.html', {'warehouses': warehouses})


# def warehouse_search_view(request, whs_no):
#     return render(request, 'warehouse/warehouse_search_details.html', {'whs_no': whs_no})



from django.shortcuts import render, redirect
from .models import Warehouse
from .forms import WarehouseForm

def warehouse_view(request):
    # === FORM HANDLING (Left Side) ===
    if request.method == 'POST':
        form = WarehouseForm(request.POST, request.FILES)
        if form.is_valid():
            warehouse = form.save()
            return redirect('warehouse_detail', whs_no=warehouse.whs_no)  # Replace with your URL name
    else:
        form = WarehouseForm()

    # === SEARCH + TABLE (Right Side) ===
    query = request.GET.get('search')
    if query:
        warehouses = Warehouse.objects.filter(whs_no__icontains=query)
    else:
        warehouses = Warehouse.objects.all()  # Show all if no search

    return render(request, 'warehouse/warehouse.html', {
        'form': form,
        'warehouses': warehouses,
        'query': query
    })


def warehouse_detail_view(request, whs_no):
    warehouse = get_object_or_404(Warehouse, whs_no=whs_no)
    return render(request, 'warehouse/warehouse_details.html', {'warehouse': warehouse})

def warehouse_search_view(request, whs_no):
    warehouse = get_object_or_404(Warehouse, whs_no=whs_no)
    return render(request, 'warehouse/warehouse_search_details.html', {'warehouse': warehouse})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Warehouse
from .forms import WarehouseForm

def edit_warehouse(request, whs_no):
    warehouse = get_object_or_404(Warehouse, whs_no=whs_no)

    if request.method == 'POST':
        form = WarehouseForm(request.POST, request.FILES, instance=warehouse)
        if form.is_valid():
            form.save()
            return redirect('warehouse_view')  # or 'warehouse_search_details', whs_no=warehouse.whs_no
    else:
        form = WarehouseForm(instance=warehouse)

    return render(request, 'warehouse/warehouse_edit.html', {'form': form, 'warehouse': warehouse})




# ...................
# product_detail
# ..................
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.utils import timezone
from .forms import ProductForm

# def add_product(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         product_id = request.POST.get('id')
#         quantity = request.POST.get('quantity')
#         pallet_no = request.POST.get('pallet_no')
#         sku = request.POST.get('sku')
#         description = request.POST.get('description')
#         unit_of_measure = request.POST.get('unit_of_measure')
#         category = request.POST.get('category')
#         re_order_level = request.POST.get('re_order_level')
#         images = request.FILES.get('images')

#         try:
#             product = Product.objects.create(
#                 product_id=product_id,
#                 name=name,
#                 quantity=quantity,
#                 pallet_no=pallet_no,
#                 sku=sku,
#                 description=description,
#                 unit_of_measure=unit_of_measure,
#                 category=category,
#                 re_order_level=re_order_level,
#                 images=images,
#                 created_at=timezone.now(),
#                 updated_at=timezone.now()
#             )
#             return redirect('product_detail', product_id=product.product_id)
#         except Exception as e:
#             return render(request, 'product/add_product.html', {'error': str(e)})

#     return render(request, 'product/add_product.html')

# from django.shortcuts import get_object_or_404, render, redirect
# from .models import Product

# def product_edit(request, product_id):
#     product = get_object_or_404(Product, product_id=product_id)

#     if request.method == "POST":
#         product.name = request.POST.get('name')
#         product.quantity = request.POST.get('quantity')
#         product.pallet_no = request.POST.get('pallet_no')
#         product.sku = request.POST.get('sku')
#         product.description = request.POST.get('description')
#         product.unit_of_measure = request.POST.get('unit_of_measure')
#         product.category = request.POST.get('category')
#         product.re_order_level = request.POST.get('re_order_level')
#         if request.FILES.get('images'):
#             product.images = request.FILES['images']

#         try:
#             product.save()
#             return redirect('product_list')  
#         except Exception as e:
#             print("Save failed:", e)  
#             return render(request, 'product/product_edit.html', {'product': product, 'error': str(e)})

#     return render(request, 'product/product_edit.html', {'product': product})




# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'product/product_list.html', {'products': products})


def product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('product_detail', product_id=product.product_id)
        else:
            print("❌ Form errors:", form.errors)  # Debug print (optional)
    else:
        form = ProductForm()

    query = request.GET.get('search')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'product/add_product.html', {
        'form': form,
        'products': products,
        'query': query
    })


def product_detail_view(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    return render(request, 'product/product_detail.html', {'product': product})

# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Product
# from django.utils import timezone

# def add_product(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         product_id = request.POST.get('id')
#         quantity = request.POST.get('quantity')
#         pallet_no = request.POST.get('pallet_no')
#         sku = request.POST.get('sku')
#         description = request.POST.get('description')
#         unit_of_measure = request.POST.get('unit_of_measure')
#         category = request.POST.get('category')
#         re_order_level = request.POST.get('re_order_level')
#         images = request.FILES.get('images')

#         try:
#             product = Product.objects.create(
#                 product_id=product_id,
#                 name=name,
#                 quantity=quantity,
#                 pallet_no=pallet_no,
#                 sku=sku,
#                 description=description,
#                 unit_of_measure=unit_of_measure,
#                 category=category,
#                 re_order_level=re_order_level,
#                 images=images,
#                 created_at=timezone.now(),
#                 updated_at=timezone.now()
#             )
#             return redirect('product_detail', product_id=product.product_id)
#         except Exception as e:
#             return render(request, 'product/add_product.html', {'error': str(e)})

#     return render(request, 'product/add_product.html')



# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Product
# from .forms import ProductForm
# from django.contrib import messages

# def product_detail(request, product_id):
#    product= get_object_or_404(Product, product_id=product_id)
#    return render(request, 'product/product_detail.html', {'product': product})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product
from .forms import ProductForm

def product_edit(request, product_id):
    # Get the existing product or return 404
    product = get_object_or_404(Product, product_id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'product/product_edit.html', {'form': form, 'product': product})
    
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})

    

  
# views.py
from .models import Inventory

def inventory_view(request):
    inventory = Inventory.objects.select_related('product').all()
    return render(request, 'inventory/inventory_list.html', {'inventory': inventory})

  

def product_delete(request, product_id):

    product = get_object_or_404(Product, product_id=product_id)
    product.delete()
    return redirect('product_list')  

# .......................
# customers.views.py
# .......................
from .forms import Customersform
from .models import Customers
from.models import vendor
from django.utils import timezone
from django.contrib import messages
def add_customers(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        id= request.POST.get('id')
        customer_code = request.POST.get('customer_code')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        address = request.POST.get('address')
        location = request.POST.get('location')

        try:
            customer = Customers.objects.create(
                name=name,
                id=id,
                customer_code=customer_code,
                email=email,
                phone_no=phone_no,
                address=address,
                location=location,
                )
            return redirect('customers_detail', customer_id=customer.id)
        except Exception as e:
            return render(request, 'customers/add_customers.html', {'error': str(e)})

    return render(request, 'customers/add_customers.html')

def customers_detail(request, customer_id):  
    customer = get_object_or_404(Customers, id=customer_id)
    return render(request, 'customers/customers_detail.html', {'customer': customer})

def customers_edit(request, customer_id):
    customer = get_object_or_404(Customers, id=customer_id)

    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.customer_code = request.POST.get('customer_code')
        customer.email = request.POST.get('email')
        customer.phone_no = request.POST.get('phone_no')
        customer.address = request.POST.get('address')
        customer.location = request.POST.get('location')
        
        customer.save()
        messages.success(request, "Customer updated successfully.")
        return redirect('customers_list')

    return render(request, 'customers/customers_edit.html', {'customer': customer})


def customers_list(request):
    customers = Customers.objects.all()
    return render(request, 'customers/customers_list.html', {'customer': customers})



# from django.views.decorators.http import require_POST

# @require_POST
# def customers_delete(request, customer_id):
#     customer = get_object_or_404(Customers, id=customer_id)
#     customer.delete()
#     return redirect('customers_edit')

def customers_delete(request, pk):
    customer = get_object_or_404(Customers, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customers_list') 
    
from .models import Warehouse

def whs_no_dropdown_view(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'stock_upload/batch_product.html', {'warehouses': warehouses})


from .forms import PalletForm

from django.shortcuts import render, redirect
from .forms import PalletForm
from .models import Pallet
from django.contrib.auth.models import User


def creating_pallet(request):
    # Handle form submission
    if request.method == 'POST':
        form = PalletForm(request.POST)
        if form.is_valid():
            pallet = form.save(commit=False)
            pallet.created_by = request.user
            pallet.updated_by = request.user
            pallet.save()
            return redirect('creating_pallet')  # Refresh page after submission
    else:
        form = PalletForm()

    # Handle pallet search
    query = request.GET.get('search')
    if query:
        pallets = Pallet.objects.filter(pallet_no__icontains=query)
    else:
        pallets = Pallet.objects.all()  

    
    return render(request, 'pallet/creating_pallet.html', {
        'form': form, 
        'pallets': pallets, 
        'query': query
        })


def pallet_search(request, pallet_no):
    pallet = get_object_or_404(Pallet, pallet_no=pallet_no)
    return render(request, 'pallet/pallet_search_details.html', {'pallet': pallet})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Pallet
from .forms import PalletForm

def edit_pallet(request, pallet_no):
    pallet = get_object_or_404(Pallet, pallet_no=pallet_no)

    if request.method == 'POST':
        form = PalletForm(request.POST, request.FILES, instance=pallet)
        if form.is_valid():
            form.save()
            return redirect('pallet_search_details', pallet_no=pallet.pallet_no)
    else:
        form = PalletForm(instance=pallet)

    return render(request, 'pallet/pallet_edit.html', {'form': form, 'pallet': pallet})



# from django.shortcuts import render, redirect


def add_vendor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        vendor_code = request.POST.get('vendor_code') 
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        address = request.POST.get('address')
        location = request.POST.get('location')
        profile_image = request.FILES.get('profile_image')  
 
        vendor = vendor(
            name=name,
            vendor_code=vendor_code,
            email=email,
            phone_no=phone_no,
            address=address,
            location=location,
            profile_image=profile_image
        )
        vendor.save()

        return redirect('vendor/vendor_detail')  

    return render(request, 'vendor/add_vendor.html')  

from django.shortcuts import render, redirect, get_object_or_404
from .forms import PurchaseOrderForm
from .models import PurchaseOrder
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from .models import PurchaseOrder
from django.urls import reverse

def add_purchase(request):
    if request.method == 'POST':
        try:
            # Extract form data
            company_name = request.POST.get('company_name')
            company_address = request.POST.get('company_address')
            phone_number = request.POST.get('phone_number')
            email_address = request.POST.get('email_address')
            website = request.POST.get('website')

            date = request.POST.get('date')  # not used due to auto_now_add
            po_number = request.POST.get('po_number')
            customer_number = request.POST.get('customer_number')

            vendor_contact_name = request.POST.get('vendor_contact_name')
            vendor_company_name = request.POST.get('vendor_company_name')
            vendor_address = request.POST.get('vendor_address')
            vendor_phn_number = request.POST.get('vendor_phn_number')
            vendor_website = request.POST.get('vendor_website')
            vendor_email = request.POST.get('vendor_email')

            ship_to_name = request.POST.get('ship_to_name')
            ship_cmpny_name = request.POST.get('ship_cmpny_name')
            ship_address = request.POST.get('ship_address')
            ship_phn_no = request.POST.get('ship_phn_no')
            ship_email = request.POST.get('ship_email')
            ship_website = request.POST.get('ship_website')

            item_number = request.POST.get('item_number')
            product_name = request.POST.get('product_name')
            quantity = int(request.POST.get('quantity'))
            unit_price = Decimal(request.POST.get('unit_price'))
            total_price = quantity * unit_price

            # Save to DB
            po = PurchaseOrder.objects.create(
                company_name=company_name,
                company_address=company_address,
                company_phone=phone_number,
                company_email=email_address,
                company_website=website,
                po_number=po_number,
                customer_number=customer_number,
                vendor_contact_name=vendor_contact_name,
                vendor_company_name=vendor_company_name,
                vendor_address=vendor_address,
                vendor_phone=vendor_phn_number,
                vendor_website=vendor_website,
                vendor_email=vendor_email,
                ship_to_name=ship_to_name,
                ship_to_company_name=ship_cmpny_name,
                ship_to_address=ship_address,
                ship_to_phone=ship_phn_no,
                ship_to_email=ship_email,
                ship_to_website=ship_website,
                item_number=item_number,
                product_name=product_name,
                product_quantity=quantity,
                unit_price=unit_price,
                total_price=total_price
            )

            # Redirect to detail view that shows data in PDF-style format
            return redirect('purchase_detail', pk=po.pk)

        except Exception as e:
            return render(request, 'purchase_order/add_purchase.html', {'error': str(e)})

    return render(request, 'purchase_order/add_purchase.html')


# from django.shortcuts import render, redirect
# from .forms import PurchaseOrderForm
# from models import PurchaseOrder


# def add_purchase(request):
#     if request.method == 'POST':
#         form = PurchaseOrderForm(request.POST)
#         if form.is_valid():
#             purchase_order = form.save()
#             return redirect('add_purchase', pk=purchase_order.pk)  # Redirect to PDF view
#     else:
#         form = PurchaseOrderForm()
#     return render(request, 'purchase_order/add_purchase.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from .models import PurchaseOrder



def purchase_detail(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    return render(request, 'purchase_order/purchase_detail.html', {'po': po})

def rf_ptl(request):
    return render(request, 'rf_pick_to_light/dashboard.html')
