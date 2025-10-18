import argparse
import Lessons
import Unavailable
import datetime
import pandas as pd
import sys


class elephant_memory(object):
    def __init__(self, args):
        self.lessons = Lessons.Lessons(args.lessons)
        self.unavailable = Unavailable.Unavailable(args.unavailable,
                                                   self.lessons.start_date, self.lessons.duration)
        self.out_filename = args.lessons.split('.')[0] + '_Schedule.csv'
        self.target_ratio = 1.7  # golden ratio is 1.618
        self.initial_interval = 4.0  # initial review is 4 days

        # placeholder variables
        self.schedule = None
        self.schedule_df = None

    def reviews_possible(self, set_day):
        lessons = []
        if set_day in self.unavailable.blocked_days:
            return []
        # Try initial review day
        repeat_day = set_day + datetime.timedelta(days=self.initial_interval)
        # if first day doesn't work, try a day previous
        if repeat_day in self.unavailable.blocked_days:
            repeat_day = set_day + \
                datetime.timedelta(days=self.initial_interval - 1)
        # if that doesn't work, return, a different inital_day might work
        if repeat_day in self.unavailable.blocked_days:
            return []
        # at this point the inital review worked

        lessons.append(set_day)
        lessons.append(repeat_day)

        previous_day = set_day
        current_day = repeat_day
        prev_interval = (current_day - previous_day).days

        while current_day < self.lessons.end_date + datetime.timedelta(days=-prev_interval):
            prev_interval = (current_day - previous_day).days
            target_interval = int(0.5 + prev_interval * self.target_ratio)
            next_day = current_day + datetime.timedelta(days=target_interval)
            while next_day in self.unavailable.blocked_days:
                next_day = next_day + datetime.timedelta(days=-1)
                if next_day <= current_day:
                    # There is a problem with the review, stop
                    return []
            previous_day = current_day
            current_day = next_day
            lessons.append(next_day)
        return lessons

    def get_next_intro_day(self, this_date):
        for i in range(7):
            next_day = this_date + datetime.timedelta(days=(i + 1))
            if next_day.weekday() in self.lessons.allowable_intro:
                return next_day

    def make_schedule(self):
        date_to_try = self.lessons.start_date
        self.schedule = []
        for lesson_entry in self.lessons.lesson_lines:

            lesson_dates = self.reviews_possible(date_to_try)
            while not lesson_dates:
                date_to_try = self.get_next_intro_day(date_to_try)
                if date_to_try > self.lessons.end_date:
                    print("Unable to schedule lesson", lesson_entry)
                    return None
                if date_to_try in self.unavailable.blocked_days:
                    continue
                lesson_dates = self.reviews_possible(date_to_try)
            # should have found lessons, date_to_try is good

            # build tuple to sort (date,  count, lesson_desciption)
            for i, review_day in enumerate(lesson_dates):
                self.schedule.append({'Date': review_day,
                                      'ReviewCount': i,
                                      'LessonDescription': lesson_entry})
            # advance to next day
            date_to_try = self.get_next_intro_day(date_to_try)
        self.schedule_df = pd.DataFrame(self.schedule)
        self.schedule_df.sort_values(by=['Date'], inplace=True)
        self.schedule_df.to_csv(self.out_filename, index=False)


if __name__ == '__main__':
    # command line example
    # $ python elephant_mem.py -l Lessons.txt -u UnavailableDays.txt

    parser = argparse.ArgumentParser(
        description="A script used to build a learing schedule.  e.g. $ python elephant_mem.py -l Lessons.txt -u UnavailableDays.txt")
    parser.add_argument('-l', '--lessons',
                        help='A file of list of the lessons for review')
    parser.add_argument('-u', '--unavailable',
                        help='A file of days where review in unavailable')

    if len(sys.argv) == 1:
        args = parser.parse_args(['--help'])
    else:
        args = parser.parse_args()

    em = elephant_memory(args)

    em.make_schedule()
    print(f"Result File: {em.out_filename}")
