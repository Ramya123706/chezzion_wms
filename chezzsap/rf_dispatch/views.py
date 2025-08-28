import uuid
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
def stock_upload_login(request):
    return render(request, 'stock_upload/login_in_RFUI.html')
def stock_menu(request):
    return render(request, 'stock_upload/stock_menu.html')
def task(request):
    return render(request, 'rf_pick_to_light/task_solving.html')

# -------------------------------------
# TRUCK CHECKIN/CHECKOUT AND INSPECTION
# -------------------------------------

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
                    print(f"YardHdr with truck_no {truck_no} does not exist.")

            return redirect('truck_inspection', truck_no=instance.truck_no)

    else:
        form = YardHdrForm()
    warehouses = Warehouse.objects.all()
    
    return render(request, 'truck_screen/one.html', {'form': form, 'warehouses': warehouses, 'truck': Truck.objects.all()})

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
from .utils import log_truck_status 

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


def truck_list(request):
    query = request.GET.get('search')
    if query:
        trucks = YardHdr.objects.filter(truck_no__icontains=query)
    else:
        trucks = YardHdr.objects.all()

    return render(request, 'truck_screen/truck_list.html', {'trucks': trucks, 'query': query})


from .models import YardHdr, TruckLog
from .utils import log_truck_status  

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

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import YardHdr
from .utils import log_truck_status  

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

# ------------
# STOCK UPLOAD
# -------------
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, StockUpload

def batch_product_view(request):
    if request.method == 'POST':
        whs_no = request.POST.get('whs_no')
        product_id = request.POST.get('product')  
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        batch = request.POST.get('batch')
        bin = request.POST.get('bin')
        pallet = request.POST.get('pallet')
        p_mat = request.POST.get('p_mat')
        inspection = request.POST.get('inspection')
        stock_type = request.POST.get('stock_type')
        wps = request.POST.get('wps')
        doc_no = request.POST.get('doc_no')
        pallet_status = request.POST.get('pallet_status')

        try:
            product_instance = get_object_or_404(Product, product_id__iexact=product_id)

            whs_key = request.POST.get('whs_no')
            warehouse = Warehouse.objects.get(whs_no=whs_key)
            bin_instance = get_object_or_404(Bin, id=bin)
            StockUpload.objects.create(
                whs_no=warehouse,
                product=product_instance,
                description=description,
                quantity=int(quantity),
                batch=batch,
                bin=bin_instance,
                pallet=pallet,
                p_mat=p_mat,
                inspection=inspection,
                stock_type=stock_type,
                wps=wps,
                doc_no=doc_no,
                pallet_status=pallet_status
            )

            products = Product.objects.all()
            
            return render(request, 'stock_upload/batch_product.html', {
                'products': products,
                'warehouse': Warehouse.objects.all(),
                'bins': Bin.objects.all(),
                'success': True
            })

        except Exception as e:
            print("❌ Error during StockUpload creation:", e)
            products = Product.objects.all()
            
            return render(request, 'stock_upload/batch_product.html', {
                'products': products,
                'warehouse': Warehouse.objects.all(),
                'bins': Bin.objects.all(),
                'error': str(e),
                
            })

    products = Product.objects.all()
    warehouse = Warehouse.objects.all()
    bins = Bin.objects.all()
    return render(request, 'stock_upload/batch_product.html', {'products': products, 'warehouse': warehouse, 'bins': bins})


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

# -----------
# WAREHOUSE
# -----------

from django.shortcuts import render, redirect
from .models import Warehouse
from .forms import WarehouseForm

def warehouse_view(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST, request.FILES)
        if form.is_valid():
            warehouse = form.save()
            return redirect('warehouse_detail', whs_no=warehouse.whs_no) 
    else:
        form = WarehouseForm()

    # === SEARCH + TABLE (Right Side) ===
    query = request.GET.get('search')
    if query:
        warehouses = Warehouse.objects.filter(whs_no__icontains=query)
    else:
        warehouses = Warehouse.objects.all() 

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

def edit_warehouse(request, whs_no):
    warehouse = get_object_or_404(Warehouse, whs_no=whs_no)

    if request.method == 'POST':
        form = WarehouseForm(request.POST, request.FILES, instance=warehouse)
        if form.is_valid():
            form.save()
            return redirect('warehouse_view')  
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

