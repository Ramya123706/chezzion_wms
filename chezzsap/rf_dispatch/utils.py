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