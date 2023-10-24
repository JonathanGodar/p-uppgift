from my_calendar.note import Note
import datetime as dt
from user_input_utils import get_alternative_from_user, get_date_from_user
from cli.main_menu import main_menu
import tkinter as tk
from tkinter import ttk
from gui.app import App
import os

if __name__ == '__main__':
	window = tk.Tk()
	window.minsize(1080, 720)
	app = App(window, window.destroy)
	app.pack(fill=tk.BOTH)
	window.mainloop()
	


	# root.mainloop()
	
	# .Tk()
	# root.minsize(400, 800)

	# browse_page = tk.Frame(root)
	# browse_menu = tk.Frame(browse_page)

	# next_page_button = tk.Button(browse_menu, text="Föregående anteckning")
	# current_note_title = tk.Label(browse_menu, text="PLACEHOLDER")
	# previous_page_button= tk.Button(browse_menu, text="Nästa anteckning")

	# next_page_button.grid(row = 0, column=0)
	# current_note_title.grid(row = 0, column=1, padx=20)
	# previous_page_button.grid(row = 0, column=2)

	# browse_menu.pack(padx=40)

	# main_content_view = tk.Text(browse_page)
	# main_content_view.pack()
	# browse_page.pack()


	# root.mainloop()
	
	
	# cal = Calendar()
	# cal.try_add_note(Note(dt.datetime(2003, 11, 19, 7, 00), dt.datetime(2003, 11, 19, 8, 00), "Föddes"))
	# print(cal.get_previews(80))
	# cal.try_add_note(Note(dt.datetime(2003, 11, 19, 9, 00), dt.datetime(2003, 11, 19, 10, 00), "Chillade"))
	# print(cal.get_previews(80))
	# cal.try_add_note(Note(dt.datetime(2003, 11, 18, 9, 00), dt.datetime(2003, 11, 18, 10, 00), "Fanns inte"))
	# print(cal.get_previews(80))
	# cal.try_add_note(Note(dt.datetime(2003, 11, 19, 8, 00), dt.datetime(2003, 11, 19, 9, 00), "Oklart"))
	# print(cal.get_previews(80))


