from my_calendar import Calendar
from user_input_utils import get_alternative_from_user, get_date_from_user
from calendar_page_view import calendar_page_view
from note import Note
from save_menu import save_menu
import os


def print_main_menu_help():
	print("1 - Lägg till en minnesantäckning")
	print("2 - Bläddra igenom minnesantäcknignar")
	print("3 - Skriv ut en översikt över kalendern")
	print("4 - Avsluta (och spara)")

def main_menu(calendar: Calendar):
	print_main_menu_help()
	user_choice = get_alternative_from_user("Vad vill du göra?", ["1", "2", "3", "4"])
	if user_choice == "1":
		add_note_to_calendar(calendar)
	elif user_choice == "2":
		calendar_page_view(calendar)
	elif user_choice == "3":
		MARGIN = 8
		calendar_previews = calendar.get_previews(os.get_terminal_size().columns - MARGIN)
		print('\n'.join(calendar_previews))
	elif user_choice == "4":
		save_menu(calendar)
		return

 # Kanske inte rekursivt
	main_menu(calendar)

def add_note_to_calendar(calendar: Calendar):
		date = get_date_from_user("Vilket datum ska minnesantäckningen ha?") 
		note_text = input("Skriv din minnesanteckning: ")
		note = Note(date, note_text) # type: ignore
		calendar.try_add_note(note)
