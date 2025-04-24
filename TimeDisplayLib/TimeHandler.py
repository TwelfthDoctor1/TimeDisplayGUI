import datetime


def push_time():
    ctime = datetime.datetime.now()

    return f"{ctime.strftime('%I')}:{ctime.strftime('%M')}:{ctime.strftime('%S')}"
