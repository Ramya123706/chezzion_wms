from .models import TruckLog
from datetime import datetime

def log_truck_status(truck_instance, status, user=None, comment=''):
    TruckLog.objects.create(
        truck_no=truck_instance,
        truck_date=datetime.today().date(),
        truck_time=datetime.today().time(),
        status=status,
        status_changed_by=user,
        comment=comment
    )
