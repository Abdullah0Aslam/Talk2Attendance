def calculate_hours(start_time, end_time):
    
    if not end_time:
        return None
    diff = end_time - start_time
    hours = diff.total_seconds() / 3600
    return round(hours, 2)

def calculate_duration(start_date, end_date):
    
    if not end_date:
        return None
    diff = end_date - start_date
    return diff.days