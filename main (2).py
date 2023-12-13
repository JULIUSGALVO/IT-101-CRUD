import tkinter as tk
from tkinter import ttk
import time
from tkinter import messagebox

# Function to handle Time In
def time_in():
    if entry_name.get() and entry_id.get() and validate_id_input():
        name = entry_name.get()
        employee_id = entry_id.get()
        time_in = time.strftime("%H:%M:%S")
        date = time.strftime("%Y-%m-%d")
        data = (str(employee_id), name, date, time_in, '-')
        with open("time_records.txt", "a") as file:
            file.write('/'.join(data) + '\n')
        messagebox.showinfo("Success", "Successfully Recorded")
        entry_id.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        display_records()
        pass
    else:
        messagebox.showerror("Missing Information",
                             "Please fill in the Name and ID fields correctly to proceed with Time In.")


# Function to check if the ID is numeric and has a length of 6 digits
def validate_id_input():
    entered_id = entry_id.get()
    if not entered_id.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid ID (numeric characters only).")
        return False
    elif len(entered_id) != 6:
        messagebox.showerror("Invalid Input", "Please enter your 6 digit ID.")
        return False
    return True


# Function to handle Time Out
def time_out():
    selected_item = display_tree.focus()
    if selected_item:
        data = display_tree.item(selected_item)['values']
        if data[-1] == '-':  # Check if Time Out is empty
            time_out = time.strftime("%H:%M:%S")
            data[-1] = time_out
            updated_data = '/'.join(map(str, data)) + '\n'
            with open("time_records.txt", "r") as file:
                lines = file.readlines()
            with open("time_records.txt", "w") as file:
                for line in lines:
                    if line.split(',')[0] != str(data[0]):
                        file.write(line)
                    else:
                        file.write(updated_data)
            messagebox.showinfo("Success", "Successfully Recorded")
            display_records()
        else:
            messagebox.showinfo("Time Out Filled", "Time Out is already filled and cannot be changed.")

# Function to handle double click event on Treeview items
def on_item_double_click(event):
    item = display_tree.selection()[0]
    data = display_tree.item(item)['values']
    open_edit_window(item, data)

# Function that will open another window for Update and Delete
def open_edit_window(item, data):
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit/Delete Item")
    edit_window.geometry("200x200")
    edit_window.resizable(False, False)

    # Centering the components
    edit_window.rowconfigure(0, weight=1)
    edit_window.columnconfigure(0, weight=1)

    edit_frame = tk.Frame(edit_window)
    edit_frame.grid(row=0, column=0, sticky="nsew")

    # Display the selected item's details
    tk.Label(edit_frame, text="ID:").grid(row=0, column=0)
    id_entry = tk.Entry(edit_frame)
    id_entry.insert(0, data[0])
    id_entry.grid(row=0, column=1)

    tk.Label(edit_frame, text="Name:").grid(row=1, column=0)
    name_entry = tk.Entry(edit_frame)
    name_entry.insert(0, data[1])
    name_entry.grid(row=1, column=1)

    tk.Label(edit_frame, text="Date:").grid(row=2, column=0)
    date_entry = tk.Entry(edit_frame)
    date_entry.insert(0, data[2])
    date_entry.grid(row=2, column=1)

    tk.Label(edit_frame, text="Time In:").grid(row=3, column=0)
    time_in_entry = tk.Entry(edit_frame)
    time_in_entry.insert(0, data[3])
    time_in_entry.grid(row=3, column=1)

    tk.Label(edit_frame, text="Time Out:").grid(row=4, column=0)
    time_out_entry = tk.Entry(edit_frame)
    time_out_entry.insert(0, data[4])
    time_out_entry.grid(row=4, column=1)

    # Function to update the item's details
    def update_item():
        updated_data = [
            id_entry.get(),
            name_entry.get(),
            date_entry.get(),
            time_in_entry.get(),
            time_out_entry.get()
        ]
        display_tree.item(item, values=updated_data)
        update_text_file()
        edit_window.destroy()

    # Button to update the item's details
    update_button = tk.Button(edit_window, text="Update", command=update_item)
    update_button.grid(row=7, columnspan=2, pady=10)

    # Function to delete the item
    def delete_item():
        display_tree.delete(item)
        update_text_file()
        edit_window.destroy()

    # Button to delete the item
    delete_button = tk.Button(edit_window, text="Delete", command=delete_item)
    delete_button.grid(row=8, columnspan=2, pady=10)

