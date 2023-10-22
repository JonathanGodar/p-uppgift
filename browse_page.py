import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from my_calendar import Calendar
from filofax_page_view import FilofaxPageView
from note import Note
import datetime as dt
from enum import Enum

class FilofaxDisplayAmmount(Enum):
	DAY = 0
	MONTH = 1
	ALL_PAGES=2

class BrowsePage(ttk.Frame):
	def __init__(self, root: tk.Frame, calendar: Calendar):
		super().__init__(root)
		self.calendar = calendar
		self.cursor_date = dt.date.today()

		(browse_menu, cursor_date_label) = self.create_browse_menu()
		self.cursor_date_label = cursor_date_label
		self.update_cursor_date_label()

		self.filofax_page_view = FilofaxPageView(self)

		options_menu = self.create_note_options_menu()
		(view_ammount_menu, view_ammount) = self.create_view_ammount_menu()
		self.view_ammount_menu = view_ammount_menu
		self.view_ammount = view_ammount

		browse_menu.pack(padx=40)
		self.filofax_page_view.pack(fill=tk.BOTH, padx=20)
		options_menu.pack()
		view_ammount_menu.pack()

		self.update_filofax_view()

	def update_cursor_date_label(self):
		self.cursor_date_label.config(text=self.cursor_date.strftime("%Y %m %d"))

	def create_view_ammount_menu(self) -> (tk.Frame, tk.IntVar):
		view_ammount_menu = tk.Frame(self)

		tk.Label(view_ammount_menu, text="VY: ").pack(side=tk.LEFT)
		note_display_ammount = tk.IntVar()

		for (text, disp_ammount) in [("Dag", FilofaxDisplayAmmount.DAY), ("Månad", FilofaxDisplayAmmount.MONTH), ("Alla", FilofaxDisplayAmmount.ALL_PAGES)]:
			radio_button = tk.Radiobutton(view_ammount_menu, text=text, variable=note_display_ammount, value=disp_ammount.value)
			radio_button.pack(side=tk.LEFT)

		note_display_ammount.set(FilofaxDisplayAmmount.DAY.value)
		note_display_ammount.trace_add('write', lambda *_: self.update_filofax_view())

		return (view_ammount_menu, note_display_ammount)

	def edit_selected_note(self):
		note = self.filofax_page_view.get_selected_note()
		if note == None:
			messagebox.showwarning("Gick inte att redigera", "Du måste välja ett element för att kunna redigera") 
			return
		
		raise NotImplementedError()
		
	
	def delete_selected_note(self):
		note = self.filofax_page_view.get_selected_note()
		if note == None:
			messagebox.showwarning("Det gick inte att radera", "Du måste välja ett element för att kunna radera") 
			return
		self.calendar.delete_note_by_date(note.start_datetime)
		self.update_filofax_view()
	
	def update_filofax_view(self):
		new_notes = []
		if self.view_ammount == FilofaxDisplayAmmount.DAY.value:
			new_notes = self.calendar.get_notes_for_date(self.current_date)
		elif self.view_ammount == FilofaxDisplayAmmount.MONTH.value:
			new_notes = self.calendar.get_notes_for_month(self.current_date)
		elif self.view_ammount == FilofaxDisplayAmmount.ALL_PAGES.value:
			new_notes = self.calendar.get_all_notes()

		self.filofax_page_view.set_notes(new_notes)

	def create_browse_menu(self)-> (tk.Frame, tk.Label):
		browse_menu = tk.Frame(self)

		next_page_button = tk.Button(browse_menu, text="Föregående anteckning")
		cursor_date_label = tk.Label(browse_menu)
		previous_page_button= tk.Button(browse_menu, text="Nästa anteckning")

		next_page_button.pack(side=tk.LEFT)
		cursor_date_label.pack(side=tk.LEFT, padx=20)
		previous_page_button.pack(side=tk.LEFT)
		return (browse_menu, cursor_date_label)

	def create_note_options_menu(self):
		note_options_menu= tk.Frame(self)

		delete_button = tk.Button(note_options_menu, text="Radera", command=lambda *_: self.delete_selected_note())
		edit_button= tk.Button(note_options_menu, text="Redigera", command=lambda *_: self.edit_selected_note())

		delete_button.pack(side=tk.LEFT)
		edit_button.pack(side=tk.LEFT, padx=20)

		return note_options_menu