import datetime
import Unavailable
import DateUtils
import importlib
importlib.reload(DateUtils)


class Lessons(object):
    """ The file reads the
    """

    def __init__(self, file_name, duration=365):
        with open(file_name) as fp:
            lesson_lines = fp.read().splitlines()

        lesson_lines = [x.strip() for x in lesson_lines if x.strip() and not
                        (x.strip().startswith("#") or
                         x.strip().startswith("//"))]

        # Look for set day
        # TODO : I am not sure what constraints should be put on set day
        #        at this point, if there is at least one setday, the first
        #        will define the start.  If you have more than 1, you can move
        #        introduction days around.
        set_days = [x for x in lesson_lines if x.lower().startswith('setday')]
        if set_days:
            start_day = set_days[0].split(':')[-1].strip().replace('-', '/')
            self.start_date = DateUtils.str_to_date(start_day)
        else:
            print("WARNING: no start day set, using today's date")
            self.start_date = datetime.datetime.today()
        self.end_date = self.start_date + datetime.timedelta(duration)

        # now get just the lessons.
        self.lesson_lines = [x for x in lesson_lines
                             if not x.lower().startswith('lessonrate') and not
                             x.lower().startswith('setday') and not
                             x.lower().startswith('allowableintrodays')]

    def increment_on_success(self):
        pass

    def increment_on_failure(self):
        pass


if __name__ == '__main__':
    lessons = Lessons('Lessons.txt')
    unavailable = Unavailable.Unavailable('UnavailableDays.txt')

    print("Number of Lessons", len(lessons.lesson_lines))
