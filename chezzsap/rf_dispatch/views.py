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

def truck_inspection_view(request, truck_no):
    from .models import YardHdr
    from .forms import TruckInspectionForm

    try:
        # Get the existing truck instance
        existing_truck = YardHdr.objects.get(truck_no=truck_no)
        seal_no = existing_truck.seal_no
    except YardHdr.DoesNotExist:
        existing_truck = None
        seal_no = ''

    if request.method == 'POST':
        # Bind the form to existing instance (if it exists)
        form = TruckInspectionForm(request.POST, instance=existing_truck)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.truck_no = truck_no  # ensure truck_no is set
            if not instance.seal_no:
                instance.seal_no = seal_no  # fallback seal_no
            instance.save()
            return redirect('one')
        else:
            print(form.errors)  # debug: shows form errors
    else:
        # Load form with existing instance or initial data
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
