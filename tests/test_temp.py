__author__ = "noah.provenzano@fischerjordan.com"

from datetime import date, datetime, timedelta
from classes.training_tracker import TrainingTracker
from classes.tracker_sheet import TrackerSheet
from classes.training_email_sender import TrainingEmailSender
from classes.dataclasses.course import Course
from typing import List

REMINDER_DAYS_ADVANCE: int = 3
ALERT_AFTER_DEADLINE_DAYS: int = 1
COURSE_COMPLETE_PERCENTAGE: float = 0.9
COURSE_REMINDER_PERCENTAGE: float = 0.5

TODAY: date = datetime.today().date()

def main():
    tracker_sheet = TrackerSheet("Online Training Course Repository", "Tracker")
    email_sender = TrainingEmailSender()
    tracker = TrainingTracker(tracker_sheet)

    courses: List[Course] = tracker.get_courses()
    course: Course
    
    for i, course in enumerate(courses):
        sheet_row = i + 2
        if course.links[0] == "" or course.login == "":
            continue # this takes care of Youtube courses
            
        if course.was_rescheduled:
            if (course.end_date + timedelta(days=ALERT_AFTER_DEADLINE_DAYS)).date() == TODAY:
                tracker.update_course_completion(course, courses)
                tracker.log_completion(sheet_row, course)
                tracker.reset_link()
                tracker.log_cleared_course(sheet_row)
            continue
                            
        # Send reminder email before due date pre notice
        if ((datetime.today() + timedelta(days=REMINDER_DAYS_ADVANCE)).date() == course.end_date.date()):
            try:
                tracker.update_course_completion(course, courses)
                email_was_sent = False                
                if course.box_completion < COURSE_REMINDER_PERCENTAGE:
                    email_sender.send_training_reminder_email(course)
                    email_was_sent = True
                tracker.log_completion(sheet_row, course)
                tracker.log_precompletion_email(sheet_row, email_was_sent)
                
            except Exception as e:
                email_sender.send_error_email(course, e)
                
                
        # On day after alert after check everything and reset and  either warning or congratulations.
        if (course.end_date + timedelta(days=ALERT_AFTER_DEADLINE_DAYS)).date() == TODAY:
            try:        
                tracker.update_course_completion(course, courses)
                tracker.log_completion(sheet_row, course)
                tracker.reset_link()
                tracker.log_cleared_course(sheet_row)
                        
                if course.box_completion > COURSE_COMPLETE_PERCENTAGE:
                    email_sender.send_completion_email(course)
                else:
                    email_sender.send_unfinished_by_deadline_email(course)
                
            except Exception as e:
                email_sender.send_error_email(course, e)
                
                
        # Send feedback request reminder if still haven't  finished  survey and it is a subsequent weeks one day after
        days_after_due: date = (course.end_date + timedelta(ALERT_AFTER_DEADLINE_DAYS)).date()
        if (days_after_due < TODAY and (TODAY - days_after_due) % timedelta(7) == timedelta(0)):
            try:
                if not course.feedback_provided:
                    # make sure box completion is not null otherwise check if its below what it should be
                    if course.box_completion != None:
                        if course.box_completion > COURSE_COMPLETE_PERCENTAGE:
                            email_sender.send_feedback_request_email(course)
                    else:
                        email_sender.send_feedback_request_email(course)
                        
                
            except Exception as e:
                email_sender.send_error_email(course, e)

    print("Done")
        
        

if __name__ == "__main__":
    main()