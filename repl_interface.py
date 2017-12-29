import cmd
import main

class ReplInterface(cmd.Cmd):
    intro = "Welcome to hochschulsport_autosubscriber. Type help or ? to list commands\n"
    prompt = "$~: "

    def do_print_courses(self, arg):
        "Prints a list of all available courses on the site"
        main.print_courses()
    
    def do_print_offers(self, arg):
        "Prints a list of all available offers for the specified course"
        main.print_offers(arg)
    
    def do_subscribe(self, args):
        "Subscribes to the given course & offer with the given account-details"
        course_id, offer_num, acc_details_path = args.split(" ")
        offer_num = int(offer_num)
        main.subscribe(course_id, offer_num, acc_details_path)