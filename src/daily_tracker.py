from datetime import date, datetime, time, timedelta
import os
import sys
import time
import random
from typing import List

sys.path.append(os.getcwd())

import training_emails
import training_sheet
import quiz
from course import Course
from udemy_scraper import UdemyScraper
from reset_course_new import reset_course_new

from fjutils.sheets.google_sheet import GoogleSheet
from fjutils.email.email import TextEmail

from config import CONFIG

def main():
    start_email = TextEmail(to=CONFIG.CODE_ADMIN_EMAILS,
                            subject="Starting Training Tracker")
    start_email.send()

    tracker_sheet = GoogleSheet(
        CONFIG.TRACKER_SHEET_NAME, CONFIG.TRACKER_WORKSHEET_NAME)
    udemy_scraper = UdemyScraper()

    mc_questions: List[dict] = GoogleSheet(
        CONFIG.MC_QUESTIONS_SHEET_NAME, CONFIG.MC_QUESTIONS_WORKSHEET_NAME).sheet.get_all_records()

    courses: List[Course] = training_sheet.get_courses(tracker_sheet)
    assert len(courses) > 1, "Didn't get all of the courses"

    course: Course
    for i, course in enumerate(courses):
        sheet_row = i + 2
        print(
            f"sheet_row: {sheet_row}, end_date: {course.end_date}, login: {course.login}")

        if not course.currently_tracking:
            continue

        if course.complete_with_quiz:
            continue

        is_youtube_course = course.links[0] == "" or course.login == ""
        if is_youtube_course:   

            # Youtube start email
            if ((datetime.today() + timedelta(days=CONFIG.START_EMAIL_DAYS_BEFORE)).date() == course.start_date):
                training_emails.send_course_start_email(course)

            # Youtube Completion email
            if (course.end_date + timedelta(days=CONFIG.ALERT_AFTER_DEADLINE_DAYS)) == date.today():
                quiz_url = quiz.generate_quiz(
                    tracker_sheet, course, mc_questions)
                if quiz_url is None:
                    training_emails.send_error_email(
                        course, Exception("Quiz URL is None, failed to generate quiz"))
                else:
                    training_emails.send_completion_email_with_quiz(
                        course, quiz_url)
                    training_sheet.log_quiz_sent_date(
                        tracker_sheet, sheet_row, course)
                    training_sheet.log_completion_email_is_sent(
                        tracker_sheet, sheet_row, True)
                    course.box_completion = 1.00
                    training_sheet.log_completion(
                        tracker_sheet, sheet_row, course)

            # Youtube subsequent week feedback reminder
            start_feedback_reminders_date: date = (
                course.end_date + timedelta(CONFIG.ALERT_AFTER_DEADLINE_DAYS))
            if (start_feedback_reminders_date < date.today()
                and (date.today() - start_feedback_reminders_date) % timedelta(7) == timedelta(0)
                    and not course.feedback_provided):

                training_emails.send_feedback_request_email(course)

            need_quiz = course.end_date > datetime(2022, 7, 9).date()
            weeks = (date.today() - course.end_date).days

            if need_quiz and weeks in [7, 14] and course.quiz1 == 'QNT':
                if len(course.quiz_url) == 0:
                    continue
                training_emails.send_quiz_request_email(course)

            if need_quiz and course.quiz1 == 'QF1':
                training_emails.send_failed_quiz_email(course)
                training_sheet.log_quiz_completion_email(
                    tracker_sheet, sheet_row, True)
                time.sleep(3)

            if need_quiz and course.quiz1 == 'QP':
                training_emails.send_completion_after_quiz_email(course)
                training_sheet.log_quiz_completion_email(
                    tracker_sheet, sheet_row, True)
                time.sleep(3)

            if need_quiz and weeks in [7, 14] and course.quiz2 == 'QNT':
                if len(course.quiz_url) == 0:
                    continue
                training_emails.send_quiz_request_email(course)

            if need_quiz and course.quiz2 == 'QF2':
                training_emails.send_failed_quiz_twice_email(course)
                training_sheet.log_quiz_completion_email(
                    tracker_sheet, sheet_row, True)
                time.sleep(3)

            if need_quiz and course.quiz2 == 'QP':
                training_emails.send_completion_after_quiz_email(course)
                training_sheet.log_quiz_completion_email(
                    tracker_sheet, sheet_row, True)
                time.sleep(3)

            if need_quiz and course.final_state == 'CnQ':
                training_sheet.log_quiz_completion_email(
                    tracker_sheet, sheet_row, True)
                time.sleep(3)
            continue

        # If course was rescheduled, then don't send emails.
        if course.was_rescheduled:
            if (course.end_date + timedelta(days=CONFIG.ALERT_AFTER_DEADLINE_DAYS)) == date.today():
                udemy_scraper.update_course_completion(course, courses)
                training_sheet.log_completion(
                    tracker_sheet, sheet_row, course)
            continue  # Do this regardless

        # Send a welcome greeting email on the day before the start date with credentials and reset course.
        if ((datetime.today() + timedelta(days=CONFIG.START_EMAIL_DAYS_BEFORE)).date() == course.start_date):
            print("new course")
            if (course.is_reschedule):
                print("rescheduled course")
                try:
                    # Todo make this set course set back progress if a reschedule
                    training_emails.send_course_start_email_rescheduled(course)
                    training_sheet.log_welcome_email(tracker_sheet, sheet_row)
                    udemy_scraper.reset_course(course)
                    time.sleep(random.randint(2,5))
                    training_sheet.log_cleared_course(tracker_sheet, sheet_row)
                    time.sleep(2)
                except Exception as e:
                    training_emails.send_error_email(course, e)
                    training_emails.send_cannot_track_email(course, sheet_row)
                continue
            else:
                try:
                    # Todo make this set course set back progress if a reschedule
                    training_emails.send_course_start_email(course)
                    training_sheet.log_welcome_email(tracker_sheet, sheet_row)
                    print("resetting course ")

                except Exception as e:
                    training_emails.send_error_email(course, e)
                    # cannot_track_email(course, sheet_row)
                continue

        # Send reminder email before due date pre notice
        if ((datetime.today() + timedelta(days=CONFIG.REMINDER_DAYS_ADVANCE)).date() == course.end_date
                and not datetime.today().date() == course.start_date):
            try:
                udemy_scraper.update_course_completion(course, courses)
                time.sleep(3)
                email_was_sent = False
                if course.box_completion < CONFIG.COURSE_REMINDER_PERCENTAGE:
                    training_emails.send_training_reminder_email(course)
                    email_was_sent = True
                # send_training_reminder_email(course)
                # email_was_sent = True
                training_sheet.log_completion(
                    tracker_sheet, sheet_row, course)
                time.sleep(1)
                training_sheet.log_precompletion_email(
                    tracker_sheet, sheet_row, email_was_sent)
                time.sleep(1)
            except Exception as e:
                training_emails.send_error_email(course, e)
                training_emails.send_cannot_track_email(course, sheet_row)

        # On end date check everything and either warning or congratulations.
        if (course.end_date + timedelta(days=CONFIG.ALERT_AFTER_DEADLINE_DAYS)) == date.today():
            # tracker.scraper.delete_all_cookies()
            if (course.is_reschedule):
                try:
                    print("calling update reschedule")
                    if (udemy_scraper.update_course_completion_rescheduled(course, courses)):
                        time.sleep(1)
                        training_sheet.log_completion(
                            tracker_sheet, sheet_row, course)
                        time.sleep(1)

                        if course.box_completion >= CONFIG.COURSE_COMPLETE_PERCENTAGE:
                            quiz_url = quiz.generate_quiz(tracker_sheet,
                                                          course, mc_questions)
                            if quiz_url == None:
                                training_emails.send_error_email(
                                    course, Exception("Quiz URL was None"))
                            else:
                                training_emails.send_completion_email_with_quiz(
                                    course, quiz_url)
                            # update quiz url
                            log_complete = True
                        else:
                            training_emails.send_unfinished_by_deadline_email(
                                course)
                            log_complete = False

                        training_sheet.log_completion_email_is_sent(
                            tracker_sheet, sheet_row, log_complete)
                        # tracker.reset_course(course)
                        # time.sleep(random.randint(5,10))
                        # tracker.log_cleared_course(sheet_row)
                        time.sleep(2)

                except Exception as e:
                    print(e)
                    # cannot_track_email(course, sheet_row)
                    training_emails.send_error_email(course, e)
            else:
                try:
                    if (udemy_scraper.update_course_completion(course, courses)):
                        time.sleep(1)
                        training_sheet.log_completion(
                            tracker_sheet, sheet_row, course)
                        time.sleep(1)

                        if course.box_completion >= CONFIG.COURSE_COMPLETE_PERCENTAGE:
                            quiz_url = quiz.generate_quiz(tracker_sheet,
                                course, mc_questions)
                            if quiz_url == None:
                                training_emails.send_error_email(
                                    course, Exception("Quiz URL was None"))
                            else:
                                training_emails.send_completion_email_with_quiz(
                                    course, quiz_url)
                            # update quiz url
                            log_complete = True
                        else:
                            training_emails.send_unfinished_by_deadline_email(
                                course)
                            log_complete = False

                        # tracker.reset_course(course)
                        # time.sleep(random.randint(5,10))
                        # tracker.log_cleared_course(sheet_row)
                        # time.sleep(2)
                        training_sheet.log_completion_email_is_sent(
                            tracker_sheet, sheet_row, log_complete)

                except Exception as e:
                    print(e)
                    training_emails.send_cannot_track_email(course, sheet_row)
                    training_emails.send_error_email(course, e)

        # If subsequent week after and never did a reschedule then send another reschedule email
        if (course.end_date < date.today() and (date.today() - course.end_date) % timedelta(7) == timedelta(0)):
            try:
                if course.needs_reschedule:
                    training_emails.send_reschedule_reminder_email(course)
            except Exception as e:
                training_emails.send_error_email(course, e)
                training_emails.send_cannot_track_email(course, sheet_row)

        # Send feedback request reminder if still haven't  finished  survey and it is a subsequent weeks one day after
        start_feedback_reminders_date: date = (
            course.end_date + timedelta(CONFIG.ALERT_AFTER_DEADLINE_DAYS))
        if (start_feedback_reminders_date < date.today() and (date.today() - start_feedback_reminders_date) % timedelta(7) == timedelta(0)):
            try:
                if not course.feedback_provided:
                    # make sure box completion is not null otherwise check if its below what it should be
                    if course.box_completion != None:
                        if course.box_completion >= CONFIG.COURSE_COMPLETE_PERCENTAGE:
                            training_emails.send_feedback_request_email(course)
                    else:
                        training_emails.send_feedback_request_email(course)

            except Exception as e:
                training_emails.send_error_email(course, e)
                training_emails.send_cannot_track_email(course, sheet_row)

        # Conditions for quiz pass or fail
        need_quiz = course.end_date > datetime(2022, 7, 9).date()
        weeks = (date.today() - course.end_date).days

        if need_quiz and weeks in [7, 14] and course.quiz1 == 'QNT':
            if len(course.quiz_url) == 0:
                continue
            training_emails.send_quiz_request_email(course)

        if need_quiz and course.quiz1 == 'QF1':
            training_emails.send_failed_quiz_email(course)
            training_sheet.log_quiz_completion_email(
                tracker_sheet, sheet_row, True)
            time.sleep(3)

        if need_quiz and course.quiz1 == 'QP':
            training_emails.send_completion_after_quiz_email(course)
            training_sheet.log_quiz_completion_email(
                tracker_sheet, sheet_row, True)
            time.sleep(3)

        if need_quiz and weeks in [7, 14] and course.quiz2 == 'QNT':
            if len(course.quiz_url) == 0:
                continue
            training_emails.send_quiz_request_email(course)

        if need_quiz and course.quiz2 == 'QF2':
            training_emails.send_failed_quiz_twice_email(course)
            training_sheet.log_quiz_completion_email(
                tracker_sheet, sheet_row, True)
            time.sleep(3)

        if need_quiz and course.quiz2 == 'QP':
            training_emails.send_completion_after_quiz_email(course)
            training_sheet.log_quiz_completion_email(
                tracker_sheet, sheet_row, True)
            time.sleep(3)

        if need_quiz and course.final_state == 'CnQ':
            training_sheet.log_quiz_completion_email(
                tracker_sheet, sheet_row, True)
            time.sleep(3)

        udemy_scraper.scraper.delete_all_cookies()
        time.sleep(random.randint(1, 5))

    print("Done")
    end_email = TextEmail(to=CONFIG.CODE_ADMIN_EMAILS,
                          subject="Finished Training Tracker")
    end_email.send()
    udemy_scraper.scraper.quit()

    print("STARTING FIXED RESET ISSUE CODE")
    for i, course in enumerate(courses):
        sheet_row = i + 2

        print(f"sheet_row: {sheet_row}")
        print(course.end_date)
        if course.links[0] == "" or course.login == "":
            continue
        try:
            if ((datetime.today() + timedelta(days=CONFIG.START_EMAIL_DAYS_BEFORE)).date() == course.start_date):
                if (reset_course_new(course.links[0], course.login) == 1):
                    print("course reset successfully")
        except:
            continue


if __name__ == "__main__":
    main()
