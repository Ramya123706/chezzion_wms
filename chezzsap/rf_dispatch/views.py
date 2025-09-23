import csv
import json
import uuid
import contextlib
import random
from decimal import Decimal, InvalidOperation
from itertools import chain, zip_longest
from datetime import datetime, timezone
from django.urls import reverse
from django.utils.dateparse import parse_date
from django import forms
from django.contrib import messages
from django.contrib.auth import (
    authenticate, login, logout, update_session_auth_hash
)
from django.contrib.auth.decorators import (
    login_required, user_passes_test
)
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q, Prefetch
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.timezone import now
from weasyprint import HTML
# Forms
from .forms import (
    YardHdrForm, TruckInspectionForm, Trucksearchform,
    PalletForm, PalletEditForm, CustomerForm, ProductForm, WarehouseForm,
    PurchaseOrderForm, GoodsReceiptForm, VendorForm,
    CategoryForm, PackingForm, PackedItemFormSet
)

# Models
from .models import (
    # Core
    Truck, YardHdr, TruckLog, Pallet, Product,
    Category, SubCategory, StockUpload, Warehouse, Bin,
    PackingMaterial, Profile, Customers, Vendor, Inventory,

    # Purchase / Goods Flow
    PurchaseOrder, PurchaseItem, GoodsReceipt, GoodsReceiptItem,
    InboundDelivery, InboundDeliveryproduct, OutboundDelivery,
    OutboundDeliveryItem, PostGoodsIssue,

    # Warehouse Ops
    Putaway, Picking, Packing, PackedItem,

    # Sales
    SalesOrderCreation, SalesOrderItem,

    # Inspection
    InspectionResponse, InspectionQuestion
)

# Utils
from .utils import (
    log_truck_status, generate_outbound_delivery_number, safe_decimal
)

@login_required
def index(request):
    return render(request, 'home.html')

@login_required
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
from django.contrib import messages

def yard_checkin_view(request):
    if request.method == 'POST':
        truck_no = request.POST.get('truck_no')

        existing = YardHdr.objects.filter(
            truck_no=truck_no
        ).exclude(truck_status='checkout').last()

        if existing:
            messages.error(request, f"Truck {truck_no} is already checked in and not checked out!")
        else:
            request.session['page1_data'] = {
                'whs_no': request.POST.get('whs_no'),
                'truck_no': truck_no,
                'truck_type': request.POST.get('truck_type'),
                'driver_name': request.POST.get('driver_name'),
                'driver_phn_no': request.POST.get('driver_phn_no'),
                'po_no': request.POST.get('po_no'),
                'truck_date': request.POST.get('truck_date'),
                'truck_time': request.POST.get('truck_time'),
                'seal_no': request.POST.get('seal_no'),
                'yard_scan': request.POST.get('yard_scan'),
                'truck_status': request.POST.get('truck_status'),
            }
            return redirect('inspection', truck_no=truck_no)

    form = YardHdrForm()

    return render(request, 'truck_screen/one.html', {
        'form': form,
        'truck': Truck.objects.all(),
    })

 
def inspection_view(request, truck_no):
    page1_data = request.session.get('page1_data')
    if not page1_data:
        messages.error(request, "Page 1 data not found. Please fill Truck Check-in first.")
        return redirect('yard_checkin')
 
    questions = InspectionQuestion.objects.all()
 
    if request.method == 'POST':
        all_yes = True
        responses = {}
        for q in questions:
            ans = request.POST.get(f"question_{q.id}")
            responses[q] = ans
            if ans != "Yes":
                all_yes = False
 
        if not all_yes:
            messages.error(request, "Inspection failed! All answers must be 'Yes' to proceed.")
            return render(request, "truck_screen/two.html", {"questions": questions, "truck_no": truck_no})
 
        yard_instance = YardHdr.objects.create(
            whs_no_id = page1_data['whs_no'],
            truck_no = page1_data['truck_no'],
            truck_type = page1_data['truck_type'],
            driver_name = page1_data['driver_name'],
            driver_phn_no = page1_data['driver_phn_no'],
            po_no = page1_data['po_no'],
            truck_date = page1_data['truck_date'],
            truck_time = page1_data['truck_time'],
            seal_no = page1_data['seal_no'],
            yard_scan = page1_data['yard_scan'],
            truck_status = "Inspected"
        )
       
        for q, ans in responses.items():
            InspectionResponse.objects.create(
                yard = yard_instance,
                question = q,
                answer = ans
            )
       
 
        if not Truck.objects.filter(truck_no=yard_instance.truck_no).exists():
            Truck.objects.create(
                truck_no = yard_instance.truck_no,
                driver_name = yard_instance.driver_name,
                driver_phn_no = yard_instance.driver_phn_no
            )
 
        if 'page1_data' in request.session:
            del request.session['page1_data']
 
            messages.success(request, "Truck inspection completed successfully!")
        return redirect('yard_checkin')
   
    return render(request, "truck_screen/two.html", {"questions": questions, "truck_no": truck_no})
 


@user_passes_test(lambda u: u.is_superuser)
def add_questions(request):
    old_questions = InspectionQuestion.objects.all().order_by("id")

    if request.method == "POST":
        if "count" in request.POST:
            count = int(request.POST["count"])
            return render(
                request,
                "truck_screen/add_question.html",
                {"count": count, "old_questions": old_questions},
            )
        else:  
            questions = []
            for key, value in request.POST.items():
                if key.startswith("question") and value.strip():
                    questions.append(value.strip())
            for q in questions:
                InspectionQuestion.objects.create(text=q)

            return redirect("add_questions") 

    return render(
        request,
        "truck_screen/add_question.html",
        {"old_questions": old_questions},
    )


@user_passes_test(lambda u: u.is_superuser)
def delete_question(request, pk):
    question = get_object_or_404(InspectionQuestion, pk=pk)
    question.delete()
    return redirect("add_questions")


@user_passes_test(lambda u: u.is_superuser)
def edit_question(request, pk):
    question = get_object_or_404(InspectionQuestion, pk=pk)

    if request.method == "POST":
        new_text = request.POST.get("text", "").strip()
        if new_text:
            question.text = new_text
            question.save()

            return JsonResponse({"success": True, "text": new_text})
        return JsonResponse({"success": False, "error": "Empty text"})

    return JsonResponse({"success": False, "error": "Invalid request"})


@login_required
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



@login_required
def inspection_summary_view(request):
    inspections = YardHdr.objects.all().order_by('-truck_date', '-truck_time') 
    return render(request, 'truck_screen/summary.html', {'inspections': inspections})

@login_required
def truck_landing(request):
    return render(request, 'truck_screen/truck_landing_page.html')

@login_required
def status_log_view(request, truck_no):
    logs = TruckLog.objects.filter(truck_no__truck_no=truck_no).order_by('-truck_date', '-truck_time')
    return render(request, 'truck_screen/status_log.html', {'logs': logs, 'truck_no': truck_no})


@login_required
def truck_log_view(request):
    truck_no_query = request.GET.get('truck_no')
    logs = []
    truck_details = None
    error_message = ""

    if truck_no_query:
        logs = TruckLog.objects.filter(
            truck_no__truck_no__iexact=truck_no_query
        ).order_by('-truck_date', '-truck_time')
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



@login_required
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
        'trucklog':TruckLog.objects.filter(truck_no__truck_no=truck_no).order_by('-truck_date', '-truck_time').first() if truck else None
    })

@login_required
def truck_list(request):
    query = request.GET.get('search')
    if query:
        trucks = YardHdr.objects.filter(truck_no__icontains=query)
    else:
        trucks = YardHdr.objects.all()

    return render(request, 'truck_screen/truck_list.html', {'trucks': trucks, 'query': query})



def truck_detail(request, truck_no):
    try:
        truck = YardHdr.objects.filter(truck_no=truck_no).order_by('-truck_date', '-truck_time').first()
        if not truck:
            return render(request, 'truck_screen/truck_detail.html', {'error': 'Truck not found'})

        logs = TruckLog.objects.filter(truck_no=truck).order_by('-truck_date', '-truck_time')
        inspection_qs = InspectionQuestion.objects.all()
        inspection_as = InspectionResponse.objects.filter(yard=truck)
        inspection_map = {resp.question.id: resp.answer for resp in inspection_as}

        return render(request, 'truck_screen/truck_detail.html', {
            'truck': truck,
            'logs': logs,
            'inspection_qs': inspection_qs,
            'inspection_map': inspection_map,
        })

    except YardHdr.DoesNotExist:
        return render(request, 'truck_screen/truck_detail.html', {'error': 'Truck not found'})




@login_required
def update_truck_status(request, truck_no):
    if request.method == "POST":
        new_status = request.POST.get("new_status")
        comment = request.POST.get("comment", "")

        try:
            truck = YardHdr.objects.filter(truck_no=truck_no).last()
            truck.truck_status = new_status
            truck.save()

            log_truck_status(truck_instance=truck, status=new_status, user=request.user, comment=comment)

            messages.success(request, f"Truck status updated to {new_status}.")
        except YardHdr.DoesNotExist:
            messages.error(request, "Truck not found.")

    return redirect("truck_detail", truck_no=truck_no)



# ------------
# STOCK UPLOAD
# -------------

 
def batch_product_view(request):
    query = ""
    categories = Category.objects.all()  # Make sure categories is always defined
    warehouse = Warehouse.objects.all()
    materials = PackingMaterial.objects.all()
    

    if request.method == 'POST':
        whs_no = request.POST.get('whs_no')
        product_id = request.POST.get('product')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        batch = request.POST.get('batch')
        bin_id = request.POST.get('bin')
        pallet = request.POST.get('pallet')
        p_mat = request.POST.get('p_mat')
        inspection = request.POST.get('inspection')
        stock_type = request.POST.get('stock_type')
        item_number = request.POST.get('item_number')
        doc_no = request.POST.get('doc_no')
        pallet_status = request.POST.get('pallet_status')
        category = request.POST.get('category')
        sub_category = request.POST.get('sub_category')

        try:
            product_instance, _ = Product.objects.get_or_create(
                product_id=product_id,
                defaults={
                    'name': product_id,
                    'description': description
                }
            )

            warehouse_instance = get_object_or_404(Warehouse, whs_no=whs_no)
            bin_instance = Bin.objects.filter(id=bin_id).first() 
            p_mat_instance = PackingMaterial.objects.filter(id=p_mat).first() if p_mat else None
            batch = request.POST.get('batch_input') or batch or ''

            StockUpload.objects.create(
                whs_no=warehouse_instance,
                product=product_instance,
                description=description,
                quantity=int(quantity or 0),
                batch=batch,
                bin=bin_instance,
                pallet=pallet,
                p_mat=p_mat_instance,
                inspection=inspection,
                stock_type=stock_type,
                item_number=item_number,
                doc_no=doc_no,
                pallet_status=pallet_status,
                category=category,
                sub_category=sub_category
            )

        except Exception as e:
            query = request.GET.get('search', '')
            stock_uploads = StockUpload.objects.all()
            return render(request, 'stock_upload/batch_product.html', {
                'products': Product.objects.all(),
                'warehouse': warehouse,
                'materials': materials,
                'stocks': stock_uploads,
                'query': query,
                'categories': categories,
                'error': str(e),
            })

    # For both GET and successful POST
    stock_uploads = StockUpload.objects.all()
    query = request.GET.get('search', '')
    return render(request, 'stock_upload/batch_product.html', {
        'products': Product.objects.all(),
        'warehouse': warehouse,
        'materials': materials,
        'stocks': stock_uploads,
        'query': query,
        'categories': categories,
    })


