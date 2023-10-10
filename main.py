from note import Note
import datetime as dt
from my_calendar import Calendar, SingleFileCalendarSaver, DirectoryCalendarSaver
from user_input_utils import get_alternative_from_user, get_date_from_user
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
		calendar_page_view_menu(calendar)
	elif user_choice == "3":
		MARGIN = 8
		calendar_previews = calendar.get_previews(os.get_terminal_size().columns - MARGIN)
		print('\n'.join(calendar_previews))
	elif user_choice == "4":
		save_menu(calendar)
		return

	main_menu(calendar)

def calendar_page_view_menu(calendar: Calendar, note_idx = 0):
	os.system('cls') # Credit for this line of code: ChatGPT
	note = calendar.get_note_by_idx(note_idx)
	if note == None:
		print("Det finns inga antecknignar att visa")
		return
	
	print(note)
	user_choice = get_alternative_from_user("1 - Bakåt, 2 - Frammåt, 3 - Ta bort nuvarande", ["1", "2", "3"])
	if user_choice == "1":
		note_idx -= 1 
	elif user_choice == "2":
		note_idx += 1
	elif user_choice == "3":
		calendar.delete_note_by_idx(note_idx)


	note_idx = calendar.constrain_int_to_notes_idx_bounds(note_idx)
	calendar_page_view_menu(calendar, note_idx)

def add_note_to_calendar(calendar: Calendar):
		date = get_date_from_user("Vilket datum ska minnesantäckningen ha?") 
		note_text = input("Skriv din minnesanteckning: ")
		note = Note(date, note_text) # type: ignore
		calendar.add_note(note)

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
		SingleFileCalendarSaver.save(calendar, file_path)
	elif user_choice == 2:
		# TODO Use get_from_user_with_transformations
		file_path = input("Skriv in din fil: ")
		DirectoryCalendarSaver.save(calendar, file_path)
	elif user_choice == 3:
		user_choice = get_alternative_from_user("Är du säker på att du inte vill spara? [j/n]", ["j","n"])
		if user_choice != "n":
			save_menu(calendar)

if __name__ == '__main__':
	main_menu(Calendar())