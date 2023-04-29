__author__ = "noah.provenzano@fischerjordan.com"

# Only run once a night

import code
from datetime import date, datetime, time, timedelta
import time
from classestt.training_tracker import TrainingTracker
from classestt.google_sheet import GoogleSheet
from classestt.training_email_sender import TrainingEmailSender
from classestt.dataclasses.course import Course
from classestt.email import TextEmail
from classestt.training_reset_issue import ResetCourse 
from typing import List
import random

REMINDER_DAYS_ADVANCE: int = 2
START_EMAIL_DAYS_BEFORE: int = 0
ALERT_AFTER_DEADLINE_DAYS: int = 1
COURSE_COMPLETE_PERCENTAGE: float = 0.9
COURSE_REMINDER_PERCENTAGE: float = 0.5

TODAY: date = datetime.today().date()
# print(datetime.today())
# exit()
# Make script use date which is after midnight
NOW: time = datetime.now().time()
# if time(12) < NOW: # if after 12pm then shift date forward
#     TODAY = TODAY + timedelta(days=1)
code_admin = ["yash.jain@fischerjordan.com","ayushman.agrawal@fischerjordan.com","muskan.laul@fischerjordan.com"]

def main():
    start_email = TextEmail(to=code_admin, subject="Starting Training Tracker")
    start_email.send()
    
    tracker_sheet = GoogleSheet("Online Training Course Repository", "Tracker")
    email_sender = TrainingEmailSender()
    tracker = TrainingTracker(tracker_sheet)
    reset_course=ResetCourse()
    
    mc_questions: List[dict] = GoogleSheet("Online Training Course Repository", "Quiz Question-MCQ").sheet.get_all_records()
    
    courses: List[Course] = tracker.get_courses()
    assert len(courses) > 1, "Didn't get all of the courses"
    course: Course
    
    for i, course in enumerate(courses):
        sheet_row = i + 2
                                
        print(f"sheet_row: {sheet_row}")
        print(course.end_date)
        print(course.login)
        if not course.currently_tracking:
            continue
        
        if course.complete_with_quiz:
            continue
            
        if course.only_quiz:
            course.quiz_url = tracker.generate_quiz(course, mc_questions)
            email_sender.only_quiz_email(course)
            print("quiz sent")
        # continue
        if course.only_feed:

            email_sender.send_feedback_request_email(course)
            print("feedback sent")            
        continue
        
        # Do checks if Youtube course
        if course.links[0] == "" or course.login == "":
            
            # Youtube start email
            if ((datetime.today() + timedelta(days=START_EMAIL_DAYS_BEFORE)).date() == course.start_date.date()):
                email_sender.send_course_start_email(course)
            
            # Youtube Completion email
            if (course.end_date + timedelta(days=ALERT_AFTER_DEADLINE_DAYS)).date() == TODAY:
                quiz_url = tracker.generate_quiz(course, mc_questions)
                email_sender.send_completion_email_with_quiz(course, quiz_url)
                tracker.log_completion_email(sheet_row, True)
                course.box_completion=1.00
                tracker.log_completion(sheet_row, course)
               
            # Youtube subsequent week feedback reminder 
            days_after_due: date = (course.end_date + timedelta(ALERT_AFTER_DEADLINE_DAYS)).date()
            if (days_after_due < TODAY and (TODAY - days_after_due) % timedelta(7) == timedelta(0)):
                if not course.feedback_provided:
                    email_sender.send_feedback_request_email(course)
            need_quiz = course.end_date.date() > datetime(2022,7,9).date()
            weeks = (TODAY - course.end_date.date()).days
            
            if need_quiz and weeks in [7,14] and course.quiz1 == 'QNT':
                if len(course.quiz_url) == 0:
                    continue
                email_sender.send_quiz_request_email(course)
                
            if need_quiz and course.quiz1 == 'QF1':
                email_sender.send_failed_quiz_email(course)       
                tracker.log_quiz_completion_email(sheet_row,True)
                time.sleep(3)

            if need_quiz and course.quiz1 == 'QP':
                email_sender.send_completion_after_quiz_email(course)
                tracker.log_quiz_completion_email(sheet_row,True)
                time.sleep(3)

            if need_quiz and weeks in [7,14] and course.quiz2 == 'QNT':
                if len(course.quiz_url) == 0:
                    continue
                email_sender.send_quiz_request_email(course)
                
            if need_quiz and course.quiz2 == 'QF2':
                email_sender.send_failed_quiz_twice_email(course)
                tracker.log_quiz_completion_email(sheet_row,True)
                time.sleep(3)
                
            if need_quiz and course.quiz2 == 'QP':
                email_sender.send_completion_after_quiz_email(course)
                tracker.log_quiz_completion_email(sheet_row,True)
                time.sleep(3)
                
            if need_quiz and course.final_state=='CnQ':
                tracker.log_quiz_completion_email(sheet_row,True)
                time.sleep(3)            
            continue
            
        # If course was rescheduled, then don't send emails.
        if course.was_rescheduled:
            if (course.end_date + timedelta(days=ALERT_AFTER_DEADLINE_DAYS)).date() == TODAY:
                tracker.update_course_completion(course, courses)
                tracker.log_completion(sheet_row, course)
            continue # Do this regardless
        
        
        # Send a welcome greeting email on the day before the start date with credentials and reset course.
        if ((datetime.today() + timedelta(days=START_EMAIL_DAYS_BEFORE)).date() == course.start_date.date()):
            print("new course")
            if(course.is_reschedule):
                print("rescheduled course")
                try:
                    # Todo make this set course set back progress if a reschedule
                    email_sender.send_course_start_email_rescheduled(course)
                    tracker.log_welcome_email(sheet_row)
                    # tracker.reset_course(course)
                    # time.sleep(random.randint(2,5))
                    # tracker.log_cleared_course(sheet_row)
                    time.sleep(2)    
                except Exception as e:
                    email_sender.send_error_email(course, e)
                    email_sender.cannot_track_email(course, sheet_row)
                continue   
            else:
                try:
                    # Todo make this set course set back progress if a reschedule
                    email_sender.send_course_start_email(course)
                    tracker.log_welcome_email(sheet_row)
                    print("resetting course ")

                    
                except Exception as e:
                    email_sender.send_error_email(course, e)
                    # email_sender.cannot_track_email(course, sheet_row)
                continue

        
        # Send reminder email before due date pre notice 
        if ((datetime.today() + timedelta(days=REMINDER_DAYS_ADVANCE)).date() == course.end_date.date()
            and not datetime.today().date() == course.start_date.date()):
            try:
                tracker.update_course_completion(course, courses)
                time.sleep(1)
                email_was_sent = False                
                if course.box_completion < COURSE_REMINDER_PERCENTAGE:
                    email_sender.send_training_reminder_email(course)
                    email_was_sent = True
                # email_sender.send_training_reminder_email(course)
                # email_was_sent = True
                tracker.log_completion(sheet_row, course)
                time.sleep(1)
                tracker.log_precompletion_email(sheet_row, email_was_sent)
                time.sleep(1)
            except Exception as e:
                email_sender.send_error_email(course, e)
                email_sender.cannot_track_email(course, sheet_row)


        # On end date check everything and either warning or congratulations.
        if (course.end_date + timedelta(days=ALERT_AFTER_DEADLINE_DAYS)).date() == TODAY:
            # tracker.scraper.delete_all_cookies()
            if(course.is_reschedule):
                try:
                    print("calling update reschedule")
                    if(tracker.update_course_completion_rescheduled(course, courses)):
                        time.sleep(1)
                        tracker.log_completion(sheet_row, course)
                        time.sleep(1)
                    
                        if course.box_completion >= COURSE_COMPLETE_PERCENTAGE:
                            quiz_url = tracker.generate_quiz(course, mc_questions)
                            email_sender.send_completion_email_with_quiz(course, quiz_url)
                            #update quiz url
                            log_complete = True
                        else:
                            email_sender.send_unfinished_by_deadline_email(course)
                            log_complete = False


                        tracker.log_completion_email(sheet_row, log_complete)
                        # tracker.reset_course(course)
                        # time.sleep(random.randint(5,10))
                        # tracker.log_cleared_course(sheet_row)
                        time.sleep(2)                       
                    
                except Exception as e:
                    print(e)
                    # email_sender.cannot_track_email(course, sheet_row)
                    email_sender.send_error_email(course, e)      
            else:                  
                try:
                    if(tracker.update_course_completion(course, courses)):
                        time.sleep(1)
                        tracker.log_completion(sheet_row, course)
                        time.sleep(1)
                    
                        if course.box_completion >= COURSE_COMPLETE_PERCENTAGE:
                            quiz_url = tracker.generate_quiz(course, mc_questions)
                            email_sender.send_completion_email_with_quiz(course, quiz_url)
                            #update quiz url
                            log_complete = True
                        else:
                            email_sender.send_unfinished_by_deadline_email(course)
                            log_complete = False

                        # tracker.reset_course(course)
                        # time.sleep(random.randint(5,10))
                        # tracker.log_cleared_course(sheet_row)
                        # time.sleep(2)
                        tracker.log_completion_email(sheet_row, log_complete)
                    
                except Exception as e:
                    print(e)
                    email_sender.cannot_track_email(course, sheet_row)
                    email_sender.send_error_email(course, e)
                
        # If subsequent week after and never did a reschedule then send another reschedule email
        if (course.end_date.date() < TODAY and (TODAY - course.end_date.date()) % timedelta(7) == timedelta(0)):
            try:
                if course.needs_reschedule:
                    email_sender.send_reschedule_reminder_email(course)    
            except Exception as e:
                email_sender.send_error_email(course, e)  
                email_sender.cannot_track_email(course, sheet_row)          
                
        # Send feedback request reminder if still haven't  finished  survey and it is a subsequent weeks one day after
        days_after_due: date = (course.end_date + timedelta(ALERT_AFTER_DEADLINE_DAYS)).date()
        if (days_after_due < TODAY and (TODAY - days_after_due) % timedelta(7) == timedelta(0)):
            try:
                if not course.feedback_provided:
                    # make sure box completion is not null otherwise check if its below what it should be
                    if course.box_completion != None:
                        if course.box_completion >= COURSE_COMPLETE_PERCENTAGE:
                            email_sender.send_feedback_request_email(course)
                    else:
                        email_sender.send_feedback_request_email(course)
                        
                
            except Exception as e:
                email_sender.send_error_email(course, e)
                email_sender.cannot_track_email(course, sheet_row)
        
        #Conditions for quiz pass or fail
        need_quiz = course.end_date.date() > datetime(2022,7,9).date()
        weeks = (TODAY - course.end_date.date()).days
        
        if need_quiz and weeks in [7,14] and course.quiz1 == 'QNT':
            if len(course.quiz_url) == 0:
                continue
            email_sender.send_quiz_request_email(course)
            
        if need_quiz and course.quiz1 == 'QF1':
            email_sender.send_failed_quiz_email(course)
            tracker.log_quiz_completion_email(sheet_row,True)
            time.sleep(3)

        if need_quiz and course.quiz1 == 'QP':
            email_sender.send_completion_after_quiz_email(course)
            tracker.log_quiz_completion_email(sheet_row,True)
            time.sleep(3)

        if need_quiz and weeks in [7,14] and course.quiz2 == 'QNT':
            if len(course.quiz_url) == 0:
                continue
            email_sender.send_quiz_request_email(course)
            
        if need_quiz and course.quiz2 == 'QF2':
            email_sender.send_failed_quiz_twice_email(course)
            tracker.log_quiz_completion_email(sheet_row,True)
            time.sleep(3)
            
        if need_quiz and course.quiz2 == 'QP':
            email_sender.send_completion_after_quiz_email(course)
            tracker.log_quiz_completion_email(sheet_row,True)
            time.sleep(3)
            
        if need_quiz and course.final_state=='CnQ':
            tracker.log_quiz_completion_email(sheet_row,True)
            time.sleep(3)  

        tracker.scraper.delete_all_cookies()
        time.sleep(random.randint(1,5))

    print("Done")
    end_email = TextEmail(to=code_admin, subject="Finished Training Tracker")
    end_email.send()
    tracker.scraper.quit()
    
    exit()
    print("STARTING FIXED RESET ISSUE CODE")
    for i, course in enumerate(courses):
        sheet_row = i + 2
                                
        print(f"sheet_row: {sheet_row}")
        print(course.end_date) 
        if course.links[0] == "" or course.login == "":
            continue
        try:
            if ((datetime.today() + timedelta(days=START_EMAIL_DAYS_BEFORE)).date() == course.start_date.date()):
                if(reset_course.reset_course_new(course.links[0],course.login)==1):
                    print("course reset successfully")
        except:
            continue                    
                
                
            


            
        

if __name__ == "__main__":
    main()