from django.http import JsonResponse

def get_bins(request, subcategory_id):
    bins = Bin.objects.filter(sub_category_id=subcategory_id)
    bin_list = []
    for b in bins:
        remaining = b.capacity - b.existing_quantity
        bin_list.append({
            "id": b.id,
            "bin_id": b.bin_id,
            "capacity": b.capacity,
            "remaining": remaining,
        })
    return JsonResponse({"bins": bin_list})


# from django.http import JsonResponse
# from .models import SubCategory, Bin

# def get_subcategories(request):
#     category_id = request.GET.get('category_id')
#     subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
#     data = {'subcategories': list(subcategories)}
#     return JsonResponse(data)

# def get_bins(request):
#     category_id = request.GET.get('category_id')
#     sub_category_id = request.GET.get('sub_category_id')

#     bins = Bin.objects.filter(
#         category_id=category_id,
#         sub_category_id=sub_category_id
#     ).values('id', 'bin_id', 'existing_quantity', 'capacity')

#     # Prepare formatted data
#     bin_list = [
#         {
#             'id': b['id'],
#             'display': f"{b['bin_id']} (Remaining: {b['capacity'] - b['existing_quantity']}/{b['capacity']})"
#         }
#         for b in bins
#     ]

#     return JsonResponse({'bins': bin_list})



def batch_product_csv_upload(request):  # sourcery skip: low-code-quality
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Please upload a CSV file only.")
            return redirect('batch_product')

        try:
            file_data = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(file_data)

            for row in reader:
                category_value = row.get('Category')
                category_instance = None
                if category_value:
                    if category_value.isdigit():
                        category_instance = Category.objects.filter(id=category_value).first()
                    else:
                        category_instance, _ = Category.objects.get_or_create(name=category_value)

                sub_category_value = row.get('Sub Category')
                sub_category_instance = None
                if sub_category_value:
                    if sub_category_value.isdigit():
                        sub_category_instance = SubCategory.objects.filter(id=sub_category_value).first()
                    else:
                        sub_category_instance, _ = SubCategory.objects.get_or_create(name=sub_category_value)

                product_instance, _ = Product.objects.get_or_create(
                    product_id=row.get('Product ID'),
                    defaults={
                        'description': row.get('Description', ''),
                        'category': category_instance,
                        'sub_category': sub_category_instance,
                    }
                )

                warehouse = Warehouse.objects.filter(whs_no=row.get('Warehouse')).first()
                if not warehouse:
                    raise ValueError(f"Warehouse '{row.get('Warehouse')}' not found")

                bin_instance = Bin.objects.filter(bin_id=row.get('Bin')).first()

                p_mat_instance = PackingMaterial.objects.filter(id=row.get('P_Mat')).first()

                StockUpload.objects.create(
                    whs_no=warehouse,
                    product=product_instance,
                    description=row.get('Description', ''),
                    quantity=int(row.get('Quantity') or 0),
                    batch=row.get('Batch', ''),
                    bin=bin_instance,
                    pallet=row.get('Pallet', ''),
                    p_mat=p_mat_instance,
                    inspection=row.get('Inspection', ''),
                    stock_type=row.get('Stock Type', 'Unrestricted'),
                    item_number=row.get('Item Number', ''),
                    doc_no=row.get('Doc No', ''),
                    pallet_status=row.get('Pallet Status', 'Planned'),
                    category=category_instance,
                    sub_category=sub_category_instance,
                )

            messages.success(request, "CSV uploaded successfully!")

        except Exception as e:
            messages.error(request, f"Error processing CSV: {e}")

    return redirect('batch_product')






def get_product_description(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        return JsonResponse({'description': product.description})
    except Product.DoesNotExist:
        return JsonResponse({'description': ''}, status=404)


def stock_detail_view(request, pk):
    stock = get_object_or_404(StockUpload, pk=pk)
    return render(request, 'stock_upload/stock_detail.html', {'stock': stock})

# -----------
# WAREHOUSE
# -----------

def stock_list(request):
    stocks = StockUpload.objects.all()
    return render(request, 'stock_upload/stock_list.html', {'stocks': stocks})

def stock_edit(request, pk):
    stock = get_object_or_404(StockUpload, pk=pk)
    warehouse = Warehouse.objects.all()
    materials = PackingMaterial.objects.all()
    products = Product.objects.all()
    bins = Bin.objects.all() 

    if request.method == "POST":

        try:
            whs_no_instance = Warehouse.objects.get(whs_no=request.POST.get("whs_no"))
            p_mat_instance = PackingMaterial.objects.get(id=request.POST.get("p_mat"))
            product_instance = Product.objects.get(product_id=request.POST.get("product"))
            bin_id = request.POST.get("bin")
            if bin_id:
                bin_instance = Bin.objects.get(pk=bin_id)
            else:
                bin_instance = None

            stock.whs_no = whs_no_instance
            stock.p_mat = p_mat_instance
            stock.product = product_instance
            stock.bin = bin_instance
            stock.category = request.POST.get("category") or ""
            stock.sub_category = request.POST.get("sub_category") or ""
            stock.description = request.POST.get("description") or ""
            stock.quantity = int(request.POST.get("quantity") or 0)
            stock.pallet = request.POST.get("pallet") or ""
            stock.inspection = request.POST.get("inspection") or "Not Inspected"
            stock.stock_type = request.POST.get("stock_type") or "Unrestricted"
            stock.wps = request.POST.get("wps") or ""
            stock.doc_no = request.POST.get("doc_no") or ""
            stock.pallet_status = request.POST.get("pallet_status") or "Planned"

            stock.save()
            messages.success(request, "Stock updated successfully!")
            return redirect("stock_list")

        except Warehouse.DoesNotExist:
            messages.error(request, "Selected warehouse does not exist.")
        except Product.DoesNotExist:
            messages.error(request, "Selected product does not exist.")
        except PackingMaterial.DoesNotExist:
            messages.error(request, "Selected packing material does not exist.")
        except Bin.DoesNotExist:
            messages.error(request, "Selected bin does not exist.")
        except Exception as e:
            messages.error(request, f"Error updating stock: {str(e)}")

    context = {
        "stock": stock,
        "warehouse": warehouse,
        "materials": materials,
        "products": products,
        "bins": bins,
    }
    return render(request, "stock_upload/stock_edit.html", context)


def warehouse_view(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST, request.FILES)
        if form.is_valid():
            warehouse = form.save()
            return redirect('warehouse_detail', whs_no=warehouse.whs_no) 
    else:
        form = WarehouseForm()

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





def product_list(request):
    products = Product.objects.all().order_by('-created_at')

    paginator = Paginator(products, 8)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # If AJAX request → return partial HTML
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'product/product_list_partial.html', {'products': page_obj})

    # Normal full render
    return render(request, 'product/product_list.html', {'products': page_obj})




from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Category, SubCategory, Product

def generate_product_id():
    """
    Generate a short unique product id using the current date and uuid.
    Uses already-imported datetime and uuid at top of this module.
    """
    return f"P{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:6].upper()}"


def add_product(request):
    pallets = pallet.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        pallet_id = request.POST.get('pallet_no')
        sku = request.POST.get('sku')
        description = request.POST.get('description')
        unit_of_measure = request.POST.get('unit_of_measure')
        category_id = request.POST.get('category')
        sub_category_id = request.POST.get('sub_category_id')
        re_order_level = request.POST.get('re_order_level')
        unit_price = request.POST.get('unit_price')
        images = request.FILES.get('images')

        if not name or not category_id:
            messages.error(request, "Please fill required fields: Name, Category.")
            return render(request, 'product/add_product.html', {
                'pallets': pallets,
                'categories': categories,
                'subcategories': subcategories,
            })

        try:
            category = Category.objects.get(id=category_id)
            sub_category = SubCategory.objects.get(id=sub_category_id) if sub_category_id else None
            pallet = Pallet.objects.get(id=pallet_id) if pallet_id else None

            product_id = generate_product_id()

            Product.objects.create(
                product_id=product_id,
                name=name,
                quantity=quantity,
                pallet_no=pallet,
                sku=sku,
                description=description,
                unit_of_measure=unit_of_measure,
                category=category,
                sub_category=sub_category,
                re_order_level=re_order_level,
                unit_price=unit_price,
                images=images,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )

            messages.success(request, f"Product {product_id} added successfully!")
            return redirect('product_list')

        except Exception as e:
            messages.error(request, f"Unexpected error: {e}")

    return render(request, 'product/add_product.html', {
        'pallets': pallets,
        'categories': categories,
        'subcategories': subcategories,
    })






