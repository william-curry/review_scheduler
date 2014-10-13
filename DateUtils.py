import datetime

sun, mon, tue, wed, thr, fri, sat = range(7)
day_map = dict(zip(('sun', 'mon', 'tue', 'wed', 'thr', 'fri', 'sat'),
                    range(7)))

def calc_easter(year):
    "Returns Easter as a date object."
    a = year % 19
    b = year // 100
    c = year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    month = f // 31
    day = f % 31 + 1    
    return datetime.date(year, month, day)


def str_to_date(date_str):
    try:
        return datetime.datetime.strptime(date_str,
                                            "%m/%d/%Y").date()
    except ValueError:
        return datetime.datetime.strptime(date_str,
                                            "%m/%d/%y").date()
