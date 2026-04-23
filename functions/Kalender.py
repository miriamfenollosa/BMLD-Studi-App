from datetime import datetime, timedelta
 
def get_current_month():
    return datetime.today().replace(day=1)
 
def next_month(date):
    if date.month == 12:
        return date.replace(year=date.year + 1, month=1)
    return date.replace(month=date.month + 1)
 
def prev_month(date):
    if date.month == 1:
        return date.replace(year=date.year - 1, month=12)
    return date.replace(month=date.month - 1)
 
def generate_calendar_days(start_date):
    start = start_date - timedelta(days=start_date.weekday())
    return [start + timedelta(days=i) for i in range(42)]