def bulk_upload_products(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]

        if not csv_file.name.endswith('.csv'):
            messages.error(request, "File must be a CSV.")
            return redirect("add_product")

        file_data = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(file_data)

        created, skipped = 0, 0
        for row in reader:
            try:
                product_id = row["Product ID"]
                name = row["Name"]
                quantity = row["Quantity"]
                pallet_no = row["Pallet No"]
                sku = row["SKU"]
                description = row["Description"]
                unit_of_measure = row["Unit of Measure"]
                category_name = row["Category"]
                subcategory_name = row.get("Sub Category")
                re_order_level = row["Reorder Level"]
                unit_price = row["Unit Price"]

                category, _ = Category.objects.get_or_create(category=category_name)

                sub_category = None
                if subcategory_name:
                    sub_category, _ = SubCategory.objects.get_or_create(
                        name=subcategory_name, category=category
                    )

                Product.objects.create(
                    product_id=product_id,
                    name=name,
                    quantity=quantity,
                    pallet_no=pallet_no,
                    sku=sku,
                    description=description,
                    unit_of_measure=unit_of_measure,
                    category=category,
                    sub_category=sub_category,
                    re_order_level=re_order_level,
                    unit_price=unit_price,
                )
                created += 1
            except Exception as e:
                print("Skipping row:", row, "Error:", e)
                skipped += 1

        messages.success(request, f"Uploaded {created} products, skipped {skipped}.")
        return redirect("add_product")

    return redirect("add_product")


def update_product_from_post(product, post_data, files_data):
    product.name = post_data.get('name')
    product.quantity = post_data.get('quantity')
    product.unit_price = post_data.get('unit_price')
    product.pallet_no = post_data.get('pallet_no')
    product.sku = post_data.get('sku')
    product.description = post_data.get('description')
    product.unit_of_measure = post_data.get('unit_of_measure')
    product.re_order_level = post_data.get('re_order_level')

    # Handle category (foreign key) with contextlib.suppress
    if (category_id := post_data.get('category')):
        with contextlib.suppress(ValueError):
            product.category_id = int(category_id)

    if files_data.get('images'):
        product.images = files_data['images']

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


        update_product_from_post(product, request.POST, request.FILES)
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


def inventory_view(request):
    search_query = request.GET.get("search", "").strip()
    category_filter = request.GET.get("category", "")
    subcategory_filter = request.GET.get("subcategory", "")

    inventory_qs = Inventory.objects.select_related(
        "product", "product__category", "product__sub_category"
    )

    if search_query:
        inventory_qs = inventory_qs.filter(
            Q(product__name__icontains=search_query) |
            Q(product__product_id__icontains=search_query)
        )

    if category_filter:
        inventory_qs = inventory_qs.filter(product__category__id=category_filter)

    if subcategory_filter:
        inventory_qs = inventory_qs.filter(product__sub_category__id=subcategory_filter)

    inventory_data = []
    for item in inventory_qs:
        po_item = PurchaseItem.objects.filter(product=item.product).select_related("purchase_order").order_by("-purchase_order__po_date").first()
        gr_item = GoodsReceiptItem.objects.filter(
            inbound_delivery_product__product=item.product
        ).select_related("goods_receipt").order_by("-goods_receipt__posting_date").first()
        inventory_data.append({
            "inventory": item,
            "po_number": po_item.purchase_order.po_number if po_item and po_item.purchase_order else "-",
            "gr_number": gr_item.goods_receipt.gr_no if gr_item and gr_item.goods_receipt else "-",
        })

    context = {
        "inventory_data": inventory_data,
        "categories": Category.objects.all(),
        "subcategories": SubCategory.objects.all(),
        "search_query": search_query,
        "category_filter": category_filter,
        "subcategory_filter": subcategory_filter,
    }

    return render(request, "inventory/inventory_list.html", context)




   
# .........
# CUSTOMERS
# .........

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


def whs_no_dropdown_view(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'stock_upload/batch_product.html', {'warehouses': warehouses})

# -----
# PALLET
# ------

def creating_pallet(request):
    if request.method == 'POST':
        form = PalletForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                
                pallet = form.save(commit=False)
                pallet.created_by = str(request.user)
                pallet.updated_by = str(request.user)
                
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


# --------------------
# PURCHASE ORDER
# -------------------

from decimal import Decimal
from django.shortcuts import render, redirect
from django.utils.timezone import now
from .models import PurchaseOrder, Product, PurchaseItem, Vendor


def generate_po_number():
    today = now().strftime("%Y%m%d")
    last_po = PurchaseOrder.objects.filter(po_number__startswith=today).order_by('-id').first()
    if last_po:
        last_num = int(last_po.po_number[-4:])  # last 4 digits
        new_num = last_num + 1
    else:
        new_num = 1
    return f"{today}{new_num:04d}"

import datetime
from django.utils.crypto import get_random_string

def generate_invoice_number():
    today = datetime.date.today().strftime("%Y%m%d")
    random_part = get_random_string(4, allowed_chars="0123456789")
    return f"INV-{today}-{random_part}"

def add_purchase(request):
    if request.method == 'POST':
        try:
            # --- Create Purchase Order ---
            po = PurchaseOrder.objects.create(
                company_name=request.POST.get('company_name'),
                company_address=request.POST.get('company_address'),
                company_phone=request.POST.get('company_phone'),
                company_email=request.POST.get('company_email'),
                company_website=request.POST.get('company_website'),
                po_date=request.POST.get('po_date'),
                po_number=generate_po_number(),
                invoice_number=generate_invoice_number(),
                vendor_company_name=request.POST.get('vendor_company_name'),
                vendor_contact_name=request.POST.get('vendor_contact_name'),
                vendor_phone=request.POST.get('vendor_phone'),
                vendor_address=request.POST.get('vendor_address'),
                vendor_website=request.POST.get('vendor_website'),
                vendor_email=request.POST.get('vendor_email'),
            )

            # --- Get product item details ---
            item_numbers = request.POST.getlist('item_number[]')
            product_names = request.POST.getlist('product_name[]')
            quantities = request.POST.getlist('quantity[]')
            unit_prices = request.POST.getlist('unit_price[]')
            warehouses = request.POST.getlist('warehouse[]')  # NEW

            for i in range(len(item_numbers)):
                item_number = (item_numbers[i] or '').strip()
                product_name = (product_names[i] or '').strip()
                quantity_raw = (quantities[i] or '').strip()
                unit_price_raw = (unit_prices[i] or '').strip()
                warehouse_id = warehouses[i] or None  # NEW

                if not all([product_name, quantity_raw, unit_price_raw]):
                    continue  # skip incomplete rows

                try:
                    quantity = int(quantity_raw)
                    unit_price = Decimal(unit_price_raw)
                except (ValueError, TypeError):
                    continue

                # --- Try finding product ---
                product = None
                if item_number:
                    product = Product.objects.filter(product_id=item_number).first()

                if not product and product_name:
                    product = Product.objects.filter(name__iexact=product_name).first()

                # --- If product not found → create new one ---
                if not product:
                    product = Product.objects.create(
                        product_id=item_number or f"ID-{uuid.uuid4().hex[:6]}",
                        name=product_name,
                        quantity=0,  # inventory remains 0 until GR
                        pallet_no=f"PALLET-{item_number or product_name[:5].upper()}",
                        sku=f"SKU-{item_number or product_name[:5].upper()}",
                        unit_price=unit_price,
                        description=product_name,
                        unit_of_measure="pcs",
                        re_order_level=10,
                    )
                    messages.info(request, f"New product created: {product.name}")

                # --- Update unit price if changed ---
                if product.unit_price != unit_price:
                    product.unit_price = unit_price
                    product.save()

                # --- Link product with purchase order including warehouse ---
                warehouse_obj = None
                if warehouse_id:
                    warehouse_obj = Warehouse.objects.filter(pk=warehouse_id).first()

                PurchaseItem.objects.create(
                    purchase_order=po,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=quantity * unit_price,
                    warehouse=warehouse_obj  # NEW
                )

            return redirect('purchase_detail', pk=po.pk)

        except Exception as e:
            return render(request, 'purchase_order/add_purchase.html', {
                'error': str(e),
                'data': request.POST,
                'vendors': Vendor.objects.all(),
                'warehouses': Warehouse.objects.all(),  # make sure warehouses are passed
            })

    # GET request → render template
    return render(request, 'purchase_order/add_purchase.html', {
        'vendors': Vendor.objects.all(),
        'warehouses': Warehouse.objects.all(),  # pass warehouses to template
    })


