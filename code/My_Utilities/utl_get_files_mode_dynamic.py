import tkinter as tk
from tkinter import Tk, StringVar

class OpenFileMode:
	def __init__(self, parent_win, absulote_file_path=[], file_name=[]):
		
		self.absulote_file_path = absulote_file_path
		self.file_name = file_name
		self.parent_win = parent_win
		self.font_size = 10
		self.btn_width = 17
		self.mode = ''
		self.files_count = 0
		self.check_input_lists()
		self.create_window()
		self.set_up_ui()

	def check_input_lists(self):
		if len(self.absulote_file_path) != len(self.file_name):
			print(f'Input lists are not same size. List contents: \n'
		          f'absulote_file_path list: {self.absulote_file_path} \n'
		          f'file_name list: {self.file_name}'
				  'Aborting this function')
			return
		else:
			self.files_count = len(self.absulote_file_path)

	def create_window(self):
		self.win1 = tk.Toplevel(self.parent_win)
		self.win1.geometry('600x250')
		self.win1.title(f'Select the method to get the following files')

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

		current_row = 5
		for i in range(self.files_count):
			file_name_lable = tk.Label(self.win1, text=f'Default {self.file_name[i]} File:', font=("Arial", self.font_size))
			file_name_lable.grid(row=current_row, column=0, sticky=tk.NW, pady=(0, 0), padx=(5, 0))
			current_row += 1

			file_path_lable = tk.Label(self.win1, text=self.absulote_file_path[i], font=("Arial", self.font_size))
			file_path_lable.grid(row=current_row, column=0, sticky=tk.NW, pady=(0, 5), padx=(50, 0))
			current_row += 1

		# Buttons
		submit_btn = tk.Button(self.win1, text='Submit', command=self.submit, width=self.btn_width, bg='light gray')
		submit_btn.grid(row=current_row, column=0, sticky=tk.NW, pady=(10, 5), padx=(5, 0))
		current_row += 1

		stop_btn = tk.Button(self.win1, text='Abort Program', command=self.stop_program, width=self.btn_width, bg='light gray')
		stop_btn.grid(row=current_row, column=0, sticky=tk.NW, pady=(0, 5), padx=(5, 0))

		self.adjust_window_size(current_row)
	
	
	def adjust_window_size(self, current_row):
		width = 600
		height = current_row * 28
		
		# Set the new geometry
		self.win1.geometry(f"{width}x{height}")


def run_the_pop_up():
	root = tk.Tk()
	root.withdraw()
	open_file_mode_app = OpenFileMode(root, ['path1', 'path2','path1', 'path2'], ['name1', 'name2','path1', 'path2'])
	root.wait_window(open_file_mode_app.win1)
	print('---------- window closed')
	print(open_file_mode_app.mode)

if __name__ == '__main__':
	run_the_pop_up()

