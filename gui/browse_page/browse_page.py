import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from gui.add_note_page import AddNotePage
from gui.browse_page.browse_menu_frame import BrowseMenuFrame 
from gui.multipage_frame import MultipageFrame
from my_calendar.my_calendar import AddNoteResult, Calendar, RemoveNoteResult
from my_calendar.note import Note
from gui.notes_view_frame import NotesViewFrame
from dateutil.relativedelta import relativedelta
import datetime as dt
from enum import Enum

from time_utils import strip_days, strip_seconds


class NotesViewWidth(Enum):
	"""An enum that describes how "wide" the notes view should be. 

	Eg. it describes if you should see one day at a time or an entire month"""

	DAY = 0
	MONTH = 1
	ALL_PAGES = 2

class BrowsePage(MultipageFrame):
	"""A page that allows the user to browse and edit a calendar"""
	
	def __init__(self, root: tk.Frame, calendar: Calendar, calendar_save_function, callback):
		super().__init__(root)
		self.calendar_save_function = calendar_save_function
		self.callback = callback
		self.calendar = calendar
		self.create_main_page()
		
		self.switch_to_page(self.main_page)

	def create_main_page(self):
		""" The page where the main navigation happens and where the edit options are"""
		self.main_page = tk.Frame(self)
		self.cursor_date = dt.date.today()


		self.browse_menu = BrowseMenuFrame(self, self.browse_backward_one_unit, self.browse_backward, self.browse_forward, self.browse_backward_one_unit)
		# self.create_browse_menu()
		# self.browse_menu = browse_menu
		# self.cursor_date_label = cursor_date_label
		# self.update_cursor_date_label()

		self.notes_view = NotesViewFrame(self.main_page)

		options_menu = self.create_note_options_menu()
		(view_ammount_menu, view_ammount) = self.create_view_ammount_menu()
		self.view_ammount_menu = view_ammount_menu
		self.view_ammount = view_ammount

		view_ammount_menu.pack()
		options_menu.pack()
		self.notes_view.pack(fill=tk.BOTH, padx=20)
		self.browse_menu.pack(padx=40)

	
		self.cursor_changed()
		# self.update_browse_menu_date_label()
		# self.update_notes_view()

	def update_browse_menu_date_label(self):
		show_day = self.view_ammount.get() == NotesViewWidth.DAY.value
		self.browse_menu.set_cursor_date_label(self.cursor_date, show_day)

		# self.cursor_date_label.config(text=self.cursor_date.strftime("%Y %m %d"))

	def create_view_ammount_menu(self) -> (tk.Frame, tk.IntVar):
		view_ammount_menu = tk.Frame(self.main_page)

		tk.Label(view_ammount_menu, text="VY: ").pack(side=tk.LEFT)
		note_display_ammount = tk.IntVar()

		for (text, disp_ammount) in [("Dag", NotesViewWidth.DAY), ("Månad", NotesViewWidth.MONTH), ("Alla", NotesViewWidth.ALL_PAGES)]:
			radio_button = tk.Radiobutton(view_ammount_menu, text=text, variable=note_display_ammount, value=disp_ammount.value)
			radio_button.pack(side=tk.LEFT)

		note_display_ammount.set(NotesViewWidth.DAY.value)
		note_display_ammount.trace_add('write', lambda *_: self.cursor_changed())

		return (view_ammount_menu, note_display_ammount)
	
	def add_new_note(self, preset:Note|None = None):
		if preset == None:
			now = dt.datetime.now().time()
			start = strip_seconds(dt.datetime.combine(self.cursor_date, now))
			end = strip_seconds(dt.datetime.combine(self.cursor_date, now) + dt.timedelta(hours=1))
			preset = Note(start, end, "")

		self.switch_to_page(AddNotePage(self, self.user_submitted_note_callback, preset))
	
	def user_submitted_note_callback(self, new_note: Note):
		overlaps = self.calendar.get_overlapping_notes(new_note)
		if overlaps != []:
			overlap_previews = map(lambda note: note.get_preview(35), overlaps)
			overlap_previews_str = '\n'.join(overlap_previews)
			messagebox.showwarning('Överlappande anteckningar', f'Din anteckning överlappar med följande anteckningar:\n{overlap_previews_str}')
			return
		
		res = self.calendar.try_add_note(new_note)
		if res != AddNoteResult.Ok:
			print("WARNING: browse_page.py - ", res)

		self.switch_to_page(self.main_page)
		self.update_notes_view()

	def edit_selected_note(self):
		note = self.notes_view.get_selected_note()
		if note == None:
			messagebox.showwarning("Gick inte att redigera", "Du måste välja ett element för att kunna redigera") 
			return
		
		self.delete_selected_note()
		self.add_new_note(preset=note)
	
	def delete_selected_note(self):
		note = self.notes_view.get_selected_note()
		if note == None:
			messagebox.showwarning("Det gick inte att radera", "Du måste välja ett element för att kunna radera") 
			return
		res = self.calendar.delete_note_by_datetime(note.start_datetime)

		if res != RemoveNoteResult.Ok:
			print("WARNING: browse_page.py - ", res)

		self.update_notes_view()
	
	def cursor_changed(self):
		self.update_notes_view()
		self.update_browse_menu_date_label()
	
	def update_notes_view(self):
		new_notes = []
		view_ammount = self.view_ammount.get()
		if view_ammount == NotesViewWidth.DAY.value:
			new_notes = self.calendar.get_notes_for_date(self.cursor_date)
		elif view_ammount == NotesViewWidth.MONTH.value:
			new_notes = self.calendar.get_notes_for_month(self.cursor_date)
		elif view_ammount == NotesViewWidth.ALL_PAGES.value:
			new_notes = self.calendar.get_all_notes()

		if view_ammount == NotesViewWidth.ALL_PAGES.value:
			self.browse_menu.pack_forget()
		else:
			self.browse_menu.pack()

		self.notes_view.set_notes(new_notes)

	def get_current_move_delta(self) -> relativedelta:
		view_ammount = NotesViewWidth(self.view_ammount.get())
		if view_ammount == NotesViewWidth.DAY:
			delta = relativedelta(days=1)
		elif view_ammount == NotesViewWidth.MONTH:
			delta = relativedelta(months=1)
		
		return delta

	
	def browse_forward_one_unit(self):
		delta = self.get_current_move_delta()
		self.cursor_date += delta

		self.cursor_changed()

	def browse_backward_one_unit(self):
		delta = self.get_current_move_delta()
		self.cursor_date -= delta

		self.cursor_changed()
	
	def browse_forward(self):
		after = dt.datetime.combine(self.cursor_date, dt.time(23,59))
		if len(self.notes_view.get_notes()) > 0:
			after = self.notes_view.get_notes()[-1].start_datetime

		note = self.calendar.get_first_note_after(after)

		if note == None:
			messagebox.showinfo("Inga fler antecknignar", "Du har nått den sista anteckningar. Det finns inga senare antecknignar")
			return 

		self.cursor_date = note.start_datetime.date()
		self.cursor_changed()

	def browse_backward(self):
		after = dt.datetime.combine(self.cursor_date, dt.time(0, 0))
		if len(self.notes_view.get_notes()) > 0:
			after = self.notes_view.get_notes()[0].start_datetime

		# before = self.cursor_date - self.get_current_move_delta()
		note = self.calendar.get_first_note_before(after)

		if note == None:
			messagebox.showinfo("Inga fler antecknignar", "Du har nått den första anteckningen. Det finns inga tidigare antecknignar")
			return 

		self.cursor_date = note.start_datetime.date()
		self.cursor_changed()

	def create_note_options_menu(self):
		note_options_menu= tk.Frame(self.main_page)

		delete_button = tk.Button(note_options_menu, text="Radera", command=lambda: self.delete_selected_note())
		new_note_buttom = tk.Button(note_options_menu, text="Ny anteckning", command=lambda: self.add_new_note())
		edit_button = tk.Button(note_options_menu, text="Redigera", command=lambda: self.edit_selected_note())
		save_and_exit_button = tk.Button(note_options_menu, text="Spara och avsluta", command=self.save_and_exit)

		delete_button.pack(side=tk.LEFT)
		new_note_buttom.pack(side=tk.LEFT, padx=20)
		edit_button.pack(side=tk.LEFT, padx=20)
		save_and_exit_button.pack(side=tk.LEFT)

		return note_options_menu
	
	def save_and_exit(self):
		self.calendar_save_function()
		self.callback()
