from datetime import datetime
import random
import time
from typing import Dict, List
from course import Course, CourseTaker
from fjutils.sheets.google_sheet import GoogleSheet


def get_courses(sheet: GoogleSheet) -> List[Course]:
    courses: List[Course] = []
    tracker_sheet: List[Dict[str, str]] = sheet.sheet.get_all_records()
    i = 0
    for row in tracker_sheet:

        try:
            box_completion = float(row['Boxes Completion'])
        except:
            box_completion = 0.0

        incomplete_modules: List[str] = row['Incomplete Modules'].split(
            ", ")
        if incomplete_modules[0] == "":
            incomplete_modules.clear()
        
        try:
            quiz_result = float(row['quiz results'])
        except:
            quiz_result = None
            
        try:
            quiz_date = datetime.strptime(row['Quiz sent date'], "%m/%d/%y")
        except:
            quiz_date = None

        courses.append(Course(row_number=i+2,
                              name=row['Course'],
                              links=row['Course Link'].split(", "),
                              login=row['email'],
                              password=row['password'],
                              start_date=datetime.strptime(
                                  row['Start Date'], "%m/%d/%y").date(),
                              end_date=datetime.strptime(
                                  row['End Date'], "%m/%d/%y").date(),
                              taker=CourseTaker(name=row['Name'],
                                                email=row['Email']),
                              box_completion=box_completion,
                              feedback_provided=row['Feedback Provided'] == 1,
                              is_reschedule=row['Is a Reschedule'] == "TRUE",
                              was_rescheduled=row['Was Rescheduled'] == "TRUE",
                              incomplete_modules=incomplete_modules,
                              needs_reschedule=row['Needs Reschedule'] == "TRUE",
                              currently_tracking=row['Currently Tracking'] == "TRUE",
                              quiz1=row['Quiz1'],
                              quiz2=row['Quiz2'],
                              complete_with_quiz=row['Complete'] == 1,
                              quiz_url=row['Quiz URL'],
                              only_quiz=row['Only Quiz']==1,
                              only_feed=row['Only feedback']==1,
                              final_state=row['FINAL STATE'],
                              quiz_date=quiz_date,
                              quiz_result=quiz_result
                              ))
        i = i+1
    return courses


def log_completion(sheet: GoogleSheet, row: int, course: Course) -> None:
    try:
        boxes_completion_entry = [float(course.box_completion)]
    except:
        boxes_completion_entry = ["Error"]
    try:
        incomplete_modules_entry = [", ".join(course.incomplete_modules)]
    except:
        incomplete_modules_entry = ["Error"]
    sheet.write_list(row, sheet.col_search(
        "Boxes Completion"), boxes_completion_entry)
    time.sleep(random.randint(1, 2))
    sheet.write_list(row, sheet.col_search(
        "Incomplete Modules"), incomplete_modules_entry)
    time.sleep(random.randint(1, 2))


def log_precompletion_email(sheet: GoogleSheet, row: int, sent: bool) -> None:
    sent_str = "EMAIL_SENT" if sent else "NOT_NEEDED"
    sheet.write_list(row, sheet.col_search(
        "Precompletion Reminder Email"), [sent_str])


def log_completion_email_is_sent(sheet: GoogleSheet, row: int, is_complete: bool) -> None:
    sent_str = "EMAIL_SENT" if is_complete else "RESCHEDULE_EMAIL_SENT"
    sheet.write_list(row, sheet.col_search(
        "Completion Email"), [sent_str])


def log_welcome_email(sheet: GoogleSheet, row: int) -> None:
    sheet.write_list(row, sheet.col_search(
        "Welcome Email"), ["EMAIL_SENT"])


def log_cleared_course(sheet: GoogleSheet, row: int) -> None:
    sheet.write_list(row, sheet.col_search(
        "Course Cleared"), ["CLEARED_FOR_START"])


def log_quiz_completion_email(sheet: GoogleSheet, row: int, is_complete: bool) -> None:
    sent_str = 1 if is_complete else 0
    sheet.write_list(
        row, sheet.col_search("Complete"), [sent_str])

def log_quiz_sent_date(sheet: GoogleSheet, row: int, course: Course) -> None:
    sheet.sheet.update_cell(row, sheet.col_search(
            "Quiz sent date"), str(course.quiz_date.strftime("%m/%d/%y")))