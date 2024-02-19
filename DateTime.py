from datetime import date, time, datetime

from dateutil.utils import today

now=datetime.combine(today, current_time)
print(now)