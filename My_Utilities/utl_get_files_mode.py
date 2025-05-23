import tkinter as tk
from tkinter import Tk, StringVar

class OpenFileMode:
	def __init__(self, parent_win, absulote_file_path1='', file_name1='', absulote_file_path2 ='', file_name2=''):
		if absulote_file_path1:
			self.absulote_file_path1 = absulote_file_path1
			self.file_name1 = file_name1
		else:
			self.absulote_file_path1, self.file_name1 = "Name not Provided", "Name not Provided"
		if absulote_file_path2:
			self.absulote_file_path2 = absulote_file_path2
			self.file_name2 = file_name2
		else:
			self.absulote_file_path2, self.file_name2 = "Name not Provided", "Name not Provided"
		self.parent_win = parent_win
		self.font_size = 10
		self.btn_width = 17
		self.mode = ''
		self.create_window()
		self.set_up_ui()

	def create_window(self):
		self.win1 = tk.Toplevel(self.parent_win)
		self.win1.geometry('600x250')
		self.win1.title(f'Select the method to get the "{self.file_name1}" and "{self.file_name2}" files')

	def submit(self):
		self.mode = self.radio_var.get()
		self.win1.destroy()

	def stop_program(self):
		self.mode = ''
		self.win1.destroy()

	def bind_escape(self):
		self.win1.bind("<Escape>", lambda event: self.win1.destroy())

	def set_up_ui(self):
		self.bind_escape()
		self.radio_var = StringVar(value="d")
		
		# Radio Buttons
		rdio1 = tk.Radiobutton(self.win1, text='Default Files', font=("Arial", self.font_size), variable=self.radio_var, value='d')
		rdio1.grid(row=3, column=0, sticky=tk.NW, pady=(0, 0), padx=(5, 0))

		rdio2 = tk.Radiobutton(self.win1, text='Select Files Manually', font=("Arial", self.font_size), variable=self.radio_var, value='m')
		rdio2.grid(row=4, column=0, sticky=tk.NW, pady=(0, 5), padx=(5, 0))

		# Labels for File Names
		#self.win1.columnconfigure(0, minsize=150)  # Set minimum width for column 0
		self.win1.columnconfigure(1, weight=1) 
		param_label = tk.Label(self.win1, text=f'Default {self.file_name1} File:', font=("Arial", self.font_size))
		param_label.grid(row=5, column=0, sticky=tk.NW, pady=(0, 0), padx=(5, 0))

		param_file_label = tk.Label(self.win1, text=self.absulote_file_path1, font=("Arial", self.font_size))
		param_file_label.grid(row=6, column=0, sticky=tk.NW, pady=(0, 5), padx=(50, 0))

		data_label = tk.Label(self.win1, text=f'Default {self.file_name2} File:', font=("Arial", self.font_size))
		data_label.grid(row=7, column=0, sticky=tk.NW, pady=(0, 0), padx=(5, 0))

		data_file_label = tk.Label(self.win1, text=self.absulote_file_path2, font=("Arial", self.font_size))
		data_file_label.grid(row=8, column=0, sticky=tk.NW, pady=(0, 5), padx=(50, 0))

		# Buttons
		submit_btn = tk.Button(self.win1, text='Submit', command=self.submit, width=self.btn_width, bg='light gray')
		submit_btn.grid(row=9, column=0, sticky=tk.NW, pady=(10, 5), padx=(5, 0))

		stop_btn = tk.Button(self.win1, text='Abort Program', command=self.stop_program, width=self.btn_width, bg='light gray')
		stop_btn.grid(row=10, column=0, sticky=tk.NW, pady=(0, 5), padx=(5, 0))
	


def run_the_pop_up():
	root = tk.Tk()
	root.withdraw()
	open_file_mode_app = OpenFileMode(root, 'absulote_file_path1', 'name1', 'absulote_file_path2', 'name2')
	root.wait_window(open_file_mode_app.win1)
	print('---------- window closed')
	print(open_file_mode_app.mode)

if __name__ == '__main__':
	run_the_pop_up()