def product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('product_detail', product_id=product.product_id)
        else:
            print("❌ Form errors:", form.errors) 
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
    product = get_object_or_404(
        Product.objects.prefetch_related(
            "purchaseitem_set__purchase_order"  
        ),
        product_id__iexact=product_id
    )
    return render(request, "product/product_detail.html", {"product": product})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.utils import timezone

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        product_id = request.POST.get('id')
        quantity = request.POST.get('quantity')
        pallet_no = request.POST.get('pallet_no')
        sku = request.POST.get('sku')
        description = request.POST.get('description')
        unit_of_measure = request.POST.get('unit_of_measure')
        category = request.POST.get('category')
        re_order_level = request.POST.get('re_order_level')
        images = request.FILES.get('images')

        try:
            product = Product.objects.create(
                product_id=product_id,
                name=name,
                quantity=quantity,
                pallet_no=pallet_no,
                sku=sku,
                description=description,
                unit_of_measure=unit_of_measure,
                category=category,
                re_order_level=re_order_level,
                unit_price=unit_price,
                images=images,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            return redirect('product_detail', product_id=product.product_id)
        except Exception as e:
            return render(request, 'product/add_product.html', {'error': str(e)})

    return render(request, 'product/add_product.html')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import ProductForm
from .models import Product
from .models import Category

def product_edit(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.quantity = request.POST.get('quantity')
        product.unit_price = request.POST.get('unit_price')
        product.pallet_no = request.POST.get('pallet_no')
        product.sku = request.POST.get('sku')
        product.description = request.POST.get('description')
        product.unit_of_measure = request.POST.get('unit_of_measure')
        product.re_order_level = request.POST.get('re_order_level')

        category_id = request.POST.get('category')
        if category_id:
            try:
                product.category_id = int(category_id)
            except ValueError:
                pass  

        if request.FILES.get('images'):
            product.images = request.FILES['images']

        product.save()
        messages.success(request, "✅ Product updated successfully.")
        return redirect('product_detail', product_id=product.product_id)

    return render(request, 'product/product_edit.html', {
        'product': product,
        'categories': categories
    })


    
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


def product_delete(request, product_id):

    product = get_object_or_404(Product, product_id=product_id)
    product.delete()
    return redirect('product_list') 

# --------
# INVENTORY
# --------
from .models import Inventory

def inventory_view(request):
    inventory = Inventory.objects.select_related('product').all()
    return render(request, 'inventory/inventory_list.html', {'inventory': inventory})

   
# .........
# CUSTOMERS
# .........
from .forms import CustomerForm
from .models import Customers
from.models import Vendor
from django.utils import timezone
from django.contrib import messages

def add_customers(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        customer_id= request.POST.get('customer_id')
        customer_code = request.POST.get('customer_code')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        address = request.POST.get('address')
        location = request.POST.get('location')

        try:
            customer = Customers.objects.create(
                name=name,
                customer_id=customer_id,
                customer_code=customer_code,
                email=email,
                phone_no=phone_no,
                address=address,
                location=location,
                )
            return redirect('customers_detail', customer_id=customer.customer_id)
        except Exception as e:
            return render(request, 'customers/add_customers.html', {'error': str(e)})

    return render(request, 'customers/add_customers.html')

def customers_detail(request, customer_id):  
    customer = get_object_or_404(Customers, customer_id=customer_id)
    return render(request, 'customers/customers_detail.html', {'customer': customer})

def customers_edit(request, customer_id):
    customer = get_object_or_404(Customers, customer_id=customer_id)

    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.customer_id = request.POST.get('customer_id')
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

def customers_delete(request, customer_id):
    customer = get_object_or_404(Customers, customer_id=customer_id)
    if request.method == 'POST':
        customer.delete()
        return redirect('customers_list') 

from .models import Warehouse

def whs_no_dropdown_view(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'stock_upload/batch_product.html', {'warehouses': warehouses})

# -----
# PALLET
# ------
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import transaction
from .forms import PalletForm
from .models import Pallet
from django.shortcuts import render, get_object_or_404

def creating_pallet(request):
    if request.method == 'POST':
        form = PalletForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                
                pallet = form.save(commit=False)
                pallet.created_by = str(request.user)
                pallet.updated_by = str(request.user)
                pallet.created_at = timezone.now()
                pallet.save()

                
                has_children = form.cleaned_data.get('has_child_pallets')
                num_children = form.cleaned_data.get('number_of_children') or 0

               
                if has_children and not pallet.parent_pallet and num_children > 0:
                    for _ in range(num_children):
                        child = Pallet(
                            parent_pallet=pallet,
                            product=pallet.product,
                            p_mat=pallet.p_mat,
                            quantity=0, 
                            weight=None,
                            created_at=pallet.created_at,
                            created_by=pallet.created_by,
                            updated_by=pallet.updated_by,
                        )
                        child.save()

            return redirect('creating_pallet')
    else:
        form = PalletForm()

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

def pallet_detail(request, pallet_no):
    pallet = get_object_or_404(Pallet, pallet_no=pallet_no)
    # Get children pallets (if any)
    child_pallets = Pallet.objects.filter(parent_pallet=pallet)
    return render(request, 'pallet/pallet_detail.html', {
        'pallet': pallet,
        'child_pallets': child_pallets
    })

def pallet_search(request, pallet_no):
    pallet = get_object_or_404(Pallet, pallet_no=pallet_no)
    return render(request, 'pallet/pallet_search_details.html', {'pallet': pallet})

def edit_pallet(request, pallet_no):
    pallet = get_object_or_404(Pallet, pallet_no=pallet_no)

    if request.method == 'POST':
        form = PalletForm(request.POST, request.FILES, instance=pallet)
        if form.is_valid():
            form.save()
            return redirect('creating_pallet', pallet_no=pallet.pallet_no)
    else:
        form = PalletForm(instance=pallet)

    return render(request, 'pallet/Pallet_edit.html', {'form': form, 'pallet': pallet})

def delete_pallet(request, pallet_no):
    pallet = get_object_or_404(Pallet, pallet_no=pallet_no)
    pallet.delete()
    messages.success(request, "Pallet deleted successfully.")
    return redirect('creating_pallet')

from django.shortcuts import render, redirect, get_object_or_404
from .forms import PurchaseOrderForm
from .models import PurchaseOrder, PurchaseItem
from decimal import Decimal

# --------------------
# PURCHASE ORDER
# -------------------

def add_purchase(request):
    if request.method == 'POST':
        try:
           
            po = PurchaseOrder.objects.create(
                company_name=request.POST.get('company_name'),
                company_address=request.POST.get('company_address'),
                company_phone=request.POST.get('company_phone'),
                company_email=request.POST.get('company_email'),
                company_website=request.POST.get('company_website'),
                po_date=request.POST.get('po_date'),
                po_number=request.POST.get('po_number'),
                customer_number=request.POST.get('customer_number'),
                vendor_company_name=request.POST.get('vendor_company_name'),
                vendor_contact_name=request.POST.get('vendor_contact_name'),
                vendor_phone=request.POST.get('vendor_phone'),
                vendor_address=request.POST.get('vendor_address'),
                vendor_website=request.POST.get('vendor_website'),
                vendor_email=request.POST.get('vendor_email'),
            )

            
            item_numbers = request.POST.getlist('item_number[]')
            product_names = request.POST.getlist('product_name[]')
            quantities = request.POST.getlist('quantity[]')
            unit_prices = request.POST.getlist('unit_price[]')

            for i in range(len(item_numbers)):
                item_number = (item_numbers[i] or '').strip()
                product_name = (product_names[i] or '').strip()
                quantity_raw = (quantities[i] or '').strip()
                unit_price_raw = (unit_prices[i] or '').strip()

                # ⚠️ Skip if row is incomplete
                if not item_number or not product_name or not quantity_raw or not unit_price_raw:
                    continue

                try:
                    quantity = int(quantity_raw)
                    unit_price = Decimal(unit_price_raw)
                except (ValueError, TypeError):
                    continue  # skip invalid rows

                
                product, created = Product.objects.get_or_create(
                    product_id=item_number,
                    defaults={
                        'name': product_name,
                        'quantity': 0,  
                        'pallet_no': f"PALLET-{item_number}",
                        'sku': f"SKU-{item_number}",
                        'description': product_name,
                        'unit_of_measure': "pcs",
                        're_order_level': 10,   
                    }
                )

               
                product.quantity += quantity
                product.save()   

                
                PurchaseItem.objects.create(
                    purchase_order=po,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=quantity * unit_price
                )

            return redirect('purchase_detail', pk=po.pk)

        except Exception as e:
            return render(request, 'purchase_order/add_purchase.html', {
                'error': str(e),
                'data': request.POST
            })

    return render(request, 'purchase_order/add_purchase.html')

def purchase_detail(request, pk):
    po = PurchaseOrder.objects.get(pk=pk)
    return render(request, "purchase_order/purchase_detail.html", {"po": po})

from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string


def download_po_pdf(request, pk): 
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

def purchase_edit(request, po_number):
    po = get_object_or_404(PurchaseOrder, po_number=po_number)

    if request.method == 'POST':
        
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

# -----------------
# BIN
# -----------------

from django.shortcuts import render, redirect
from .models import Bin, Warehouse, Category
from django.http import JsonResponse
from .forms import CategoryForm


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
                'categories': Category.objects.all(), 
            })

    return render(request, 'bin/create_bin.html', {
        'warehouse': Warehouse.objects.all(),
        'bins': Bin.objects.all(),
        'categories': Category.objects.all(), 
    })

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_bin')  
    else:
        form = CategoryForm()
    categories = Category.objects.all()
    return render(request, 'bin/create_bin.html', {
        'categories': categories,
        'category_form': form,
    })

# -----------------
# VENDOR
# -----------------

from django.shortcuts import render, redirect
from .models import Vendor
from django.shortcuts import render, redirect, get_object_or_404
from .forms import VendorForm

def add_vendor(request, vendor_id=None):
    vendor = None
    if vendor_id:
        vendor = get_object_or_404(Vendor, vendor_id=vendor_id)

    form = VendorForm(request.POST or None, request.FILES or None, instance=vendor)

    if request.method == 'POST' and form.is_valid():
        saved_vendor = form.save()
        return redirect('vendor_detail', vendor_id=saved_vendor.vendor_id)

    
    search_query = request.GET.get('search', '')
    vendors = Vendor.objects.filter(vendor_id__icontains=search_query) if search_query else Vendor.objects.none()

    context = {
        'form': form,
        'vendors': vendors,
        'vendor':vendor,
    }
    return render(request, 'vendor/add_vendor.html', context)

def vendor_list(request):
    search_query = request.GET.get('search')
    if search_query:
        vendors = Vendor.objects.filter(vendor_id__icontains=search_query)
    else:
        vendors = Vendor.objects.all()

    return render(request, 'vendor/vendor_list.html', {'vendors': vendors})

def vendor_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, vendor_id=vendor_id)
    return render(request, 'vendor/vendor_detail.html', {'vendor': vendor})

