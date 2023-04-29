__author__ = "noahpro"
__contact__ = "noah.provenzano@fischerjordan.com"
__version__ = "2021-1-19"

import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem



class SeleniumScraper_old(webdriver.Chrome):
    def __init__(self, windows:bool=False, wait_time:float=5) -> None:
        self.wait_time = wait_time
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value,
                            OperatingSystem.LINUX.value]
        user_agent_rotator = UserAgent(software_names=software_names,
                                       operating_system = operating_systems,
                                       limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()
        options = webdriver.ChromeOptions()
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_experimental_option("detach", True)
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36")
        # options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--start-maximized")

        if windows:
            options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            super().__init__(options=options, executable_path=r"C:\Processes\training_tracker\bin\chromedriver.exe")
        else: 
            options.add_argument('--headless')
            options.add_argument('--window-size=1920,1080')
            # options.add_argument("--disable-gpu")
            # options.add_argument("--ignore-certificate-errors")
            super().__init__(options=options)

    def wait(self, class_name:str=None, seconds=0): 
        if class_name:
            try:
                Wait = WebDriverWait(self, self.wait_time)       
                Wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
            except:
                pass
        if seconds != 0:
            time.sleep(seconds)

    def scroll_to(self, element=None, bottom=False):
        """ Scrolls the driver to either the bottom of page or to an element. """
        if element:
            self.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)
        if bottom:
            self.wait(seconds=1)
            self.execute_script("window.scrollBy(0,document.body.scrollHeight)")
            
    def open_new_tab(self):
        self.execute_script("window.open('');")
        self.switch_to.window(self.window_handles[len(self.window_handles)-1])
    
    def close_tab(self):
        self.close()
        
    def paste_keys(self, xpath, text):
        os.system("echo %s| clip" % text.strip())
        el = self.find_element(By.XPATH, xpath)
        el.send_keys(Keys.CONTROL, 'v')
        
        

class SeleniumScraper(webdriver.Firefox):
    def __init__(self, windows:bool=False, wait_time:float=5) -> None:
        self.wait_time = wait_time
        software_names = [SoftwareName.FIREFOX.value]
        operating_systems = [OperatingSystem.WINDOWS.value,
                            OperatingSystem.LINUX.value]
        # user_agent_rotator = UserAgent(software_names=software_names,
        #                                operating_system = operating_systems,
        #                                limit=100)
        # user_agent = user_agent_rotator.get_random_user_agent()
        options = webdriver.FirefoxOptions()
        profile = webdriver.FirefoxProfile('C:\\Users\\eeshi\\AppData\\Local\\Mozilla\\Firefox\\Profiles\\jegw8o0g.default-release')
        profile.accept_untrusted_certs = True

       
        # capabilities = webdriver.DesiredCapabilities().FIREFOX
        # capabilities['acceptSslCerts'] = True
        # desired_caps = DesiredCapabilities.FIREFOX.copy()
        # desired_caps.update({'acceptInsecureCerts': True, 'acceptSslCerts': True})
        # # options.add_argument("--no-sandbox")
        # # options.add_argument("--disable-gpu")
        # # options.add_argument('--proxy-server=%s' % PROXY)
        # options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_argument("--disable-infobars")
        # options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36")
        # options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--start-maximized")

        if windows:
            # options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            options.binary_location = r"C:\\Program Files\\Mozilla Firefox\\firefox.exe"
            # super().__init__(options=options, executable_path=r"C:\Users\AYUSHMAN\Desktop\FJ\training_tracker\bin\chromedriver.exe")
            super().__init__(options=options, executable_path=r"C:\\Processes\\training_tracker\\bin\\geckodriver.exe", firefox_profile= profile)
            # options.add_argument('--headless')
            # options.add_argument('--window-size=1920,1080')
            # options.add_argument("--disable-gpu")
            # options.add_argument("--ignore-certificate-errors")
            # super().__init__(options=options)

    def wait(self, class_name:str=None, seconds=0): 
        if class_name:
            try:
                Wait = WebDriverWait(self, self.wait_time)       
                Wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
            except:
                pass
        if seconds != 0:
            time.sleep(seconds)

    def scroll_to(self, element=None, bottom=False):
        """ Scrolls the driver to either the bottom of page or to an element. """
        if element:
            self.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)
        if bottom:
            self.wait(seconds=1)
            self.execute_script("window.scrollBy(0,document.body.scrollHeight)")
            
    def open_new_tab(self):
        self.execute_script("window.open('');")
        self.switch_to.window(self.window_handles[len(self.window_handles)-1])
    
    def close_tab(self):
        self.close()
        
    def paste_keys(self, xpath, text):
        os.system("echo %s| clip" % text.strip())
        el = self.find_element(By.XPATH, xpath)
        el.send_keys(Keys.CONTROL, 'v')        