from datetime import datetime
import random
from typing import List, Optional
import requests

from course import Course
from fjutils.sheets.google_sheet import GoogleSheet


def generate_quiz(sheet: GoogleSheet, course: Course, mc_questions: List[dict]) -> Optional[str]:
    """Generates a quiz for a given course and returns the url of the quiz
    """
    quiz_dict = _generate_quiz_dict(sheet, course, mc_questions)

    if quiz_dict == {}:
        return ""

    web_app_url: str = "https://script.google.com/a/macros/fischerjordan.com/s/AKfycbyZAL8HVEorj2hpGR1vOgmaHBASBCbqEF2KwZdNOQ_oIVKip9TUs9SJCb1WPcQVcoiY3w/exec"

    response = requests.post(web_app_url, json=quiz_dict)
    if response.status_code != 200:
        print(f"Error generating quiz for {course.name}")
        return None

    quiz_url = response.text
    course.quiz_date = datetime.today().date()

    return quiz_url

def _generate_quiz_dict(sheet: GoogleSheet, course: Course, mc_questions: List[dict]) -> dict:

    quiz_dict = {}
    number_questions_to_use = int(0)
    course_questions = []
    for question in mc_questions:
        if question['Course'] == course.name:
            course_questions.append(question)
            number_questions_to_use = question['Max Number of Questions to Use in Quiz']
    sheet.sheet.update_cell(course.row_number, sheet.col_search(
        "#Questions in Quiz Available"), number_questions_to_use)
    if number_questions_to_use < 5:
        return quiz_dict
        raise Exception(
            "Could not find number of questions to use from mc question tab")

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