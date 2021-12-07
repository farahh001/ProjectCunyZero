import datetime

def time_to_timestamp(time):
    current_time = datetime.datetime.now()
    time = f"{time}".split(':')
    return current_time.replace(hour=int(time[0]), minute=int(time[1])).timestamp()

