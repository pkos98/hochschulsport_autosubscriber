#!/usr/bin/python3
import datetime
import argparse
import requests
import course
import repl_interface
from bs4 import BeautifulSoup
from selenium import webdriver
from browser import Browser

COURSES_CACHE = []

def main():
    args = _parse_args()
    if args.interactive:
        repl = repl_interface.ReplInterface()
        repl.cmdloop() # starts the repl
    if args.list_courses:
        print_courses()
    if args.list_offers != None:
        print_offers(args.list_offers)
    if args.course:
        account_details = _parse_acc_details(args.course[2])
        subscribe(args.course[0], args.course[1], account_details)
        while(True):
            continue

def usage():
    return """hochschulsport_autosubscriber
    --interactive -i 
        Start in interactive mode
    --list-courses -l
        List all available courses
    --list-offers | -o [COURSE_NAME OR ID]
        List all available offers for course
    --course | -c [COURSE_NAME OR ID] [OFFER_ID] [ACCOUNT_DETAILS_FILE_PATH]
        Subscribe to the specified offer"""

def print_courses():
    print("[+] The following courses are available:")
    available_courses = get_available_courses()
    for i in range(0, len(available_courses)):
        course_name = available_courses[i][0]
        print("[" +  str(i) + "] " + course_name)
       
def print_offers(course_index_or_name):
    selected_course = create_course(course_index_or_name)
    print("[+] {} has the following offers:".format(selected_course.name))
    for offer in selected_course.get_offers():
        print("\t{}".format(str(offer)))

def subscribe(course_index_or_name, offer_id, acc_details):
    selected_course = create_course(course_index_or_name)
    selected_offer = next(offer for offer in selected_course.get_offers() if offer.id == offer_id)
    if not "pw" in acc_details:
        selected_course.subscribe(selected_offer, acc_details) 

def get_available_courses():
    global COURSES_CACHE
    if COURSES_CACHE:
        return COURSES_CACHE
    course_url_prefix = "https://anmeldung.sport.uni-augsburg.de/angebote/aktueller_zeitraum/"
    r = requests.get("https://anmeldung.sport.uni-augsburg.de/angebote/aktueller_zeitraum/index_bereiche.html")
    soup = BeautifulSoup(r.content, "html.parser")
    menu_elem = soup.find("dl", "bs_menu")
    courses = sorted(menu_elem.find_all("dd"), key=lambda x:x.string)
    # convert to tuple of name and url {COURSE_NAME, COURSE_URL}
    courses = [(course.text, course_url_prefix + course.a["href"]) for course in courses]
    COURSES_CACHE = courses # fill cache
    return courses

def create_course(course_index_or_name):
    course_name, course_url = _lookup_course(course_index_or_name)
    return course.Course(course_name, course_url, Browser())

def _lookup_course(course_index_or_name):
    try:
        if course_index_or_name.isnumeric(): # If course_index is given
            course_index = int(course_index_or_name)
            return get_available_courses()[course_index]
        else: # If course_name is given
            return next(x for x in get_available_courses() if x[0] == course_index_or_name)
    except:
        print("[Error] Invalid input. Exiting")
        exit(-1)

def _parse_args():
    parser = argparse.ArgumentParser(description="Automatische Anmeldung bei Kursen \
                                    für den Hochschulsport in Augsburg",usage=usage())
    parser.add_argument("-c", "--course", nargs=3, help="COURSE_NUM OFFER_NUM ACC_DETAILS_PATH")
    parser.add_argument("-l", "--list-courses", action="store_true", 
        help="Prints a list of available courses")
    parser.add_argument("-o", "--list-offers", nargs=None, default=None,
        help="Prints a list of available courses")
    parser.add_argument("-i", "--interactive", action="store_true",
        help="Spawn in interactive (REPL) mode")
    args = parser.parse_args()
    if not args.course and not args.list_courses and not args.list_offers and not args.interactive:
        parser.print_usage()
    return args

def _parse_acc_details(path):
    try:
        global ACCOUNT_DETAILS
        ACCOUNT_DETAILS = {}
        with open(path, "r") as f:
            lines = [x.replace("\n", "") for x in f.readlines()]
            for line in lines:
                k, v = line.split(":")
                ACCOUNT_DETAILS[k] = v
        return ACCOUNT_DETAILS
    except:
        print("[Error] Cannot read the account-details file")
        exit(-1)


if __name__ == "__main__":
    main()
