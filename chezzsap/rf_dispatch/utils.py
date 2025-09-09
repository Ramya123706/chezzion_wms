from .models import TruckLog
from datetime import datetime
from decimal import Decimal, InvalidOperation
import random

def log_truck_status(truck_instance, status, user=None, comment=''):
    TruckLog.objects.create(
        truck_no=truck_instance,
        truck_date=datetime.today().date(),
        truck_time=datetime.today().time(),
        status=status,
        status_changed_by=user,
        comment=comment
    )

def generate_outbound_delivery_number():
    return f"OBD{random.randint(1000, 9999)}"

def safe_decimal(value, default=0):
    try:
        return Decimal(default) if value is None or value == "" else Decimal(value)
    except (InvalidOperation, ValueError):
        return Decimal(default)