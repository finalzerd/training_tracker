from datetime import datetime
from pathlib import Path
import gspread as gs
from course import Course
from typing import List
import random
import requests
import pandas as pd

import training_emails
from config import _get_config

from fjutils.sheets.google_sheet import GoogleSheet

CONFIG = _get_config("config/config.json")

mc_questions: List[dict] = GoogleSheet("Offline Training Course Repository", "Sheet4").sheet.get_all_records()


def _generate_quiz_dict(self, course: Course, mc_questions: List[dict]) -> dict:
    
    quiz_dict = {}
    number_questions_to_use = int(0)
    course_questions = []
    for question in mc_questions:
        if question['Course'] == course.name:
            course_questions.append(question)
            number_questions_to_use = question['Max Number of Questions to Use in Quiz']
    self.sheet.sheet.update_cell(course.row_number, self.sheet.col_search("#Questions in Quiz Available"), number_questions_to_use)
    if number_questions_to_use < 5:
        return quiz_dict
        raise Exception("Could not find number of questions to use from mc question tab")
        

    random_questions = random.sample(
        course_questions, k=number_questions_to_use)

    questions = []

    for question in random_questions:
        questions.append({"question": question['Question'],
                        "choices": [{"name": question['A1'],
                                    "correct": question['Correct'] == 1},
                                    {"name": question['A2'],
                                    "correct": question['Correct'] == 2},
                                    {"name": question['A3'],
                                    "correct": question['Correct'] == 3},
                                    {"name": question['A4'],
                                    "correct": question['Correct'] == 4},
                                    {"name": question['A5'],
                                    "correct": question['Correct'] == 5}]})

    quiz_dict = {"title": f"{course.name.capitalize()} Quiz",
                "name": course.taker.name,
                "course": course.name,
                "questions": questions}
    
    return quiz_dict

def generate_quiz(self,course:Course, mc_questions: List[dict]) -> str:
    """AI is creating summary for generate_form

    Args:
        course (Course): [one course]
        mc_questions (List[dict]): [all questions from mc question tab]

    Returns:
        str: [form url]
    """
    quiz_dict = self._generate_quiz_dict(course, mc_questions)
    
    if quiz_dict == {}:
        return ""
    
    web_app_url: str = "https://script.google.com/home/projects/15WJmGXkuP7fjbOqTwg8yNCE4BLwqE2p3v6Z6gUdvs0nmy5LEkUiV5gz_/edit"

    response = requests.post(web_app_url, json=quiz_dict)
    
    quiz_url = response.text
    course.quiz_date=datetime.today().date()
    # print(type(course.quiz_date))
    self.sheet.sheet.update_cell(course.row_number, self.sheet.col_search("Quiz sent date"), str(course.quiz_date.strftime("%m/%d/%y")))
      
    
    return quiz_url

def main():
    
    gc = gs.service_account(filename=Path(r"bin\service_account.json"))
    sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1LgThxBOaICV6Ak8GJ0Kqztx0VBo9khr3372wU_cwhuw/edit#gid=1167738258')
    ws = sh.worksheet('Tracker')
    df = pd.DataFrame(ws.get_all_records())
    print(df.shape)
    # for i in range(df.shape[0]):
        
        # if(datetime.strptime(df.iloc[i,3])-datetime.today().date()==1):
        #     training_emails.send_offline_pre_training_email(df.iloc[i,1],df.iloc[i,2])
        # if(datetime.today().date()-df.iloc[i,4]==1):
        #     training_emails.send_offline_post_training_email(df.iloc[i,1],df.iloc[i,2])
            
            
if __name__ == "__main__":
    main()
    
