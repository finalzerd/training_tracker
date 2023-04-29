__author__ = "noah.provenzano@fischerjordan.com"

from datetime import datetime
import time
import pyautogui
from typing import Dict, List
import random
import requests
import pickle
import json

from .dataclasses.course import Course, CourseTaker
from .selenium_scraper import SeleniumScraper
from .google_sheet import GoogleSheet
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

js_expand_sec="""let dropdownBtns = document.querySelectorAll(
            ".ud-btn.ud-btn-large.ud-btn-link.ud-heading-md.js-panel-toggler.accordion-panel-module--panel-toggler--1RjML"
            );          

            dropdownBtns.forEach((dropdownBtn) => {
            // If is not expanded, then expand it.
            if (dropdownBtn.getAttribute("aria-expanded") === "false") {
                dropdownBtn.click();
            }
            });"""
class TrainingTracker:
    """tracker class for main function to use abstractly"""

    def __init__(self, training_sheet: GoogleSheet) -> None:
        self.scraper = SeleniumScraper(windows=True)
        self.sheet = training_sheet
        self.current_account = ""
        self.forms_credentials = ["sitetracker@fischerjordan.com", "Calcinosis3"]
        self.logged_into_google = False
        self.section_names_to_not_count: List[str] = ["Section 22: APPENDIX: OLDER PYTHON 2 MATERIAL", 
                                                     "Section 23: BONUS SECTION: THANK YOU!",
                                                     "Section 21: Bonus Material - Introduction to GUIs",
                                                     "Section 1: Course Overview",
                                                     "Section 1: Introduction",
                                                     "Section 1: Welcome to the Complete Microsoft PowerPoint Course",
                                                     "Section 1: Welcome",
                                                     "Section 7: BONUS Section: Database Design",
                                                     "Section 42: Course Wrap Up",
                                                     "Section 1: Microsoft Excel 101 Course Introduction",
                                                     "Section 7: Added Material: Putting it all together in a real life example",
                                                     "Section 8: Appendix: Stochastic & Markov Processes for Jarrow Model"]


    def get_courses(self) -> List[Course]:
        courses: List[Course] = []
        tracker_sheet: List[Dict[str, str]] = self.sheet.sheet.get_all_records()
        i=0
        for row in tracker_sheet:
            
            try:
                box_completion = float(row['Boxes Completion'])
            except:
                box_completion = None
                
            incomplete_modules: List[str] = row['Incomplete Modules'].split(", ")
            if incomplete_modules[0] == "":
                incomplete_modules.clear()
                
            courses.append(Course(row_number=i+2,
                                  name = row['Course'],
                                  links = row['Course Link'].split(", "),
                                  login = row['email'],
                                  password = row['password'],
                                  start_date = datetime.strptime(row['Start Date'], "%m/%d/%y"),
                                  end_date = datetime.strptime(row['End Date'], "%m/%d/%y"),
                                  taker = CourseTaker(name = row['Name'], 
                                                      email = row['Email']),
                                  box_completion = box_completion,
                                  feedback_provided = row['Feedback Provided'] == 1,
                                  is_reschedule = row['Is a Reschedule'] == "TRUE",
                                  was_rescheduled = row['Was Rescheduled'] == "TRUE",
                                  incomplete_modules = incomplete_modules,
                                  needs_reschedule = row['Needs Reschedule'] == "TRUE",
                                  currently_tracking = row['Currently Tracking'] == "TRUE",
                                  quiz1 = row['Quiz1'],
                                  quiz2 = row['Quiz2'],
                                  complete_with_quiz = row['Complete'] == 1,
                                  quiz_url = row['Quiz URL'],
                                  only_quiz=row['Only Quiz'],
                                  only_feed=row['Only feedback'],
                                  to_be_check=row['To be checked'],
                                  final_state=row['FINAL STATE'],
                                  quiz_date=row['Quiz sent date'],
                                  quiz_result=row['quiz results']
                                  ))
            i=i+1
        return courses

    def _go_to_course_link(self, course: Course, link: str)->bool:
        if not self.current_account == course.login:
            
            self.scraper.get("https://www.udemy.com")
            # cookies_path= "C:\Processes\training_tracker\bin"
            if course.login == "anoushka.khanna@fischerjordan.com":
                cookies = json.load(open(r"bin\cookies_anoushka.json", "r"))
            elif course.login == "engage@fischerjordan.com":
                cookies = json.load(open(r"bin\cookies_engage.json", "r", newline=''))
            elif course.login == "rprogramming.fj@gmail.com":
                cookies = json.load(open(r"bin\cookies_rprogramming.json", "r"))
            elif course.login == "salikb@yahoo.com":
                cookies = json.load(open(r"bin\cookies_salikb.json", "r"))
            elif course.login == "regressionmodeling.fj@gmail.com":
                cookies = json.load(open(r"bin\cookies_regressionmodelling.json", "r"))    
            elif course.login == "projectmanagement.fj@gmail.com":
                cookies = json.load(open(r"bin\cookies_projectmanagement.json", "r"))
            elif course.login == "darshana.shetty@fischerjordan.com":
                cookies = json.load(open(r"bin\cookies_darshana.json", "r"))
            else:
                raise Exception(f"No login cookies for {course.login}")

            time.sleep(random.randint(1,4))

            for cookie in cookies:
                self.scraper.add_cookie(cookie)
                # time.sleep(random.randint(1,4).5)

            self.scraper.wait(seconds=random.randint(1,3))  
            # self.get_cookies_func(course.login)
            self.scraper.execute_script(f"window.location = '{link}'")
              
            print("starting wait")
            time.sleep(random.randint(4,5))
            print("ending wait")
            self.scraper.execute_script(js_expand_sec)
            self.scraper.wait(seconds=random.randint(2,3)) 
            # print(self.scraper.find_elements(By.CLASS_NAME, "curriculum-item-link--progress-toggle--1CMcg ud-toggle-input-container ud-text-sm"))
            # print(len((self.scraper.find_elements(By.CLASS_NAME, "curriculum-item-link--progress-toggle--1CMcg ud-toggle-input-container ud-text-sm"))))

            if(len(self.scraper.find_elements(By.CLASS_NAME, "curriculum-item-link--progress-toggle--1CMcg.ud-toggle-input-container.ud-text-sm"))==0):
                print("loading cookies again")
                self.scraper.delete_all_cookies()  
                self.scraper.wait(seconds=random.randint(1,2))
                self._go_to_course_link(course,link)


            # time.sleep(random.randint(1,3))
            
            return True
       
            
            # Old Style
            # self.scraper.get("https://www.udemy.com/join/login-popup/?locale=en_US&response_type=html&next=https%3A%2F%2Fwww.udemy.com%2F")
            # self.scraper.wait(seconds=1)
            # self.ensure_human_verification_completed()
            # self.scraper.wait(seconds=1)            
            # self.scraper.find_element(By.ID, "email--1").send_keys(course.login)
            # self.scraper.wait(seconds=1)
            # self.scraper.find_element(By.ID, "id_password").send_keys(course.password)
            # self.scraper.wait(seconds=1)
            # self.scraper.find_element(By.ID, "submit-id-submit").click()
            # self.scraper.wait(seconds=3)
            # self.current_account = True
            # self.ensure_human_verification_completed()
            
            self.current_account = course.login

        

        # self.scraper.get(link)
        # self.scraper.wait(seconds=2)
        
        try:
            not_now_button = self.scraper.find_element(By.CLASS_NAME, "ab-message-button")
            if not_now_button.text == "Not now":
                not_now_button.click()
                self.scraper.wait(seconds=2)
        except:
            pass
       

        
        # self._expand_sections(close_count_exclusions=False)
        
    def _expand_sections(self, close_count_exclusions:bool):
        """
        Expands the sections in the course that the driver is currently on
        Only use when driver is on course
        Throws error on failure
        """
        print(1)
        time.sleep(random.randint(1,4))
        try:
            section_headers: List[str] = [elem.text for elem in self.scraper.find_elements(By.CLASS_NAME, "section--section-heading--2k6aW")]
            expand_arrows = self.scraper.find_elements(By.CLASS_NAME, "panel--expand-icon--1ZzXo")
            for idx, (arrow, header_name) in enumerate(zip(expand_arrows, section_headers)):
                if close_count_exclusions:
                    if header_name in self.section_names_to_not_count:
                        # Close section
                        if not arrow.value_of_css_property("transform") == "none":
                            self.scraper.scroll_to(arrow)
                            arrow.click()
                        continue
                    
                # Otherwise expand the section
                if arrow.value_of_css_property("transform") == "none":
                    self.scraper.scroll_to(arrow)
                    arrow.click()
        except:
            raise Exception("Unable to expand sections")

    def update_course_completion(self, course:Course, courses:List[Course]) -> bool:
        
        
        total_checkboxes = 0
        total_checked_checkboxes = 0
        incomplete_modules: List[str] = []
                
        # for course_idx, link in enumerate(course.links):
        # print(course.links)
        if(self._go_to_course_link(course, course.links[0])):
            time.sleep(random.randint(1,3))
            js_expand_sec="""let dropdownBtns = document.querySelectorAll(
            ".ud-btn.ud-btn-large.ud-btn-link.ud-heading-md.js-panel-toggler.accordion-panel-module--panel-toggler--1RjML"
            );          

            dropdownBtns.forEach((dropdownBtn) => {
            // If is not expanded, then expand it.
            if (dropdownBtn.getAttribute("aria-expanded") === "false") {
                dropdownBtn.click();
            }
            });"""
            self.scraper.execute_script(js_expand_sec)
            time.sleep(random.randint(1,2))
            
            checkboxes = self.scraper.find_elements(By.CLASS_NAME, "curriculum-item-link--progress-toggle--1CMcg.ud-toggle-input-container.ud-text-sm")[:-2]
            # print(checkboxes)
            # remove the exception boxes "coding exercises", we don't want to count them
            exercises = self.scraper.find_elements(By.CLASS_NAME, "curriculum-item-link--curriculum-item--KX9MD")  
            for module_idx, (checkbox, exercise) in enumerate(zip(checkboxes, exercises)):
                
                if "Coding Exercise" in exercise.text:
                    continue
                
                total_checkboxes += 1
                
                try:
                
                    if ' complete' in checkbox.text: # if checked
                        total_checked_checkboxes += 1
                    else:
                        incomplete_modules.append(f"0-{module_idx}")    
                except:
                    continue
                        
            assert total_checkboxes > 5, "Found less than 5 checkboxes total" 
            print(total_checkboxes) 
            print(total_checked_checkboxes)            
            course.box_completion = total_checked_checkboxes / total_checkboxes
            print(f"Box completion: {course.box_completion}")
            course.incomplete_modules = incomplete_modules
            return True
    
    def update_course_completion_rescheduled(self, course:Course, courses:List[Course]) -> bool:
        
        
        for i in range(len(course.incomplete_modules)):
            course.incomplete_modules[i]= course.incomplete_modules[i][2:]
        total_checkboxes = [eval(i) for i in course.incomplete_modules]
        print(total_checkboxes)
        print(type(total_checkboxes))
        # print(len(total_checkboxes))
        total_checked_checkboxes = 0
        incomplete_modules_re: List[str] = []
        incomplete_modules: List[str] = []
                
        # for course_idx, link in enumerate(course.links):
        # print(course.links)
        if(self._go_to_course_link(course, course.links[0])):
            time.sleep(random.randint(1,3))
            js_expand_sec="""let dropdownBtns = document.querySelectorAll(
            ".ud-btn.ud-btn-large.ud-btn-link.ud-heading-md.js-panel-toggler.accordion-panel-module--panel-toggler--1RjML"
            );          

            dropdownBtns.forEach((dropdownBtn) => {
            // If is not expanded, then expand it.
            if (dropdownBtn.getAttribute("aria-expanded") === "false") {
                dropdownBtn.click();
            }
            });"""
            print("rescheduled update called")
            self.scraper.execute_script(js_expand_sec)
            # time.sleep(random.randint(,3))
            print(len(total_checkboxes))
            print('waiting')
            time.sleep(random.randint(5,8))
            self.scraper.wait(seconds=random.randint(10,12))
            print('starting again')
            
            checkboxes = self.scraper.find_elements(By.CLASS_NAME, "curriculum-item-link--progress-toggle--1CMcg.ud-toggle-input-container.ud-text-sm")[:-2]
            print(len(checkboxes))
            # remove the exception boxes "coding exercises", we don't want to count them
            exercises = self.scraper.find_elements(By.CLASS_NAME, "curriculum-item-link--curriculum-item--KX9MD")  
            for module_idx, (checkbox, exercise) in enumerate(zip(checkboxes, exercises)):
                
                if "Coding Exercise" in exercise.text:
                    continue
                
                
                
                try:
                    # print(type(total_checkboxes[module_idx]),module_idx, type(module_idx),total_checkboxes.count(module_idx), type(total_checkboxes.count(module_idx)))
                    if((total_checkboxes.count(module_idx)))>0:
                        if ' complete' in checkbox.text : # if checked
                            total_checked_checkboxes += 1
                        else:
                            incomplete_modules_re.append(f"0-{module_idx}")    
                except:
                    continue
                        
            # assert total_checkboxes > 5, "Found less than 5 checkboxes total"  
            print("total checked boxes ", total_checked_checkboxes)            
            course.box_completion = total_checked_checkboxes / len(total_checkboxes)
            print(f"Box completion: {course.box_completion}")
            course.incomplete_modules = incomplete_modules_re
            return True
        
    def log_completion(self, row: int, course: Course) -> None:
        try:
            boxes_completion_entry = [float(course.box_completion)]
        except:
            boxes_completion_entry = ["Error"]
        try:
            incomplete_modules_entry = [", ".join(course.incomplete_modules)]
        except:
            incomplete_modules_entry = ["Error"]
        self.sheet.write_list(row, self.sheet.col_search("Boxes Completion"), boxes_completion_entry)
        time.sleep(random.randint(1,2))
        self.sheet.write_list(row, self.sheet.col_search("Incomplete Modules"), incomplete_modules_entry)
        time.sleep(random.randint(1,2))

    def log_precompletion_email(self, row: int, sent: bool) -> None:
        sent_str = "EMAIL_SENT" if sent else "NOT_NEEDED"
        self.sheet.write_list(row, self.sheet.col_search("Precompletion Reminder Email"), [sent_str])
         
    def log_completion_email(self, row: int, is_complete: bool) -> None:
        sent_str = "EMAIL_SENT" if is_complete else "RESCHEDULE_EMAIL_SENT"
        self.sheet.write_list(row, self.sheet.col_search("Completion Email"), [sent_str])
    
    def log_welcome_email(self, row: int) -> None:
        self.sheet.write_list(row, self.sheet.col_search("Welcome Email"), ["EMAIL_SENT"])
        
    def log_cleared_course(self, row: int) -> None:
        self.sheet.write_list(row, self.sheet.col_search("Course Cleared"), ["CLEARED_FOR_START"])

    def log_quiz_completion_email(self, row: int, is_complete: bool) -> None:
        sent_str = 1 if is_complete else 0
        self.sheet.write_list(row, self.sheet.col_search("Complete"), [sent_str])
    
    def reset_link(self):
        # """Works if course link is opened. Resets at start to what is needed"""
        
        js_reset_course= """

        console.log("Helllo");
        // Get all the input checkboxes
        var inputCheckBoxes = document.querySelectorAll(
        ".curriculum-item-link--progress-toggle--1CMcg.ud-toggle-input-container.ud-text-sm"
        );

        inputCheckBoxes.forEach((inputCheckBox) => {
        // If checked, then uncheck it.
        if(inputCheckBox.textContent.indexOf(" complete") !== -1) {
            inputCheckBox.click()
        }
        });
        console.log("code executed");"""
        
        self.scraper.execute_script(js_reset_course)
        time.sleep(random.randint(5,6))
        print("reset function called")
        # self._expand_sections(close_count_exclusions=False)
        # time.sleep(random.randint(1,4))
        # print("check")
        # checkboxes = self.scraper.find_elements(By.CLASS_NAME, "udlite-icon.udlite-icon-xsmall.udlite-fake-toggle-input.udlite-fake-toggle-checkbox")[:-2]
        # exercises = self.scraper.find_elements(By.CLASS_NAME, "curriculum-item-link--curriculum-item--KX9MD")
        # for idx, (checkbox, exercise) in enumerate(zip(checkboxes, exercises)):
        #     try:
        #         is_checked = not checkbox.value_of_css_property("color") == "rgba(0, 0, 0, 0)"
        #         if is_checked:
        #             self.scroll_element_into_view(checkbox)
        #             time.sleep(random.randint(1,4))
        #             print(1)
        #             checkbox.click()
        #             continue
                
        #         if "Coding Exercise" in exercise.text:
        #             print(2)
        #             exercise.click()
                    
        #             # Click the reset code button
        #             time.sleep(random.randint(1,4))
        #             all_buttons = self.scraper.find_elements(By.CLASS_NAME, "udlite-btn-ghost")
        #             for button in all_buttons:
        #                 if button.text == "Reset code":
        #                     button.click()
        #                     time.sleep(random.randint(1,4))
        #                     break
        #             # Click the yes reset button
        #             all_buttons = self.scraper.find_elements(By.CLASS_NAME, "udlite-btn-primary")
        #             for button in all_buttons:
        #                 if button.text == "Yes, reset":
        #                     button.click()
        #                     time.sleep(random.randint(1,4))
        #                     break
        #     except:
        #         raise
        #         return False
        # return True
        
    def reset_course(self, course: Course)-> bool:
        """Clears all links in the course by going to each one"""
        if(self._go_to_course_link(course, course.links[0])):
            time.sleep(5.0)
            print("calling reset link")
            self.reset_link()
            print("control back to calling func")    
        return True

    def reset_course_reschedule(self, course:Course) -> bool:
        # """Works if course link is opened. Resets at start to what is needed"""
        if(self._go_to_course_link(course, course.links[0])):
             time.sleep(1.0)
        incomplete_mods=course.to_be_check
        incomplete_mods=[e[2:] for e in incomplete_mods]
        print(incomplete_mods)
        incomplete_mods = [int(i) for i in incomplete_mods]

        # with open(r'\bin\incomplete.txt',"w") as file:
        #     file.writelines(incomplete_mods)


        js_reset_course= """
        console.log("Helllo");
        // Get all the input checkboxes
        let inputCheckBoxes = document.querySelectorAll(
        ".curriculum-item-link--progress-toggle--1CMcg.ud-toggle-input-container.ud-text-sm"
        );

        inputCheckBoxes.forEach((inputCheckBox) => {
        // If checked, then uncheck it.
        if(inputCheckBox.textContent.indexOf(" complete") !== -1) {
            inputCheckBox.click()
        }
        });
        var i=0
        inputCheckBoxes.forEach((inputCheckBox) => {

        if(incomplete_mods.indexOf(i)==-1) {
            inputCheckBox.click()
        }
        i=i+1
        });
        console.log("code executed");"""
        
        self.scraper.execute_script(js_reset_course,incomplete_mods)
        time.sleep(random.randint(2,3))
        print("reset function called")  
        return True
        
    def need_to_complete_modules_from_previous_enrollment(self, course:Course, courses:List[Course]) -> List[str]:
        """
        Only for rescheduled courses, returns list of modules that weren't completed last time if any.
        """
        if not course.is_reschedule:
            return []
        for other_course in courses:
            if other_course.name == course.name and other_course.taker.name == course.taker.name:
                return other_course.incomplete_modules
            
        raise ValueError("Modules not found")
    
    def ensure_human_verification_completed(self,
                                    max_tries:int=6,
                                    wait_between_tries:int=4,
                                    max_hold_per_try:int=10) -> None:
        try:
            self.scraper.find_element(By.ID, "px-captcha")
        except:
            return # All good
        
        num_tries: int = 0
        
        start_time = time.perf_counter()
        pyautogui.mouseDown(x=286, y=308, button='left')
        print('mouse down')
        
        while time.perf_counter() - start_time < 10:
            if pyautogui.locateOnScreen("bin\check.png"):
                time.sleep(0.4)
                break
                    
        pyautogui.mouseUp()
        print("mouse up")
            
        try:
            self.scraper.find_element(By.ID, "px-captcha")
            num_tries += 1
            time.sleep(wait_between_tries)
        except:
            return
        
        raise Exception("Couldn't pass human verification")

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
        
        web_app_url: str = "https://script.google.com/a/macros/fischerjordan.com/s/AKfycbyZAL8HVEorj2hpGR1vOgmaHBASBCbqEF2KwZdNOQ_oIVKip9TUs9SJCb1WPcQVcoiY3w/exec"

        response = requests.post(web_app_url, json=quiz_dict)
        
        quiz_url = response.text
        course.quiz_date=datetime.today().date()
        # print(type(course.quiz_date))
        self.sheet.sheet.update_cell(course.row_number, self.sheet.col_search("Quiz sent date"), str(course.quiz_date.strftime("%m/%d/%y")))
        
        
        
        return quiz_url
    
    def get_cookies_func(self, course)-> None:
        # driver= selenium.webdriver.Firefox()
        # self.scraper.get("https://www.udemy.com")
        cookies=self.scraper.get_cookies()
        if course == "engage@fischerjordan.com":
            with open(r"bin\cookies_engage.json", "w")as outfile:
                json.dump(cookies, outfile)
        elif course =="anoushka.khanna@fischerjordan.com":
            with open(r"bin\cookies_anoushka.json", "w")as outfile:
                json.dump(cookies, outfile)
        elif course =="rprogramming.fj@gmail.com":
            with open(r"bin\cookies_rprogramming.json", "w")as outfile:
                json.dump(cookies, outfile)
        elif course =="regressionmodeling.fj@gmail.com":
            with open(r"bin\cookies_regressionmodelling.json", "w")as outfile:
                json.dump(cookies, outfile)
        elif course =="projectmanagement.fj@gmail.com":
            with open(r"bin\cookies_projectmanagement.json", "w")as outfile:
                json.dump(cookies, outfile)
        elif course =="salikb@yahoo.com":
            with open(r"bin\cookies_salikb.json", "w")as outfile:
                json.dump(cookies, outfile)
        elif course =="darshana.shetty@fischerjordan.com":
            with open(r"bin\cookies_darshana.json", "w")as outfile:
                json.dump(cookies, outfile)
        else:
                raise Exception(f"No login cookies for {course.login}")        
        return None
        
        
    
    
    