def purchase_detail(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    return render(request, "purchase_order/purchase_detail.html", {"po": po})

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.contrib.staticfiles import finders

def download_po_pdf(request, pk): 
    po = get_object_or_404(PurchaseOrder, pk=pk)
    html_string = render_to_string('purchase_order/purchase_order_pdf.html', {'po': po})

    # Find CSS if using static files
    css_path = finders.find('css/purchase_order.css')
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    pdf = html.write_pdf(stylesheets=[CSS(css_path)] if css_path else None)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="purchase_order_{pk}.pdf"'
    return response






def purchase_edit(request, po_id):
    po = get_object_or_404(PurchaseOrder, id=po_id)
    item = PurchaseItem.objects.filter(purchase_order=po).first()

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

        if item:
            product_id = request.POST.get('product_id')
            if product_id:
                item.product = get_object_or_404(Product, id=product_id)

            quantity = request.POST.get('product_quantity')
            unit_price = request.POST.get('unit_price')

            if quantity:
                item.quantity = int(quantity)   
            if unit_price:
                item.unit_price = Decimal(unit_price) 
            
            item.total_price = item.quantity * item.unit_price
            item.save()

        po.save()
        messages.success(request, "Purchase order updated successfully.")
        return redirect('purchase_detail', pk=po.id)


    products = Product.objects.all()
    return render(request, 'purchase_order/purchase_edit.html', {
        'po': po,
        'item': item,
        'products': products,
    })





def rf_ptl(request):
    return render(request, 'rf_pick_to_light/dashboard.html')

# -----------------
# BIN
# -----------------
from .utils import generate_bin_id  
def create_bin(request):
    if request.method == 'POST':
        try:
            whs_key = request.POST.get('whs_no')
            warehouse = Warehouse.objects.get(whs_no=whs_key)

            category = Category.objects.get(id=request.POST.get('category'))
            sub_category_id = request.POST.get('subcategory')
            sub_category = None
            if sub_category_id:
                sub_category = SubCategory.objects.get(id=sub_category_id)

            bin_id = generate_bin_id(warehouse)

            Bin.objects.create(
                whs_no=warehouse,
                bin_id=bin_id,
                bin_type=request.POST.get('bin_type'),
                capacity=int(request.POST.get('capacity')),
                location=request.POST.get('location'),
                existing_quantity=int(request.POST.get('existing_quantity') or 0),
                category=category,
                sub_category=sub_category,
                updated_by=request.POST.get('updated_by') or "system",
                created_by=request.POST.get('created_by') or "system"
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


def bin_detail(request, bin_id):
    return render(request, 'bin/bin_detail.html', {'bin_id': bin_id})

def get_bin_location(request, bin_id):
    try:
        bin_obj = Bin.objects.get(id=bin_id)
        return JsonResponse({
            "location": bin_obj.location
        })
    except Bin.DoesNotExist:
        return JsonResponse({"error": "Bin not found"}, status=404)



# -----------------
# VENDOR
# -----------------

def task(request):
    return render(request, 'rf_pick_to_light/task_solving.html')




def add_category(request):
    if request.method == "POST":
        try:
            category_name = request.POST.get("category")
            description = request.POST.get("description")

            category = Category.objects.create(
                category=category_name,
                description=description
            )

            # Subcategories
            subcategories = []
            for key, value in request.POST.items():
                if key.startswith("sub_category_") and value.strip():
                    subcat = SubCategory.objects.create(
                        category=category,
                        name=value.strip()
                    )
                    subcategories.append(subcat.name)

            return JsonResponse({
                "success": True,
                "id": category.id,
                "category": category.category,
                "subcategories": subcategories
            })

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request"})

def get_subcategories(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = list(category.subcategories.values("id", "name"))
    return JsonResponse({"subcategories": subcategories})

def load_subcategories(request):
    category_id = request.GET.get("category_id")
    subcategories = SubCategory.objects.filter(category_id=category_id).values("id", "name")
    return JsonResponse({"subcategories": list(subcategories)})


def bin_detail(request, bin_id):
    bin_instance = get_object_or_404(Bin, bin_id=bin_id)
    return render(request, 'bin/bin_detail.html', {'bin': bin_instance})


from django.shortcuts import render, get_object_or_404

from django.shortcuts import get_object_or_404, redirect, render
from .models import Bin, Warehouse, Category, SubCategory

def edit_bin(request, bin_id):
    bin_obj = get_object_or_404(Bin, pk=bin_id)
    categories = Category.objects.all()

    if request.method == "POST":
        whs_no = request.POST.get('whs_no')
        bin_id_input = request.POST.get('bin_id')
        bin_type = request.POST.get('bin_type')
        capacity = request.POST.get('capacity')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')

        # Fetch related model instances
        whs_instance = get_object_or_404(Warehouse, whs_no=whs_no)
        category_instance = get_object_or_404(Category, id=category_id)
        subcategory_instance = get_object_or_404(SubCategory, id=subcategory_id)

        # Update bin object
        bin_obj.whs_no = whs_instance
        bin_obj.bin_id = bin_id_input
        bin_obj.bin_type = bin_type
        bin_obj.capacity = capacity
        bin_obj.category = category_instance
        bin_obj.subcategory = subcategory_instance
        bin_obj.save()

        return redirect('bin_detail', bin_id=bin_obj.id)

    return render(request, 'bin/bin_edit.html', {
        'bin': bin_obj,
        'categories': categories,
    })


# -----------------
# VENDOR
# -----------------

def task(request):
    return render(request, 'rf_pick_to_light/task_solving.html')




# def add_category(request):
#     if request.method == "POST":
#         try:
#             category_name = request.POST.get("category")
#             description = request.POST.get("description")

#             category = Category.objects.create(
#                 category=category_name,
#                 description=description
#             )

#             # Subcategories
#             subcategories = []
#             for key, value in request.POST.items():
#                 if key.startswith("sub_category_") and value.strip():
#                     subcat = SubCategory.objects.create(
#                         category=category,
#                         name=value.strip()
#                     )
#                     subcategories.append(subcat.name)

#             return JsonResponse({
#                 "success": True,
#                 "id": category.id,
#                 "category": category.category,
#                 "subcategories": subcategories
#             })

#         except Exception as e:
#             return JsonResponse({"success": False, "message": str(e)})

#     return JsonResponse({"success": False, "message": "Invalid request"})

# def get_subcategories(request, category_id):
#     category = get_object_or_404(Category, id=category_id)
#     subcategories = list(category.subcategories.values("id", "name"))
#     return JsonResponse({"subcategories": subcategories})

# def load_subcategories(request):
#     category_id = request.GET.get("category_id")
#     subcategories = SubCategory.objects.filter(category_id=category_id).values("id", "name")
#     return JsonResponse({"subcategories": list(subcategories)})





def add_vendor(request, vendor_id=None):
    vendor = None
    if vendor_id:
        vendor = get_object_or_404(Vendor, vendor_id=vendor_id)

    form = VendorForm(request.POST or None, request.FILES or None, instance=vendor)

    if request.method == 'POST' and form.is_valid():
        saved_vendor = form.save()
        return redirect('vendor_detail', vendor_id=saved_vendor.vendor_id)

    search_query = request.GET.get('search', '')
    if search_query:
        vendors = Vendor.objects.filter(
            Q(vendor_id__icontains=search_query) |
            Q(name__icontains=search_query)
        )
    else:
        vendors = Vendor.objects.all()  

    context = {
        'form': form,
        'vendors': vendors,
        'vendor': vendor,
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
    if request.method == "POST":
        vendor.delete()
        return redirect('vendor_list')
    return redirect('vendor_list')


def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor/vendor_list.html', {'vendors': vendors})


def vendor_delete(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    vendor.delete()
    return redirect('vendor_list')


# ----------------
# PUTAWAY
# ----------------

def putaway_task(request):
    products = Product.objects.all()
    warehouses = Warehouse.objects.all()
    bins = Bin.objects.all()
    pallets = Pallet.objects.all()

    if request.method == "POST":
        pallet_id = request.POST.get("pallet")
        source_location = request.POST.get("source_location")
        destination_location = request.POST.get("destination_location")
        putaway_task_type = request.POST.get("putaway_task_type")
        status = request.POST.get("status")
        warehouse_id = request.POST.get("whs_no")
        product_id = request.POST.get("product")
        bin_id = request.POST.get("bin")

        putaway = Putaway(
            source_location=source_location,
            destination_location=destination_location,
            putaway_task_type=putaway_task_type,
            status=status,
            created_by=request.user.username if request.user.is_authenticated else "System",
            updated_by=request.user.username if request.user.is_authenticated else "System",
            putaway_id=f"PUT-{now().strftime('%Y%m%d%H%M%S')}",  # optional: auto-generate ID
        )

        if pallet_id:
            putaway.pallet_id = pallet_id
        if warehouse_id:
            putaway.warehouse_id = warehouse_id
        if product_id:
            putaway.product_id = product_id
        if bin_id:
            putaway.bin_id = bin_id

        putaway.save()
        messages.success(request, "Putaway task created successfully.")
        return redirect("putaway_pending")

    temp_putaway_id = f"PUT-{now().strftime('%Y%m%d%H%M%S')}"


    context = {
        "putaway_id": temp_putaway_id,
        "products": products,
        "warehouses": warehouses,
        "bins": bins,
        "pallets": pallets,
    }
    return render(request, "putaway/putaway_task.html", context)



def putaway_pending(request):
    pending_tasks = Putaway.objects.filter(status__iexact="In Progress").order_by("putaway_id")
    return render(request, "putaway/pending_task.html", {"pending_tasks": pending_tasks})

def edit_putaway(request, putaway_id):
    putaway = get_object_or_404(Putaway, putaway_id=putaway_id)
    pallets = Pallet.objects.all()

    if request.method == "POST":
        pallet_id = request.POST.get("pallet")
        if pallet_id:
            putaway.pallet = Pallet.objects.get(id=pallet_id)
        else:
            putaway.pallet = None

        putaway.source_location = request.POST.get("source_location")
        putaway.destination_location = request.POST.get("destination_location")
        putaway.putaway_task_type = request.POST.get("putaway_task_type")
        putaway.status = request.POST.get("status")
        putaway.updated_by = request.user.username if request.user.is_authenticated else "System"

        putaway.save()
        messages.success(request, "Putaway task updated successfully.")
        return redirect("putaway_pending")

    return render(
        request,
        "putaway/edit_putaway.html",
        {"putaway": putaway, "pallets": pallets} 
    )

def confirm_putaway(request, putaway_id):
    putaway = get_object_or_404(Putaway, putaway_id=putaway_id)
    if putaway.status == "In Progress":
        putaway.status = "Completed"
        putaway.confirmed_at = now()  
    else:
        putaway.status = "In Progress"
        putaway.confirmed_at = None  

    putaway.updated_by = request.user.username if request.user.is_authenticated else "System"
    putaway.save()

    messages.info(request, f"Putaway {putaway.putaway_id} status updated.")
    return redirect("all_tasks")

def delete_putaway(request, putaway_id):
    task = get_object_or_404(Putaway, putaway_id=putaway_id)
    task.delete()
    messages.success(request, "Putaway task deleted successfully.")
    return redirect("all_tasks")


from .models import Warehouse 

def whs_suggestions(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        warehouses = Warehouse.objects.filter(whs_no__icontains=query)[:10]
        results = [{'whs_no': w.whs_no} for w in warehouses]

    return JsonResponse({'results': results})

def truck_suggestions(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        trucks = Truck.objects.filter(truck_no__icontains=query)[:10]
        results = [{'truck_no': t.truck_no} for t in trucks]

    return JsonResponse({'results': results})

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




def whs_suggestions(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        whs_list = Warehouse.objects.filter(whs_no__icontains=query).values_list('whs_no', flat=True).distinct()[:10]
        results = [{'whs_no': wh} for wh in whs_list]

    return JsonResponse({'results': results})



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
from django.shortcuts import render, get_object_or_404, redirect
from .models import Picking
from .forms import PickingForm

# 🔹 Add Picking
def add_picking(request):
    if request.method == "POST":
        form = PickingForm(request.POST)
        if form.is_valid():
            picking = form.save(commit=False)
            # Set created_by and updated_by automatically
            picking.created_by = request.user.username if request.user.is_authenticated else "System"
            picking.updated_by = request.user.username if request.user.is_authenticated else "System"
            picking.confirmed_at = None  # Initially not confirmed
            picking.save()
            return redirect("pending_task")
    else:
        form = PickingForm()

    return render(request, "picking/add_picking.html", {"form": form})


# 🔹 Show Pending Pickings
def pending_task(request):
    pending_picking = Picking.objects.filter(status__iexact="In Progress").order_by("picking_id")
    return render(request, "picking/picking_pending_task.html", {"pending_picking": pending_picking})


# 🔹 Edit Picking
def edit_picking(request, picking_id):
    picking = get_object_or_404(Picking, picking_id=picking_id)
    if request.method == "POST":
        form = PickingForm(request.POST, instance=picking)
        if form.is_valid():
            picking = form.save(commit=False)
            # Update only updated_by
            picking.updated_by = request.user.username if request.user.is_authenticated else "System"
            picking.save()
            return redirect("pending_task")
    else:
        form = PickingForm(instance=picking)

    return render(request, "picking/edit_picking.html", {"form": form, "picking": picking})


# 🔹 Confirm / Toggle Picking Status
def confirm_picking(request, picking_id):
    picking = get_object_or_404(Picking, picking_id=picking_id)

    if picking.status == "In Progress":
        picking.status = "Completed"
    else:
        picking.status = "In Progress"

    # Track who updated it
    picking.updated_by = request.user.username if request.user.is_authenticated else "System"
    picking.confirmed_at = now() if picking.status == "Completed" else None
    picking.save()

    return redirect("all_tasks")


# 🔹 Delete Picking
def delete_picking(request, picking_id):
    picking = get_object_or_404(Picking, picking_id=picking_id)
    picking.delete()
    return redirect("all_tasks")

def customer(request):
    products = Product.objects.all()  
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
        supplier_obj = Vendor.objects.filter(pk=vendor_id).first()

        delivery_date = parse_date(request.POST.get('delivery_date')) or None
        document_date = parse_date(request.POST.get('document_date')) or None

        delivery = InboundDelivery.objects.create(
            inbound_delivery_number=inbound_delivery_number,
            delivery_date=delivery_date,
            document_date=document_date,
            supplier=supplier_obj,
            purchase_order_number_id=request.POST.get('po_number'),
            whs_no_id=request.POST.get('whs_no'),
            delivery_status=request.POST.get('delivery_status'),
            remarks=request.POST.get('remarks')
        )

        product_ids = request.POST.getlist('product[]')
        qty_delivered = request.POST.getlist('quantity_delivered[]')
        qty_received = request.POST.getlist('quantity_received[]')
        unit_of_measure = request.POST.getlist('unit_of_measure[]')
        batch_number = request.POST.getlist('batch_number[]')

        for i in range(len(product_ids)):
            pid = product_ids[i].strip()
            if not pid:
                continue

            try:
                product_obj = Product.objects.get(product_id=pid)
            except Product.DoesNotExist:
                continue

            # Create inbound delivery product record (no inventory update here)
            InboundDeliveryproduct.objects.create(
                delivery=delivery,
                product=product_obj,
                product_description=product_obj.name,
                quantity_delivered=int(qty_delivered[i]) if qty_delivered[i] else 0,
                quantity_received=int(qty_received[i]) if qty_received[i] else 0,
                unit_of_measure=unit_of_measure[i],
                batch_number=batch_number[i] if batch_number[i] else None
            )

        return redirect('inbound_delivery')

    return render(request, 'inbound/inbound_delivery.html', {
        'deliveries': deliveries,
        'warehouses': warehouses,
        'vendors': vendors,
        'purchase_orders': purchase_orders,
        'products': products_list
    })




def generate_inbound_delivery_number():
    return f"IBD{random.randint(1000, 9999)}"



def delivery_detail(request, inbound_delivery_number):
    delivery = get_object_or_404(InboundDelivery, inbound_delivery_number=inbound_delivery_number)

    ibdproducts = []
    for p in delivery.products.all():  
        product_obj = p.product
        ibdproducts.append({
            "product": product_obj.product_id or product_obj.name,
            "product_description": p.product_description or product_obj.name,
            "quantity_delivered": p.quantity_delivered,
            "quantity_received": p.quantity_received or 0,
            "unit_of_measure": p.unit_of_measure or product_obj.unit_of_measure or "",
            "batch_number": p.batch_number or "",
        })

    return render(request, 'inbound/delivery_detail.html', {
        'delivery': delivery,
        'ibdproducts': ibdproducts,
    })



# views.py (add this)
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import PurchaseOrder, PurchaseItem, Vendor

def get_po_products(request, po_id):
    """
    Return PO header + line items as JSON.
    Attempts to find a Vendor record matching PO.vendor_company_name;
    if found, returns vendor_id so the select can be auto-selected.
    """
    try:
        po = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return JsonResponse({"error": "PO not found"}, status=404)

    items_qs = PurchaseItem.objects.filter(purchase_order=po).select_related('product')

    products = []
    for it in items_qs:
        prod = it.product
        products.append({
            "code": prod.product_id,
            "description": prod.name,
            "quantity": int(it.quantity),
            "uom": prod.unit_of_measure or "",
        })

    # try to match vendor string to a Vendor record
    vendor_obj = None
    vendor_name = getattr(po, "vendor_company_name", "") or ""
    if vendor_name:
        vendor_obj = Vendor.objects.filter(name__iexact=vendor_name).first()

    vendor_data = {
        "vendor_id": vendor_obj.vendor_id if vendor_obj else None,
        "display": f"{vendor_obj.vendor_id} - {vendor_obj.name}" if vendor_obj else vendor_name
    }

    data = {
        "vendor": vendor_data,
        "po_date": po.po_date.strftime("%Y-%m-%d") if getattr(po, "po_date", None) else "",
        "products": products
    }
    return JsonResponse(data)



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

def po_suggestions(request):
    query = request.GET.get('q', '')
    if query:
        purchase_orders = PurchaseOrder.objects.filter(
            po_number__icontains=query  
        ).values_list('po_number', flat=True)[:10]
    else:
        purchase_orders = []

    return JsonResponse(list(purchase_orders), safe=False)  


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


def get_warehouse_address(request, whs_id):
    try:
        warehouse = Warehouse.objects.get(whs_no=whs_id)
        return JsonResponse({"address": warehouse.address})
    except Warehouse.DoesNotExist:
        return JsonResponse({"error": "Warehouse not found"}, status=404)
    

# views.py
from django.http import JsonResponse
from .models import Product

def product_autocomplete(request):
    term = request.GET.get("term", "")
    products = Product.objects.filter(name__icontains=term)[:10]  
    results = [
        {
            "id": p.product_id, 
            "name": p.name,
            "unit_price": float(p.unit_price),
            "stock": p.quantity,
            "uom": p.unit_of_measure,
        }
        for p in products
    ]
    return JsonResponse(results, safe=False)



  
from decimal import Decimal
from django.shortcuts import render, redirect
from django.db import transaction
from .models import SalesOrderCreation, SalesOrderItem, Warehouse

from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from decimal import Decimal
from .models import SalesOrderCreation, SalesOrderItem, Warehouse, Product

def generate_so_no():
    last_so = SalesOrderCreation.objects.order_by('-id').first()
    if last_so and last_so.so_no.startswith("SO"):
        last_number = int(last_so.so_no.replace("SO", ""))
        new_number = last_number + 1
    else:
        new_number = 1
    return f"SO{new_number:04d}"  



def sales_order_creation(request):
    warehouses = Warehouse.objects.all()
    product_rows = []

    if request.method == 'POST':
        try:
            # Fetch warehouse
            whs_no = request.POST.get('whs_no')
            if not whs_no:
                raise ValueError("Warehouse is required")
            warehouse = get_object_or_404(Warehouse, whs_no=whs_no)

            # Fetch product data from form
            product_ids = request.POST.getlist('product_id[]')
            product_names = request.POST.getlist('product_name[]')
            quantities = request.POST.getlist('quantity[]')
            unit_prices = request.POST.getlist('unit_price[]')

            if not product_ids:
                raise ValueError("At least one product must be added")

            net_total = Decimal(0)
            status = request.POST.get('status', 'Draft')

            with transaction.atomic():
                # Create sales order
                so_no_obj = SalesOrderCreation.objects.create(
                    whs_no=warehouse,
                    whs_address=warehouse.address,
                    customer_id=request.POST.get('customer_id'),
                    customer_code=request.POST.get('customer_code'),
                    order_date=request.POST.get('order_date'),
                    delivery_date=request.POST.get('delivery_date'),
                    status=status,
                    remarks=request.POST.get('remarks', '')
                )

                # Loop through products
                for i in range(len(product_ids)):
                    pid = product_ids[i].strip()
                    if not pid:
                        continue

                    product = get_object_or_404(Product, product_id=pid)


                    quantity = int(quantities[i])
                    unit_price = Decimal(unit_prices[i])
                    if quantity <= 0 or unit_price < 0:
                        raise ValueError(f"Invalid quantity or price for product {product.name}")

                    total_price = quantity * unit_price
                    net_total += total_price

                    # Create SalesOrderItem
                    SalesOrderItem.objects.create(
                        so_no=so_no_obj,
                        product=product,
                        product_name=product.name,
                        existing_quantity=product.quantity,
                        quantity=quantity,
                        unit_price=unit_price,
                        unit_total_price=total_price
                    )

                    product_rows.append({
                        'product': product.product_id,
                        'product_name': product.name,
                        'existing_quantity': product.quantity,
                        'quantity': quantity,
                        'unit_price': str(unit_price),
                        'unit_total_price': str(total_price)
                    })


                    # Update inventory if order is confirmed
                    if status.lower() == 'confirmed':
                        if product.quantity < quantity:
                            raise ValueError(f"Not enough stock for product {product.name}")
                        product.quantity -= quantity
                        product.save()

                # Update net total in sales order
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

    # GET request
    return render(request, 'sales/sales_order_creation.html', {
        'warehouses': warehouses,
        'product_rows': [],
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

        whs_no = request.POST.get("whs_no")
        so_obj.whs_no = get_object_or_404(Warehouse, whs_no=whs_no)
        so_obj.whs_address = getattr(so_obj.whs_no, 'address', "Unknown")

        so_obj.customer_id = request.POST.get("customer_id")
        so_obj.customer_code = request.POST.get("customer_code")
        so_obj.order_date = request.POST.get("order_date")
        so_obj.delivery_date = request.POST.get("delivery_date")
        so_obj.remarks = request.POST.get("remarks")
        so_obj.status = request.POST.get("status") or "Draft"
        so_obj.save()

        # Delete existing items and re-add
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
                            product_obj = Product.objects.get(product_id=product_ids[i])
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



def get_total_quantity(request, product_id):
    from .models import Inventory
    try:
        inventory = Inventory.objects.get(product__product_id=product_id)
        return JsonResponse({"total_quantity": inventory.total_quantity})
    except Inventory.DoesNotExist:
        return JsonResponse({"total_quantity": 0})




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



def outbound_delivery_item_number():
    prefix = "OBDIN"
    last_item = OutboundDeliveryItem.objects.order_by("id").last()

    if last_item and last_item.dlv_it_no and last_item.dlv_it_no.startswith(prefix):
        last_number = int(last_item.dlv_it_no.replace(prefix, ""))
        new_number = last_number + 1
    else:
        new_number = 1

    return f"{prefix}{new_number:05d}" 






# Example outbound delivery number generator
def generate_outbound_delivery_number():
    last = OutboundDelivery.objects.order_by("id").last()
    next_id = last.id + 1 if last else 1
    return f"OBD{str(next_id).zfill(5)}"




from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect, render
from itertools import zip_longest
from decimal import Decimal

def safe_decimal(value):
    try:
        return Decimal(value)
    except (TypeError, ValueError, InvalidOperation):
        return Decimal('0.00')

def outbound(request):
    sales_orders = SalesOrderCreation.objects.all()
    delivery_no = generate_outbound_delivery_number()

    if request.method == "POST":
        so_id = request.POST.get("so_no")
        so_obj = get_object_or_404(SalesOrderCreation, id=so_id)

        whs_id = request.POST.get("whs_no")
        warehouse = Warehouse.objects.filter(whs_no=whs_id).first() if whs_id else None

        outbound_delivery = OutboundDelivery.objects.create(
            dlv_no=delivery_no,
            so_no=so_obj,
            whs_no=warehouse,
            whs_address=request.POST.get("whs_address") or None,
            ord_date=request.POST.get("ord_date") or None,
            del_date=request.POST.get("del_date") or None,
            sold_to=request.POST.get("customer_id"),
            ship_to=request.POST.get("ship_to"),
            cust_ref=request.POST.get("cust_ref"),
        )

        # Fetch all item lists safely
        product_ids = request.POST.getlist("product_id[]")
        product_names = request.POST.getlist("product_name[]")
        dlv_it_nos = request.POST.getlist("dlv_it_no[]")
        qty_orders = request.POST.getlist("qty_order[]")
        qty_issueds = request.POST.getlist("qty_issued[]")
        unit_prices = request.POST.getlist("unit_price[]")
        vols = request.POST.getlist("vol_per_item[]")  # optional

        # Track used dlv_it_no to prevent duplicates
        existing_numbers = set()

        i_counter = 1
        for i, (pid, pname, dlv_no_item, qty_ord, qty_iss, unit_price, vol) in enumerate(
            zip_longest(
                product_ids,
                product_names,
                dlv_it_nos,
                qty_orders,
                qty_issueds,
                unit_prices,
                vols,
                fillvalue=""
            )
        ):
            if not pid:
                continue  # skip empty row

            qty_order = safe_decimal(qty_ord)
            qty_issued = safe_decimal(qty_iss)
            unit_price = safe_decimal(unit_price)
            vol = safe_decimal(vol)

            unit_total_price = qty_issued * unit_price
            net_total_price = unit_total_price

            # Generate unique dlv_it_no
            base_no = dlv_no_item or f"{delivery_no}IN"
            while f"{base_no}{str(i_counter).zfill(2)}" in existing_numbers:
                i_counter += 1
            unique_dlv_it_no = f"{base_no}{str(i_counter).zfill(2)}"
            existing_numbers.add(unique_dlv_it_no)
            i_counter += 1

            OutboundDeliveryItem.objects.create(
                delivery=outbound_delivery,
                dlv_it_no=unique_dlv_it_no,
                product_id=pid,
                product_name=pname,
                qty_order=qty_order,
                qty_issued=qty_issued,
                unit_price=unit_price,
                unit_total_price=unit_total_price,
                net_total_price=net_total_price,
                **({"vol_per_item": vol} if hasattr(OutboundDeliveryItem, "vol_per_item") else {}),
            )

        return redirect("outbound_detail", delivery_no=delivery_no)

    return render(
        request,
        "outbound/obd.html",
        {"sales_orders": sales_orders, "delivery_no": delivery_no},
    )




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



def all_tasks(request):
    putaway_tasks = Putaway.objects.all().values(
        "putaway_id", "pallet", "source_location","destination_location","putaway_task_type", "status", "created_at", "confirmed_at"
    )
    picking_tasks = Picking.objects.all().values(
        "picking_id", "pallet", "source_location","destination_location", "product", "quantity", "picking_type", "status"
    )

    for task in putaway_tasks:
        task["task_type"] = "Putaway"
        task["task_id"] = task["putaway_id"]

    for task in picking_tasks:
        task["task_type"] = "Picking"
        task["task_id"] = task["picking_id"]

    tasks = list(chain(putaway_tasks, picking_tasks))

    tasks = sorted(
        tasks, key=lambda x: x.get("created_at") or datetime.min.replace(tzinfo=timezone.utc), reverse=True
    )
    return render(request, "tasks/list.html", {"tasks": tasks})


def putaway_detail(request, putaway_id):
    task = get_object_or_404(Putaway, putaway_id=putaway_id)
    return render(request, "putaway/putaway_detail.html", {"task": task})

def picking_detail(request, picking_id):
    task = get_object_or_404(Picking, picking_id=picking_id)
    return render(request, "picking/picking_detail.html", {"task": task})




def material_create(request):
    if request.method == "POST":
        material= request.POST.get("p_mat")
        description = request.POST.get("description")

        if material:  
            PackingMaterial.objects.create(material=material, description=description)
            messages.success(request, "Packing material created successfully!")
            return redirect("material_list")
        else:
            messages.error(request, "Material name is required.")

    return render(request, "material/mat_creation.html")



def material_list(request):
    materials = PackingMaterial.objects.all().order_by("id")
    return render(request, "material/material_list.html", {"materials": materials})


def material_edit(request, id):
    material_obj = get_object_or_404(PackingMaterial, id=id)

    if request.method == "POST":
        material = request.POST.get("material")
        description = request.POST.get("description")

        if material:
            material_obj.material = material
            material_obj.description = description
            material_obj.save()
            messages.success(request, "Packing material updated successfully!")
            return redirect("material_list")  # corrected redirect to list view
        else:
            messages.error(request, "Material name cannot be empty!")

    return render(request, "material/mat_edit.html", {"material": material_obj})


def material_delete(request, id):
    material_obj = get_object_or_404(PackingMaterial, id=id)
    material_obj.delete()
    messages.success(request, "Packing material deleted successfully!")
    return redirect("material_list")




def outbound_detail(request, delivery_no):
    outbound = get_object_or_404(OutboundDelivery, dlv_no=delivery_no)
    items = outbound.items.all() 

    return render(request, "outbound/detail.html", {
        "outbound": outbound,
        "items": items,
    })





# ---------------------------
# Post Goods Issue (PGI)
# ---------------------------

def post_goods_issue(request, delivery_no):
    # Fetch the outbound delivery
    delivery = get_object_or_404(OutboundDelivery, dlv_no=delivery_no)

    # Redirect if PGI already exists for this delivery
    if hasattr(delivery, "pgi"):
        return redirect("pgi_detail", pgi_no=delivery.pgi.pgi_no)

    if request.method == "POST":
        posted_by = request.POST.get("posted_by")
        remarks = request.POST.get("remarks")

        # Generate PGI number
        pgi_no = f"PGI{now().strftime('%Y%m%d%H%M%S')}"

        # Create PGI record
        pgi = PostGoodsIssue.objects.create(
            pgi_no=pgi_no,
            delivery=delivery,
            posted_by=posted_by,
            remarks=remarks,
        )

        # Reduce inventory for each delivery item
        for item in delivery.items.all():
            try:
                inventory = Inventory.objects.get(product=item.product_id)
                inventory.total_quantity -= item.qty_issued
                if inventory.total_quantity < 0:
                    inventory.total_quantity = 0
                inventory.save()
            except Inventory.DoesNotExist:
                # If no inventory exists, create one with 0 quantity
                Inventory.objects.create(product=item.product_id, total_quantity=0)

        return redirect("pgi_detail", pgi_no=pgi.pgi_no)

    return render(request, "pgi/create.html", {"delivery": delivery})



def pgi_detail(request, pgi_no):
    pgi = get_object_or_404(PostGoodsIssue, pgi_no=pgi_no)
    items = []

    for item in pgi.delivery.items.all():
        # Get current inventory
        try:
            inventory = Inventory.objects.get(product=item.product_id)
            current_qty = inventory.total_quantity
        except Inventory.DoesNotExist:
            current_qty = 0

        # Add warning flag
        low_stock = current_qty < item.qty_issued

        items.append({
            "dlv_it_no": item.dlv_it_no,
            "product_name": item.product_name,
            "qty_order": item.qty_order,
            "qty_issued": item.qty_issued,
            "unit_price": item.unit_price,
            "unit_total_price": item.unit_total_price,
            "net_total_price": item.net_total_price,
            "vol_per_item": getattr(item, "vol_per_item", ""),
            "current_qty": current_qty,
            "low_stock": low_stock,
        })

    return render(request, "pgi/detail.html", {"pgi": pgi, "items": items})



def pgi_list(request):
    # Fetch all PGI records, newest first
    pgi_records = PostGoodsIssue.objects.select_related('delivery').order_by('-posting_date')
    return render(request, "pgi/list.html", {"pgi_records": pgi_records})
  

# ---------------------------
# Goods Receipt (GR)
# ---------------------------
def goods_receipt(request, inbound_no):
    inbound = get_object_or_404(InboundDelivery, inbound_delivery_number=inbound_no)

    if hasattr(inbound, "gr"):
        return redirect("gr_detail", gr_no=inbound.gr.gr_no)

    if request.method == "POST":
        posted_by = request.POST.get("posted_by")
        remarks = request.POST.get("remarks")

        gr_no = f"GR{now().strftime('%Y%m%d%H%M%S')}"
        gr = GoodsReceipt.objects.create(
            gr_no=gr_no,
            inbound_delivery=inbound,
            posted_by=posted_by,
            remarks=remarks,
        )

        # 🔼 Increase Inventory for each inbound item
        for item in inbound.items.all():
            inventory, created = Inventory.objects.get_or_create(
                product=item.product,
                defaults={"total_quantity": 0}
            )
            inventory.total_quantity += item.quantity
            inventory.save()

        return redirect("gr_detail", gr_no=gr.gr_no)

    return render(request, "gr/confirm.html", {"inbound": inbound})



def gr_detail(request, gr_no):
    gr = get_object_or_404(GoodsReceipt, gr_no=gr_no)
    return render(request, "gr/detail.html", {"gr": gr})



def create_gr(request):
    if request.method == "POST":
        form = GoodsReceiptForm(request.POST)
        if form.is_valid():
            gr = form.save(commit=False)

            # Auto-generate GR number (your model's save() already handles it)
            gr.save()

            # Loop over inbound delivery products & create GR items
            inbound_items = InboundDeliveryproduct.objects.filter(delivery=gr.inbound_delivery)

            for inbound_item in inbound_items:
                # Create GR item record
                gr_item = GoodsReceiptItem.objects.create(
                    goods_receipt=gr,
                    inbound_delivery_product=inbound_item,
                    quantity_received=inbound_item.quantity_received,
                    batch_number=inbound_item.batch_number or str(uuid.uuid4())[:8]
                )

                # ✅ Update Inventory here
                inventory, created = Inventory.objects.get_or_create(product=inbound_item.product)
                inventory.total_quantity += inbound_item.quantity_received
                inventory.save()

            messages.success(request, f"Goods Receipt {gr.gr_no} created and inventory updated!")
            return redirect('inventory')

    else:
        form = GoodsReceiptForm()

    # Show inbound deliveries without GR yet
    pending_deliveries = InboundDelivery.objects.filter(gr__isnull=True)

    return render(
        request,
        'gr/create_gr.html',
        {
            'form': form,
            'pending_deliveries': pending_deliveries
        }
    )


 

def gr_list(request):
    search_query = request.GET.get('q', '')
    gr_list = GoodsReceipt.objects.all().order_by('-posting_date')
    if search_query:
        gr_list = gr_list.filter(gr_no__icontains=search_query)
    paginator = Paginator(gr_list, 10)  # 10 per page
    page = request.GET.get('page')
    gr_list = paginator.get_page(page)
    
    return render(request, 'gr/gr_list.html', {'gr_list': gr_list, 'search_query': search_query})



def search(request):
    query = request.GET.get("q", "")

    results = {
        "features": [],
        "trucks": [],
        "products": [],
        "warehouses": [],
        "customers": [],
        "vendors": [],
    }

    if query:
        # Static features
        features = [
            {"name": "Yard Check-In", "url": "one"},
            {"name": "Check Status", "url": "truck_list"},
            {"name": "Stock Upload", "url": "#"},
            {"name": "RF Dispatch", "url": "#"},
            {"name": "Pallet Labels", "url": "#"},
        ]
        results["features"] = [f for f in features if query.lower() in f["name"].lower()]

        # Trucks
        results["trucks"] = Truck.objects.filter(
            truck_no__icontains=query
        )

        # Products
        results["products"] = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

        # Warehouses
        results["warehouses"] = Warehouse.objects.filter(
            Q(whs_name__icontains=query) | Q(whs_no__icontains=query)
        )

        # Customers
        results["customers"] = Customers.objects.filter(
            Q(name__icontains=query) | Q(customer_id__icontains=query)
        )

        # Vendors
        results["vendors"] = Vendor.objects.filter(
            Q(name__icontains=query) | Q(vendor_id__icontains=query)
        )

    return render(request, "search.html", {"query": query, "results": results})




import csv
from django.contrib import messages
from django.shortcuts import redirect
from .models import Bin, Warehouse, Category, SubCategory
def bulk_upload_bins(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]

        if not csv_file.name.endswith(".csv"):
            messages.error(request, "File must be a CSV.")
            return redirect("create_bin")

        try:
            file_data = csv_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(file_data)
        except Exception:
            messages.error(request, "Invalid CSV format.")
            return redirect("create_bin")

        created, skipped = 0, 0
        for row in reader:
            try:
                warehouse_code = row.get("Warehouse")
                bin_id = row.get("Bin ID")
                bin_type = row.get("Bin Type")
                capacity = int(row.get("Capacity", 0))
                existing_quantity = int(row.get("Existing Quantity", 0))
                category_name = row.get("Category")
                subcategory_name = row.get("Sub Category")

                if not (warehouse_code and bin_id and category_name and subcategory_name):
                    raise ValueError("Missing required fields")

                # ✅ Get or create Warehouse
                warehouse, _ = Warehouse.objects.get_or_create(whs_no=warehouse_code)

                # ✅ Get or create Category
                category, _ = Category.objects.get_or_create(category=category_name)

                # ✅ Get or create Subcategory
                subcategory, _ = SubCategory.objects.get_or_create(
                    name=subcategory_name, category=category
                )

                # ✅ Create Bin with audit info
                Bin.objects.create(
                    whs_no=warehouse,
                    bin_id=bin_id,
                    bin_type=bin_type,
                    capacity=capacity,
                    existing_quantity=existing_quantity,
                    category=category,
                    sub_category=subcategory,
                    created_by=request.user.username if request.user.is_authenticated else "system",
                    updated_by=request.user.username if request.user.is_authenticated else "system",
                )
                created += 1
            except Exception as e:
                print("Skipping row:", row, "Error:", e)
                skipped += 1

        messages.success(request, f"Uploaded {created} bins, skipped {skipped}.")
        return redirect("create_bin")

    return redirect("create_bin")

 
from .models import Profile
 
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "Please enter both username and password")
            return redirect("login")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "account/login.html")

@login_required
def profile_detail_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    return render(request, "account/profile_detail.html", {
        "user": user,
        "profile": profile,
    })
    
@login_required
def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.email = request.POST.get("email", user.email)
        profile.phone = request.POST.get("phone", profile.phone)
        profile.company_name = request.POST.get("company_name", profile.company_name)
        warehouse_id = request.POST.get("warehouse")
        if warehouse_id:
            profile.warehouse = Warehouse.objects.get(id=warehouse_id)
        else:
            profile.warehouse = None
        if "image" in request.FILES:
            profile.image = request.FILES["image"]

        user.save()
        profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("profile_detail")
    warehouses = Warehouse.objects.all()
    return render(request, "account/profile_edit.html", {
        "profile": profile,
        "warehouses": warehouses,
    })

@login_required
def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = request.user
        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect("change_password")
        if new_password != confirm_password:
            messages.error(request, "New password and Confirm password do not match.")
            return redirect("change_password")

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        messages.success(request, "Your password has been changed successfully.")
        return redirect("profile_detail")

    return render(request, "account/change_password.html")

def logout_view(request):
    logout(request)
    return render(request, "account/logout.html")

def bulk_upload_bins(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]

        if not csv_file.name.endswith('.csv'):
            messages.error(request, "File must be a CSV.")
            return redirect("create_bin")

        file_data = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(file_data)

        created, skipped = 0, 0
        for row in reader:
            try:
                warehouse_code = row["Warehouse"]
                bin_id = row["Bin ID"]
                bin_type = row["Bin Type"]
                capacity = row["Capacity"]
                existing_quantity = row.get("Existing Quantity", 0)
                category_name = row["Category"]
                subcategory_name = row["Sub Category"]

                # ✅ Get or create Warehouse
                warehouse, _ = Warehouse.objects.get_or_create(whs_no=warehouse_code)

                # ✅ Get or create Category
                category, _ = Category.objects.get_or_create(category=category_name)

                # ✅ Get or create Subcategory
                subcategory, _ = SubCategory.objects.get_or_create(
                    name=subcategory_name, category=category
                )

                # ✅ Create Bin
                Bin.objects.create(
                    whs_no=warehouse,
                    bin_id=bin_id,
                    bin_type=bin_type,
                    capacity=capacity,
                    existing_quantity=existing_quantity,
                    category=category,
                    sub_category=subcategory,
                )
                created += 1
            except Exception as e:
                print("Skipping row:", row, "Error:", e)
                skipped += 1

        messages.success(request, f"Uploaded {created} bins, skipped {skipped}.")
        return redirect("create_bin")

    return redirect("create_bin")



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile, Warehouse

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile, Warehouse

def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        company_name = request.POST.get('company_name')
        warehouse_id = request.POST.get('warehouse')
        image = request.FILES.get('image')

        # Create User safely
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        warehouse = Warehouse.objects.get(whs_no=warehouse_id) if warehouse_id else None

        # Create Profile
        Profile.objects.create(
            user=user,
            phone=phone,
            company_name=company_name,
            warehouse=warehouse,
            image=image
        )

        return redirect('user_list')
    if request.user.is_superuser:
        warehouses = Warehouse.objects.all()
    else:

        profile = getattr(request.user, "profile", None)
        if profile and profile.warehouse:
            warehouses = Warehouse.objects.filter(whs_no=profile.warehouse.whs_no)
        else:
            warehouses = Warehouse.objects.none() 

    return render(request, 'account/add_user.html', {'warehouses': warehouses})

# User Detail
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'account/user_detail.html', {'user': user})


# Edit User
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        profile.phone = request.POST.get('phone')
        profile.company_name = request.POST.get('company_name')

        warehouse_id = request.POST.get('warehouse')
        profile.warehouse = Warehouse.objects.get(pk=warehouse_id) if warehouse_id else None

        if request.FILES.get('image'):
            profile.image = request.FILES['image']

        profile.save()
        return redirect('user_detail', user_id=user.id)

    warehouses = Warehouse.objects.all()
    return render(request, 'account/edit_user.html', {'user': user, 'warehouses': warehouses})


# Delete User
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_list')


# User List
def user_list(request):
    users = User.objects.all().select_related('profile')
    return render(request, 'account/user_list.html', {'users': users})


def get_po_products(request, po_id):
    try:
        items = PurchaseItem.objects.filter(purchase_order_id=po_id)
        products = []

        for item in items:
            product = item.product
            products.append({
                "code": getattr(product, "code", product.name),  # fallback to name if code not exist
                "description": product.name,
                "quantity": item.quantity,
                "uom": getattr(product, "unit_of_measure", ""),  # make sure Product model has uom
            })

        return JsonResponse({"products": products})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



def all_putaway_tasks(request):
    """
    View to display all putaway tasks in a table.
    """
    tasks = Putaway.objects.all().order_by('-created_at')  # newest first
    context = {'tasks': tasks }
    return render(request, 'putaway/all_tasks.html', context)


def get_product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return JsonResponse({
        "total_quantity": product.quantity,   
        "unit_price": str(product.unit_price)
    })



def outbound_list(request):
    deliveries = OutboundDelivery.objects.all().order_by('-id')  # latest first
    return render(request, "outbound/list.html", {"deliveries": deliveries})

def superadmin_base_view(request):
  return redirect("superadmin_dashboard")

def superadmin_dashboard(request):
    return render(request, "account/superadmin_dashboard.html")

# ----------
# Category Creation
# ----------

# views.py
from django.shortcuts import render, redirect
from .forms import CategoryForm
from .models import Category, SubCategory

def create_category_with_subcategories(request):
    success_message = ''
    
    if request.method == 'POST':
        category_form = CategoryForm(request.POST)
        subcategories = []
        for key, value in request.POST.items():
            if key.startswith('sub_category_') and value.strip():
                subcategories.append(value.strip())

        if category_form.is_valid():
            category_obj = category_form.save(commit=False)
            category_obj.created_by = request.user.username  # Optional
            category_obj.save()

            # Save subcategories linked to this category
            for subcat_name in subcategories:
                SubCategory.objects.create(category=category_obj, name=subcat_name)

            success_message = "Category and Subcategories created successfully!"
            category_form = CategoryForm()  # Reset form after success

    else:
        category_form = CategoryForm()

    context = {
        'category_form': category_form,
        'success_message': success_message,
    }
    return render(request, 'category/create_category.html', context)


from django.shortcuts import render
from .models import Category

def category_list_view(request):
    categories = Category.objects.all().order_by('-created_at')
    return render(request, 'category/list_of_category.html', {'categories': categories})

from django.shortcuts import redirect, get_object_or_404
from .models import Category

def delete_category_view(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('category_list')

from django.shortcuts import get_object_or_404, redirect
from .models import Category

def edit_category_view(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.category = request.POST.get('category')
        category.description = request.POST.get('description')
        category.save()
    return redirect('category_list')

# ---------------
# shipment
# ---------------   
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Shipment

from django.shortcuts import render


@login_required
def shipment_dashboard(request):
    shipments = Shipment.objects.all().order_by('-created_at')
    return render(request, 'shipment/shipment_dashboard.html', {'shipments': shipments})



import datetime
import random
from django.utils.crypto import get_random_string

import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from .models import Shipment, Truck, YardHdr

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Shipment, Truck, YardHdr
from django.db import IntegrityError




from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Shipment, Truck, YardHdr, PostGoodsIssue

def add_shipment(request):
    available_trucks = Truck.objects.all()
    yards = YardHdr.objects.all()
    unassigned_pgis = PostGoodsIssue.objects.filter(shipment__isnull=True)

    if request.method == 'POST':
        truck_id = request.POST.get('truck_number')
        yard_id = request.POST.get('yard')
        planned_dispatch = request.POST.get('planned_dispatch')
        status = request.POST.get('status')
        selected_pgis = request.POST.getlist('pgis')  # List of selected PGI IDs

        try:
            truck = Truck.objects.get(id=truck_id)
            yard_hdr = YardHdr.objects.get(id=yard_id)

            shipment_no = f"SHIP-{Shipment.objects.count() + 1:05d}"

            shipment = Shipment.objects.create(
                shipment_no=shipment_no,
                truck=truck,
                yard_hdr=yard_hdr,
                planned_dispatch_date=planned_dispatch,
                shipment_status=status,
                created_by=request.user.username if request.user.is_authenticated else 'admin'
            )

            # Link selected PGIs to the created Shipment
            PostGoodsIssue.objects.filter(id__in=selected_pgis).update(shipment=shipment)

            messages.success(request, 'Shipment added successfully, and PGIs linked.')
            return redirect('shipment_dashboard')

        except Truck.DoesNotExist:
            messages.error(request, 'Invalid Truck selected.')
        except YardHdr.DoesNotExist:
            messages.error(request, 'Invalid Yard selected.')
        except IntegrityError as e:
            messages.error(request, f'Database error: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    context = {
        'available_trucks': available_trucks,
        'yards': yards,
        'unassigned_pgis': unassigned_pgis,
    }
    return render(request, 'shipment/add_shipment.html', context)



from django.shortcuts import render, get_object_or_404
from .models import Shipment

def shipment_detail(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    # Get all PGIs linked to this shipment
    linked_pgis = PostGoodsIssue.objects.filter(shipment=shipment)

    context = {
        'shipment': shipment,
        'linked_pgis': linked_pgis
    }
    return render(request, 'shipment/shipment_detail.html', context)


def edit_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    
    available_trucks = Truck.objects.all()
    yards = YardHdr.objects.all()

    # Fetch PGIs that are not assigned to other shipments OR currently linked to this shipment
    unassigned_pgis = PostGoodsIssue.objects.filter(
        Q(shipment__isnull=True) | Q(shipment=shipment)
    )

    if request.method == 'POST':
        truck_id = request.POST.get('truck_number')
        yard_id = request.POST.get('yard')
        planned_dispatch = request.POST.get('planned_dispatch')
        status = request.POST.get('status')
        selected_pgis = request.POST.getlist('pgis')

        try:
            truck = Truck.objects.get(id=truck_id)
            yard_hdr = YardHdr.objects.get(id=yard_id)

            # Update shipment
            shipment.truck = truck
            shipment.yard_hdr = yard_hdr
            shipment.planned_dispatch_date = planned_dispatch
            shipment.shipment_status = status
            shipment.save()

            # Update PGIs: first unlink all PGIs currently linked
            PostGoodsIssue.objects.filter(shipment=shipment).update(shipment=None)
            # Link selected PGIs to this shipment
            PostGoodsIssue.objects.filter(id__in=selected_pgis).update(shipment=shipment)

            messages.success(request, 'Shipment updated successfully.')
            return redirect('shipment_dashboard')

        except Truck.DoesNotExist:
            messages.error(request, 'Invalid Truck selected.')
        except YardHdr.DoesNotExist:
            messages.error(request, 'Invalid Yard selected.')
        except IntegrityError as e:
            messages.error(request, f'Database error: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    context = {
        'shipment': shipment,
        'available_trucks': available_trucks,
        'yards': yards,
        'unassigned_pgis': unassigned_pgis
    }
    return render(request, 'shipment/edit_shipment.html', context)


from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def delete_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    try:
        shipment.delete()
        messages.success(request, 'Shipment deleted successfully.')
    except Exception as e:
        messages.error(request, f'Error deleting shipment: {str(e)}')
    return redirect('shipment_dashboard')


from .forms import SortingForm
from .models import Sorting, SalesOrderCreation, OutboundDelivery
from django.utils.timezone import now
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from .models import SalesOrderCreation, OutboundDelivery, Sorting
from .forms import SortingForm


def create_sorting(request):
    sales_orders = SalesOrderCreation.objects.all()
    delivery_no = f"OD{now().strftime('%Y%m%d%H%M%S')}"

    if request.method == "POST":
        so_no = request.POST.get("so_no")  # Selected SalesOrder ID from dropdown
        so_obj = get_object_or_404(SalesOrderCreation, pk=so_no)
        warehouse = so_obj.whs_no

        # Step 1: Create OutboundDelivery linked to SalesOrder
        outbound_delivery = OutboundDelivery.objects.create(
            dlv_no=delivery_no,
            so_no=so_obj,  # Assign SalesOrder instance
            whs_no=warehouse,
            whs_address=so_obj.whs_address,
            ord_date=so_obj.order_date,
            del_date=so_obj.delivery_date,
            sold_to=so_obj.customer_id,
        )

        form = SortingForm(request.POST)
        if form.is_valid():
            sorting = form.save(commit=False)
            sorting.outbound = outbound_delivery  #
            sorting.so_no = so_obj               
            sorting.warehouse = warehouse  
            if not sorting.location:
              sorting.location = warehouse.default_location       
            if request.user.is_authenticated:
                sorting.created_by = request.user.username
                sorting.updated_by = request.user.username 
            sorting.save()
            return redirect("sorting_detail", id=sorting.id)
        else:
            # Handle invalid form
            return render(
                request,
                "sorting/create_sorting_task.html",
                {
                    "form": form,
                    "sales_orders": sales_orders,
                    "delivery_no": delivery_no,
                    "error": "Please correct the errors below.",
                }
            )

    else:
        form = SortingForm()

    return render(
        request,
        "sorting/create_sorting_task.html",
        {
            "form": form,
            "sales_orders": sales_orders,
            "delivery_no": delivery_no,
        }
    )



def sorting_detail(request, id):
    sorting = get_object_or_404(Sorting, pk=id)
    return render(request, "sorting/sorting_detail.html", {"sorting": sorting})

def sorting_edit(request, id):
    sorting = get_object_or_404(Sorting, pk=id)

    if request.method == "POST":
        form = SortingForm(request.POST, instance=sorting)
        if form.is_valid():
            updated_sorting = form.save(commit=False)
            updated_sorting.so_no = sorting.so_no
            updated_sorting.outbound = sorting.outbound
            if request.user.is_authenticated:
                updated_sorting.updated_by = request.user.username
            updated_sorting.save()
            return redirect("sorting_detail", id=updated_sorting.id)
    else:
        form = SortingForm(instance=sorting)

    return render(
        request,
        "sorting/sorting_edit.html",
        {"form": form, "sorting": sorting},
    )

def sorting_list(request):
    sortings = Sorting.objects.all().order_by('location', '-sorted_at')
    return render(request, "sorting/sorting_list.html", {"sortings": sortings})


def delete_sorting(request, id):
    sorting = get_object_or_404(Sorting, pk=id)
    try:
        sorting.delete()
        messages.success(request, 'Sorting task deleted successfully.')
    except Exception as e:
        messages.error(request, f'Error deleting sorting task: {str(e)}')
    return redirect('sorting_list')


from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Bin, BinLog
@login_required
def bin_log_view(request):
    # Get the bin ID from the query string
    bin_id_query = request.GET.get('bin_id', '').strip()
    
    logs = []
    bin_details = None
    error_message = ""

    if bin_id_query:
        try:
            # Get the Bin object by bin_id (case-insensitive)
            bin_details = Bin.objects.get(bin_id__iexact=bin_id_query)
            
            # Get related logs, ordered newest first
            logs = BinLog.objects.filter(bin=bin_details).order_by('-created_at')

        except Bin.DoesNotExist:
            error_message = f"No bin found with ID: {bin_id_query}"

    context = {
        'logs': logs,
        'bin_id_query': bin_id_query,  # used in template search box
        'bin_details': bin_details,
        'error_message': error_message,
    }

    return render(request, 'bin/bin_log.html', context)