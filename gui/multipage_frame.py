import tkinter as tk

class MultipageFrame(tk.Frame):
	""" A class used to be able to switch the content of a frame easily. Mimics "page" functionality """

	def __init__(self, root, *args, **kwargs):
		"""
		Parameters
		----------
		root : tkinter.Frame
			The frame to which this frame shall be bound
		
		*args, **kwargs : 
			Will be passed on to the tkinter.Frame constructor
		"""
		super().__init__(root, *args, **kwargs)

		self.active_page = None
	
	def switch_to_page(self, page: tk.Frame):
		""" Hides the current page and replaces it with the one passed as a parameter
		Parameters
		----------
		page : tk.Frame
			The page to show
		"""
		self.__hide_current_page()
		self.active_page = page
		self.active_page.pack(fill=tk.BOTH)

	def __hide_current_page(self):
		""" Internal function to hide the currently visible child frame """
		if self.active_page != None:
			self.active_page.pack_forget()

	