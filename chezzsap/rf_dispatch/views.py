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
from .models import Truck


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
            elif 'checkin' in scan:
                instance.truck_status = 'checkin'
            elif 'gate' in scan:
                instance.truck_status = 'gate'
            elif 'checkout' in scan:
                instance.truck_status = 'checkout'
            else:
                instance.truck_status = 'not planned'
            instance.save()
            truck_no = request.POST.get('truck_no')
            driver_name = request.POST.get('driver_name')
            driver_phn_no = request.POST.get('driver_phn_no')

            if truck_no:
                try:
                    yard_instance = YardHdr.objects.filter(truck_no=truck_no).last()
                    if yard_instance and not Truck.objects.filter(truck_no=yard_instance).exists():
                        Truck.objects.create(
                            truck_no=yard_instance,
                            driver_name=driver_name,
                            driver_phn_no=driver_phn_no
                        )
                except YardHdr.DoesNotExist:
                    # This should never happen since YardHdr was just saved
                    print(f"YardHdr with truck_no {truck_no} does not exist.")

            # ✅ Redirect to truck_inspection_view with truck_no
            return redirect('truck_inspection', truck_no=instance.truck_no)

    else:
        form = YardHdrForm()
    warehouses = Warehouse.objects.all()
    
    return render(request, 'truck_screen/one.html', {'form': form, 'warehouses': warehouses, 'truck': Truck.objects.all()})




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


from django.http import JsonResponse
from .models import Truck

def get_truck_details(request):
    truck_no = request.GET.get('truck_no')
    try:
        truck = Truck.objects.get(truck_no=truck_no)
        data = {
            'driver_name': truck.driver_name,
            'driver_phn_no': truck.driver_phn_no
        }
    except Truck.DoesNotExist:
        data = {
            'driver_name': '',
            'driver_phn_no': ''
        }
    return JsonResponse(data)


from django.shortcuts import render, redirect
from .forms import TruckInspectionForm
from .models import Pallet, YardHdr, TruckLog
from .utils import log_truck_status  # create this helper

def truck_inspection_view(request, truck_no):
    try:
        existing_truck = YardHdr.objects.filter(truck_no=truck_no).last()

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
        'trucklog':TruckLog.objects.filter(truck_no__truck_no=truck_no).order_by('-truck_date', '-truck_time') if truck else None
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
        description = request.POST.get('description')
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
            whs_key = request.POST.get('whs_no')
            warehouse = Warehouse.objects.get(whs_no=whs_key)

            StockUpload.objects.create(
                whs_no=warehouse,
                product=product_instance,
                description=description,
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
                'warehouse': Warehouse.objects.all(),
                'success': True
            })

        except Exception as e:
            print("❌ Error during StockUpload creation:", e)
            products = Product.objects.all()
            
            return render(request, 'stock_upload/batch_product.html', {
                'products': products,
                'warehouse': Warehouse.objects.all(),
                'error': str(e)
            })

    # GET request
    products = Product.objects.all()
    warehouse = Warehouse.objects.all()
    return render(request, 'stock_upload/batch_product.html', {'products': products, 'warehouse': warehouse})


from django.http import JsonResponse
from .models import Product

def get_product_description(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        return JsonResponse({'description': product.description})
    except Product.DoesNotExist:
        return JsonResponse({'description': ''}, status=404)
 

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
        'query': query,
        'categories': Category.objects.all(),
    })


