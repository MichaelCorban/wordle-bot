import pytz, datetime

def wordle_number():
    eastern_tz = pytz.timezone('America/New_York')
    d2 = datetime.datetime.now(eastern_tz)
    # March 5 2022 is Wordle 259
    d1 = datetime.datetime(2022, 3, 5, tzinfo=eastern_tz)
    delta = d2 - d1
    return delta.days + 259