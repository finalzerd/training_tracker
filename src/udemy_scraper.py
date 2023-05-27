import time
from typing import List
import random
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import CONFIG
from course import Course

from fjutils.scraping.selenium_scraper import SeleniumScraper

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
    """tracker class for main function to use abstractly"""

    def __init__(self) -> None:
        self.scraper = SeleniumScraper(windows=CONFIG.WINDOWS)
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
        
        self.CONFIG = CONFIG
        self.current_account_username: str | None = None

    def _go_to_course_link(self, course: Course, link: str) -> bool:
        """goes to course link and logs in if necessary"""
        self.scraper.get("https://www.udemy.com")
        # cookies_path= "C:\Processes\training_tracker\bin"
        if course.login == "anoushka.khanna@fischerjordan.com":
            cookies = json.load(open(r"bin\cookies_anoushka.json", "r"))
        elif course.login == "engage@fischerjordan.com":
            cookies = json.load(
                open(r"bin\cookies_engage.json", "r", newline=''))
        elif course.login == "rprogramming.fj@gmail.com":
            cookies = json.load(
                open(r"bin\cookies_rprogramming.json", "r"))
        elif course.login == "salikb@yahoo.com":
            cookies = json.load(open(r"bin\cookies_salikb.json", "r"))
        elif course.login == "regressionmodeling.fj@gmail.com":
            cookies = json.load(
                open(r"bin\cookies_regressionmodelling.json", "r"))
        elif course.login == "projectmanagement.fj@gmail.com":
            cookies = json.load(
                open(r"bin\cookies_projectmanagement.json", "r"))
        elif course.login == "darshana.shetty@fischerjordan.com":
            cookies = json.load(open(r"bin\cookies_darshana.json", "r"))
        else:
            raise Exception(f"No login cookies for {course.login}")

        time.sleep(random.randint(7, 8))

        for cookie in cookies:
            self.scraper.add_cookie(cookie)
            # time.sleep(random.randint(1,4).5)

        self.scraper.wait(seconds=random.randint(7, 8))
        # self.get_cookies_func(course.login)
        self.scraper.execute_script(f"window.location = '{link}'")

        print("starting wait")
        time.sleep(random.randint(30, 40))
        print("ending wait")
        self.scraper.execute_script(js_expand_sec)
        self.scraper.wait(seconds=random.randint(2, 3))
        # print(self.scraper.find_elements(By.CLASS_NAME, "curriculum-item-link--progress-toggle--1CMcg ud-toggle-input-container ud-text-sm"))
        # print(len((self.scraper.find_elements(By.CLASS_NAME, "curriculum-item-link--progress-toggle--1CMcg ud-toggle-input-container ud-text-sm"))))

        if (len(self.scraper.find_elements(By.CLASS_NAME, "curriculum-item-link--progress-toggle--1CMcg.ud-toggle-input-container.ud-text-sm")) == 0):
            print("loading cookies again")
            self.scraper.delete_all_cookies()
            self.scraper.wait(seconds=random.randint(1, 2))
            self._go_to_course_link(course, link)

        # time.sleep(random.randint(1,3))

        return True

        # self.scraper.get(link)
        # self.scraper.wait(seconds=2)

        try:
            not_now_button = self.scraper.find_element(
                By.CLASS_NAME, "ab-message-button")
            if not_now_button.text == "Not now":
                not_now_button.click()
                self.scraper.wait(seconds=2)
        except:
            pass

        # self._expand_sections(close_count_exclusions=False)

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
            self.scraper.wait(seconds=random.randint(10, 12))
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

    def reset_link(self):
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

    def reset_course(self, course: Course) -> bool:
        """Clears all links in the course by going to each one"""
        if (self._go_to_course_link(course, course.links[0])):
            time.sleep(5.0)
            print("calling reset link")
            self.reset_link()
            print("control back to calling func")
        return True

    def get_cookies_func(self, course) -> None:
        # driver= selenium.webdriver.Firefox()
        # self.scraper.get("https://www.udemy.com")
        cookies = self.scraper.get_cookies()
        if course == "engage@fischerjordan.com":
            with open(r"bin\cookies_engage.json", "w") as outfile:
                json.dump(cookies, outfile)
        elif course == "anoushka.khanna@fischerjordan.com":
            with open(r"bin\cookies_anoushka.json", "w") as outfile:
                json.dump(cookies, outfile)
        elif course == "rprogramming.fj@gmail.com":
            with open(r"bin\cookies_rprogramming.json", "w") as outfile:
                json.dump(cookies, outfile)
        elif course == "regressionmodeling.fj@gmail.com":
            with open(r"bin\cookies_regressionmodelling.json", "w")as outfile:
                json.dump(cookies, outfile)
        elif course == "projectmanagement.fj@gmail.com":
            with open(r"bin\cookies_projectmanagement.json", "w")as outfile:
                json.dump(cookies, outfile)
        elif course == "salikb@yahoo.com":
            with open(r"bin\cookies_salikb.json", "w")as outfile:
                json.dump(cookies, outfile)
        elif course == "darshana.shetty@fischerjordan.com":
            with open(r"bin\cookies_darshana.json", "w")as outfile:
                json.dump(cookies, outfile)
        else:
            raise Exception(f"No login cookies for {course.login}")
        return None
