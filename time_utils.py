import datetime as dt

def date_to_year_month_tuple(date: dt.date):
	return (date.year, date.month)

def strip_seconds(date_time: dt.datetime) -> dt.datetime:
	""" Sets the seconds and milliseconds of a datetime to 00. NOTE: Copies, does not mutate the parameter
	Parameters
	----------
	date_time: datetime.datetime

	Returns
	-------
	datetime.datetime:
		The date_time that was passed in but without seconds or millis

	"""
	return dt.datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute)
	# return date - dt.timedelta(seconds=date.second, microseconds=date.microsecond)

def strip_days(date: dt.datetime) -> dt.datetime:
	""" Sets the day to 1 and hours, minutes, seconds and milliseconds of a datetime to 00. NOTE: Copies, does not mutate the parameter
	Parameters
	----------
	date_time: datetime.datetime

	Returns
	-------
	datetime.datetime:
		The date_time that was passed in but with only informatoin about the year and month 
	"""
	return dt.datetime(date.year, date.month, 1)
	