import datetime as dt

def date_to_year_month_tuple(date: dt.date):
	return (date.year, date.month)

def strip_seconds(date: dt.datetime) -> dt.datetime:
	return dt.datetime(date.year, date.month, date.day, date.hour, date.minute)
	# return date - dt.timedelta(seconds=date.second, microseconds=date.microsecond)

def strip_days(date: dt.datetime) -> dt.datetime:
	return dt.datetime(date.year, date.month, 1)
	