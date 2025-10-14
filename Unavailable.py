
import DateUtils as DU
import datetime


def block_weekly_repeats(start_day, repeat_days, duration):
    out = []
    for day in repeat_days:
        set_day = DU.get_next_weekday(day, start_day)
        out.extend(DU.get_all_weekdays_in_range(set_day, duration))
    return set(out)


class Unavailable(object):
    def __init__(self, file_name, start_day, duration):
        self.start_day = start_day
        self.duration = duration
        with open(file_name) as fp:
            unavail_lines = fp.read().splitlines()

        unavail_lines = [x.strip() for x in unavail_lines if x.strip()
                         and not (x.strip().startswith("#") or
                                  x.strip().startswith("//"))]

        self.blocked_days = set()

        for line in unavail_lines:
            try:
                days_on_line = [DU.str_to_date(x.strip()) for x in line.split(',')]
                self.blocked_days |= set(days_on_line)

                if len(days_on_line) == 2:
                    assert (days_on_line[0] < days_on_line[1])
                    first_break_day = days_on_line[0]
                    last_break_day = days_on_line[1]
                    temp_day = first_break_day
                    while temp_day < last_break_day:
                        self.blocked_days.add(temp_day)
                        temp_day += datetime.timedelta(days=1)
            except ValueError:
                lower_line = line.strip().lower()
                repeat_days = []
                if lower_line.startswith('weekend'):
                    repeat_days.append(DU.sat)
                    repeat_days.append(DU.sun)
                elif lower_line.startswith('sunday'):
                    repeat_days.append(DU.sun)
                elif lower_line.startswith('monday'):
                    repeat_days.append(DU.mon)
                elif lower_line.startswith('tuesday'):
                    repeat_days.append(DU.tue)
                elif lower_line.startswith('wednesday'):
                    repeat_days.append(DU.wed)
                elif lower_line.startswith('thursday'):
                    repeat_days.append(DU.thr)
                elif lower_line.startswith('friday'):
                    repeat_days.append(DU.fri)
                elif lower_line.startswith('saturday'):
                    repeat_days.append(DU.sat)
                else:
                    print("WARNING: UNKNOWN line, ", line)
                self.blocked_days |= block_weekly_repeats(self.start_day, repeat_days, self.duration)


if __name__ == '__main__':
    unavail = Unavailable("UnavailableDays.txt", datetime.date(2025, 9, 2), 360)
    print(sorted(unavail.blocked_days))
