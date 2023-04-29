from datetime import datetime
import sys
import unittest



sys.path.append(r"C:\Users\noahp\Documents\Fischer Jordan\AWS Instance\custom_trackers\training_tracker")
from classes.training_tracker import TrainingTracker, TrackerSheet
from classes.dataclasses.course import Course, CourseTaker


class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.tracker = TrainingTracker(TrackerSheet("Online Training Course Repository", "Tracker"))
        self.course_example = Course("Microsoft Excel -  Beginner to Advanced + Project Based Excel Course + Practice Tests",
                                    "https://www.udemy.com/course/complete-python-bootcamp/learn/lecture/20205526?start=0#overview",
                                    "anoushka.khanna@fischerjordan.com",
                                    "alwaysbetraining1",
                                    datetime.today(),
                                    datetime.today(),
                                    CourseTaker("Jasika walia", "noah.provenzano@fischerjordan.com")
                                    )
        return super().setUp()

    # def test_get_courses(self):
    #     courses = self.tracker.get_courses()
    #     for course in courses:
    #         print(course, "\n\n")

    def test_is_course_complete(self):
        self.assertFalse(self.tracker.is_course_complete(self.course_example))


if __name__ == '__main__':
    unittest.main()
