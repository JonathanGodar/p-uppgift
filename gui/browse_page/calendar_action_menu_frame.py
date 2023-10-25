# Niklasson Godar, Jonathan | jonathan.godar@ug.kth.se

import tkinter as tk
class CalendarActionMenu(tk.Frame):
	""" A menu with buttons for editing a calendar, eg. creating new notes or deleting them """

	def __init__(self, root, delete_selected_note_fn, add_new_note_fn, edit_selected_note_fn, save_and_exit_fn):
		"""
		Parameters:
		root : tk.Frame
			The frame to which this frame shall bind to
		delete_selected_note_fn : function() -> None
			Is called when the user wants to delete the selected note
		add_new_note_fn : function() -> None
			Is called when the user wants to add a new note
		edit_selected_note_fn : function() -> None
			Is called when the user wants to edit the selected note
		save_and_exit_fn: function() -> None
			Is called when the user wants to save the calendar and exit 
		"""
		super().__init__(root)

		#																			"Delete"
		delete_button = tk.Button(self, text="Radera", command=delete_selected_note_fn)
		#																			"New note"
		new_note_buttom = tk.Button(self, text="Ny anteckning", command=add_new_note_fn)
		#																	"Edit"
		edit_button = tk.Button(self, text="Redigera", command=edit_selected_note_fn)
		#																						"Save and return"
		save_and_exit_button = tk.Button(self, text="Spara och återgå", command=save_and_exit_fn)

		delete_button.pack(side=tk.LEFT)
		new_note_buttom.pack(side=tk.LEFT, padx=20)
		edit_button.pack(side=tk.LEFT, padx=20)
		save_and_exit_button.pack(side=tk.LEFT)