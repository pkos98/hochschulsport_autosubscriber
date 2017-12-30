import requests
from time import sleep
from offer import Offer
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select

WEEKDAYS = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

class Course():
    def __init__(self, name, url, browser):
        self.name = name
        self.url = url
        self._browser = browser
        self._offers = None

    def get_offers(self):
        if self._offers == None:
            self._offers = self._parse_offers()
        return self._offers

    def subscribe(self, offer, acc_details):
        if not offer.get_is_bookable():
            print("[+] Course is currently not bookable")
            return

        self._browser.start()
        self._browser.get(self.url)
        subscribe_button = None
        subscribe_button = self._browser.find_element_by_class_name("bs_btn_buchen")

        self._browser.try_click("bs_btn_buchen", lambda f: len(f.window_handles) ==  2)
        self._browser.switch_to.window(self._browser.window_handles[-1])

        if self._is_existing_account(acc_details):
            self._fill_form_login(acc_details)
        else:
            self._fill_form_register(acc_details)

        subscribe_button_selector = "/html/body/form/div/div[2]/div[1]/div[5]/div[1]/div[2]/input"
        subscribe_button = self._browser.find_element_by_xpath(subscribe_button_selector)
        #self._browser.try_click(subscribe_button)

    def _fill_form_login(self, acc_details):
        infotext_elem = self._browser.find_element_by_xpath("/html/body/form/div/div[2]/div[2]/div[2]")
        self._browser.try_click(infotext_elem)
        sleep(1)
        email_field_selector = "/html/body/form/div/div[2]/div[1]/div[2]/div[2]/input"
        pw_field_selector = "/html/body/form/div/div[2]/div[1]/div[3]/div[2]/input"
        email_field = self._browser.find_element_by_xpath(email_field_selector)
        pw_field = self._browser.find_element_by_xpath(pw_field_selector)
        self._browser.fill_form_field(email_field, acc_details["email"])
        self._browser.fill_form_field(pw_field, acc_details["passwort"])
            
    def _fill_form_register(self, acc_details):
        sex_button_selector = "#bs_kl_anm > div:nth-child(3) > div.bs_form_sp2 > label:nth-child(2) > input"
        if acc_details["sex"] == "female":
            sex_button_selector = "#bs_kl_anm > div:nth-child(3) > div.bs_form_sp2 > label:nth-child(1) > input"
        prename_field_selector = "#bs_kl_anm > div:nth-child(4) > div:nth-child(2) > input:nth-child(1)"
        surname_field_selector = "#bs_kl_anm > div:nth-child(5) > div:nth-child(2) > input:nth-child(1)"
        street_field_selector = "#bs_kl_anm > div:nth-child(6) > div:nth-child(2) > input:nth-child(1)"
        postcode_field_selector = "html body.anmeldung form div#bs_form_content div#bs_form_main div#bs_kl_anm div.bs_form_row div.bs_form_sp2 input.bs_form_field.bs_fval_ort"
        state_field_selector = "select.bs_form_field"
        mat_field_selector = ".bs_fval_status11"
        email_field_selector = ".bs_fval_email"
        iban_field_selector = ".bs_fval_iban"
        bic_field_selector = ".bs_fval_bic"
        acc_owner_selector = "#bs_lastschrift > div:nth-child(5) > div.bs_form_sp2 > input"

        sex_rb_btn = self._browser.find_element_by_css_selector(sex_button_selector)
        prename_field = self._browser.find_element_by_css_selector(prename_field_selector)
        surname_field = self._browser.find_element_by_css_selector(surname_field_selector)
        street_field = self._browser.find_element_by_css_selector(street_field_selector)
        postcode_field = self._browser.find_element_by_css_selector(postcode_field_selector)
        state_field = self._browser.find_element_by_css_selector(state_field_selector)
        mat_field = self._browser.find_element_by_css_selector(mat_field_selector) 
        email_field = self._browser.find_element_by_css_selector(email_field_selector)
        iban_field = self._browser.find_element_by_css_selector(iban_field_selector)
        bic_field = self._browser.find_element_by_css_selector(bic_field_selector)
        acc_owner_field = self._browser.find_element_by_css_selector(acc_owner_selector)

        self._browser.try_click(sex_rb_btn)
        self._browser.fill_form_field(prename_field, acc_details["vorname"])
        self._browser.fill_form_field(surname_field, acc_details["name"])
        self._browser.fill_form_field(street_field, acc_details["strasse"])
        self._browser.fill_form_field(postcode_field, acc_details["ort"])
        Select(state_field).select_by_index(self._uni_hs_to_index(acc_details["uni_hs"])) 
        # MUST BE EXECUTED AFTER THE ACTION ABOVE
        self._browser.fill_form_field(mat_field, acc_details["matnr"])
        self._browser.fill_form_field(email_field, acc_details["email"])
        self._browser.fill_form_field(iban_field, acc_details["iban"])
        # MUST CLICK SO THAT BIC-FIELD APPEARS!
        self._browser.try_click(acc_owner_field) 
        self._browser.fill_form_field(bic_field, acc_details["bic"])
        # accept terms
        input_terms = self._browser.find_element_by_name("tnbed")
        self._browser.try_click(input_terms)

    def _is_existing_account(self, key_values):
        return len(key_values.keys()) == 2

    def _uni_hs_to_index(self, value):
        if value == "uni":
            return 1
        return 2

    def _parse_offers(self, raw=False):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, "html.parser")
        tables = soup.find_all("table", class_="bs_kurse")
        raw_offers_list = []
        for table in tables:
            raw_offers_list.extend(table.find("tbody").find_all("tr"))

        offers_list = [Offer(offer) for offer in raw_offers_list]
        return offers_list
