import tkinter as tk
from tkinter import PhotoImage
import sys
import os

# Get the directory of the script to load images from the correct path
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(script_dir)

# Example action data and corresponding image paths
actions = [
    ("Copy Files", "copy_files.png"),
    ("Delete Specific Files", "delete_specific_files.png"),
    ("Delete Files by Type", "delete_files_by_type.png"),
    ("Backup Files", "backup_files.png")
]

# Array of image paths corresponding to each action
image_paths = [
    "file_copy.png",            # Image for "Copy Files"
    "target.png",               # Image for "Delete Specific Files"
    "delete_files.png",         # Image for "Delete Files by Type"
    "backup.png"                # Image for "Backup Files"
]

# Function to handle button clicks (dummy function for now)
def show_screen(action):
    print(f"Action: {action}")

# Create main window
root = tk.Tk()
root.title("Main Menu")
root.geometry("800x550")  # Set the window size
root.configure(bg="#ffffff")  # Set the root background color to white

# Create main frame to hold content
main_frame = tk.Frame(root, bg="#ffffff")  # Set the background color of the main frame to white
main_frame.pack(fill="both", expand=True)

# Label at the top
tk.Label(main_frame, text="What do you want to do?", font=("Helvetica", 16), bg="#ffffff", fg="black").pack(pady=20)

# Frame for the buttons
buttons_frame = tk.Frame(main_frame, bg="#ffffff")  # Set the background color of the buttons frame to white
buttons_frame.pack(pady=20)

# Store references to images to prevent garbage collection
image_references = []

# Set the width and height for the frames and buttons to make them uniform
frame_width = 150
frame_height = 150

# Use grid to place the frames side by side
buttons_frame.grid_columnconfigure(0, weight=1)
buttons_frame.grid_columnconfigure(1, weight=1)
buttons_frame.grid_columnconfigure(2, weight=1)
buttons_frame.grid_columnconfigure(3, weight=1)

# Iterate through actions and corresponding image paths to create buttons
for idx, (text, icon_path) in enumerate(zip([action[0] for action in actions], image_paths)):
    # Load the icon image (make sure the paths are correct)
    try:
        icon = PhotoImage(file=icon_path)
        print("icon = ", icon, " path is ", icon_path)
    except Exception as e:
        print(f"Error loading image {icon_path}: {e}")
        continue
    
    image_references.append(icon)  # Keep reference to avoid garbage collection

    # Create a button without the border around it
    button = tk.Button(buttons_frame, image=icon, text=text, font=("Helvetica", 12), bg="white", fg="black", 
                       compound="top", command=lambda a=text: show_screen(a), highlightthickness=0, borderwidth=0)

    # Place the button side by side in the same row using grid
    button.grid(row=0, column=idx, padx=10, pady=10)

    # Set button size to match the frame size
    button.config(width=frame_width, height=frame_height)

# Start the Tkinter event loop
root.mainloop()
