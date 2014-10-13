import datetime

import DateUtils as DU

class Unavailable(object):
    def __init__(self, file_name):
        with open(file_name) as fp:
            unavail_lines = fp.read().splitlines()

        unavail_lines = [x.strip() for x in unavail_lines if x.strip()
                   and not (x.strip().startswith("#") or
                   x.strip().startswith("//"))]

        self.specific_dates = set()
        self.weekdays = set()

        for line in unavail_lines:
            try:
                self.specific_dates |= set([DU.str_to_date(x.strip()) for
                                            x in line.split(',')])
            except ValueError:
                lower_line = line.strip().lower()
                if lower_line.startswith('weekend'):
                    self.weekdays.add(DU.sat)
                    self.weekdays.add(DU.sun)
                elif lower_line.startswith('sunday'):
                    self.weekdays.add(DU.sun)
                elif lower_line.startswith('monday'):
                    self.weekdays.add(DU.mon)
                elif lower_line.startswith('tuesday'):
                    self.weekdays.add(DU.tue)
                elif lower_line.startswith('wednesday'):
                    self.weekdays.add(DU.wed)
                elif lower_line.startswith('thursday'):
                    self.weekdays.add(DU.thu)
                elif lower_line.startswith('friday'):
                    self.weekdays.add(DU.fri)
                elif lower_line.startswith('saturday'):
                    self.weekdays.add(DU.sat)
                else:
                    print "WARNING: UNKNOWN line, ", line


    def is_available(self, some_date):
        return (some_date not in self.specific_dates and
                some_date.weekday() not in self.weekdays)

    def reviews_possible(self,load_day, end_day, target_ratio, initial_interval):
        pass

if __name__ == '__main__':
    unavail = Unavailable("UnavailableDays.txt")
    print unavail.specific_dates
