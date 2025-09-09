from datetime import datetime
from .models import TruckLog

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