def vendor_edit(request, vendor_id):
    vendor = get_object_or_404(Vendor, vendor_id=vendor_id)
    if request.method == 'POST':
        vendor.name = request.POST.get('name')
        vendor.vendor_code = request.POST.get('vendor_code')
        vendor.email = request.POST.get('email')
        vendor.phone_no = request.POST.get('phone_no')
        vendor.address = request.POST.get('address')
        if request.FILES.get('profile_image'):
            vendor.profile_image = request.FILES.get('profile_image')
        vendor.save()
        return redirect('vendor_list')
    return render(request, 'vendor/vendor_edit.html', {'vendor': vendor})

def vendor_delete(request, vendor_id):
    vendor = get_object_or_404(Vendor, vendor_id=vendor_id)
    vendor.delete()
    messages.success(request, f"Vendor {vendor.name} deleted successfully.")
    return redirect('vendor_list')

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


# ----------------
# PUTAWAY
# ----------------

from django.shortcuts import render, get_object_or_404
from .models import Putaway 
from django.shortcuts import render, redirect


def putaway_task(request):
    if request.method == 'POST':
     
        putaway_id = request.POST.get('putaway_id')
        pallet = request.POST.get('pallet')
        location = request.POST.get('location')
        putaway_task_type = request.POST.get('putaway_task_type')
        status = request.POST.get('status')
        putaway = Putaway(
            putaway_id=putaway_id,
            pallet=pallet,
            location=location,
            status = status,
            putaway_task_type=putaway_task_type
            
        )
        putaway.save()

        return redirect('putaway_pending')

    return render(request, 'putaway/putaway_task.html')
    
