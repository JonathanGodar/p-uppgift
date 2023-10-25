import tkinter as tk

from gui.browse_page.notes_view_width import NotesViewWidth

class ViewWidthMenuFrame(tk.Frame):
		""" A menu whre the user can choose how wide (Day, Month, All available) a view should be """
		def __init__(self, root, view_width_updated_fn):
			"""
			Parameters
			----------
			root : tk.Frame
				The parent frame that should be set
			view_width_updated_fn : function(notes_view_width.NotesViewWidth) -> None
				Is called whenever the user decides to change the view width
			"""
			super().__init__(root)

	 		# 									"View"
			tk.Label(self, text="VY: ").pack(side=tk.LEFT)
			self.note_view_width = tk.IntVar()

	 		#														"Day"												"Month"														"All"
			for (text, view_width) in [("Dag", NotesViewWidth.DAY), ("Månad", NotesViewWidth.MONTH), ("Alla", NotesViewWidth.ALL_PAGES)]:
				radio_button = tk.Radiobutton(self, text=text, variable=self.note_view_width, value=view_width.value)
				radio_button.pack(side=tk.LEFT)

			self.note_view_width.set(NotesViewWidth.DAY.value)
			self.note_view_width.trace_add('write', lambda *_: view_width_updated_fn())

		def get_view_width(self):
			"""
			Returns
			-------
			notes_view_width.NotesViewWidth : 
				The currently selected view width
			"""
			return NotesViewWidth(self.note_view_width.get())