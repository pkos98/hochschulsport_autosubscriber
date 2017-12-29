import datetime

WEEKDAYS = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
class Offer():
    def __init__(self, raw_offer_html):
        self._raw_offer = raw_offer_html
        self.id = self._parse_course_id(self._raw_offer)
        self._season_times = None
        self._exercise_days = None
        self._start_times = None
        self._is_bookable = None

    def get_season(self):
        if self._season_times == None:
            self._season_times = self._parse_season(self._raw_offer)
        return self._season_times

    def get_exercise_days(self):
        if self._exercise_days == None:
            self._exercise_days = self._parse_exercise_days(self._raw_offer)
        return self._exercise_days

    def get_start_times(self):
        if self._start_times == None:
            self._start_times = self._parse_start_times(self._raw_offer)
        return self._start_times

    def get_is_bookable(self):
        if self._is_bookable == None:
            self._is_bookable = self._parse_bookable(self._raw_offer)
        return self._is_bookable

    def _parse_course_id(self, offer_html):
        course_id = offer_html.find("td", class_="bs_sknr").text
        return course_id

    def _parse_season(self, offer_html):
        try:
            season = offer_html.find("td", class_="bs_szr").text
            parts = season.replace("\n","").split("-")
            season_start = parts[0]
            season_start_wrong_fmt_used = season_start.split(".")[-1] == ""
            if len(parts) == 1: # If no end date is specified (e.g. Zumba Party, Fitnesstraining an Geräten)
                return [season_start]
            season_end = parts[1]
            return [season_start, season_end]
        except:
            return ["Unable to parse season"]

    def _parse_exercise_days(self, offer_html):
        try:
            exercise_days = offer_html.find("td", class_="bs_stag").text
            splitted_ranges = exercise_days.split("\n")
            exercise_days = []
            for day_range in splitted_ranges:
                if not "-" in day_range: # If it is a SINGLE DAY, NO RANGE
                    exercise_days.append(day_range)
                    continue
                first_day = day_range.split("-")[0]
                last_day = day_range.split("-")[1]
                index_of_first_day = WEEKDAYS.index(first_day)
                index_of_latter_day = WEEKDAYS.index(last_day)
                exercise_days.extend(WEEKDAYS[index_of_first_day : index_of_latter_day + 1])
            return exercise_days
        except:
            return ["Unable to parse exercise days"]

    def _parse_start_times(self, offer_html):
        exercise_start = offer_html.find("td", class_="bs_szeit").text
        time_ranges = exercise_start.split("\n")
        exercise_start_times = []
        for time_range in time_ranges:
            start_time = time_range.split("-")[0]
            start_time_hours = int(start_time.split(":")[0])
            start_time_minutes = int(start_time.split(":")[1])
            start_time = datetime.time(start_time_hours, start_time_minutes)
            exercise_start_times.append(start_time)
        return exercise_start_times
        
    def _parse_bookable(self, offer_html):
        return offer_html.find("input", class_="bs_btn_buchen") != None


    def __str__(self):
        return """
    ID: {}
    Season: {}
    Exercise days: {}
    Start times: {}
    Bookable: {}""".format(self.id, " - ".join(self.get_season()), \
    self.get_exercise_days(), [x.strftime("%H:%M") for x in self.get_start_times()], self.get_is_bookable())
