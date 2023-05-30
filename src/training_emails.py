from datetime import datetime
from course import Course, CourseTaker
from config import CONFIG

from fjutils.email.fj_email import FJEmailSimple

def send_training_email(email:FJEmailSimple) -> None:
    """Sends an email to the taker of a course taking into account testing configurations."""
    if CONFIG.SEND_LIVE_EMAILS:
        email.send()
    else:
        print(f"\n=== TESTING email sent ==========================")
        print(f"TO: {email.to}")
        print(f"CC: {email.cc}")
        print(f"BCC: {email.bcc}")
        print(f"SUBJECT: {email.subject}")
        print(f"TITLE: {email.title}")
        print(f"TEXT: {email.text}")
        print(f"==================================================\n")

def send_course_start_email(course: Course) -> None:
    """To be sent to the taker a day before the course starts."""
    taker: CourseTaker = course.taker
    word_course: str = "course" if len(course.links) == 1 else "courses"

    title: str = "FJ Training Course Start"

    email_text = f"""Hi {taker.first_name()},<br><br>
                        Welcome to the {course.name} {word_course}!<br><br>
                        Please do your best to complete the {word_course} by the end date of {course.end_date.strftime("%m/%d/%y")}.
                        When you are ready, please login the {word_course} using the following link and login credentials:<br><br>
                        <a href={course.links[0]}>{course.name}</a><br><br>
                        Login: {course.login}<br><br>
                        Password: {course.password}<br><br>
                        Please make sure to take notes during the {word_course} and re-take sections that are unclear to you.
                        Once you complete the {word_course}, you will be given a short quiz about the contents, as well as a feedback survey.
                        If you do not pass the quiz you will be given the option to re-take the {word_course} or carrying an incomplete for the {word_course}.<br><br>
                        If you have any questions, Please fell free to contact {CONFIG.MAIN_ADMIN_EMAIL}.<br><br>   
                        Thanks,<br><br>
                        FJ Training"""

    email = FJEmailSimple(to=[taker.email],
                          cc=CONFIG.ADMIN_EMAILS,
                          bcc=CONFIG.CODE_ADMIN_EMAILS,
                          subject=title,
                          title=title,
                          text=email_text)
    send_training_email(email)


def send_course_start_email_rescheduled(course: Course) -> None:
    """To be sent to the taker a day before the course starts."""
    taker: CourseTaker = course.taker
    word_course: str = "course" if len(course.links) == 1 else "courses"

    title: str = "FJ Training Rescheduled Course Start"

    email_text = f"""Hi {taker.first_name()},<br><br>
                        Welcome to the {course.name} {word_course}!<br><br>
                        Please do your best to complete the {word_course} by the end date of {course.end_date.strftime("%m/%d/%y")}.
                        
                        When you are ready, please login the {word_course} using the following link and login credentials:<br><br>
                        <a href={course.links[0]}>{course.name}</a><br><br>
                        Login: {course.login}<br><br>
                        Password: {course.password}<br><br>
                        Please make sure to take notes during the {word_course} and re-take sections that are unclear to you.
                    <br><br>
                        If you have any questions, Please fell free to contact {CONFIG.MAIN_ADMIN_EMAIL}.<br><br>   
                        Thanks,<br><br>
                        FJ Training"""

    email = FJEmailSimple(to=[taker.email],
                          cc=CONFIG.ADMIN_EMAILS,
                          bcc=CONFIG.CODE_ADMIN_EMAILS,
                          subject=title,
                          title=title,
                          text=email_text)
    send_training_email(email)


