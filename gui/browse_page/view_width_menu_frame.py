import tkinter as tk

from gui.browse_page.notes_view_width_menu_frame import NotesViewWidth

class ViewWidthMenuFrame(tk.Frame):
		""" A menu whre the user can choose how wide a view should be """

		def __init__(self, root, view_width_updated_fn):
			super().__init__(root)

			tk.Label(self, text="VY: ").pack(side=tk.LEFT)
			self.note_view_width = tk.IntVar()

			for (text, view_width) in [("Dag", NotesViewWidth.DAY), ("Månad", NotesViewWidth.MONTH), ("Alla", NotesViewWidth.ALL_PAGES)]:
				radio_button = tk.Radiobutton(self, text=text, variable=self.note_view_width, value=view_width.value)
				radio_button.pack(side=tk.LEFT)

			self.note_view_width.set(NotesViewWidth.DAY.value)
			self.note_view_width.trace_add('write', lambda *_: view_width_updated_fn())

		def get_view_width(self):
			return NotesViewWidth(self.note_view_width.get())