def putaway_pending(request):
    pending_tasks = Putaway.objects.filter(status__iexact='In Progress').order_by('putaway_id')
    return render(request, 'putaway/pending_task.html', {'pending_tasks': pending_tasks})

def edit_putaway(request, putaway_id):
    putaway = get_object_or_404(Putaway, putaway_id=putaway_id)  # or use putaway_id=putaway_id if field is unique

    if request.method == 'POST':
        putaway.putaway_id = request.POST.get('putaway_id')
        putaway.pallet = request.POST.get('pallet')
        putaway.location = request.POST.get('location')
        putaway.putaway_task_type = request.POST.get('putaway_task_type')
        putaway.status = request.POST.get('status')

        putaway.save()
        return redirect('putaway_pending')  # go back to pending list

    return render(request, 'putaway/edit_putaway.html', {'putaway': putaway})

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
    return redirect('putaway_pending')


from .models import Warehouse 

def whs_suggestions(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        warehouses = Warehouse.objects.filter(whs_no__icontains=query)[:10]
        results = [{'whs_no': w.whs_no} for w in warehouses]

    return JsonResponse({'results': results})

from django.http import JsonResponse
from .models import Truck 

def truck_suggestions(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        trucks = Truck.objects.filter(truck_no__icontains=query)[:10]
        results = [{'truck_no': t.truck_no} for t in trucks]

    return JsonResponse({'results': results})

from django.http import JsonResponse
from .models import Product

def product_suggestions(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return JsonResponse({'results': []})

    products = Product.objects.filter(
        name__icontains=query
    ).values(
        'product_id',   
        'name',
        'description',
        'category'
    )[:10]  

    return JsonResponse({'results': list(products)})


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
from .models import Category  

def category_suggestions(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        cats = Category.objects.filter(category__icontains=query).values_list('category', flat=True).distinct()[:10]
        results = [{'category': cat} for cat in cats]

    return JsonResponse({'results': results})

# ------------------
# PICKING
# -----------------

from django.shortcuts import render, redirect
from .models import Picking
from .forms import PickingForm

def add_picking(request):
    if request.method == 'POST':
       
        picking_id = request.POST.get('picking_id')
        pallet = request.POST.get('pallet')
        location = request.POST.get('location')
        product = request.POST.get('product')
        quantity = request.POST.get('quantity')
        status = request.POST.get('status')

     
        Picking.objects.create(
            picking_id=picking_id,
            pallet=pallet,
            location=location,
            product=product,
            quantity=quantity,
            status=status
        )
     
        return redirect('pending_task') 
    return render(request, 'picking/add_picking.html')

    
def pending_task(request):
    pending_picking = Picking.objects.filter(status__iexact='In Progress').order_by('picking_id')
    return render(request, 'picking/picking_pending_task.html', {'pending_picking': pending_picking})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Picking
from .forms import PickingForm

def edit_picking(request, picking_id):
    picking = get_object_or_404(Picking, picking_id=picking_id)
    if request.method == 'POST':
        form = PickingForm(request.POST, instance=picking)
        if form.is_valid():
            form.save()
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

# -------------
# INBOUND DELIVERY
# -------------

from django.shortcuts import render,get_object_or_404, redirect
from django.contrib import messages
from .models import InboundDelivery, InboundDeliveryproduct, Warehouse , Vendor , PurchaseOrder
import random

def generate_inbound_delivery_number():
    return f"IBD{random.randint(1000, 9999)}"

def generate_inbound_delivery_number():
    return f"IBD{random.randint(1000, 9999)}"

def inbound_delivery(request):
    
    search_term = request.GET.get('inbound_delivery_number')
    if search_term:
        deliveries = InboundDelivery.objects.filter(
            inbound_delivery_number__icontains=search_term
        ).order_by('-delivery_date')
    else:
        deliveries = InboundDelivery.objects.all().order_by('-delivery_date')

    warehouses = Warehouse.objects.all().order_by('whs_no')
    vendors = Vendor.objects.all()
    purchase_orders = PurchaseOrder.objects.all()
    products_list = Product.objects.all().order_by('name')  

    if request.method == 'POST':
        inbound_delivery_number = generate_inbound_delivery_number()
        vendor_id = request.POST.get('vendor')
        vendor_obj = Vendor.objects.get(pk=vendor_id)
        delivery = InboundDelivery.objects.create(
            inbound_delivery_number=inbound_delivery_number,
            delivery_date=request.POST.get('delivery_date'),
            document_date=request.POST.get('document_date'),
            gr_date=request.POST.get('gr_date'),
            vendor=vendor_obj,
            purchase_order_number_id=request.POST.get('po_number'),
            whs_no_id=request.POST.get('whs_no'),
            storage_location=request.POST.get('storage_location'),
            delivery_status=request.POST.get('delivery_status'),
            carrier_info=request.POST.get('carrier_info'),
            remarks=request.POST.get('remarks')
        )

        product_ids = request.POST.getlist('product[]') 
        descriptions = request.POST.getlist('product_description[]')
        qty_delivered = request.POST.getlist('quantity_delivered[]')
        qty_received = request.POST.getlist('quantity_received[]')
        unit_of_measure = request.POST.getlist('unit_of_measure[]')
        batch_number = request.POST.getlist('batch_number[]')

        for i in range(len(product_ids)):
            if product_ids[i].strip():
                product_obj = Product.objects.get(pk=product_ids[i])
                InboundDeliveryproduct.objects.create(
                    delivery=delivery,
                    product=product_obj,
                    quantity_delivered=int(qty_delivered[i]) if qty_delivered[i] else 0,
                    quantity_received=int(qty_received[i]) if qty_received[i] else 0,
                    unit_of_measure=unit_of_measure[i],
                    batch_number=batch_number[i] if batch_number[i] else str(uuid.uuid4())[:8]
                )

        return redirect('inbound_delivery')

    return render(request, 'inbound/inbound_delivery.html', {
        'deliveries': deliveries,
        'warehouses': warehouses,
        'vendors': vendors,
        'purchase_orders': purchase_orders,
        'products': products_list
    })


from django.shortcuts import render, get_object_or_404
from .models import InboundDelivery, InboundDeliveryproduct,  PurchaseOrder, Product
from django.http import JsonResponse

def delivery_detail(request, inbound_delivery_number):
    delivery = get_object_or_404(InboundDelivery, inbound_delivery_number=inbound_delivery_number)
    ibdproducts = InboundDeliveryproduct.objects.filter(delivery=delivery)
    return render(request, 'inbound/delivery_detail.html', {
        'delivery': delivery,
        'ibdproducts': ibdproducts,
    })

def get_po_products(request, po_id):
    try:
        po = PurchaseOrder.objects.get(pk=po_id)
        
        products = po.purchase_items.all() 
        data = []
        for item in products:
            data.append({
                "code": item.product.id,
                "description": item.product.description,
                "uom": item.product.unit_of_measure,
                "quantity": item.quantity,
            })
        return JsonResponse({"products": data})
    except PurchaseOrder.DoesNotExist:
        return JsonResponse({"products": []})


def edit_inbound_delivery(request, inbound_delivery_number):
    delivery = get_object_or_404(InboundDelivery, inbound_delivery_number=inbound_delivery_number)
    ibdproducts = InboundDeliveryproduct.objects.filter(delivery=delivery)

    if request.method == 'POST':
        vendor_id = request.POST.get('vendor') 
        po_number_id = request.POST.get('purchase_order_number')  

        if vendor_id:
            delivery.vendor = get_object_or_404(Vendor, vendor_id=vendor_id)  

        if po_number_id:
            delivery.purchase_order_number = get_object_or_404(PurchaseOrder, po_number=po_number_id) 

        delivery.delivery_status = request.POST.get('delivery_status')
        delivery.save()
        for product in ibdproducts:
            prefix = f"product_{product.id}_"
            product.product_description = request.POST.get(prefix + 'product_description', product.product_description)
            product.quantity_delivered = request.POST.get(prefix + 'quantity_delivered', product.quantity_delivered)
            product.quantity_received = request.POST.get(prefix + 'quantity_received', product.quantity_received)
            product.unit_of_measure = request.POST.get(prefix + 'unit_of_measure', product.unit_of_measure)
            product.save()
        return redirect('inbound_delivery')

    return render(request, 'inbound/delivery_info_edit.html', {
        'delivery': delivery,
        'ibdproducts': ibdproducts
    })
from django.http import JsonResponse
from .models import PurchaseOrder  

def po_suggestions(request):
    query = request.GET.get('q', '')
    if query:
        purchase_orders = PurchaseOrder.objects.filter(
            po_number__icontains=query  
        ).values_list('po_number', flat=True)[:10]
    else:
        purchase_orders = []

    return JsonResponse(list(purchase_orders), safe=False)  

from django.shortcuts import render, get_object_or_404, redirect
from .models import Pallet
from .forms import PalletEditForm

def edit_pallet(request, pallet_no):
    pallet = get_object_or_404(Pallet, pallet_no=pallet_no)

    if request.method == 'POST':
        form = PalletEditForm(request.POST, instance=pallet)
        if form.is_valid():
            form.save()
            return redirect('creating_pallet')  
    else:
        form = PalletEditForm(instance=pallet)

    return render(request, 'pallet/edit_pallet.html', {'form': form, 'pallet': pallet})

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def add_child_pallet(request):
    if request.method == "POST":
        parent_no = request.POST.get("parent_pallet")
        num_children = int(request.POST.get("num_children"))
        
        parent = get_object_or_404(Pallet, pallet_no=parent_no)
        
        for i in range(num_children):
            Pallet.objects.create(
                parent_pallet=parent,
                product=parent.product,
                p_mat=parent.p_mat,
                quantity=0, 
                weight=0,    
            )
        
        messages.success(request, f"{num_children} child pallet(s) created for {parent_no}")
        return redirect('creating_pallet')  

from django.shortcuts import render
from .models import PurchaseOrder
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import PurchaseOrder

def purchase_list_view(request):
    search_query = request.GET.get("q", "")
    purchase_orders = PurchaseOrder.objects.all().order_by("-po_date")

    if search_query:
        purchase_orders = purchase_orders.filter(
            po_number__icontains=search_query
        )

    paginator = Paginator(purchase_orders, 5)
    page_number = request.GET.get("page")
    purchase_orders_page = paginator.get_page(page_number)

    return render(request, "purchase_order/purchase_list.html", {
        "purchase_orders": purchase_orders_page,
        "search_query": search_query
    }) 
 
# ----------------
# SALES ORDER
# ---------------

from django.shortcuts import render, redirect, get_object_or_404
from .models import SalesOrderCreation, SalesOrderItem, Warehouse, Product
from django.utils.crypto import get_random_string


def generate_so_no():
    last_so = SalesOrderCreation.objects.order_by('-id').first()
    if last_so:
        last_number = int(last_so.so_no.replace("SO", ""))
        new_number = last_number + 1
    else:
        new_number = 1
    return f"SO{new_number:04d}"  

from django.http import JsonResponse
from .models import Warehouse

def get_warehouse_address(request, whs_id):
    try:
        warehouse = Warehouse.objects.get(whs_no=whs_id)
        return JsonResponse({"address": warehouse.address})
    except Warehouse.DoesNotExist:
        return JsonResponse({"error": "Warehouse not found"}, status=404)
    

from django.http import JsonResponse
from .models import Product

def product_autocomplete(request):
    term = request.GET.get('term', '')  
    products = Product.objects.filter(name__icontains=term)[:10]  
    suggestions = []
    for p in products:
        suggestions.append({
            'id': p.id,
            'name': p.name,
        })
    return JsonResponse(suggestions, safe=False)

  
from decimal import Decimal
from django.shortcuts import render, redirect
from django.db import transaction
from .models import SalesOrderCreation, SalesOrderItem, Warehouse


def sales_order_creation(request):
    warehouses = Warehouse.objects.all()
    product_rows = []

    if request.method == 'POST':
        try:
           
            whs_no = request.POST.get('whs_no')
            if not whs_no:
                raise ValueError("Warehouse is required")

            try:
                warehouse = Warehouse.objects.get(whs_no=whs_no)
            except Warehouse.DoesNotExist:
                raise ValueError("Selected warehouse does not exist")

            product_ids = request.POST.getlist('product_id[]')
            product_names = request.POST.getlist('product_name[]')
            quantities = request.POST.getlist('quantity[]')
            unit_prices = request.POST.getlist('unit_price[]')
            unit_total_price = request.POST.getlist('unit_total_price[]')

            if not product_ids:
                raise ValueError("At least one product must be added")

            net_total = Decimal(0)

            with transaction.atomic():
                so_no_obj = SalesOrderCreation.objects.create(
                    whs_no=warehouse,
                    whs_address=warehouse.address,
                    customer_id=request.POST.get('customer_id'),
                    customer_code=request.POST.get('customer_code'),
                    order_date=request.POST.get('order_date'),
                    delivery_date=request.POST.get('delivery_date'),
                    status=request.POST.get('status', 'Draft'),
                    remarks=request.POST.get('remarks', '')
                )

                for i in range(len(product_ids)):
                    if not product_ids[i].strip():
                        continue

                    try:
                        quantity = int(quantities[i])
                        unit_price = Decimal(unit_prices[i])
                    except ValueError:
                        raise ValueError(f"Invalid quantity or price for product {product_names[i]}")

                    unit_total_price = quantity * unit_price
                    net_total += unit_total_price

                    SalesOrderItem.objects.create(
                        so_no=so_no_obj,
                        product_id=product_ids[i].strip(),
                        product_name=product_names[i].strip(),
                        quantity=quantity,
                        unit_price=unit_price,
                        unit_total_price=unit_total_price
                    )
                    product_rows.append({
                        'product': product_ids[i],
                        'product_name': product_names[i],
                        'quantity': quantities[i],
                        'unit_price': unit_prices[i],
                        'unit_total_price': str(unit_total_price)
                    })

                so_no_obj.net_total_price = net_total
                so_no_obj.save()

            return redirect('sales_order_list')

        except Exception as e:
            return render(request, 'sales/sales_order_creation.html', {
                'error': str(e),
                'data': request.POST,
                'warehouses': warehouses,
                'product_rows': product_rows
            })
        
    
    so_no = generate_so_no()
    return render(request, 'sales/sales_order_creation.html', {
        'warehouses': warehouses,
        'product_rows': [],
        'so_no': so_no,
    })


def sales_order_detail(request, so_no):
    sales_order = get_object_or_404(SalesOrderCreation, so_no=so_no)
    so=SalesOrderItem.objects.filter(so_no=sales_order)

    so_items = SalesOrderItem.objects.filter(so_no=sales_order)
    return render(request, "sales/sales_order_detail.html", {"sales_order": sales_order, "so_items": so_items, "so": so})

def sales_order_edit(request, so_no):
    warehouses = Warehouse.objects.all()
    products = Product.objects.all()

    
    so_obj = get_object_or_404(SalesOrderCreation, so_no=so_no)
    so_items = SalesOrderItem.objects.filter(so_no=so_obj)

    if request.method == 'POST':
        
        so_obj.so_no = request.POST.get("so_no")
        whs_id = request.POST.get("whs_no")
        so_obj.whs_no = get_object_or_404(Warehouse, id=whs_id)
        so_obj.whs_address = getattr(so_obj.whs_no, 'address', "Unknown")
        so_obj.customer_id = request.POST.get("customer_id")
        so_obj.customer_code = request.POST.get("customer_code")
        so_obj.order_date = request.POST.get("order_date")
        so_obj.delivery_date = request.POST.get("delivery_date")
        so_obj.remarks = request.POST.get("remarks")
        so_obj.status = request.POST.get("status") or "Draft"
        so_obj.save()


        SalesOrderItem.objects.filter(so_no=so_obj).delete()

        product_ids = request.POST.getlist("product_id[]")
        product_names = request.POST.getlist("product_name[]")
        quantities = request.POST.getlist("quantity[]")
        prices = request.POST.getlist("unit_price[]")
        unit_totals = request.POST.getlist("unit_total_price[]")

        if product_names:
            for i in range(len(product_names)):
                if product_names[i]:
                    try:
                        qty = int(quantities[i]) if quantities[i] else 0
                    except ValueError:
                        qty = 0
                    try:
                        price = float(prices[i]) if prices[i] else 0
                    except ValueError:
                        price = 0
                    product_obj = None
                    if product_ids[i]:
                        try:
                            product_obj = Product.objects.get(id=product_ids[i])
                        except Product.DoesNotExist:
                            pass
                    try:
                        unit_total = float(unit_totals[i]) if unit_totals[i] else qty * price
                    except ValueError:
                        unit_total = qty * price

                    SalesOrderItem.objects.create(
                        so_no=so_obj,
                        product=product_obj,
                        product_name=product_names[i],
                        quantity=qty,
                        unit_price=price,
                        unit_total_price=unit_total,
                    )

        return redirect('sales_order_list')

    return render(request, 'sales/sales_order_edit.html', {
        'warehouses': warehouses,
        'products': products,
        'so_obj': so_obj,
        'so_items': so_items,
    })


def sales_order_delete(request, so_no):
    sales_order = get_object_or_404(SalesOrderCreation, so_no=so_no)
    sales_order.delete()
    return redirect('sales_order_list') 


def sales_order_list(request):
    sales_orders = SalesOrderCreation.objects.all().order_by('-order_date')
    so=SalesOrderItem.objects.filter(so_no__in=sales_orders)
    return render(request, 'sales/sales_order_list.html', {'sales_orders': sales_orders, 'so': so})

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from weasyprint import HTML
from .models import SalesOrderCreation

def sales_order_pdf(request, so_no):
    so = get_object_or_404(SalesOrderCreation, so_no=so_no)

    whs_name = "-"
    if hasattr(so, "whs") and so.whs:
        whs_name = getattr(so.whs, "whs_name", str(so.whs))
    elif hasattr(so, "warehouse") and so.warehouse:
        whs_name = getattr(so.warehouse, "name", str(so.warehouse))

    items = []
    if hasattr(so, "items") and hasattr(so.items, "all"):
        items = list(so.items.all())

    if items:
        rows_html = "".join(
            f"""
            <tr>
                <td style="text-align:center">{idx+1}</td>
                <td>{getattr(it, 'product_id', '')}</td>
                <td>{getattr(it, 'product_name', '')}</td>
                <td style="text-align:right">{getattr(it, 'quantity', '')}</td>
                <td style="text-align:right">{getattr(it, 'unit_price', '')}</td>
                <td style="text-align:right">{getattr(it, 'unit_total_price', '')}</td>
            </tr>
            """
            for idx, it in enumerate(items)
        )
    else:
        rows_html = "<tr><td colspan='6' style='text-align:center;color:#777'>No products in this order</td></tr>"

    html_string = f"""
    <html>
    <head>
      <style>
        @page {{ size: A4; margin: 20mm; }}
        body {{ font-family: Arial, sans-serif; font-size: 12px; }}
        h1 {{ text-align: center; font-size: 18px; margin-bottom: 15px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
        th, td {{ border: 1px solid #444; padding: 6px; }}
        th {{ background: #eee; }}
        .right {{ text-align: right; }}
      </style>
    </head>
    <body>
      <h1>Sales Order {so.so_no}</h1>
      <table>
        <tr><th>SO Number</th><td>{so.so_no}</td></tr>
        <tr><th>Warehouse</th><td>{whs_name}</td></tr>
        <tr><th>Order Date</th><td>{getattr(so, 'order_date', '')}</td></tr>
        <tr><th>Delivery Date</th><td>{getattr(so, 'delivery_date', '')}</td></tr>
        <tr><th>Status</th><td>{getattr(so, 'status', '')}</td></tr>
      </table>

      <h3>Items</h3>
      <table>
        <tr>
          <th>#</th>
          <th>Product ID</th>
          <th>Product Name</th>
          <th>Quantity</th>
          <th>Unit Price</th>
          <th>Total Price</th>
        </tr>
        {rows_html}
      </table>

      <table style="margin-top:12px;">
        <tr><th>Net Total</th><td class="right">{getattr(so, 'net_total_price', '')}</td></tr>
        <tr><th>Remarks</th><td>{getattr(so, 'remarks', '')}</td></tr>
      </table>
    </body>
    </html>
    """

    pdf_bytes = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="SalesOrder_{so.so_no}.pdf"'
    return response

# ----------------
# OUTBOUND DELIVERY
# ----------------

def generate_outbound_delivery_number():
    return f"OBD{random.randint(1000, 9999)}"

def outbound_delivery_item_number():
    prefix = "OBDIN"
    last_item = OutboundDeliveryItem.objects.order_by("id").last()

    if last_item and last_item.dlv_it_no and last_item.dlv_it_no.startswith(prefix):
        last_number = int(last_item.dlv_it_no.replace(prefix, ""))
        new_number = last_number + 1
    else:
        new_number = 1

    return f"{prefix}{new_number:05d}" 


from .models import OutboundDeliveryItem, OutboundDelivery

from django.shortcuts import redirect

def outbound(request):
    sales_orders = SalesOrderCreation.objects.all()
    delivery_no = generate_outbound_delivery_number()
    deliveries = OutboundDelivery.objects.all()
    if request.method == "POST":
        
        so_id = request.POST.get("so_no")
        outbound_delivery = OutboundDelivery.objects.create(
            dlv_no=delivery_no,
            so_no_id=so_id,
            whs_no_id=request.POST.get("whs_no") or None,
            whs_address=request.POST.get("whs_address") or None,
            ord_date=request.POST.get("ord_date") or None,
            del_date=request.POST.get("del_date") or None,
            sold_to=request.POST.get("sold_to"),
            ship_to=request.POST.get("ship_to"),
            cust_ref=request.POST.get("cust_ref"),
        )

        
        product_ids = request.POST.getlist("product_id[]")
        product_names = request.POST.getlist("product_name[]")
        dlv_it_no = request.POST.getlist("dlv_it_no[]")
        qty_orders = request.POST.getlist("qty_order[]")
        qty_issueds = request.POST.getlist("qty_issued[]")
        unit_prices = request.POST.getlist("unit_price[]")
        unit_total_prices = request.POST.getlist("unit_total_price[]")
        net_prices = request.POST.getlist("net_price[]")
        vols = request.POST.getlist("vol_per_item[]")

        for i in range(len(product_ids)):
            dlv_it_no = outbound_delivery_item_number()
            OutboundDeliveryItem.objects.create(
                delivery=outbound_delivery,
                dlv_it_no=dlv_it_no,
                product_id=product_ids[i],  
                product_name=product_names[i],
                qty_order=qty_orders[i] or 0,
                qty_issued=qty_issueds[i] or 0,
                unit_price=unit_prices[i] or 0,
                unit_total_price=unit_total_prices[i] or 0,
                net_total_price=net_prices[i] or 0,
                vol_per_item=vols[i] or 0,
            )
        return redirect("outbound")
    return render(request, "outbound/obd.html", {"sales_orders": sales_orders, "delivery_no": delivery_no})




from django.http import JsonResponse
from .models import SalesOrderCreation, SalesOrderItem, Product  


def get_so_products(request, so_id):
    try:
        so = SalesOrderCreation.objects.get(pk=so_id)
        salesorder = so.items.all()
        data = []
        for index, item in enumerate(salesorder, start=1):
            net_price = item.unit_total_price  
            data.append({
                "dlv_it_no": outbound_delivery_item_number(),  
                "product_id": item.product_id,
                "product_name": item.product_name,
                "qty_order": item.quantity,
                "unit_price": float(item.unit_price),
                "unit_total_price": float(item.unit_total_price),
                "net_price": float(net_price),
            })

        so_data = {
            "so_no": so.so_no,
            "whs_no": so.whs_no.whs_no if so.whs_no else None,
            "whs_address": so.whs_address,
            "customer_id": so.customer_id if so.customer_id else None,
            "status": so.status,
            "order_date": so.order_date.strftime("%Y-%m-%d") if so.order_date else None,
            "delivery_date": so.delivery_date.strftime("%Y-%m-%d") if so.delivery_date else None,
        }
        return JsonResponse({"salesorder": data, "so_data": so_data})
    except SalesOrderCreation.DoesNotExist:
        return JsonResponse({"salesorder": [], "so_data": {}})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Picking, Packing, PackedItem
from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from .models import Packing   # make sure you import your model


from .forms import PackingForm, PackedItemFormSet

def create_packing(request):
    if request.method == "POST":
        packing_form = PackingForm(request.POST)
        item_formset = PackedItemFormSet(request.POST, queryset=PackedItem.objects.none())

        if packing_form.is_valid() and item_formset.is_valid():
            packing = packing_form.save()
            for form in item_formset:
                if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                    item = form.save(commit=False)
                    item.packing = packing
                    item.save()
            return redirect("packing_list")
    else:
        packing_form = PackingForm()
        item_formset = PackedItemFormSet(queryset=PackedItem.objects.none())

    return render(request, "packing/create_packing.html", {
        "packing_form": packing_form,
        "item_formset": item_formset,
    })



def packing_list(request):
    packings = Packing.objects.all()
    return render(request, "packing/packing_list.html", {"packings": packings})


def packing_detail(request, packing_id):
    packing = get_object_or_404(Packing, id=packing_id)
    items = packing.items.all()  # assuming related_name='items' on ForeignKey
    return render(request, "packing/packing_detail.html", {"packing": packing, "items": items})

from .forms import PackingForm, PackedItemFormSet

def edit_packing(request, packing_id):
    packing = get_object_or_404(Packing, id=packing_id)

    if request.method == "POST":
        packing_form = PackingForm(request.POST, instance=packing)
        item_formset = PackedItemFormSet(request.POST, queryset=packing.items.all())

        if packing_form.is_valid() and item_formset.is_valid():
            packing_form.save()
            for form in item_formset:
                if form.cleaned_data:
                    if form.cleaned_data.get("DELETE"):
                        if form.instance.pk:  # only delete if it exists
                            form.instance.delete()
                    else:
                        item = form.save(commit=False)
                        item.packing = packing
                        item.save()
            return redirect("packing_detail", packing_id=packing.id)
    else:
        packing_form = PackingForm(instance=packing)
        item_formset = PackedItemFormSet(queryset=packing.items.all())

    return render(request, "packing/edit_packing.html", {
        "packing_form": packing_form,
        "item_formset": item_formset,
        "packing": packing,
    })


def delete_packing(request, packing_id):
    packing = get_object_or_404(Packing, id=packing_id)
    packing.delete()
    return redirect("packing_list")

from .forms import PackedItemForm

def add_packed_item(request, packing_id):
    packing = get_object_or_404(Packing, id=packing_id)

    if request.method == "POST":
        form = PackedItemForm(request.POST)
        if form.is_valid():
            packed_item = form.save(commit=False)
            packed_item.packing = packing  # link to parent Packing
            packed_item.save()
            return redirect("packing_detail", packing_id=packing.id)
    else:
        form = PackedItemForm()

    return render(request, "packing/add_packed_item.html", {"form": form, "packing": packing})
