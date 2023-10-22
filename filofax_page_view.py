import tkinter as tk
from tkinter import messagebox
import datetime as dt
from typing import List

from note import Note

class FilofaxPageView(tk.Frame):
	def __init__(self, root: tk.Frame, notes: List[Note] =[]):
		super().__init__(root)
		# https://www.geeksforgeeks.org/scrollable-frames-in-tkinter/
		# self.scroll_bar = tk.Scrollbar(self, orient=tk.VERTICAL)
		# self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

		self.content = tk.Listbox(self)
		self.content.pack(fill=tk.BOTH, expand=True)

		self.set_notes(notes)
	
	
	
	def set_notes(self, notes: List[Note]):
		# notes.sort(key=lambda note: note.start_datetime)
		self.notes = notes
		self.update_content_view()

	def update_content_view(self):
		self.content.selection_clear(0, tk.END)
		self.content.delete(0, tk.END)
		for note in self.notes:
			self.content.insert(tk.END, note)
	
	def get_selected_note(self) -> None | Note:
		selected_indicies = self.content.curselection()
		if len(selected_indicies) == 0:
			return None

		return self.notes[selected_indicies[0]]