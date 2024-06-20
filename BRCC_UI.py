import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import subprocess
from tkcalendar import DateEntry


TIME_VALUES = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
# Function to handle button click
def on_button_click():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    time_frame_start = time_frame_start_entry.get()
    time_frame_end = time_frame_end_entry.get()
    time_zone = time_zone_combobox.get()

    # Store the values in a temporary file or pass them as arguments
    with open('config.txt', 'w') as f:
        f.write(f"{start_date},{end_date},{time_frame_start},{time_frame_end},{time_zone}")

    # Run the other Python file
    result = subprocess.Popen(["venv\\Scripts\\python", "BRCC_Task.py"], stderr=subprocess.PIPE)

    if result.returncode != 0:
        print(result.stderr.readlines()[-1].decode("utf-8"))

# Initialize the main window
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("BRCC Task")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.geometry("600x200")

# Widgets for start date, end date, time frame, and time zone
start_date_label = ctk.CTkLabel(root, text="Start Date (YYYY-MM-DD):")
start_date_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
start_date_entry = DateEntry(root, date_pattern='yyyy-mm-dd', background='darkblue', foreground='white', borderwidth=2)
start_date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

end_date_label = ctk.CTkLabel(root, text="End Date (YYYY-MM-DD):")
end_date_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
end_date_entry = DateEntry(root, date_pattern='yyyy-mm-dd', background='darkblue', foreground='white', borderwidth=2)
end_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

time_frame_start_label = ctk.CTkLabel(root, text="Time Frame:")
time_frame_start_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")
time_frame_start_entry = ctk.CTkOptionMenu(root, values=TIME_VALUES)
time_frame_start_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

time_frame_end_label = ctk.CTkLabel(root, text="Time Frame:")
time_frame_end_label.grid(row=1, column=2, padx=5, pady=5, sticky="e")
time_frame_end_entry = ctk.CTkOptionMenu(root, values=TIME_VALUES)
time_frame_end_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")



time_zone_label = ctk.CTkLabel(root, text="Time Zone:")
time_zone_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
time_zone_combobox = ctk.CTkOptionMenu(root, values=["CET", "EEST", "UTC"])
time_zone_combobox.grid(row=3, column=0, padx=5, pady=5, sticky="e")

# Button to start the plotting script
start_button = ctk.CTkButton(root, text="Start Plotting", command=on_button_click)
start_button.grid(row=4, column=0, padx=5, pady=5, sticky="e")

# Run the main loop
root.mainloop()