def product_detail_view(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    return render(request, 'product/product_detail.html', {'product': product})

# def get_category(request):
#     category = request.GET.get('category')
#     try:
#         product = Product.objects.get(name=category)
#         data = {
#             'category': product.category
#         }
#     except Product.DoesNotExist:
#         data = {
#             'category': '',
#         }
#     return JsonResponse(data)

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
# from .forms import  ProductForm
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

from django.http import JsonResponse
from .models import Product

def get_product_description(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        return JsonResponse({
            'description': product.description,
            'category': product.category
        })
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)


  
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
from .forms import CustomerForm
from .models import Customers
from.models import Vendor
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


from django.shortcuts import render, redirect
from .models import Vendor  # make sure you import the model


# def add_vendor(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         vendor_code = request.POST.get('vendor_code') 
#         email = request.POST.get('email')
#         phone_no = request.POST.get('phone_no')
#         address = request.POST.get('address')
#         location = request.POST.get('location')
#         profile_image = request.FILES.get('profile_image')  

#         new_vendor = Vendor(
#             name=name,
#             vendor_code=vendor_code,
#             email=email,
#             phone_no=phone_no,
#             address=address,
#             location=location,
#             profile_image=profile_image
#         )
#         new_vendor.save()

#         return redirect('vendor_detail', vendor_id=new_vendor.id)

#     return render(request, 'vendor/add_vendor.html')
  

from django.shortcuts import render, redirect, get_object_or_404
from .forms import PurchaseOrderForm
from .models import PurchaseOrder
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from .models import PurchaseOrder
from django.urls import reverse

from django.shortcuts import render, redirect
from decimal import Decimal, InvalidOperation
from .models import PurchaseOrder

def add_purchase(request):
    if request.method == 'POST':
        try:
            # Get POST values
            company_name = request.POST.get('company_name', '').strip()
            company_address = request.POST.get('company_address', '').strip()
            phone = request.POST.get('phone', '').strip()
            email = request.POST.get('email', '').strip()
            website = request.POST.get('website', '').strip()
            po_date = request.POST.get('po_date', '').strip()
            po_number = request.POST.get('po_number', '').strip()
            customer_number = request.POST.get('customer_number', '').strip()
            vendor_company_name = request.POST.get('vendor_company_name', '').strip()
            contact_name = request.POST.get('contact_name', '').strip()
            vendor_phone = request.POST.get('vendor_phone', '').strip()
            vendor_address = request.POST.get('vendor_address', '').strip()
            vendor_email = request.POST.get('vendor_email', '').strip()
            vendor_website = request.POST.get('vendor_website', '').strip()
            # ship_to_name = request.POST.get('ship_to_name', '').strip()
            # ship_to_company_name = request.POST.get('ship_to_company_name', '').strip()
            # ship_to_address = request.POST.get('ship_to_address', '').strip()
            # ship_to_phone = request.POST.get('ship_to_phone', '').strip()
            # ship_to_email = request.POST.get('ship_to_email', '').strip()
            # ship_to_website = request.POST.get('ship_to_website', '').strip()
            item_number = request.POST.get('item_number', '').strip()
            product_name = request.POST.get('product_name', '').strip()
            quantity = request.POST.get('quantity', '').strip()
            unit_price = request.POST.get('unit_price', '').strip()

            # Validate required fields
            if not all([company_name, po_number, product_name, quantity, unit_price]):
                raise ValueError("Missing required fields")

            # Convert quantity and unit_price
            try:
                quantity = int(quantity)
            except ValueError:
                raise ValueError("Quantity must be an integer")

            try:
                unit_price = Decimal(unit_price)
            except InvalidOperation:
                raise ValueError("Unit price must be a valid decimal number")

            # Calculate total
            total_price = quantity * unit_price

            # Save to DB
            purchase_order = PurchaseOrder.objects.create(
                company_name=company_name,
                company_address=company_address,
                phone=phone,
                email=email,
                website=website,
                po_date=po_date,
                po_number=po_number,
                customer_number=customer_number,
                vendor_company_name=vendor_company_name,
                contact_name=contact_name,
                vendor_phone=vendor_phone,
                vendor_address=vendor_address,
                vendor_email=vendor_email,
                vendor_website=vendor_website,
                # ship_to_name=ship_to_name,
                # ship_to_company_name=ship_to_company_name,
                # ship_to_address=ship_to_address,
                # ship_to_phone=ship_to_phone,
                # ship_to_email=ship_to_email,
                # ship_to_website=ship_to_website,
                item_number=item_number,
                product_name=product_name,
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price
            )

            return redirect('purchase_order_detail', pk=purchase_order.pk)

        except ValueError as ve:
            return render(request, 'purchase_order/add_purchase.html', {
                'error': str(ve),
                'data': request.POST
            })

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
    
# views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from .models import PurchaseOrder  # Replace with your actual model

def download_po_pdf(request, pk):  # <-- Accept `pk` here
    po = get_object_or_404(PurchaseOrder, pk=pk)
    html_string = render_to_string('purchase_order/purchase_order_pdf.html', {'po': po})

    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="purchase_order_{pk}.pdf"'
    return response



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import PurchaseOrder
from .forms import PurchaseOrderForm

# def purchase_edit(request, po_id):
#     # Get the existing PurchaseOrder or return 404
#     po = get_object_or_404(PurchaseOrder, id=po_id)

#     if request.method == 'POST':
#         form = PurchaseOrderForm(request.POST, request.FILES, instance=po)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Purchase order updated successfully.")
#             return redirect('purchase_detail')  # Change this if needed
#     else:
#         form = PurchaseOrderForm(instance=po) 

#     return render(request, 'purchase_order/purchase_edit.html', {
#         'form': form, 
#         'po': po,
#     })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import PurchaseOrder

def purchase_edit(request, po_id):
    po = get_object_or_404(PurchaseOrder, id=po_id)

    if request.method == 'POST':
        # Update all fields manually
        po.company_name = request.POST.get('company_name')
        po.company_address = request.POST.get('company_address')
        po.company_phone = request.POST.get('company_phone')
        po.company_email = request.POST.get('company_email')
        po.company_website = request.POST.get('company_website')

        po.po_date = request.POST.get('po_date')
        po.po_number = request.POST.get('po_number')
        po.customer_number = request.POST.get('customer_number')

        po.vendor_company_name = request.POST.get('vendor_company_name')
        po.vendor_contact_name = request.POST.get('vendor_contact_name')
        po.vendor_phone = request.POST.get('vendor_phone')
        po.vendor_address = request.POST.get('vendor_address')
        po.vendor_email = request.POST.get('vendor_email')
        po.vendor_website = request.POST.get('vendor_website')

        # po.ship_to_name = request.POST.get('ship_to_name')
        # po.ship_to_company_name = request.POST.get('ship_to_company_name')
        # po.ship_to_address = request.POST.get('ship_to_address')
        # po.ship_to_phone = request.POST.get('ship_to_phone')
        # po.ship_to_email = request.POST.get('ship_to_email')
        # po.ship_to_website = request.POST.get('ship_to_website')

        po.item_number = request.POST.get('item_number')
        po.product_name = request.POST.get('product_name')
        po.product_quantity = request.POST.get('product_quantity')
        po.unit_price = request.POST.get('unit_price')
        po.total_price = request.POST.get('total_price')

        po.save()
        messages.success(request, "Purchase order updated successfully.")
        return redirect('purchase_detail', pk=po.id)

    return render(request, 'purchase_order/purchase_edit.html', {'po': po})


def rf_ptl(request):
    return render(request, 'rf_pick_to_light/dashboard.html')

from django.shortcuts import render, redirect
from .models import Bin

from django.shortcuts import render, redirect
from .models import Bin, Warehouse

# def create_bin(request):
#     if request.method == 'POST':
#         try:
#             whs_no_input = request.POST.get('whs_no')
#             bin_id = request.POST.get('bin_id')
#             capacity = request.POST.get('capacity')
#             category = request.POST.get('category')
#             product = request.POST.get('product')
#             existing_quantity = request.POST.get('existing_quantity')
#             updated_by = request.POST.get('updated_by')
#             created_by = request.POST.get('created_by')

#             # Validate and get Warehouse object
#             try:
#                 warehouse = Warehouse.objects.get(whs_no=whs_no_input)
#             except Warehouse.DoesNotExist:
#                 return render(request, 'bin/create_bin.html', {'error': f"Warehouse {whs_no_input} does not exist."})

#             # Save Bin
#             Bin.objects.create(
#                 whs_no=warehouse,
#                 bin_id=bin_id,
#                 capacity=int(capacity),
#                 category=category,
#                 products=product,
#                 existing_quantity=int(existing_quantity),
#                 updated_by=updated_by,
#                 created_by=created_by
#             )

#             return redirect('create_bin')  # Replace with your actual success URL name

#         except Exception as e:
#             return render(request, 'bin/create_bin.html', {'error': str(e)})

#     return render(request, 'bin/create_bin.html')

# from .models import Warehouse



from django.shortcuts import render, redirect
from .models import Bin, Warehouse, Category

def create_bin(request):
    if request.method == 'POST':
        try:
            whs_key = request.POST.get('whs_no')
            warehouse = Warehouse.objects.get(whs_no=whs_key)

            category = Category.objects.get(id=request.POST.get('category'))

            Bin.objects.create(
                whs_no=warehouse,
                bin_id=request.POST.get('bin_id'),
                capacity=int(request.POST.get('capacity')),
                category=category,
                
                shelves=request.POST.get('shelves'),
                updated_by=request.POST.get('updated_by'),
                created_by=request.POST.get('created_by')
            )

            return redirect('create_bin')

        except Exception as e:
            return render(request, 'bin/create_bin.html', {
                'error': str(e),
                'warehouse': Warehouse.objects.all(),
                'bins': Bin.objects.all(),
                'categories': Category.objects.all(),  # ✅ add this line
            })

    # For GET request
    return render(request, 'bin/create_bin.html', {
        'warehouse': Warehouse.objects.all(),
        'bins': Bin.objects.all(),
        'categories': Category.objects.all(),  # ✅ add this line
    })


def task(request):
    return render(request, 'rf_pick_to_light/task_solving.html')


from django.http import JsonResponse
from .models import Category
import json

from django.shortcuts import render, redirect
from .forms import CategoryForm
from .models import Category

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_bin')  # Redirect to the main form page
    else:
        form = CategoryForm()
    categories = Category.objects.all()
    return render(request, 'bin/create_bin.html', {
        'categories': categories,
        'category_form': form,
    })


# def vendor_detail(request, vendor_id):  
#     vendor = get_object_or_404(Vendor, id=vendor_id)
#     return render(request, 'vendor/vendor_detail.html', {'vendor': vendor})

# def vendor_edit(request, vendor_id):
#     Vendor = get_object_or_404(Vendor, id=vendor_id)

# def vendor_list(request):
#     vendors = Vendor.objects.all()
#     return render(request, 'vendor/vendor_list.html', {'vendors': vendors})


from django.shortcuts import render, redirect
from .models import Vendor

def add_vendor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        vendor_code = request.POST.get('vendor_code')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        address = request.POST.get('address')
        
        profile_image = request.FILES.get('profile_image')

        vendor = Vendor(
            name=name,
            vendor_code=vendor_code,
            email=email,
            phone_no=phone_no,
            address=address,
            
            profile_image=profile_image
        )
        vendor.save()

        return redirect('vendor_detail', vendor_id=vendor.vendor_id)  # or any success page
    return render(request, 'vendor/add_vendor.html')

from django.shortcuts import render, get_object_or_404
from .models import Vendor

def vendor_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, vendor_id=vendor_id)
    return render(request, 'vendor/vendor_detail.html', {'vendor': vendor})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Vendor
