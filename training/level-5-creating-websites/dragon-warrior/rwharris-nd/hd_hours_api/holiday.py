from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.easter import easter

class Holiday:

    def __init__(self):
        #Current Year
        self.this_year = 2016 #date.today().year

    def get_easter(self) -> dict:
        #Easter Calculation
        easter_day = easter(year=self.this_year, method=3)
        holiday = {str(easter_day): "Easter"}

        #Good Friday Calculation
        good_friday = easter_day - timedelta(days = 2)
        holiday[str(good_friday)] = "Good Friday"

        return holiday

    def get_memorial_day(self) -> dict:
        #Memorial Day
        memorial_day = date(self.this_year, 5, 31)
        if memorial_day.weekday() != 0:
            memorial_day = date(self.this_year, 5, 31) - relativedelta(weekday=0,weeks=1)
        holiday = {str(memorial_day): "Memorial Day"}
        return holiday

    def get_july_4(self) -> dict:
        #July 4th
        july_4 = date(self.this_year, 7, 4)
        if july_4.weekday() == 5:
            july_4 = date(self.this_year, 7, 3)
        elif july_4.weekday() == 6:
            july_4 = date(self.this_year, 7, 5)
        holiday = {str(july_4): "4th of July"}

        return holiday

    def get_thanksgiving(self) -> dict:
        #Thanksgiving
        thanksgiving = date(self.this_year, 11, 1) + relativedelta(weekday=4, weeks=3)
        holiday = {str(thanksgiving): "Thanksgiving"}

        #Day After Thanksgiving
        black_friday = thanksgiving + timedelta(days=1)
        holiday[str(black_friday)] = "Day After Thanksgiving"

        return holiday

    def get_holiday_celebration(self) -> dict:
        #Holiday Celebration
        holiday = {
            str(date(self.this_year, 12, 24)):"Christmas Celebration",
            str(date(self.this_year, 12, 25)):"Christmas Celebration",
            str(date(self.this_year, 12, 26)):"Christmas Celebration",
            str(date(self.this_year, 12, 27)):"Christmas Celebration",
            str(date(self.this_year, 12, 28)):"Christmas Celebration",
            str(date(self.this_year, 12, 29)):"Christmas Celebration",
            str(date(self.this_year, 12, 30)):"Christmas Celebration",
            str(date(self.this_year, 12, 31)): "New Year's Celebration",
            str(date(self.this_year, 1, 1)): "New Year's Celebration"
        }

        christmas_day = date(self.this_year, 12, 25).weekday
        if christmas_day == 6 | 2:
            holiday[str(date(self.this_year, 12, 23))]= "Christmas Celebration"
        elif christmas_day == 0:
            holiday[str(date(self.this_year, 12, 22))]= "Christmas Celebration"
            holiday[str(date(self.this_year, 12, 23))]= "Christmas Celebration"

        new_years_day = date(self.this_year, 1, 1).weekday()
        if new_years_day == 6 | new_years_day == 3:
            holiday[str(date(self.this_year, 1, 2))]= "New Year's Celebration"

        return holiday

    def get_all_holidays(self) -> dict:
        holiday = {}
        holiday.update(self.get_easter())
        holiday.update(self.get_memorial_day())
        holiday.update(self.get_july_4())
        holiday.update(self.get_thanksgiving())
        holiday.update(self.get_holiday_celebration())
        return holiday