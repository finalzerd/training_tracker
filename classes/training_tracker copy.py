__author__ = "noah.provenzano@fischerjordan.com"

from datetime import datetime
import os
import sys
import time
# os.environ['DISPLAY'] = ':0'
# import pyautogui
from typing import Dict, List


from training_course import Course, CourseTaker
from selenium_scraper import SeleniumScraper
from google_sheet import GoogleSheet


class TrainingTracker:
    """tracker class for main function to use abstractly"""

    def __init__(self, training_sheet: GoogleSheet, windows:bool = False) -> None:
        self.scraper = SeleniumScraper(windows=windows)
        self.sheet = training_sheet
        self.is_logged_in = False
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
        
        for row in tracker_sheet:
            
            try:
                box_completion = float(row['Boxes Completion'])
            except:
                box_completion = None
                
            incomplete_modules: List[str] = row['Incomplete Modules'].split(", ")
            if incomplete_modules[0] == "":
                incomplete_modules.clear()
                
            courses.append(Course(name = row['Course'],
                                  links = row['Course Links'].split(", "),
                                  login = row['email'],
                                  password = row['password'],
                                  start_date = datetime.strptime(row['Start Date'], "%m/%d/%y"),
                                  end_date = datetime.strptime(row['End Date'], "%m/%d/%y"),
                                  taker = CourseTaker(name = row['Name'], 
                                                      email = row['Email']),
                                  box_completion = box_completion,
                                  feedback_provided = row['Feedback provided'] == 1,
                                  is_reschedule = row['Is a Reschedule'] == "TRUE",
                                  was_rescheduled = row['Was Rescheduled'] == "TRUE",
                                  incomplete_modules = incomplete_modules,
                                  needs_reschedule = row['Needs Reschedule'] == "TRUE",
                                  currently_tracking = row['Currently Tracking'] == "TRUE"))

        return courses

    def _go_to_course_link(self, course: Course, link: str):
        if link in self.scraper.current_url:
            return
        if self.is_logged_in == False:
            self.scraper.get("https://www.udemy.com/join/login-popup/?locale=en_US&response_type=html&next=https%3A%2F%2Fwww.udemy.com%2F")
            self.scraper.wait(seconds=1)
            self.scraper.find_element_by_id("email--1").send_keys(course.login)
            self.scraper.wait(seconds=1)
            self.scraper.find_element_by_id("id_password").send_keys(course.password)
            self.scraper.wait(seconds=1)
            self.scraper.find_element_by_id("submit-id-submit").click()
            self.scraper.wait(seconds=3)
            self.is_logged_in = True
            # self.get_past_human_verification()
            time.sleep(1)          

        self.scraper.get(link)
        self.scraper.wait(seconds=2)
        
        self._expand_sections(close_count_exclusions=True)
        

    def _expand_sections(self, close_count_exclusions:bool):
        """
        Expands the sections in the course that the driver is currently on
        Only use when driver is on course
        """
        try:
            section_headers: List[str] = [elem.text for elem in self.scraper.find_elements_by_class_name("section--section-heading--2k6aW")]
            expand_arrows = self.scraper.find_elements_by_class_name("panel--expand-icon--1ZzXo")
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
            print("couldn't expand sections")

    def update_course_completion(self, course:Course, courses:List[Course]) -> None:
        total_checkboxes = 0
        total_checked_checkboxes = 0
        incomplete_modules: List[str] = []
        self.is_logged_in = False # Always re-sign in to courses because might be different 
        self.scraper.delete_all_cookies()
                
        for course_idx, link in enumerate(course.links):
            self._go_to_course_link(course, link)
            time.sleep(1)
            
            checkboxes = self.scraper.find_elements_by_class_name("udlite-fake-toggle-checkbox")[:-2]
                        
            # remove the exception boxes "coding exercises", we don't want to count them
            # also remove all modules except the ones the person didn't complete last time
            need_to_complete_modules: List[str] = self.need_to_complete_modules_from_previous_enrollment(course, courses) # Is only used if is a rescheduled course
            exercises = self.scraper.find_elements_by_class_name("curriculum-item-link--curriculum-item--KX9MD")  
            good_checkboxes = []
            for idx, (checkbox, exercise) in enumerate(zip(checkboxes, exercises)):
                if not "Coding Exercise" in exercise.text:
                    if course.is_reschedule and not len(need_to_complete_modules) == 0:
                        if f"{course_idx}-{idx}" in need_to_complete_modules:
                            good_checkboxes.append(checkbox)
                        else:
                            continue
                    else:
                        good_checkboxes.append(checkbox)
            
            total_checkboxes += len(good_checkboxes)
            
            for idx, checkbox in enumerate(good_checkboxes):
                if not checkbox.value_of_css_property("color") == "rgba(0, 0, 0, 0)": # if checked
                    total_checked_checkboxes += 1
                else:
                    incomplete_modules.append(f"{course_idx}-{idx}")
                    
        course.box_completion = total_checked_checkboxes / total_checkboxes
        course.incomplete_modules = incomplete_modules
        
    def log_completion(self, row: int, course: Course) -> None:
        try:
            boxes_completion_entry = [str(course.box_completion)]
        except:
            boxes_completion_entry = ["Error"]
        try:
            incomplete_modules_entry = [", ".join(course.incomplete_modules)]
        except:
            incomplete_modules_entry = ["Error"]
        self.sheet.write_list(row, self.sheet.col_search("Boxes Completion"), boxes_completion_entry)
        self.sheet.write_list(row, self.sheet.col_search("Incomplete Modules"), incomplete_modules_entry)

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

    def reset_link(self) -> bool:
        """works if course link is opened. resets it for next person"""
        
        self._expand_sections(close_count_exclusions=False)
        
        checkboxes = self.scraper.find_elements_by_class_name("udlite-fake-toggle-checkbox")[:-2]
        exercises = self.scraper.find_elements_by_class_name("curriculum-item-link--curriculum-item--KX9MD")
        
        for idx, (checkbox, exercise) in enumerate(zip(checkboxes, exercises)):
            try:
                is_checked = not checkbox.value_of_css_property("color") == "rgba(0, 0, 0, 0)"
                if is_checked:
                    checkbox.click()
                
                if "Coding Exercise" in exercise.text:
                    exercise.click()
                    # Click the reset code button
                    time.sleep(2)
                    all_buttons = self.scraper.find_elements_by_class_name("udlite-btn-ghost")
                    for button in all_buttons:
                        if button.text == "Reset code":
                            button.click()
                            time.sleep(2)
                            break
                    # Click the yes reset button
                    all_buttons = self.scraper.find_elements_by_class_name("udlite-btn-primary")
                    for button in all_buttons:
                        if button.text == "Yes, reset":
                            button.click()
                            time.sleep(2)
                            break
            except:
                return False
        return True
        
    def reset_course(self, course: Course):
        """Clears all links in the course by going to each one"""
        for link in course.links:
            self.scraper.delete_all_cookies()
            self._go_to_course_link(course, link)
            self.reset_link()        
        
        
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
    
    # def get_past_human_verification(self, max_tries:int=6, wait_between_tries:int=2) -> None:
    #     try:
    #         num_tries: int = 0
            
    #         while num_tries < max_tries:
    #             pyautogui.moveTo(400, 450)
    #             pyautogui.mouseDown()
    #             time.sleep(10)
    #             pyautogui.mouseUp()
                
    #             try:
    #                 self.scraper.find_element_by_class_name("header--dropdown-button-text--2jtIM")
    #                 return
    #             except:
    #                 num_tries += 1
    #                 time.sleep(wait_between_tries)
    #     except:
    #         print("Error trying to get past human verficiaion")
    
    
