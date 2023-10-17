from note import Note
import datetime as dt
from my_calendar import Calendar, SingleFileCalendarSaver, DirectoryCalendarSaver
from user_input_utils import get_alternative_from_user, get_date_from_user
from main_menu import main_menu
import os

if __name__ == '__main__':
	main_menu(Calendar())