import tkinter as tk
class CalendarActionMenu(tk.Frame):
	""" A menu for editing a calendar, eg. creating new notes or deleting them """

	def __init__(self, root, delete_selected_note_fn, add_new_note_fn, edit_selected_note_fn, save_and_exit_fn):
		super().__init__(root)

		delete_button = tk.Button(self, text="Radera", command=delete_selected_note_fn)
		new_note_buttom = tk.Button(self, text="Ny anteckning", command=add_new_note_fn)
		edit_button = tk.Button(self, text="Redigera", command=edit_selected_note_fn)
		save_and_exit_button = tk.Button(self, text="Spara och återgå", command=save_and_exit_fn)

		delete_button.pack(side=tk.LEFT)
		new_note_buttom.pack(side=tk.LEFT, padx=20)
		edit_button.pack(side=tk.LEFT, padx=20)
		save_and_exit_button.pack(side=tk.LEFT)