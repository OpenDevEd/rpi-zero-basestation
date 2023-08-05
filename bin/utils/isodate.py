from datetime import datetime 
#, timedelta, timezone

# get a date string in iso8601 format
def get_date_string_iso8601():
    date = datetime.now()
    tz_dt = date.astimezone()
    iso_date = tz_dt.isoformat()
    #return date.strftime("%Y-%m-%dT%H:%M:%S%z")
    return iso_date