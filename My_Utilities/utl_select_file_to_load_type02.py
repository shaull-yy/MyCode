import os
from tkinter import Tk, StringVar, OptionMenu, Button, Label, Entry, filedialog
print("utl_dialog_box_type01 loaded")

class FileSelectorApp:
    def __init__(self, root, initial_directory, box_title):
        self.root = root
        self.root.geometry("600x400")  # Set window size
        self.root.attributes("-topmost", True)  # Keep window on top
        self.selected_file = None  # Attribute to store the selected file
        self.files = []  # Store file paths
        self.root_directory = initial_directory  # Variable to store the root directory
        self.box_title = box_title
        self.setup_ui()

    def setup_ui(self):
        Label(self.root, text=self.box_title, font=("Arial", 14)).pack(pady=10)

        # Search box
        self.search_var = StringVar()
        self.search_box = Entry(self.root, textvariable=self.search_var, width=30)
        self.search_box.pack(pady=10)
        self.search_box.bind("<KeyRelease>", self.filter_files)  # Bind key press to filter files

        self.dropdown_var = StringVar(value="Select a File")
        self.dropdown_var.trace("w", self.on_file_selected)  # Bind variable change to selection handler
        self.dropdown_menu = OptionMenu(self.root, self.dropdown_var, [])
        self.dropdown_menu.pack(pady=10, fill="x")

        # Define a uniform button width
        button_width = 20

        Button(self.root, text="Select a Folder", width=button_width, command=self.load_files).pack(pady=5)
        Button(self.root, text="Close", width=button_width, command=self.root.destroy).pack(pady=5)

        self.status_label = Label(self.root, text="", wraplength=500, justify="left", font=("Arial", 10))
        self.status_label.pack(pady=10)

    def get_all_files(self, folder_path):
        """Recursively get all files in a folder and its subfolders."""
        file_list = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_list.append(os.path.join(root, file))
        return file_list

    def load_files(self):
        """Load all files in the selected folder."""
        folder_path = filedialog.askdirectory(title="Select Folder")
        if folder_path:
            self.root_directory = folder_path  # Store the root directory
            self.files = self.get_all_files(folder_path)
            if not self.files:
                self.status_label.config(text="No files found in the selected folder.")
                return

            self.filter_files()  # Apply filter if any search term is present

            self.dropdown_var.set("Select a file")  # Reset dropdown
            self.dropdown_menu["menu"].delete(0, "end")  # Clear previous options

            for file in self.files:
                self.dropdown_menu["menu"].add_command(
                    label=file, command=lambda value=file: self.dropdown_var.set(value)
                )

            self.status_label.config(text=f"Loaded {len(self.files)} files.")
        else:
            self.status_label.config(text="No folder selected.")

    def filter_files(self, event=None):
        """Filter files based on the search term."""
        search_term = self.search_var.get().lower()
        filtered_files = [file for file in self.files if search_term in file.lower()]

        # Reset the dropdown menu and update it with the filtered files
        self.dropdown_var.set("Select a file")  # Reset dropdown
        self.dropdown_menu["menu"].delete(0, "end")  # Clear previous options

        for file in filtered_files:
            self.dropdown_menu["menu"].add_command(
                label=file, command=lambda value=file: self.dropdown_var.set(value)
            )

        self.status_label.config(text=f"Found {len(filtered_files)} matching files.")

    def on_file_selected(self, *args):
        """Handle file selection from the dropdown."""
        selected = self.dropdown_var.get()
        if selected != "Select a File":
            self.selected_file = selected
            self.status_label.config(text=f"Selected file: {self.selected_file}")
        else:
            self.status_label.config(text="No file selected.")
            
    def get_selected_file(self): # Return the currently selected file
        return self.selected_file

#---------- Main ------------------

if __name__ == '__main__':
    initial_directory=""
    title = 'Run this class'
    root = Tk()
    app = FileSelectorApp(root, initial_directory, title)
    root.mainloop()
    if app.selected_file:
         print(app.selected_file)
    else:
         print('empty')