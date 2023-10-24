from my_calendar.my_calendar  import Calendar 
from user_input_utils import get_alternative_from_user



def print_save_menu_help():
	print("Vill du spara din kalender?")
	print("1 - Ja, i en fil")
	print("2 - Ja, i flera filer")
	print("3 - Nej")

def save_menu(calendar: Calendar):
	print_save_menu_help()
	user_choice = get_alternative_from_user("Vad vill du göra?", ["1", "2", "3"])
	if user_choice == 1:
		# TODO Use get_from_user_with_transformations
		file_path = input("Skriv in din fil: ")
		# SingleFileCalendarSaver.save(calendar, file_path)
	elif user_choice == 2:
		# TODO Use get_from_user_with_transformations
		file_path = input("Skriv in din fil: ")
		# DirectoryCalendarSaver.save(calendar, file_path)
	elif user_choice == 3:
		user_choice = get_alternative_from_user("Är du säker på att du inte vill spara? [j/n]", ["j","n"])
		if user_choice != "n":
			save_menu(calendar)