def update_text_file():
    with open("time_records.txt", "w") as file:
        for item in display_tree.get_children():
            data = display_tree.item(item)['values']
            # Convert integers to strings before writing to file
            data = [str(value) if isinstance(value, int) else value for value in data]
            file.write('/'.join(data) + '\n')

# Function to display records
def display_records():
    display_tree.delete(*display_tree.get_children())
    with open("time_records.txt", "r") as file:
        lines = file.readlines()
        for idx, line in enumerate(lines, start=1):
            data = line.strip().split('/')
            display_tree.insert("", tk.END, values=data)

            # Assigning colors to rows (light shades) and setting font attributes
            bg_color = 'lightblue' if idx % 2 == 0 else 'lightgrey'
            fg_color = 'black'
            font_style = "Arial"  # Change this to your preferred font family
            font_size = 10  # Change this to your preferred font size

            display_tree.tag_configure(f'row_{idx}', background=bg_color, foreground=fg_color, font=(font_style, font_size, "bold"))
            for col in columns:
                display_tree.tag_configure(f'col_{col}_row_{idx}', background=bg_color, foreground=fg_color, font=(font_style, font_size, "bold"))
                display_tree.set(display_tree.get_children('')[idx - 1], col, data[columns.index(col)])
                display_tree.item(display_tree.get_children('')[idx - 1], tags=(f'row_{idx}', f'col_{col}_row_{idx}'))

    # Adjust column alignment for centered text appearance
    for col in columns:
        display_tree.heading(col, anchor=tk.CENTER)
        display_tree.column(col, anchor=tk.CENTER)

    # Color settings for the title row
    for child in display_tree.get_children(''):
        display_tree.item(child, tags='header')
    display_tree.tag_configure('header', background='lightgrey', foreground='black', font=('Segou UI', 10))

# Read existing records on startup
try:
    with open("time_records.txt", "r") as file:
        pass
except FileNotFoundError:
    with open("time_records.txt", "w") as file:
        pass

def on_name_click(event):
    if entry_name.get() == "Enter your name":
        entry_name.delete(0, tk.END)
        entry_name.config(fg='black')  # Change text color to black upon editing

def on_id_click(event):
    if entry_id.get() == "Enter a 6 digit ID":
        entry_id.delete(0, tk.END)
        entry_id.config(fg='black')  # Change text color to black upon editing

# Initialize Tkinter
root = tk.Tk()
root.title("Time Tracking System")
root.geometry("1200x320")
root.resizable(False, False)

# Left side - Entry fields and buttons
left_frame = tk.Frame(root, width=200, height=320)
left_frame.pack_propagate(False)
left_frame.pack(side=tk.LEFT)

centered_frame = tk.Frame(left_frame)
centered_frame.pack(expand=True)  # Expand the centered_frame to center the components

label_name = tk.Label(centered_frame, text="Name:")
label_name.pack()

entry_name = tk.Entry(centered_frame)
entry_name.insert(0, "Enter your name")  # Set default text for Name field
entry_name.pack()

label_id = tk.Label(centered_frame, text="ID:")
label_id.pack()

entry_id = tk.Entry(centered_frame)
entry_id.insert(0, "Enter a 6 digit ID")  # Set default text for ID field
entry_id.pack()

entry_name.bind("<FocusIn>", on_name_click)
entry_id.bind("<FocusIn>", on_id_click)


button_frame = tk.Frame(centered_frame)
button_frame.pack()

button_time_in = tk.Button(button_frame, text="Time In", command=time_in, bg="green", width=10)
button_time_in.pack(side=tk.LEFT, padx=5, pady=20)
button_time_out = tk.Button(button_frame, text="Time Out", command=time_out, bg="red", width=10)
button_time_out.pack(side=tk.LEFT, padx=5, pady=20)

# Right side - Display screen (table)
right_frame = tk.Frame(root, width=1000, height=320)
right_frame.pack_propagate(False)
right_frame.pack(side=tk.RIGHT)

# Configure button colors (directly using 'bg')
button_time_in.config(bg='#90EE90')  # Lighter shade of green
button_time_out.config(bg='#FFA07A')  # Lighter shade of red

columns = ("ID", "Name", "Date", "Time In", "Time Out")
display_tree = ttk.Treeview(right_frame, columns=columns, show='headings')

for col in columns:
    display_tree.heading(col, text=col)
    display_tree.column(col, width=120)

display_tree.pack(fill=tk.BOTH, expand=1)

# Bind double click event to Treeview
display_tree.bind("<Double-1>", on_item_double_click)

# Load existing data on startup
display_records()

root.mainloop()