
import tkinter as tk

class BrowseMenuFrame(tk.Frame):
	""" Contains navigation buttons so that you can move the view """

	def __init__(self, root, browse_backward_unit_fn, browse_backward_fn, browse_forward_fn, browse_forward_unit_fn):
		"""
		Parameters
		----------
		root : tk.Frame
			The parent frame of this frame
		browse_backward_unit_fn : function() -> None
			Is called when the user wants to browse backward by one unit
		browse_backward_fn : function() -> None
			Is called when the user wants to browse backward to the first view that contains atleast one note 
		browse_forward_fn : function() -> None
			Is called when the user wants to browse forward to the first view that contains atleast one note 
		forward_forward_unit_fn : function() -> None
			Is called when the user wants to browse forward by one unit
		"""
		# The _unit_fn refer to the functions that move the view one unit forward (e.g one day). The other function should skip to the next view that contains notes """
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
		""" Updates the cursor_date label
		Parameters
		----------
		new_cursor_date : datetime_datetime
			What the new cursor date label should be set too
		show_day : bool
			Dictates if the date_label contains the day of the month or just the month and the year
		"""
		time_format = "%Y %m"
		if show_day:
			time_format += " %d"
		self.cursor_date_label.config(text=new_cursor_date.strftime(time_format))