def send_training_reminder_email(course: Course) -> None:
    taker: CourseTaker = course.taker
    days_remaining: int = (course.end_date -
                           datetime.today().date()).days
    word_course: str = "course" if len(course.links) == 1 else "courses"
    end_date: str = course.end_date.strftime("%m/%d/%y")

    email_text = f"""Hi {taker.first_name()},<br><br>
                    Just a friendly reminder that the <a href={course.links[0]}>{course.name}</a> {word_course} due date is in {days_remaining} days on {end_date}.<br><br>
                    Please make sure to complete the {word_course} by this deadline or reach out to {CONFIG.MAIN_ADMIN_EMAIL} if you need more time.<br><br>
                    Thanks,<br><br>
                    FJ Training"""

    email = FJEmailSimple(to=[taker.email],
                          cc=CONFIG.ADMIN_EMAILS,
                          bcc=CONFIG.CODE_ADMIN_EMAILS,
                          subject="FJ Training Course Reminder",
                          title="FJ Training Course Reminder",
                          text=email_text)
    send_training_email(email)


def send_unfinished_by_deadline_email(course: Course) -> None:
    """On deadline if the person didn't finish has to ask Anoushka for extra time"""
    taker = course.taker
    word_course = "course" if len(course.links) == 1 else "courses"

    email_text = f"""Hi {taker.first_name()},<br><br>
                    We noticed that you have not yet completed the {course.name} {word_course}.<br><br>
                    Please contact {CONFIG.MAIN_ADMIN_EMAIL} to schedule an extension.<br><br>
                    Thanks,<br><br>
                    FJ Training"""
    email = FJEmailSimple(to=[taker.email],
                          cc=CONFIG.ADMIN_EMAILS,
                          bcc=CONFIG.CODE_ADMIN_EMAILS,
                          subject="FJ Training Course - Action Required",
                          title="FJ Training Course - Action Required",
                          text=email_text)
    send_training_email(email)


def send_reschedule_reminder_email(course: Course) -> None:
    """
    On subsequent weeks after deadline if the person didn't finish and never rescheduled,
    this asks them to contact Anoushka for extra time
    """
    taker = course.taker
    word_course = "course" if len(course.links) == 1 else "courses"

    email_text = f"""Hi {taker.first_name()},<br><br>
                    We noticed that you have not yet reached out to reschedule the {course.name} {word_course}.<br><br>
                    Please contact {CONFIG.MAIN_ADMIN_EMAIL} to schedule an extension.<br><br>
                    Thanks,<br><br>
                    FJ Training"""
    email = FJEmailSimple(to=[taker.email],
                          cc=CONFIG.ADMIN_EMAILS,
                          bcc=CONFIG.CODE_ADMIN_EMAILS,
                          subject="FJ Training Course - Action Required",
                          title="FJ Training Course - Action Required",
                          text=email_text)
    send_training_email(email)


def send_completion_email(course: Course) -> None:
    """Asking for feedback on the course after they complete as a survey link"""
    taker = course.taker
    title = "FJ Training Course - Action Required"
    word_course = "course" if len(course.links) == 1 else "courses"

    email_text = f"""Hi {taker.first_name()},<br><br>
                    Congratulations on completing the {course.name} {word_course}.<br><br>
                    Please remember to provide feedback on the {word_course} here:<br><br>
                    <a href="{course.forms_link()}">FJ Training Course Feedback</a><br><br>
                    Thanks,<br><br>
                    FJ Training"""

    email = FJEmailSimple(to=[taker.email],
                          cc=CONFIG.ADMIN_EMAILS,
                          bcc=CONFIG.CODE_ADMIN_EMAILS,
                          subject=title,
                          title=title,
                          text=email_text)
    send_training_email(email)


def send_completion_email_with_quiz(course: Course, quiz_url: str) -> None:
    """Asking for feedback on the course after they complete as a survey link
    as well as a quiz link to complete"""
    if quiz_url == "":
        send_completion_email(course)
        return
    taker = course.taker
    title = "FJ Training Course - Action Required"
    word_course = "course" if len(course.links) == 1 else "courses"

    email_text = f"""Hi {taker.first_name()},<br><br>
                    Congratulations on completing the {course.name} {word_course}.<br><br>
                    We ask that you please complete a quiz and provide feedback on the {word_course} using these links:<br><br>
                    <a href="{course.forms_link()}">FJ Training Course Feedback</a><br><br>
                    <a href="{quiz_url}">{course.name} Quiz</a><br><br>
                    Thanks,<br><br>
                    FJ Training"""

    email = FJEmailSimple(to=[taker.email],
                          cc=CONFIG.ADMIN_EMAILS,
                          bcc=CONFIG.CODE_ADMIN_EMAILS,
                          subject=title,
                          title=title,
                          text=email_text)
    send_training_email(email)


