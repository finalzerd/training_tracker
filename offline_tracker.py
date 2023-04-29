import code
from datetime import date, datetime, time, timedelta
import time
import gspread as gs
from classestt.training_tracker import TrainingTracker
from classestt.google_sheet import GoogleSheet
from classestt.training_email_sender import TrainingEmailSender
from classestt.dataclasses.course import Course
from classestt.email import TextEmail
from classestt.training_reset_issue import ResetCourse 
from typing import List
import random
import requests
import pandas as pd

code_admin = ["yash.jain@fischerjordan.com","ayushman.agrawal@fischerjordan.com","muskan.laul@fischerjordan.com"]

mc_questions: List[dict] = GoogleSheet("Offline Training Course Repository", "Sheet4").sheet.get_all_records()
email_sender = TrainingEmailSender()


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
    # start_email = TextEmail(to=code_admin, subject="Starting Training Tracker")
    # start_email.send()
    
    gc = gs.service_account(filename=r"bin\service_account.json")
    sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1LgThxBOaICV6Ak8GJ0Kqztx0VBo9khr3372wU_cwhuw/edit#gid=1167738258')
    ws = sh.worksheet('Tracker')
    df = pd.DataFrame(ws.get_all_records())
    print(df.shape)
    for i in range(df.shape[0]):
        
        if(df.iloc[i,3]-datetime.today().date()==1):
            email_sender.offline_pretraining()
        if(datetime.today().date()-df.iloc[i,4]==1):
            email_sender.offline_posttraining()    
            
            
    # print(df.head())
    
if __name__ == "__main__":
    main()
    
