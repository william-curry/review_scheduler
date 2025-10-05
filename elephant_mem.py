import argparse
import Lessons
import Unavailable
import DateUtils as DU


sun, mon, tue, wed, thr, fri, sat = list(range(7))
day_map = dict(list(zip(('sun', 'mon', 'tue', 'wed', 'thr', 'fri', 'sat'),
                    list(range(7)))))

increment_map = {'WEEKLY': 7,
                 'DAILY': 1}


class elephant_memory(object):
    def __init__(self, args):
        self.day_increment = 1
        self.unavailable_file = args.unavailable

        self.lessons = Lessons.Lessons(args.lessons)
        self.unavailable = Unavailable.Unavailable(args.unavailable)
        self.keyword_map = {'LessonRate': self.processLessonRate,
                            'SetDay': self.processSetDay,
                            'AllowableIntroDays': self.processAllowableIntroDays}

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
            lesson_tokens = lesson_entry.split(':', 1)
            if lesson_tokens[0] in self.keyword_map:
                self.keyword_map[lesson_tokens[0]](lesson_tokens[1])
                continue

            # Now try to to develope add lessons from current load


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A script used to build a learing schedule.")
    parser.add_argument('-l', '--lessons', help='A file of list of the lessons for review')
    parser.add_argument('-u', '--unavailable', help='A file of days where review in unavailable')

    args = parser.parse_args()

    em = elephant_memory(args)

    em.make_schedule()
    print("Done")