from .forms import Vendorform  # Assuming you have a form named VendorForm

from django.shortcuts import render, get_object_or_404, redirect
from .models import Vendor

def vendor_edit(request, vendor_id):
    vendor = get_object_or_404(Vendor, vendor_id=vendor_id)

def edit_putaway(request, putaway_id):
    putaway = get_object_or_404(Putaway, putaway_id=putaway_id)

    if request.method == 'POST':
        vendor.name = request.POST.get('name')
        vendor.vendor_code = request.POST.get('vendor_code')
        vendor.email = request.POST.get('email')
        vendor.phone_no = request.POST.get('phone_no')
        vendor.address = request.POST.get('address')
        
        vendor.save()
        return redirect('vendor_detail', vendor_id=vendor.vendor_id)

    return render(request, 'vendor/vendor_edit.html', {'vendor': vendor})



def confirm_putaway(request, putaway_id):
    putaway = get_object_or_404(Putaway, putaway_id=putaway_id)
    putaway.status = "Completed"
    putaway.is_confirmed = True
    putaway.save()
    return redirect('putaway_pending')

def delete_putaway(request,putaway_id):
    task = get_object_or_404(Putaway, putaway_id=putaway_id)
    task.delete()
    messages.success(request, "Task deleted successfully.")
    return redirect('putaway_pending')\
  
