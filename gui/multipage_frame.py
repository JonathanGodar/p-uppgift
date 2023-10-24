import tkinter as tk

class MultipageFrame(tk.Frame):
	def __init__(self, root, *args, **kwargs):
		super().__init__(root, *args, **kwargs)

		self.active_page = None
	
	def switch_to_page(self, page: tk.Frame):
		self.__hide_current_page()
		self.active_page = page
		self.active_page.pack(fill=tk.BOTH)

	def __hide_current_page(self):
		if self.active_page != None:
			self.active_page.pack_forget()

	