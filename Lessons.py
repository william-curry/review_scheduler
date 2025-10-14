import datetime
import DateUtils as DU


class Lessons(object):

    def __init__(self, file_name, duration=365):
        self.duration = duration
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
            self.start_date = DU.str_to_date(start_day)
        else:
            print("WARNING: no start day set, using today's date")
            self.start_date = datetime.date.today()
            
        allowable_intro_day_lines = [x for x in lesson_lines if x.lower().startswith('allowableintrodays:')]
        
        #TODO this justs looks at the first, we can update later
        if allowable_intro_day_lines:
            line = allowable_intro_day_lines[0]
            my_days = line.split(':')[-1]
            #embed()
            self.allowable_intro = [DU.day_map[x.strip().lower()] for x in my_days.split(',')]
        else:
            self.allowable_intro = [DU.mon, DU.tue, DU.wed, DU.thr, DU.fri]
            
            
        self.end_date = self.start_date + datetime.timedelta(duration)
        
        

        # now get just the lessons.
        self.lesson_lines = [x for x in lesson_lines
                             if not x.lower().startswith('lessonrate') and not
                             x.lower().startswith('setday') and not
                             x.lower().startswith('allowableintrodays')]


if __name__ == '__main__':
    lessons = Lessons('Lessons.txt')
    print("Number of Lessons", len(lessons.lesson_lines))
