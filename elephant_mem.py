import argparse
import Lessons
import Unavailable
import DateUtils as DU
import datetime


increment_map = {'WEEKLY': 7,
                 'DAILY': 1}


class elephant_memory(object):
    def __init__(self, args):
        self.day_increment = 1
        self.unavailable_file = args.unavailable

        self.lessons = Lessons.Lessons(args.lessons)
        self.unavailable = Unavailable.Unavailable(args.unavailable,
                                self.lessons.start_date, self.lessons.duration)
        self.keyword_map = {'LessonRate': self.processLessonRate,
                            'SetDay': self.processSetDay,
                            'AllowableIntroDays': self.processAllowableIntroDays}
        self.target_ratio = 1.7  # golden ratio is 1.618
        self.initial_interval = 4.0  # initial review is 4 days

    def processLessonRate(self, rate_str):
        self.day_increment = increment_map[rate_str]

    def processSetDay(self, day_str):
        new_day = DU.str_to_date(day_str)
        if new_day > self.load_day:
            self.load_day = new_day

    def processAllowableIntroDays(self, allow_str):
        allow_str.replace(',', ' ')
        days = [x.lower()[:3] for x in allow_str.split()]

    
    def reviews_possible(self, initial_day):
        lessons = []
        set_day = initial_day
        while set_day in self.unavailable.blocked_days:
            set_day = set_day + datetime.timedelta(days=1)
            if set_day > self.lessons.end_date:
                return False, []
        # Try initial review day
        repeat_day = set_day + datetime.timedelta(days=self.initial_interval)
        # if first day doesn't work, try a day previous
        if repeat_day in  self.unavailable.blocked_days:
            repeat_day =  set_day + datetime.timedelta(days=self.initial_interval - 1)
        # if that doesn't work, return, a different inital_day might work
        if repeat_day in self.unavailable.blocked_days:
            return False, []
        # at this point the inital review worked
        


    def make_schedule(self):
        self.load_day = self.lessons.start_date
        self.schedule = []

        for lesson_entry in self.lessons.lesson_lines:

            # process Keywords
            lesson_tokens = lesson_entry.split(':', 1)
            if lesson_tokens[0] in self.keyword_map:
                self.keyword_map[lesson_tokens[0]](lesson_tokens[1])
                continue

            # Now try to to develop add lessons from current load


if __name__ == '__main__':
    # command line example
    # $ python elephant_mem.py -l Lessons.txt -u UnavailableDays.txt
    
    parser = argparse.ArgumentParser(description="A script used to build a learing schedule.")
    parser.add_argument('-l', '--lessons', help='A file of list of the lessons for review')
    parser.add_argument('-u', '--unavailable', help='A file of days where review in unavailable')

    args = parser.parse_args()

    em = elephant_memory(args)

    em.make_schedule()
    print("Done")
