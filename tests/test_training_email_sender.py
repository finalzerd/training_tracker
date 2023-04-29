

from datetime import datetime
import sys
import unittest


sys.path.append(r"C:\Users\noahp\Documents\Fischer Jordan\AWS Instance\custom_trackers\training_tracker")
from classes.training_email_sender import TrainingEmailSender
from classes.dataclasses.course import Course, CourseTaker


class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.sender = TrainingEmailSender()
        return super().setUp()

    def test_send_training_reminder_email(self):
        self.sender.send_training_reminder_email(Course("windows",
                                                "login",
                                                "password",
                                                datetime.today(),
                                                datetime.today(),
                                                CourseTaker("seth",
                                                    "noah.provenzano@fischerjordan.com")))

    def send_admin_notification_email(self):
        pass


if __name__ == '__main__':
    unittest.main()
