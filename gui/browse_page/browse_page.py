import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from gui.add_note_page import AddNotePage
from gui.browse_page.browse_menu_frame import BrowseMenuFrame
from gui.browse_page.calendar_action_menu_frame import CalendarActionMenu
from gui.browse_page.notes_view_width_menu_frame import NotesViewWidth
from gui.browse_page.view_width_menu_frame import ViewWidthMenuFrame 
from gui.multipage_frame import MultipageFrame
from my_calendar.my_calendar import AddNoteResult, Calendar, RemoveNoteResult
from my_calendar.note import Note
from gui.browse_page.notes_view_frame import NotesViewFrame
from dateutil.relativedelta import relativedelta
import datetime as dt
from enum import Enum

from time_utils import strip_seconds



class BrowsePage(MultipageFrame):
	""" A page that allows the user to browse and edit a calendar """
	
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


		self.browse_menu = BrowseMenuFrame(self.main_page, self.browse_backward_one_unit, self.browse_backward, self.browse_forward, self.browse_forward_one_unit)
		self.notes_view = NotesViewFrame(self.main_page)

		self.view_width_menu = ViewWidthMenuFrame(self.main_page, self.cursor_changed)
		calendar_action_menu = CalendarActionMenu(self.main_page, self.delete_selected_note, self.add_new_note, self.edit_selected_note, self.save_and_exit)

		self.view_width_menu.pack()
		calendar_action_menu.pack()

		self.notes_view.pack(fill=tk.BOTH, padx=20)
		self.browse_menu.pack(padx=40)

	
	 	# Initial sync of views
		self.cursor_changed()

	def update_browse_menu_date_label(self):
		show_day = self.view_width_menu.get_view_width() == NotesViewWidth.DAY
		self.browse_menu.set_cursor_date_label(self.cursor_date, show_day)

	def add_new_note(self, preset:Note|None = None):
		if preset == None:
			now = dt.datetime.now().time()
			start = strip_seconds(dt.datetime.combine(self.cursor_date, now))
			end = strip_seconds(dt.datetime.combine(self.cursor_date, now) + dt.timedelta(hours=1))
			preset = Note(start, end, "")

		self.switch_to_page(AddNotePage(self, self.user_submitted_note_callback, preset))
	
	def user_submitted_note_callback(self, new_note: Note | None):
		if new_note == None:
			self.switch_to_page(self.main_page)
			self.update_notes_view()

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
		res = self.calendar.delete_note_by_start_datetime(note.start_datetime)

		if res != RemoveNoteResult.Ok:
			print("WARNING: browse_page.py - ", res)

		self.update_notes_view()

	def cursor_changed(self):
		self.update_notes_view()
		self.update_browse_menu_date_label()
	
	def update_notes_view(self):
		new_notes = []
		view_ammount = self.view_width_menu.get_view_width()
		if view_ammount == NotesViewWidth.DAY:
			new_notes = self.calendar.get_notes_for_date(self.cursor_date)
		elif view_ammount == NotesViewWidth.MONTH:
			new_notes = self.calendar.get_notes_for_month(self.cursor_date)
		elif view_ammount == NotesViewWidth.ALL_PAGES:
			new_notes = self.calendar.get_all_notes()

		if view_ammount == NotesViewWidth.ALL_PAGES:
			self.browse_menu.pack_forget()
		else:
			self.browse_menu.pack()

		self.notes_view.set_notes(new_notes)

	def get_current_move_delta(self) -> relativedelta:
		""" Gets how far the view should be moved to move one slot (depends on what the view width is)"""
		view_ammount = self.view_width_menu.get_view_width()
		if view_ammount == NotesViewWidth.DAY:
			delta = relativedelta(days=1)
		elif view_ammount == NotesViewWidth.MONTH:
			delta = relativedelta(months=1)
		
		return delta

	
	def browse_forward_one_unit(self):
		""" Moves the view forward by one view width unit """
		delta = self.get_current_move_delta()
		self.cursor_date += delta

		self.cursor_changed()

	def browse_backward_one_unit(self):
		""" Moves the view forward by one view width unit """
		delta = self.get_current_move_delta()
		self.cursor_date -= delta

		self.cursor_changed()
	
	def browse_forward(self):
		""" Jumps forward to the next view that contains notes """
		after = dt.datetime.combine(self.cursor_date, dt.time(23,59))
		if len(self.notes_view.get_notes()) > 0:
			after = self.notes_view.get_notes()[-1].start_datetime

		note = self.calendar.get_first_note_after(after)

		if note == None:
			messagebox.showinfo("Inga fler antecknignar", "Du har nått den sista anteckningen. Det finns inga senare anteckningar")
			return 

		self.cursor_date = note.start_datetime.date()
		self.cursor_changed()

	def browse_backward(self):
		""" Jumps forward to the next view that contains notes """

		after = dt.datetime.combine(self.cursor_date, dt.time(0, 0))
		if len(self.notes_view.get_notes()) > 0:
			after = self.notes_view.get_notes()[0].start_datetime

		note = self.calendar.get_first_note_before(after)

		if note == None:
			messagebox.showinfo("Inga fler antecknignar", "Du har nått den första anteckningen. Det finns inga tidigare antecknignar")
			return 

		self.cursor_date = note.start_datetime.date()
		self.cursor_changed()

	def save_and_exit(self):
		self.calendar_save_function()
		self.callback()
