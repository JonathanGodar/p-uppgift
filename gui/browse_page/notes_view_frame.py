# Niklasson Godar, Jonathan | jonathan.godar@ug.kth.se

import tkinter as tk
from tkinter import messagebox
import datetime as dt
from typing import List

from my_calendar.note import Note

class NotesViewFrame(tk.Frame):
	""" A frame which can show a list of Notes """

	def __init__(self, root: tk.Frame, notes: List[Note] =[]):
		"""
		Parameters
		----------
		root : tk.Frame
			The parent frame of this frame
		notes : List[Note] = []
			What notes should be displayed when the view is first created
		"""

		super().__init__(root)
		self.content = tk.Listbox(self)
		self.content.pack(fill=tk.BOTH, expand=True)

		self.set_notes(notes)
	
	def get_notes(self) -> [Note]:
		"""
		Returns
		-------
		[Note]: 
			The notes which are currently stored by this view
		"""
		return self.notes
	
	def set_notes(self, notes: List[Note]):
		""" Update which note should be shows
		Parameters
		----------
		notes : [Note]
			The new notes. will be sorted by start_datetime before being shown
		"""
		notes.sort(key=lambda note: note.start_datetime)
		self.notes = notes
		self.update_content_view()

	def update_content_view(self):
		""" Updates the content view by clearing all shown notes and then adding back the notes stored in self.notes"""
		self.content.selection_clear(0, tk.END)
		self.content.delete(0, tk.END)
		for note in self.notes:
			self.content.insert(tk.END, note)
	
	def get_selected_note(self) -> None | Note:
		"""
		Returns
		-------
		Note : 
			The selected note
		"""
		selected_indicies = self.content.curselection()
		if len(selected_indicies) == 0:
			return None

		return self.notes[selected_indicies[0]]