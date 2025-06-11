import tkinter as tk
from time import strftime
from tkinter import font as tkfont


def update_time():
    """Update the time display every second"""
    current_time = strftime("%H:%M:%S")
    current_date = strftime("%A, %B %d, %Y")
    time_label.config(text=current_time)
    date_label.config(text=current_date)

    # Change color every second for a subtle effect
    colors = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#3B1C32"]
    current_color = colors[int(strftime("%S")) % len(colors)]
    main_frame.config(bg=current_color)
    time_label.config(bg=current_color)
    date_label.config(bg=current_color)

    root.after(1000, update_time)


def toggle_fullscreen(event=None):
    """Toggle fullscreen mode"""
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))


def quit_app(event=None):
    """Exit the application"""
    root.destroy()


# Create main window
root = tk.Tk()
root.title("Advanced Digital Clock")
root.geometry("800x400")
root.configure(bg="#121212")
root.attributes("-alpha", 0.95)  # Slight transparency


# Make window draggable
def move_window(event):
    root.geometry(f'+{event.x_root}+{event.y_root}')


title_bar = tk.Frame(root, bg="#121212", relief="raised", bd=0)
title_bar.pack(fill=tk.X)
title_label = tk.Label(title_bar, text="Digital Clock", bg="#121212", fg="white", font=("Arial", 10))
title_label.pack(side=tk.LEFT, padx=10)

# Bind title bar for moving window
title_bar.bind("<B1-Motion>", move_window)
title_label.bind("<B1-Motion>", move_window)

# Close button
close_button = tk.Button(title_bar, text="×", bg="#121212", fg="white", bd=0,command=quit_app, font=("Arial", 12))
close_button.pack(side=tk.RIGHT)
close_button.bind("<Enter>", lambda e: close_button.config(bg="#C73E1D"))
close_button.bind("<Leave>", lambda e: close_button.config(bg="#121212"))

# Main frame for clock
main_frame = tk.Frame(root, bg="#2E86AB")
main_frame.pack(expand=True, fill=tk.BOTH)

# Custom font
try:
    custom_font = tkfont.Font(family="DS-Digital", size=80, weight="bold")
except:
    custom_font = tkfont.Font(family="Courier", size=80, weight="bold")

# Time label
time_label = tk.Label(main_frame, font=custom_font, bg="#2E86AB", fg="white")
time_label.pack(expand=True)

# Date label
date_font = tkfont.Font(family="Arial", size=20, weight="bold")
date_label = tk.Label(main_frame, font=date_font, bg="#2E86AB", fg="white")
date_label.pack(pady=(0, 20))

# Bottom controls
controls_frame = tk.Frame(root, bg="#121212")
controls_frame.pack(fill=tk.X)

# Info label
info_label = tk.Label(controls_frame, text="Press F11 to toggle fullscreen | ESC to quit",bg="#121212", fg="#888888", font=("Arial", 8))
info_label.pack(side=tk.LEFT, padx=10)

# Key bindings
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", quit_app)

# Start the clock
update_time()

root.mainloop()