from django.shortcuts import render
from .models import Vendor

def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor/vendor_list.html', {'vendors': vendors})


from django.shortcuts import get_object_or_404, redirect
from .models import Vendor

def vendor_delete(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    vendor.delete()
    return redirect('vendor_list')


from .models import Warehouse  # replace with your warehouse model name

def whs_suggestions(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        warehouses = Warehouse.objects.filter(whs_no__icontains=query)[:10]
        results = [{'whs_no': w.whs_no} for w in warehouses]

    return JsonResponse({'results': results})

from django.http import JsonResponse
from .models import Truck  # or your truck model

def truck_suggestions(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        trucks = Truck.objects.filter(truck_no__icontains=query)[:10]
        results = [{'truck_no': t.truck_no} for t in trucks]

    return JsonResponse({'results': results})

from django.http import JsonResponse
from .models import Product  # Adjust import to match your app

def product_suggestions(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        products = Product.objects.filter(
            product_id__icontains=query
        )[:10]  # Limit to top 10 matches

        for p in products:
            results.append({
                'product_id': p.product_id,
                'name': p.name,
                'description': p.description,
                'category': p.category,
            })

    return JsonResponse({'results': results})

from django.http import JsonResponse
from .models import Warehouse  # Replace with your actual model

def whs_suggestions(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        whs_list = Warehouse.objects.filter(whs_no__icontains=query).values_list('whs_no', flat=True).distinct()[:10]
        results = [{'whs_no': wh} for wh in whs_list]

    return JsonResponse({'results': results})

from django.http import JsonResponse
from .models import Category  # Adjust based on your model

def category_suggestions(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        cats = Category.objects.filter(category__icontains=query).values_list('category', flat=True).distinct()[:10]
        results = [{'category': cat} for cat in cats]

    return JsonResponse({'results': results})

from django.shortcuts import render, redirect
from .models import Picking
from .forms import PickingForm

def add_picking(request):
    if request.method == 'POST':
       
        picking_id = request.POST.get('picking_id')
        pallet = request.POST.get('pallet')
        # created_by = request.POST.get('created_by')
        location = request.POST.get('location')
        product = request.POST.get('product')
        quantity = request.POST.get('quantity')
        status = request.POST.get('status')

     
        Picking.objects.create(
            picking_id=picking_id,
            pallet=pallet,
            # created_by=created_by,
            location=location,
            product=product,
            quantity=quantity,
            status=status
        )
     
        return redirect('pending_task') 
    return render(request, 'picking/add_picking.html')

    
def pending_task(request):
    pending_picking = Picking.objects.filter(status__iexact='In Progress').order_by('picking_id')
    # pending_picking=Picking.objects.all()
    return render(request, 'picking/picking_pending_task.html', {'pending_picking': pending_picking})


# def edit_picking(request, picking_id): 
#     picking = get_object_or_404(Picking, picking_id=picking_id)
#     if request.method == 'POST':
#         form = PickingForm(request.POST, instance=picking)
#         if form.is_valid():
#             form.save()
#             return redirect('pending_task')  
#     else:
#         form = PickingForm(instance=picking)

#     return render(request, 'picking/add_picking.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Picking
from .forms import PickingForm

def edit_picking(request, picking_id):
    picking = get_object_or_404(Picking, picking_id=picking_id)
    if request.method == 'POST':
        form = PickingForm(request.POST, instance=picking)
        if form.is_valid():
            form.save()
            return redirect('pending_task', picking_id=picking.picking_id)  # or your listing page
    else:
        form = PickingForm(instance=picking)

    return render(request, 'picking/edit_picking.html', {'form': form, 'picking': picking})

def confirm_picking(request, picking_id):
    picking = get_object_or_404(Picking, picking_id=picking_id)
    picking.status = 'Completed'
    picking.save()
    return redirect('customer')  # Redirect to the customer page



def delete_picking(request, picking_id):
    picking = get_object_or_404(Picking, picking_id=picking_id)
    picking.delete()
    return redirect('pending_task') 

def customer(request):
    products = Product.objects.all()  # Assuming a Product model
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pending_task')
    else:
        form = CustomerForm()
    return render(request, 'picking/customer.html', {'form': form, 'products': products})
