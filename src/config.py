from dataclasses import dataclass
from datetime import date, datetime
import json
from typing import List
import argparse

@dataclass
class TrainingConfig:
    REMINDER_DAYS_ADVANCE: int
    START_EMAIL_DAYS_BEFORE: int
    ALERT_AFTER_DEADLINE_DAYS: int
    COURSE_COMPLETE_PERCENTAGE: float
    COURSE_REMINDER_PERCENTAGE: float
    CODE_ADMIN_EMAILS: List[str]
    TRACKER_SHEET_NAME: str
    TRACKER_WORKSHEET_NAME: str
    MC_QUESTIONS_SHEET_NAME: str
    MC_QUESTIONS_WORKSHEET_NAME: str
    REPORT_CARD_TRACKER_WORKSHEET_NAME: str
    ADMIN_EMAILS: List[str]
    MAIN_ADMIN_EMAIL: str
    WINDOWS: bool
    SEND_LIVE_EMAILS: bool
    SECTION_NAMES_NOT_TO_COUNT: List[str]
    DATE_TODAY: date = date.today()
    DATETIME_TODAY: datetime = datetime.today()
    SHEET_ROW: int|None = None
    


def _get_config(config_json_path: str) -> TrainingConfig:
    CONFIG = TrainingConfig(0, 0, 0, 0.0, 0.0, [], "",
                            "", "", "", "", [], "", True, True, [])
    with open(config_json_path, 'r') as f:
        config = json.load(f)
        CONFIG.REMINDER_DAYS_ADVANCE = config["reminder_days_advance"]
        CONFIG.START_EMAIL_DAYS_BEFORE = config["start_email_days_before"]
        CONFIG.ALERT_AFTER_DEADLINE_DAYS = config["alert_after_deadline_days"]
        CONFIG.COURSE_COMPLETE_PERCENTAGE = config["course_complete_percentage"]
        CONFIG.COURSE_REMINDER_PERCENTAGE = config["course_reminder_percentage"]
        CONFIG.CODE_ADMIN_EMAILS = config["code_admin_emails"]
        CONFIG.TRACKER_SHEET_NAME = config["tracker_sheet_name"]
        CONFIG.TRACKER_WORKSHEET_NAME = config["tracker_worksheet_name"]
        CONFIG.MC_QUESTIONS_SHEET_NAME = config["mc_questions_sheet_name"]
        CONFIG.MC_QUESTIONS_WORKSHEET_NAME = config["mc_questions_worksheet_name"]
        CONFIG.REPORT_CARD_TRACKER_WORKSHEET_NAME = config["report_card_tracker_worksheet_name"]
        CONFIG.ADMIN_EMAILS = config["admin_emails"]
        CONFIG.MAIN_ADMIN_EMAIL = config["main_admin_email"]
        CONFIG.WINDOWS = config["windows"]
        CONFIG.SEND_LIVE_EMAILS = config["send_live_emails"]
        CONFIG.SECTION_NAMES_NOT_TO_COUNT = config["section_names_not_to_count"]
    return CONFIG

parser = argparse.ArgumentParser(
    prog="Training Tracker",
    description="A program to track training progress for FischerJordan",
    epilog="Developed by: FischerJordan",
)
parser.add_argument('--test', '-t', help="to run with the test config in config/test_config.json", action="store_true", required=False)
parser.add_argument('--date', '-d', help="to run with a specific date, must be in YYYY-MM-DD format", type=str, required=False)
parser.add_argument('--row', '-r', help="run a specific row from the tracker sheet", type=int, required=False)

args = parser.parse_args()
if args.test:
    try:
        CONFIG = _get_config("config/test_config.json")
    except Exception as e:
        raise Exception("Please create a config/test_config.json file with the same structure as config/config.json to run with the test config")
else:
    CONFIG = _get_config("config/config.json")
    
if args.date is not None:
    CONFIG.DATE_TODAY = date.fromisoformat(args.date)
    CONFIG.DATETIME_TODAY = datetime.fromisoformat(args.date)
    assert type(CONFIG.DATE_TODAY) == date, "Date must be in YYYY-MM-DD format"
    assert type(CONFIG.DATETIME_TODAY) == datetime, "Date must be in YYYY-MM-DD format"

if args.row is not None:
    CONFIG.SHEET_ROW = int(args.row)
    assert type(CONFIG.SHEET_ROW) == int, "Row must be an integer"
else:
    CONFIG.SHEET_ROW = None

assert CONFIG is not None, "CONFIG must be exported from config.py"