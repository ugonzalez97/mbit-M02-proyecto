from datetime import datetime

def dates_are_valid(*dates):
    for date in dates:
        try:
            datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return False

    return True
