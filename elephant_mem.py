
import datetime
import sys
import Lessons
import Unavailable
import DateUtils as DU

reload(Lessons)
reload(Unavailable)


from datetime import date

sun, mon, tue, wed, thr, fri, sat = range(7)
day_map = dict(zip(('sun', 'mon', 'tue', 'wed', 'thr', 'fri', 'sat'),
                    range(7)))

increment_map = {'WEEKLY':7,
                 'DAILY':1}

class elephant_memory(object):
    def __init__(self):
        cmd_line = sys.argv
        self.day_increment = 1
        try:
            self.lessons_file = cmd_line[1]
        except:
            self.lessons_file = 'UnavailableDays.txt'
        try:
            self.unavailable_file = cmd_line[2]
        except:
            self.unavailable_file = 'UnavailableDays.txt'

        self.lessons = Lessons.Lessons(self.lessons_file)
        self.unavailable = Unavailable.Unavailable(self.unavailable_file)
        self.keyword_map = {'LessonRate':           self.processLessonRate,
                            'SetDay':               self.processSetDay,
                            'AllowableIntroDays':   self.processAllowableIntroDays}


    def processLessonRate(self, rate_str):
        self.day_increment = increment_map[rate_str]

    def processSetDay(self, day_str):
        new_day = DU.str_to_date(day_str)
        if new_day > self.load_day:
            self.load_day = new_day

    def processAllowableIntroDays(self, allow_str):
        allow_str.replace(',', ' ')
        days = [x.lower()[:3] for x in allow_str.split()]

    def make_schedule(self):
        self.load_day = self.lessons.start_date
        self.schedule = []

        for lesson_entry in self.lessons.lesson_lines:

            # process Keywords
            lesson_tokens = lesson_entry.split(':',1)
            if lesson_tokens[0] in self.keyword_map:
                self.keyword_map[lesson_tokens[0]](lesson_tokens[1])
                continue

            # Now try to to develope add lessons from current load



if __name__ == '__main__':
    em = elephant_memory()

    em.make_schedule()
    print "Done"


