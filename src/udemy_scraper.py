import os
import time
from typing import List
import random
import json
import pyautogui
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

from dotenv import load_dotenv
load_dotenv()

from config import CONFIG
from course import Course

js_expand_sec = """let dropdownBtns = document.querySelectorAll(
            ".ud-btn.ud-btn-large.ud-btn-link.ud-heading-md.js-panel-toggler.accordion-panel-module--panel-toggler--1RjML"
            );          

            dropdownBtns.forEach((dropdownBtn) => {
            // If is not expanded, then expand it.
            if (dropdownBtn.getAttribute("aria-expanded") === "false") {
                dropdownBtn.click();
            }
            });"""

class UdemyScraper:
    """A web scraper class for training tracker to scrape Udemy courses information"""

    def __init__(self) -> None:
        self.scraper = uc.Chrome(
            browser_executable_path=os.environ.get("CHROME_PATH"),
            driver_executable_path=os.environ.get("CHROMEDRIVER_PATH"),
        )
        self.current_account_username: str | None = None
        
    def _ensure_past_cloudflare(self) -> bool:
        try:
            time.sleep(1)
            self.scraper.set_window_size(1024, 600)
            self.scraper.maximize_window()
            time.sleep(1)
            for i in range(10):
                checkbox = pyautogui.locateOnScreen("assets/cloudflare_checkbox.png")
                if checkbox is None:
                    return True
                time.sleep(1)
                pyautogui.moveTo(checkbox)
                pyautogui.click()
                time.sleep(random.randint(8, 12))
            return False
        except:
            return False
    
    def _ensure_past_press_and_hold(self) -> bool:
        self.scraper.set_window_size(1024, 600)
        self.scraper.maximize_window()
        time.sleep(1)
        
        for i in range(10):
            print(f"start looking for hold {time.time()}")
            checkbox = pyautogui.locateOnScreen("assets/udemy_press_and_hold.png")
            if checkbox is None:
                return True
            print(f"found hold {time.time()}")
            pyautogui.moveTo(checkbox)
            pyautogui.mouseDown()
            time.sleep(random.randint(15, 16))
            pyautogui.mouseUp()
            time.sleep(5)
            if pyautogui.locateOnScreen("assets/udemy_press_and_hold.png") != None:
                continue
            else:
                return True
        return False
    
    def _login_to_account(self, login: str, password: str) -> bool:
        if "udemy.com" not in self.scraper.current_url:
            self.scraper.get("https://www.udemy.com")
        
        if self.current_account_username == login:
            return True
        
        # try to use cookies from file first
        cookies_path = f"cookies/cookies_{login.split('@')[0]}.json"
        try:
            cookies: List[dict] = json.load(open(cookies_path, "r"))
            for cookie in cookies:
                self.scraper.add_cookie(cookie)
            self.current_account_username = login
            self.scraper.refresh()
            if not self._ensure_past_cloudflare() or not self._ensure_past_press_and_hold():
                return False
            return True
        except:
            pass # cookies not found
            
        # try to login with selenium clicking and typing
        self.scraper.get("https://www.udemy.com/join/login-popup/")
        time.sleep(random.randint(3, 4))
        
        if not self._ensure_past_cloudflare() or not self._ensure_past_press_and_hold():
            return False
        
        try:
            time.sleep(random.randint(1, 2))
            self.scraper.find_element(By.XPATH, "//input[@name='email']").send_keys(login)
            time.sleep(random.randint(1, 2))
            self.scraper.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
            time.sleep(random.randint(1, 2))
            
            if "https://www.udemy.com/join/login-popup/" in self.scraper.current_url:
                time.sleep(random.randint(1, 2))
                pyautogui.hotkey("ctrl", "f")
                time.sleep(random.randint(1, 2))
                pyautogui.typewrite("log in")
                time.sleep(random.randint(1, 2))
                pyautogui.hotkey("ctrl", "enter")
                time.sleep(random.randint(1, 2))
                
            time.sleep(random.randint(4, 5))
            
            if not self._ensure_past_cloudflare() or not self._ensure_past_press_and_hold():
                return False
            
            cookies = self.scraper.get_cookies()
            with open(cookies_path, "w") as f:
                json.dump(cookies, f)
            return True
        except:
            return False
        

    def _go_to_course_link(self, course: Course, course_link: str) -> bool:
        """goes to specific course link and expands the and logs in if necessary

        Args:
            course (Course): The course that the link is from
            course_link (str): The specific link to go to from the course

        Returns:
            bool: True if successful, False if not
        """
        if not self._login_to_account(course.login, course.password):
            return False

        time.sleep(random.randint(4, 5))

        time.sleep(random.randint(7, 8))
        self.scraper.execute_script(f"window.location = '{course_link}'")

        print("starting wait")
        time.sleep(random.randint(30, 40))
        print("ending wait")
        self.scraper.execute_script(js_expand_sec)
        time.sleep(random.randint(2, 3))
        return True

    def _expand_sections(self, close_count_exclusions: bool):
        """
        Expands the sections in the course that the driver is currently on
        Only use when driver is on course
        Throws error on failure
        """
        print(1)
        time.sleep(random.randint(1, 4))
        try:
            section_headers: List[str] = [elem.text for elem in self.scraper.find_elements(
                By.CLASS_NAME, "section--section-heading--2k6aW")]
            expand_arrows = self.scraper.find_elements(
                By.CLASS_NAME, "panel--expand-icon--1ZzXo")
            for idx, (arrow, header_name) in enumerate(zip(expand_arrows, section_headers)):
                if close_count_exclusions:
                    if header_name in CONFIG.SECTION_NAMES_NOT_TO_COUNT:
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

    def update_course_completion(self, course: Course, courses: List[Course]) -> bool:

        total_checkboxes = 0
        total_checked_checkboxes = 0
        incomplete_modules: List[str] = []

        # for course_idx, link in enumerate(course.links):
        # print(course.links)
        if (self._go_to_course_link(course, course.links[0])):
            time.sleep(random.randint(1, 3))
            js_expand_sec = """let dropdownBtns = document.querySelectorAll(
            ".ud-btn.ud-btn-large.ud-btn-link.ud-heading-md.js-panel-toggler.accordion-panel-module--panel-toggler--1RjML"
            );          

            dropdownBtns.forEach((dropdownBtn) => {
            // If is not expanded, then expand it.
            if (dropdownBtn.getAttribute("aria-expanded") === "false") {
                dropdownBtn.click();
            }
            });"""
            self.scraper.execute_script(js_expand_sec)
            time.sleep(random.randint(1, 2))

            checkboxes = self.scraper.find_elements(
                By.CLASS_NAME, "curriculum-item-link--progress-toggle--1CMcg.ud-toggle-input-container.ud-text-sm")[:-2]
            # print(checkboxes)
            # remove the exception boxes "coding exercises", we don't want to count them
            exercises = self.scraper.find_elements(
                By.CLASS_NAME, "curriculum-item-link--curriculum-item--KX9MD")
            for module_idx, (checkbox, exercise) in enumerate(zip(checkboxes, exercises)):

                if "Coding Exercise" in exercise.text:
                    continue

                total_checkboxes += 1

                try:

                    if ' complete' in checkbox.text:  # if checked
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
        return False

    def update_course_completion_rescheduled(self, course: Course, courses: List[Course]) -> bool:

        for i in range(len(course.incomplete_modules)):
            course.incomplete_modules[i] = course.incomplete_modules[i][2:]
        total_checkboxes = [eval(i) for i in course.incomplete_modules]
        print(total_checkboxes)
        print(type(total_checkboxes))
        # print(len(total_checkboxes))
        total_checked_checkboxes = 0
        incomplete_modules_re: List[str] = []
        incomplete_modules: List[str] = []

        # for course_idx, link in enumerate(course.links):
        # print(course.links)
        if (self._go_to_course_link(course, course.links[0])):
            time.sleep(random.randint(1, 3))
            js_expand_sec = """let dropdownBtns = document.querySelectorAll(
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
            time.sleep(random.randint(5, 8))
            time.sleep(random.randint(10, 12))
            print('starting again')

            checkboxes = self.scraper.find_elements(
                By.CLASS_NAME, "curriculum-item-link--progress-toggle--1CMcg.ud-toggle-input-container.ud-text-sm")[:-2]
            print(len(checkboxes))
            # remove the exception boxes "coding exercises", we don't want to count them
            exercises = self.scraper.find_elements(
                By.CLASS_NAME, "curriculum-item-link--curriculum-item--KX9MD")
            for module_idx, (checkbox, exercise) in enumerate(zip(checkboxes, exercises)):

                if "Coding Exercise" in exercise.text:
                    continue

                try:
                    # print(type(total_checkboxes[module_idx]),module_idx, type(module_idx),total_checkboxes.count(module_idx), type(total_checkboxes.count(module_idx)))
                    if ((total_checkboxes.count(module_idx))) >= 0:
                        if ' complete' in checkbox.text:  # if checked
                            total_checked_checkboxes += 1
                        else:
                            incomplete_modules_re.append(f"0-{module_idx}")
                except:
                    continue

            # assert total_checkboxes > 5, "Found less than 5 checkboxes total"
            print("total checked boxes ", total_checked_checkboxes)
            course.box_completion = total_checked_checkboxes / \
                (len(total_checkboxes)+total_checked_checkboxes)
            print(f"Box completion: {course.box_completion}")
            course.incomplete_modules = incomplete_modules_re
            return True
        return False

    def _reset_link(self):
        # """Works if course link is opened. Resets at start to what is needed"""

        js_reset_course = """

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
        time.sleep(random.randint(5, 6))
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

        #             time.sleep(random.randint(1,4))
        #             all_buttons = self.scraper.find_elements(By.CLASS_NAME, "udlite-btn-ghost")
        #                     time.sleep(random.randint(1,4))
        #                     break
        #             all_buttons = self.scraper.find_elements(By.CLASS_NAME, "udlite-btn-primary")
        #                     time.sleep(random.randint(1,4))
        #                     break
        #     except:
        #         raise
        #         return False
        # return True

    def reset_course(self, course: Course) -> bool:
        """Clears all links in the course by going to each one"""
        if (self._go_to_course_link(course, course.links[0])):
            time.sleep(5.0)
            print("calling reset link")
            self._reset_link()
            print("control back to calling func")
        return True