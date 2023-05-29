from dataclasses import dataclass
import json
import re
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
    ADMIN_EMAILS: List[str]
    MAIN_ADMIN_EMAIL: str
    WINDOWS: bool
    TEST: bool
    SECTION_NAMES_NOT_TO_COUNT: List[str]


def _get_config(config_json_path: str) -> TrainingConfig:
    CONFIG = TrainingConfig(0, 0, 0, 0.0, 0.0, [], "",
                            "", "", "", [], "", True, True, [])
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
        CONFIG.ADMIN_EMAILS = config["admin_emails"]
        CONFIG.MAIN_ADMIN_EMAIL = config["main_admin_email"]
        CONFIG.WINDOWS = config["windows"]
        CONFIG.TEST = config["test"]
        CONFIG.SECTION_NAMES_NOT_TO_COUNT = config["section_names_not_to_count"]
    return CONFIG

parser = argparse.ArgumentParser(
    prog="Training Tracker",
    description="A program to track training progress for the FJ Company",
    epilog="Developed by: FJ Company",
)
parser.add_argument('--test', '-t', help="to run with the test config in config/test_config.json", action="store_true")

args = parser.parse_args()
if args.test:
    try:
        CONFIG = _get_config("config/test_config.json")
    except Exception as e:
        raise Exception("Please create a config/test_config.json file with the same structure as config/config.json to run with the test config")
        
else:
    CONFIG = _get_config("config/config.json")

assert CONFIG is not None, "CONFIG must be exported from config.py"