def send_feedback_request_email(course: Course) -> None:
    """ Asking for feedback on the subsequent weeks after. """
    taker = course.taker
    title = "FJ Training Course - Action Required"
    word_course = "course" if len(course.links) == 1 else "courses"

    email_text = f"""Hi {taker.first_name()},<br><br>
                    Just a friendly reminder to provide feedback on the {course.name} {word_course} here:<br><br>
                    <a href="{course.forms_link()}">FJ Training Course Feedback</a><br><br>
                    Thanks,<br><br>
                    FJ Training"""

    email = FJEmailSimple(to=[taker.email],
                          cc=CONFIG.ADMIN_EMAILS,
                          bcc=CONFIG.CODE_ADMIN_EMAILS,
                          subject=title,
                          title=title,
                          text=email_text)
    send_training_email(email)


def send_error_email(course: Course, error: Exception) -> None:
    course.box_completion = -1 # to prevent error on sending email
    email = FJEmailSimple(to=CONFIG.CODE_ADMIN_EMAILS,
                          subject="Training Tracker Error",
                          text=f"Error->{str(error)}<br><br>{course}")
    send_training_email(email)


def only_quiz_email(course: Course) -> None:
    """ Asking for feedback on the subsequent weeks after. """
    taker = course.taker
    title = "FJ Training Course - Action Required"
    word_course = "course" if len(course.links) == 1 else "courses"

    email_text = f"""Hi {taker.first_name()},<br><br>
                    Please take the quiz on the {course.name} {word_course} here:<br><br>
                    <a href="{course.quiz_url}">{course.name} Quiz</a><br><br>
                    Thanks,<br><br>
                    FJ Training"""

    email = FJEmailSimple(to=[taker.email],
                          cc=CONFIG.ADMIN_EMAILS,
                          bcc=CONFIG.CODE_ADMIN_EMAILS,
                          subject=title,
                          title=title,
                          text=email_text)
    send_training_email(email)


def send_quiz_request_email(course: Course) -> None:
    """ Asking for feedback on the subsequent weeks after. """
    taker = course.taker
    title = "FJ Training Course - Action Required"
    word_course = "course" if len(course.links) == 1 else "courses"

    email_text = f"""Hi {taker.first_name()},<br><br>
                    This is a friendly reminder to take the quiz on the {course.name} {word_course} here:<br><br>
                    <a href="{course.quiz_url}">{course.name} Quiz</a><br><br>
                    Thanks,<br><br>
                    FJ Training"""

    email = FJEmailSimple(to=[taker.email],
                          cc=CONFIG.ADMIN_EMAILS,
                          bcc=CONFIG.CODE_ADMIN_EMAILS,
                          subject=title,
                          title=title,
                          text=email_text)
    send_training_email(email)


def send_failed_quiz_email(course: Course) -> None:
    """Failed in Quiz then ask Anoushka to reschedule or mark as incomplete"""
    taker = course.taker
    word_course = "course" if len(course.links) == 1 else "courses"

    email_text = f"""Hi {taker.first_name()},<br><br>
                    We noticed that you scored below 80% in the {course.name} {word_course} quiz.<br><br>
                    Please contact {CONFIG.MAIN_ADMIN_EMAIL} to reschedule the {word_course}, else it will be recorded as incomplete.<br><br>
                    Thanks,<br><br>
                    FJ Training"""
    email = FJEmailSimple(to=[taker.email],
                          cc=CONFIG.ADMIN_EMAILS,
                          bcc=CONFIG.CODE_ADMIN_EMAILS,
                          subject="FJ Training Course - Action Required",
                          title="FJ Training Course - Action Required",
                          text=email_text)
    send_training_email(email)


