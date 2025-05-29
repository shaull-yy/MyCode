import tkinter as tk
from tkinter import StringVar

def get_activities_count(default_activities_count):
	num = 0
	upd_db = ''

	def submit():
		nonlocal num, upd_db
		num = entry.get()  # Retrieve input
		upd_db = upd_db_radio_var.get()
		root.destroy()

	def stop_program():
		nonlocal num, upd_db
		num = 0
		upd_db = ''
		root.destroy()

	def close_with_escape(event=None):
		nonlocal num, upd_db  # Access the enclosing scope's variable
		num = 0
		upd_db = ''
		root.destroy()  # Close the window	

	def clear_entry_on_focus(event):
		if entry.get() == default_activities_count:
			entry.delete(0, tk.END)  # Clear the entry

	# -------- Main of function -------
	default_activities_count = str(default_activities_count)
	root = tk.Tk()
	root.geometry('600x250')
	root.title('Set How Many Activities to Extract')
	# Bind Escape key to close the window
	root.bind("<Escape>", close_with_escape)

	# Set up UI
	font_size = 10
	btn_width = 17
	current_row = 3
	root.columnconfigure(1, weight=1) 
	upd_db_radio_var = StringVar(value="yes")

	# Labels
	file_name_label = tk.Label(root, text='Number of Activities to Extract:', font=("Arial", font_size))
	file_name_label.grid(row=current_row, column=0, sticky=tk.NW, pady=(0, 0), padx=(5, 0))

	# Text box for inserting a number
	current_row += 1
	entry = tk.Entry(root)
	entry.grid(row=current_row, column=0, sticky=tk.NW, pady=(10, 5), padx=(5, 0))
	entry.insert(0, default_activities_count)
	entry.bind("<FocusIn>", clear_entry_on_focus)  # Bind focus event to clear default value

	current_row += 1
	radio_btn_row = current_row

	# Buttons
	submit_btn = tk.Button(root, text='Submit', command=submit, width=btn_width, bg='light gray')
	submit_btn.grid(row=current_row, column=0, sticky=tk.NW, pady=(10, 5), padx=(5, 0))
	submit_btn.focus_set()  # Set the Submit button as the focused widget
	root.bind("<Return>", lambda event: submit())  # Bind Enter key to the Submit button

	current_row += 1

	stop_btn = tk.Button(root, text='Abort Program', command=stop_program, width=btn_width, bg='light gray')
	stop_btn.grid(row=current_row, column=0, sticky=tk.NW, pady=(0, 5), padx=(5, 0))

	radio_btn1 = tk.Radiobutton(root, text='Dont UPD Garmin DB (Tests)', variable=upd_db_radio_var, value='no')
	radio_btn1.grid(row=radio_btn_row, column=1, sticky=tk.NW, pady=(0, 5), padx=(5, 0))
	radio_btn_row += 1

	radio_btn2 = tk.Radiobutton(root, text='UPD Garmin DB', variable=upd_db_radio_var, value='yes')
	radio_btn2.grid(row=radio_btn_row, column=1, sticky=tk.NW, pady=(0, 5), padx=(5, 0))

	root.mainloop()
	return num, upd_db
