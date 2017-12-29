import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import WebDriverException


class Browser(webdriver.Firefox, webdriver.Chrome):

    def __init__(self):
        self._is_started = False

    def try_click(self, element_or_class_name, was_click_successfull_func=lambda x: True):
        element = element_or_class_name
        if isinstance(element_or_class_name, str):
            element = self.find_element_by_class_name(element_or_class_name)
        # 1. Try simple click
        try:
            element.click()
            if was_click_successfull_func(self):
                return
            else:
                raise Exception()
        except:
            try:
                self.move_and_click(element)
                if was_click_successfull_func(self):
                    return
                else:
                    raise Exception()
            except:
                if isinstance(element_or_class_name, str):  # Only if class is given
                    self.click_js(element_or_class_name)
                else:
                    print(
                        "[+] Error clicking element {}".format(str(element_or_class_name)))

    def fill_form_field(self, field_element, text):
        self.move_to(field_element)
        field_element.send_keys(text)

    def move_and_click(self, element):
        actions = webdriver.ActionChains(self)
        actions.move_to_element(element).click().perform()

    def click_js(self, class_name):
        self.execute_script("document.getElementsByClassName(\"{}\")[0].click();"
                            .format(class_name))

    def move_to(self, element):
        actions = webdriver.ActionChains(self)
        actions.move_to_element(element).perform()

    def start(self):
        if self._is_started:
            return
        user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19"
        is_windows = os.name == "nt"
        # Prefer chrome
        opts = ChromeOptions()
        opts.add_argument("user-agent=" + user_agent)
        if is_windows:
            webdriver.Chrome.__init__(self, chrome_options=opts, executable_path="./win_drivers/chromedriver.exe")
        else:  # If its Mac or Linux
            webdriver.Chrome.__init__(self, chrome_options=opts)
        self._is_started = True
