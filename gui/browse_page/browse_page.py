import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from gui.add_note_page import AddNotePage
from gui.browse_page.browse_menu_frame import BrowseMenuFrame
from gui.browse_page.calendar_action_menu_frame import CalendarActionMenu
from gui.browse_page.notes_view_width import NotesViewWidth
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
		"""
		Parameters
		----------
		root : tk.Frame
			The parent frame to which shis frame shall bind to
		calendar : my_calendar.Calendar
			The calendar which should be browsed and edited
		calendar_save_function : function() -> None
			Should save the calendar when called
		callback : function() -> None
			Will be called when the user wants to exit the BrowsePage
		"""
		super().__init__(root)
		self.calendar_save_function = calendar_save_function
		self.callback = callback
		self.calendar = calendar
		self.create_main_page()
		
		self.switch_to_page(self.main_page)

	def create_main_page(self):
		""" This function creates the page where the main navigation, notes_view and edit options are """
		self.main_page = tk.Frame(self)
		
		# Decides the date is currently beeing viewed
		self.cursor_date = dt.date.today()

		self.browse_menu = BrowseMenuFrame(self.main_page, self.browse_backward_one_unit, self.browse_backward, self.browse_forward, self.browse_forward_one_unit)
		self.notes_view = NotesViewFrame(self.main_page)

		self.view_width_menu = ViewWidthMenuFrame(self.main_page, self.cursor_changed)
		calendar_action_menu = CalendarActionMenu(self.main_page, self.delete_selected_note, self.add_new_note, self.edit_selected_note, self.save_and_exit)

		self.view_width_menu.pack()
		calendar_action_menu.pack()

		self.notes_view.pack(fill=tk.BOTH, padx=20)
		self.browse_menu.pack(padx=40)

		self.cursor_changed()


	def add_new_note(self, preset:Note|None = None):
		""" Switches the current page to a add_note_page
		Parameters:
		preset : Note|None
			What is the preset that should be sent to the constructed add_notes_page?
		
		"""

		if preset == None:
			now = dt.datetime.now().time()
			start = strip_seconds(dt.datetime.combine(self.cursor_date, now))
			end = strip_seconds(dt.datetime.combine(self.cursor_date, now) + dt.timedelta(hours=1))
			preset = Note(start, end, "")

		self.switch_to_page(AddNotePage(self, self.user_submitted_note_callback, preset))
	
	def user_submitted_note_callback(self, new_note: Note | None):
		""" Is called when the user has created a note (see self.add_new_note) 
		Parameters
		----------
		new_note : Note | None
			The new note that the user has created
		"""

		if new_note == None:
			self.switch_to_page(self.main_page)
			self.update_notes_view()
			return 

		overlaps = self.calendar.get_overlapping_notes(new_note)
		if overlaps != []:
			# If there are overlaps, display an error message with the overlapping notes and let the user continue editing the note
			overlap_previews = map(lambda note: note.get_preview(35), overlaps)
			overlap_previews_str = '\n'.join(overlap_previews)
			#											"Overlapping notes", 						"Your note is overlapping with the following notes: "
			messagebox.showwarning('Överlappande anteckningar', f'Din anteckning överlappar med följande anteckningar:\n{overlap_previews_str}')
			return
		
		res = self.calendar.try_add_note(new_note)

		# Should not fail since we have already checked that the note is not overlapping
		if res != AddNoteResult.Ok:
			#											"An error occured when we tried to add the note"
			messagebox.showerror("Fel när anteckningen försökte läggas till", str(res))
			print("WARNING: browse_page.py - ", res)

		# Switch back to the main page
		self.switch_to_page(self.main_page)
		self.update_notes_view()

	def edit_selected_note(self):
		""" Edits the selected note. NOTE: This function first deletes the selected note and then passes the selected note as a preset to self.add_new_note. This makes it so that if the user edits a note and decides to cancel when editing, the note will be deleted"""
		note = self.notes_view.get_selected_note()
		if note == None:
			#												"Unable to edit", 				"You have to choose a note to be able to edit"
			messagebox.showwarning("Gick inte att redigera", "Du måste välja en anteckning för att kunna redigera") 
			return
		
		self.delete_selected_note()
		self.add_new_note(preset=note)
	
	def delete_selected_note(self):
		""" Removes the note currently selected from the calendar """
		note = self.notes_view.get_selected_note()
		if note == None:
			#												"Unable to delete",  				"You have to choose an element to be able to delete"
			messagebox.showwarning("Det gick inte att radera", "Du måste välja ett element för att kunna radera") 
			return
		res = self.calendar.delete_note_by_start_datetime(note.start_datetime)

		if res != RemoveNoteResult.Ok: # Should not be called since the note should exist
			# 										"Unable to delete",  "An error occured when we tried to delete the note. Maybe the note is already deleted?"
			messagebox.showerror("Kunde inte radera", f'Ett fel uppstod när vi försökte radera. Kanske är anteckningen redan raderad? {str(res)}')
			print("WARNING: browse_page.py - ", res)

		self.update_notes_view()

	def cursor_changed(self):
		""" Function that should be called whenever the cursor is change (includes changing the view width)
		Updates the all labels and views affected by a cursor change
		"""
		self.update_notes_view()
		self.update_browse_menu_date_label()
	
	def update_notes_view(self):
		""" Updates the self.notes_view to match with what self.cursor and self.view_width_menu.get_view_width() wants to have shown"""
		new_notes = []
		view_ammount = self.view_width_menu.get_view_width()
		if view_ammount == NotesViewWidth.DAY:
			new_notes = self.calendar.get_notes_for_date(self.cursor_date)
		elif view_ammount == NotesViewWidth.MONTH:
			new_notes = self.calendar.get_notes_for_month(self.cursor_date)
		elif view_ammount == NotesViewWidth.ALL_PAGES:
			new_notes = self.calendar.get_all_notes()

		if view_ammount == NotesViewWidth.ALL_PAGES:
			# Remove the browse menu if all pages are shown, there are no navigation when everything is whosn
			self.browse_menu.pack_forget()
		else:
			self.browse_menu.pack()

		self.notes_view.set_notes(new_notes)

	def update_browse_menu_date_label(self):
		""" Updates the label which shows the user which date is currently being shown """
		show_day = self.view_width_menu.get_view_width() == NotesViewWidth.DAY
		self.browse_menu.set_cursor_date_label(self.cursor_date, show_day)

	def get_current_move_delta(self) -> relativedelta:
		""" Gets how far the view should be moved to move one slot (depends on what the view width is)
		Returns
		-------
		dateutil.relativedelta:
			How far one unit move should be
		"""
		view_ammount = self.view_width_menu.get_view_width()
		if view_ammount == NotesViewWidth.DAY:
			delta = relativedelta(days=1)
		elif view_ammount == NotesViewWidth.MONTH:
			delta = relativedelta(months=1)
		
		return delta

	
	def browse_forward_one_unit(self):
		""" Moves the view forward by one view width unit. Eg. one month or a day """
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

		# Default if there are no notes in the view
		after = dt.datetime.combine(self.cursor_date, dt.time(23,59))

		# Check which is the last note in the view and show a view around the first note which is after the currrently last one
		if len(self.notes_view.get_notes()) > 0:
			after = self.notes_view.get_notes()[-1].start_datetime

		note = self.calendar.get_first_note_after(after)

		if note == None:
			# 									"No more notes", 					"You have reached the last note. There are no later notes"
			messagebox.showinfo("Inga fler antecknignar", "Du har nått den sista anteckningen. Det finns inga senare anteckningar")
			return 

		self.cursor_date = note.start_datetime.date()
		self.cursor_changed()

	def browse_backward(self):
		""" Jumps backwards to the first view that contains notes. For more details see browse_forward """

		after = dt.datetime.combine(self.cursor_date, dt.time(0, 0))
		if len(self.notes_view.get_notes()) > 0:
			after = self.notes_view.get_notes()[0].start_datetime

		note = self.calendar.get_first_note_before(after)

		if note == None:
			# 									"No more notes", 					"You have reached the first note. There are no earlier notes"
			messagebox.showinfo("Inga fler antecknignar", "Du har nått den första anteckningen. Det finns inga tidigare antecknignar")
			return 

		self.cursor_date = note.start_datetime.date()
		self.cursor_changed()

	def save_and_exit(self):
		""" Saves the calendar and calls self.callback"""
		self.calendar_save_function()
		self.callback()
