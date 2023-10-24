
import tkinter as tk

class BrowseMenuFrame(tk.Frame):
	""" Contains navigation buttons so that you can move the view """

	def __init__(self, root, browse_backward_unit_fn, browse_backward_fn, browse_forward_fn, browse_forward_unit_fn):
		""" The _unit_fn refer to the functions that move the view one unit forwar (e.g one day). The other function should skip to the next view that contains notes """
		super().__init__(root)

		browse_forward_one_unit_button = tk.Button(self, text="Flytta vy framåt", command=browse_forward_unit_fn)
		browse_forward_button = tk.Button(self, text="Nästa anteckning", command=browse_forward_fn)
		self.cursor_date_label = tk.Label(self) # Shows which date the user is currently viewing
		browse_backward_button = tk.Button(self, text="Föregående anteckning", command=browse_backward_fn)
		browse_backward_one_unit_button= tk.Button(self, text="Flytta vy bakåt", command=browse_backward_unit_fn)

		browse_backward_one_unit_button.pack(side=tk.LEFT)
		browse_backward_button.pack(side=tk.LEFT, padx=20)
		self.cursor_date_label.pack(side=tk.LEFT, padx=20)
		browse_forward_button.pack(side=tk.LEFT, padx=20)
		browse_forward_one_unit_button.pack(side=tk.LEFT)
	
	def set_cursor_date_label(self, new_cursor_date, show_day = True):
		time_format = "%Y %m"
		if show_day:
			time_format += " %d"
		self.cursor_date_label.config(text=new_cursor_date.strftime(time_format))