def send_failed_quiz_twice_email(course: Course) -> None:
    """mark incomplete if failed twice"""
    taker = course.taker
    word_course = "course" if len(course.links) == 1 else "courses"

    email_text = f"""Hi {taker.first_name()},<br><br>
                    We noticed that you scored below 80% twice in the {course.name} {word_course} quiz in your second attempt.<br><br>
                    The course will now be recorded as incomplete.<br><br>
                    Thanks,<br><br>
                    FJ Training"""
    email = FJEmailSimple(to=[taker.email],
                          cc=CONFIG.ADMIN_EMAILS,
                          bcc=CONFIG.CODE_ADMIN_EMAILS,
                          subject="FJ Training Course - Action Required",
                          title="FJ Training Course - Action Required",
                          text=email_text)
    send_training_email(email)


def send_completion_after_quiz_email(course: Course) -> None:
    """Asking for feedback on the course after they complete as a survey link"""
    taker = course.taker
    title = "FJ Training Course -Quiz Result"
    word_course = "course" if len(course.links) == 1 else "courses"

    email_text = f"""Hi {taker.first_name()},<br><br>
                    Congratulations on successful completion of the {course.name} {word_course} quiz.<br><br>
                    Thanks for taking {course.name} {word_course},<br><br>
                    FJ Training"""

    email = FJEmailSimple(to=[taker.email],
                          cc=CONFIG.ADMIN_EMAILS,
                          bcc=CONFIG.CODE_ADMIN_EMAILS,
                          subject=title,
                          title=title,
                          text=email_text)
    send_training_email(email)


def send_cannot_track_email(course: Course, sheet_row) -> None:
    """Flagging the admin if cannot track """
    taker = course.taker
    title = "Cannot track progress"

    email_text = f"""The bot is unable to track progress for {taker} course on {course.name} at row number {sheet_row}. Please keep a check on the course manually<br><br>
                    """

    email = FJEmailSimple(to=CONFIG.ADMIN_EMAILS,
                          cc=CONFIG.CODE_ADMIN_EMAILS,
                          subject=title,
                          title=title,
                          text=email_text)
    send_training_email(email)


def send_weekly_report_email(course: Course, df_html: str) -> None:
    """Auto report """
    taker = course.taker
    title = "Weekly Report"

    email_text = f"""Hi {taker.first_name()},<br><br>
                    Please find below the results of your online courses to date:<br><br>
                    
                    Note that items in red require further action: <br><br>
                    {df_html}<br><br>
                    FJ Training
                    """

    email = FJEmailSimple(to=[taker.email],
                          cc=CONFIG.ADMIN_EMAILS,
                          bcc=CONFIG.CODE_ADMIN_EMAILS,
                          subject=title,
                          title=title,
                          text=email_text)
    send_training_email(email)


def send_offline_pre_training_email(course_trainer: CourseTaker) -> None:
    """Offline pre training email """
    taker = course_trainer
    title = "Pre-training email"

    email_text = f"""Hi {taker.first_name()},<br><br>
                    Please fil the Pre-training scores for the course<br><br>
                    FJ Offline Training
                    """

    email = FJEmailSimple(to=[taker.email],
                          cc=CONFIG.ADMIN_EMAILS,
                          bcc=CONFIG.CODE_ADMIN_EMAILS,
                          subject=title,
                          title=title,
                          text=email_text)
    send_training_email(email)


def send_offline_post_training_email(course_trainer: CourseTaker) -> None:
    """Offline post training email"""
    taker = course_trainer
    title = "Pre-training email"

    email_text = f"""Hi {taker.first_name()},<br><br>
                    Please fill the Post-training scores for the course <br><br>
                    FJ Offline Training
                    """

    email = FJEmailSimple(to=[taker.email],
                          cc=CONFIG.ADMIN_EMAILS,
                          bcc=CONFIG.CODE_ADMIN_EMAILS,
                          subject=title,
                          title=title,
                          text=email_text)
    send_training_email(email)
