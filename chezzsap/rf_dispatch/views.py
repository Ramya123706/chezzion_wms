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
from .models import YardHdr, TruckLog
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

            # ✅ Log status if changed
            if old_status != instance.truck_status:
                log_truck_status(instance, instance.truck_status, user=request.user)

            return redirect('one')
        else:
            print(form.errors)
    else:
        if existing_truck:
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





from .models import Product
from .forms import ProductForm
from django.utils import timezone

from django.shortcuts import render, redirect
from django.utils import timezone


from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Product

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
                images=images,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            return redirect('product_detail', product_id=product.product_id)
        except Exception as e:
            return render(request, 'product/add_product.html', {'error': str(e)})

    return render(request, 'product/add_product.html')



from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm
from django.contrib import messages

def product_detail(request, product_id):
   product= get_object_or_404(Product, product_id=product_id)
   return render(request, 'product/product_detail.html', {'product': product})


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
            return redirect('product_detail')
    else:
        form = ProductForm(instance=product)

    return render(request, 'product/product_edit.html', {'form': form, 'product': product})
    
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})

    

  
