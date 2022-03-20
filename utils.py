
from datetime import datetime
from dateutil import tz

def make_time_fields():

    # make datetime timestamps
    utc = datetime.now(tz.UTC)
    mtn = utc.astimezone(tz.gettz('America/Boise'))

    # create desired strings - all derived from the same original timestamp
    utc_ts = str(utc)[0:26]         # remove timezone info
    mtn_ts = str(mtn)[0:26]
    mtn_date = str(mtn.date())      # ISO 8601 YYYY-MM-DD
    mtn_time = str(mtn.time())[0:8] # I only want HH:MM:SS, no milli or micro seconds

    return utc_ts, mtn_ts, mtn_date, mtn_time


def all_valid(*args):
    """
    Are any of these args None? I want to accept
    empty strings and integer values of zero as
    valid values.

    #Example:
        print(all_valid(1, 3, 0, ''))  # True
        print(all_valid(1, None, 9))   # False
    
    # why not use `all()`?
    >>> all([True, True, 0])
    False
    # ^ That's why.
    # Still not sure if there's a better way though.
    """

    for arg in args:
        if arg is None:
            return False
    
    return True



