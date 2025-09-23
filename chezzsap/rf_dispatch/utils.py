from datetime import datetime
from .models import TruckLog
from decimal import Decimal, InvalidOperation
import random

def log_truck_status(truck_instance, status, user=None, comment=''):
    # Fetch the last log entry for this truck
    last_log = TruckLog.objects.filter(truck_no=truck_instance).order_by('-truck_date', '-truck_time').first()

    # Current datetime
    now = datetime.now()

    # Default time_taken
    time_taken_str = '-'

    if last_log:
        # Combine last log's date + time into a datetime object
        last_datetime = datetime.combine(last_log.truck_date, last_log.truck_time)

        # Calculate difference
        time_diff = now - last_datetime

        # Format timedelta nicely (HH:MM:SS)
        total_seconds = int(time_diff.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_taken_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    # Create new log entry with time_taken
    TruckLog.objects.create(
        truck_no=truck_instance,
        status=status,
        status_changed_by=user,
        comment=comment,
        time_taken=time_taken_str
    )

def generate_outbound_delivery_number():
    return f"OBD{random.randint(1000, 9999)}"

def safe_decimal(value, default=0):
    try:
        return Decimal(default) if value is None or value == "" else Decimal(value)
    except (InvalidOperation, ValueError):
        return Decimal(default)
    

# utils.py (you can put inside rf_dispatch/utils.py or a common utils folder)
from .models import Bin

def generate_bin_id(whs_no=None):
    """
    Generate a unique Bin ID.
    Format:
      - BIN0001, BIN0002... if no warehouse is passed
      - WHS01-BIN0001 if warehouse is passed
    """
    if whs_no:
        last_bin = Bin.objects.filter(whs_no=whs_no).order_by('-id').first()
        if last_bin and "-" in last_bin.bin_id:
            try:
                last_num = int(last_bin.bin_id.split("-")[-1].replace("BIN", ""))
            except ValueError:
                last_num = 0
            new_num = last_num + 1
        else:
            new_num = 1
        return f"{whs_no.whs_no}-BIN{new_num:04d}"
    else:
        last_bin = Bin.objects.order_by('-id').first()
        if last_bin and last_bin.bin_id.startswith("BIN"):
            last_num = int(last_bin.bin_id.replace("BIN", ""))
            new_num = last_num + 1
        else:
            new_num = 1
        return f"BIN{new_num:04d}"

from django.utils.crypto import get_random_string
from .models import Product

def generate_product_id():
    prefix = "PRD"   # you can change to whatever prefix you want
    while True:
        random_id = prefix + get_random_string(6).upper()  # e.g. PRD4GHTY
        if not Product.objects.filter(product_id=random_id).exists():
            return random_id
