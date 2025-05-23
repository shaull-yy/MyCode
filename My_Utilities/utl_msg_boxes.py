import tkinter as tk
from tkinter import messagebox


# Main program
if __name__ == "__main__":
	# Create the main application window
	root = tk.Tk()
	root.withdraw()  # Hide the main window

	# Show the pop-up window

	title, message = 'Title2', 'Message2'
	messagebox.showinfo(title, message)
	messagebox.showerror(title, message)
	messagebox.askquestion(title, message)
	messagebox.askokcancel(title, message)
	messagebox.askyesnocancel(title, message)
	messagebox.showwarning(title, message)

	# Mainloop (optional in this case, as we're just showing the popup)
	#root.mainloop()


