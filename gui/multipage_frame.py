import tkinter as tk

class MultipageFrame(tk.Frame):
	def __init__(self, root, *args, **kwargs):
		super().__init__(root, *args, **kwargs)

		# self.active_page_is_temp = False
		self.active_page = None
		# self.pages = dict()
	
	# def add_page(self, id, page: tk.Frame):
	# 	self.pages[id] = page

	# def switch_to_temp_page(self, page: tk.Frame):
	# 	self.__hide_current_page()
	# 	self.active_page_is_temp = True
	# 	page.pack(fill=tk.BOTH)

	def switch_to_page(self, page: tk.Frame):
		self.__hide_current_page()
		self.active_page = page
		self.active_page.pack(fill=tk.BOTH)

		# self.active_page_is_temp = False

		# self.active_page = self.pages[id]

	def __hide_current_page(self):
		if self.active_page != None:
			# print("Hiding page")
			# if self.active_page_is_temp:
			# 	print("Hiding temp page")
			# 	self.active_page.pack_forget()
			# else:
			self.active_page.pack_forget()
		
		# print("Page hiddeno)

	