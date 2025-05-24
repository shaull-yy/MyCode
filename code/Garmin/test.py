import tkinter as tk

def get_activities_count():
    num = 0  # Initialize num

    def submit():
        nonlocal num  # Access the enclosing scope's variable
        num = entry.get()  # Retrieve input
        root.destroy()  # Close the window

    def stop_program():
        nonlocal num  # Access the enclosing scope's variable
        num = 0  # Set num to 0
        root.destroy()  # Close the window

    def close_with_escape(event=None):
        nonlocal num  # Access the enclosing scope's variable
        num = entry.get()  # Retrieve input
        root.destroy()  # Close the window

    def clear_entry_on_focus(event):
        if entry.get() == default_value:
            entry.delete(0, tk.END)  # Clear the entry

    # Create the Tkinter window
    root = tk.Tk()
    root.geometry('600x250')
    root.title('Set How Many Activities to Extract')

    # Bind Escape key to close the window
    root.bind("<Escape>", close_with_escape)

    # Labels
    font_size = 10
    btn_width = 17
    current_row = 3
    file_name_label = tk.Label(root, text='Number of Activities to Extract:', font=("Arial", font_size))
    file_name_label.grid(row=current_row, column=0, sticky=tk.NW, pady=(0, 0), padx=(5, 0))

    # Entry box
    current_row += 1
    default_value = "10"  # Default value as a string
    entry = tk.Entry(root)
    entry.grid(row=current_row, column=0, sticky=tk.NW, pady=(10, 5), padx=(5, 0))
    entry.insert(0, default_value)  # Set default value
    entry.bind("<FocusIn>", clear_entry_on_focus)  # Bind focus event to clear default value

    # Submit button
    current_row += 1
    submit_btn = tk.Button(root, text='Submit', command=submit, width=btn_width, bg='light gray')
    submit_btn.grid(row=current_row, column=0, sticky=tk.NW, pady=(10, 5), padx=(5, 0))

    # Abort button
    current_row += 1
    stop_btn = tk.Button(root, text='Abort Program', command=stop_program, width=btn_width, bg='light gray')
    stop_btn.grid(row=current_row, column=0, sticky=tk.NW, pady=(0, 5), padx=(5, 0))

    root.mainloop()
    return int(num)  # Convert to an integer before returning

# Example usage
activities_count = get_activities_count()
print(f"Activities to extract: {activities_count}")
