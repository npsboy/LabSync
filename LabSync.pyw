import shutil
import sys
import os
import glob
import time
import re
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, ttk, PhotoImage




root = tk.Tk()
root.withdraw()
loading_window = None  
progress = None 
# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# Change the working directory to the script directory
os.chdir(script_dir)


hardcode_path = lambda i: fr"C:\Users\Tusha\OneDrive\Documents\Test_{i}\d" #change this



def show_loading_bar(percentage):
    global loading_window, progress

    if loading_window is None or not loading_window.winfo_exists():
        # Create the loading window if it doesn't exist
        loading_window = tk.Toplevel(root)
        loading_window.title("Operation in progress")
        loading_window.geometry("300x100")
        loading_window.resizable(False, False)

        # Add a label to the window
        label = tk.Label(loading_window, text="Action underway, please wait...")
        label.pack(pady=10)

        # Create the progress bar
        progress = ttk.Progressbar(loading_window, orient="horizontal", length=250, mode="determinate")
        progress.pack(pady=10)
        progress["maximum"] = 100  # Set the maximum value

    # Update the progress bar value
    progress["value"] = percentage
    loading_window.update_idletasks()  # Update the UI
   





# Function to copy files
def copy_files(source, start, end, dest_folder):

    parts = re.split(r"(?<=/d)",dest_folder,1)
    # If the second part is empty, return just the first part
    if len(parts) == 2 and parts[1] == '':
        parts.pop(1)
    if len(parts)>1:
        dest_folder = parts[1]
    else:
        dest_folder = ""
    source = source.strip('"').strip("'")
    missing_destinations = []
    folder_name = os.path.basename(source.rstrip('/'))  # For copying folders

    if not os.path.exists(source):
        messagebox.showerror("Error", f"The source file does not exist: {source}")
        return

    for i in range(start, end + 1):
        destination_path = hardcode_path(i) + dest_folder
        print('destination path = ', destination_path)
        if not os.path.exists(destination_path):
            missing_destinations.append(i)
        else:
            source_dir = os.path.dirname(source)
            if os.path.abspath(source_dir) != os.path.abspath(destination_path):
                print('went in')
                # Check if the source is a file or a directory
                if os.path.isdir(source):
                    destination_path = os.path.join(destination_path, folder_name)
                    if not os.path.exists(destination_path):
                        shutil.copytree(source, destination_path)
                else:
                    shutil.copy2(source, destination_path)

        global loading_window
        percentage = (i / (end+1-start) ) * 100
        # Update the progress bar with the calculated percentage
        show_loading_bar(percentage)  # Update the progress bar
        root.update()  # Allow the GUI to process events

        
    loading_window.destroy()
    
    if missing_destinations:
        messagebox.showinfo("File copied to most destinations",
            f"The file was copied to most computers. \nFile not copied to following computers: {missing_destinations}")
    else:
        messagebox.showinfo("Success", "Files copied successfully to all specified destinations!")

# Function to handle copy process
def run_copy(source, start, end, dest_folder):
    try:
        start = int(start)
        end = int(end)
        if start <= end:
            copy_files(source, start, end, dest_folder)  # Pass the dest_folder parameter
        else:
            messagebox.showerror("Error", "The start number must be less than or equal to the end number.")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for the range.")


def confirm_deletion():
    # Create a dialog box for confirmation
    response = simpledialog.askstring("Confirmation", "Are you sure? This will permanently delete all specified files.\n\nType 'computer lab' in the text box below to confirm.")
    
    # Check if the response matches the required confirmation phrase
    if response == "computer lab":
        return True
    else:
        messagebox.showerror("Error", "Confirmation phrase not entered correctly. Action aborted.")
        return False




# Function to delete specific files
def delete_files(unwanted_file, start, end):
    #unwanted_file = os.path.basename(unwanted_file)

    try:
        start = int(start)
        end = int(end)
        if start > end:
            messagebox.showinfo("error", "Start should not be greater than end")
            return
    except ValueError:
        messagebox.showinfo("error", "Please enter valid numbers for range")
        return



    parts = re.split(r"(?<=/d)",unwanted_file,1)
    if len(parts) == 2 and parts[1] == '':
        parts.pop(1)
    if len(parts) < 2:
        print("parts in delete files = ", parts)
        messagebox.showerror("Error", "please choose a valid file")
        return
    
    if not confirm_deletion():
            return

    missing_destinations = []

    for i in range(start, end + 1):
        if len(parts) > 1:
            unwanted_file = parts[1]
            delete_path = hardcode_path(i) + unwanted_file
        else:
           delete_path = hardcode_path(i)
        if not os.path.exists(delete_path):
            missing_destinations.append(i)
        else:
            if os.path.isdir(delete_path):
                shutil.rmtree(delete_path)
            else:
                os.remove(delete_path)

        global loading_window
        percentage = (i / (end+1-start) ) * 100
        # Update the progress bar with the calculated percentage
        show_loading_bar(percentage)  # Update the progress bar
        root.update()  # Allow the GUI to process events

        
    loading_window.destroy()

    if missing_destinations:
        messagebox.showinfo("File deleted", f"The file was deleted from most computers. \nFile not deleted from following computers: {missing_destinations}")
    else:
        messagebox.showinfo("Success", "File deleted from all computers!")


def delete_file_type(directory_path, file_extension, start, end):
    try:
        start = int(start)
        end = int(end)
        if start > end:
            messagebox.showinfo("error", "Start should not be greater than end")
            return
    except ValueError:
        messagebox.showinfo("error", "Please enter valid numbers for range")
        return


    if file_extension.startswith("."): #removes "." from the extension
        file_extension =  file_extension[1:]
    # Loop through each Test folder
    parts = re.split(r"(?<=/d)",directory_path,1)
    # If the second part is empty, return just the first part
    if len(parts) == 2 and parts[1] == '':
        parts.pop(1)
    if len(parts) < 2:
        response = messagebox.askyesno("Confirmation", fr"Are you sure? This will delete all {file_extension} files from the full d drive")
        if not response:
            messagebox.showinfo('aborted','action aborted')
            return
        
    if not confirm_deletion():
            return
    failed_computers = [] 
    print("start = ", start)
    print("end = ", end)
    print("parts = ", parts)
    for i in range(start, end+1):  # Adjust range if you have more or fewer folders
        if len(parts) > 1:
            
            folder_path = hardcode_path(i) + parts[1]
        else:
            folder_path = hardcode_path(i)
        # Check if folder exists
        if os.path.isdir(folder_path):
            # Find all files with the given extension in the folder
            files_to_delete = glob.glob(os.path.join(folder_path, f"**/*.{file_extension}"), recursive=True)
            print("folder path = ", folder_path)
            print("files to delete = ", files_to_delete)
            
            # Delete each file
            for file_path in files_to_delete:
                try:
                    os.remove(file_path)
                except Exception as e:
                    failed_computers.append(i)
        else:
            failed_computers.append(i)

        global loading_window
        percentage = (i / (end+1-start) ) * 100
        # Update the progress bar with the calculated percentage
        show_loading_bar(percentage)  # Update the progress bar
        root.update()  # Allow the GUI to process events

        
    loading_window.destroy()
    
    if failed_computers:
        messagebox.showinfo("File deleted", f"The file was deleted from most computers. \nFile not deleted from following computers: {failed_computers}")
    else:
        messagebox.showinfo("Success", "File deleted from all computers!")



def backup_files(directory_path, file_extension, destination_path, start, end):
    try:
        start = int(start)
        end = int(end)
        if start > end:
            messagebox.showinfo("error", "Start should not be greater than end")
            return
    except ValueError:
        messagebox.showinfo("error", "Please enter valid numbers for range")
        return
    
    if not os.path.exists(destination_path):
        messagebox.showinfo("error", "Destination path doe not exist")
        return
        
    parts = re.split(r"(?<=/d)",directory_path,1)
    # If the second part is empty, return just the first part
    if len(parts) == 2 and parts[1] == '':
        parts.pop(1)
    
    if file_extension.startswith("."): #removes "." from the extension
        file_extension =  file_extension[1:]
    failed_computers = []
    unexisting_sources = []
    print("start = ", start)
    print("end = ", end)
    print('directory path = ', directory_path)
    print("parts = ", parts)
    for i in range(start, end+1):  # Adjust range if you have more or fewer folders
        if len(parts) > 1:
            folder_path = hardcode_path(i) + parts[1]
        else:
            folder_path = hardcode_path(i)

        # Check if folder exists
        if os.path.isdir(folder_path):
            # Find all files with the given extension in the folder
            files_to_copy = glob.glob(os.path.join(folder_path, f"*.{file_extension}"))
            print('folder path = ', folder_path)
            # Delete each file
            if len(files_to_copy) == 0:
                unexisting_sources.append(i)
            for file_path in files_to_copy:
                try:
                    print('destinataion path = ', destination_path, i)
                    created_folder = destination_path + r"/" + "computer_" + str(i)
                    print('created folder = ', created_folder)
                    os.makedirs(created_folder, exist_ok=True) #creates a folder
                    shutil.copy(file_path,created_folder)
                except Exception as e:
                    failed_computers.append(i)
        else:
            failed_computers.append(i)
        
        global loading_window
        percentage = (i / (end+1-start) ) * 100
        # Update the progress bar with the calculated percentage
        show_loading_bar(percentage)  # Update the progress bar
        root.update()  # Allow the GUI to process events

        
    loading_window.destroy()


    if failed_computers:
        if unexisting_sources:
            messagebox.showinfo('files backed-up', f'Files backed-up from most computers. \nFile not copied from following computers: {failed_computers} \n No files to copy from following computers: {unexisting_sources}')
        else:
            messagebox.showinfo("File backed-up", f"The file was copied from most computers. \nFile not copied from following computers: {failed_computers}")
    elif unexisting_sources:
        messagebox.showinfo('files backed-up', f'Files backed-up from most computers. No files to copy from following computers: {unexisting_sources}')
    else:
        messagebox.showinfo("Success", "File has been backed up from all computers")



# Function to navigate back to the main menu
def go_back():
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Recreate the main menu
    tk.Label(main_frame, text="Select Your Task", font=("Helvetica", 20,"bold"), bg="#ffffff", fg="black").pack(pady=20)
    actions = [
    ("Copy Files", "Copy Files"),
    ("Delete Specific Files", "Delete Specific Files"),
    ("Delete Files by Type", "Delete Files by Type"),
    ("Backup Files", "Backup Files")
    ]
    image_paths = [
        fr"file_copy.png",            # Image for "Copy Files"
        fr"target.png",               # Image for "Delete Specific Files"
        fr"delete_files.png",         # Image for "Delete Files by Type"
        fr"backup.png"                # Image for "Backup Files"
    ]
    buttons_frame = tk.Frame(main_frame, bg="#ffffff")
    buttons_frame.pack(pady=20)
    image_references.clear()

    # Configure grid
    buttons_frame.grid_columnconfigure(0, weight=1)
    buttons_frame.grid_columnconfigure(1, weight=1)
    buttons_frame.grid_columnconfigure(2, weight=1)
    buttons_frame.grid_columnconfigure(3, weight=1)

    # Create buttons with icons
    for idx, (text, icon_path) in enumerate(zip([action[0] for action in actions], image_paths)):
        try:
            icon = PhotoImage(master=root, file=icon_path)
            image_references.append(icon)  # Prevent garbage collection
        except Exception as e:
            print(f"Error loading image {icon_path}: {e}")
            continue

        button = tk.Button(
            buttons_frame, image=icon, text=text, font=("Helvetica", 12), bg="white", fg="black",
            compound="top", command=lambda a=text: show_screen(a), highlightthickness=0, borderwidth=0
        )
        button.grid(row=0, column=idx, padx=10, pady=10)

# Function to open a file dialog and store the selected file path
def browse_file(entry_widget):
    selected_file_path = filedialog.askopenfilename(title="Select a File")  # Open file dialog for files

    if selected_file_path:
        entry_widget.delete(0, tk.END)  # Clear existing text
        entry_widget.insert(0, selected_file_path)  # Insert the selected file path

# Function to open a folder dialog and store the selected folder path
def browse_folder(entry_widget):
    selected_file_path = filedialog.askdirectory(title="Select a Folder")  # Open folder dialog

    if selected_file_path:
        entry_widget.delete(0, tk.END)  # Clear existing text
        entry_widget.insert(0, selected_file_path)  # Insert the selected folder path

# Function to navigate to the corresponding screen
def show_screen(action):
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Display the chosen action
    tk.Label(main_frame, text=f"{action}", font=("Helvetica", 16), bg="#ffffff", fg="black").pack(pady=20)
    if action == "Copy Files":
        # Source entry field
        source_entry = tk.Entry(main_frame, width=50, bd=1, relief="solid", fg="black")
        source_entry.pack(pady=(10, 10))

        # Create a frame to hold both buttons
        button_frame = tk.Frame(main_frame, bg="#ffffff")
        button_frame.pack(pady=(0, 10))

        # Separate buttons for browsing files and folders, placed side by side
        browse_file_button = tk.Button(button_frame, text="Browse Files", command=lambda: browse_file(source_entry), bg="#2c3e50", fg="white")
        browse_file_button.pack(side=tk.LEFT, padx=(0, 5))

        browse_folder_button = tk.Button(button_frame, text="Browse Folders", command=lambda: browse_folder(source_entry), bg="#2c3e50", fg="white")
        browse_folder_button.pack(side=tk.LEFT, padx=(5, 0))

        # Destination range label and entries
        dest_label = tk.Label(main_frame, text="Destination Range (From Number To Number):", font=("Helvetica", 12), bg="#ffffff", fg="black")
        dest_label.pack(pady=(10, 0))

        from_frame = tk.Frame(main_frame, bg="#ffffff")
        from_frame.pack(pady=(10, 0))

        tk.Label(from_frame, text="From:", font=("Helvetica", 12), bg="#ffffff", fg="black").pack(side=tk.LEFT, padx=(0, 5))
        from_entry = tk.Entry(from_frame, width=5, bd=1, relief="solid", fg="black")
        from_entry.pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(from_frame, text="To:", font=("Helvetica", 12), bg="#ffffff", fg="black").pack(side=tk.LEFT, padx=(0, 5))
        to_entry = tk.Entry(from_frame, width=5,bd=1, relief="solid", fg="black")
        to_entry.pack(side=tk.LEFT)

        # Destination folder label and folder display
        dest_folder_label = tk.Label(main_frame, text="Destination Folder (optional):", font=("Helvetica", 12), bg="#ffffff", fg="black")
        dest_folder_label.pack(pady=(10, 0))

        dest_folder_display = tk.Label(main_frame, text="", font=("Helvetica", 10),bg="white", fg="black", width=50, anchor="w", relief="solid", bd=1)
        dest_folder_display.pack(pady=(10, 10))

        # Function to browse and select the destination folder
        def browse_dest_folder():
            selected_folder = filedialog.askdirectory(title="Select Destination Folder")
            if selected_folder:
                dest_folder_display.config(text=selected_folder)  # Update label with selected folder path

        # Browse button for destination folder selection
        browse_dest_folder_button = tk.Button(main_frame, text="Browse Destination Folder", command=browse_dest_folder, bg="#2c3e50", fg="white")
        browse_dest_folder_button.pack(pady=(5, 10))

        # Run button to execute the copy function
        run_button = tk.Button(main_frame, text="Run", font=("Helvetica", 12), bg="#2c3e50", fg="white",
                               command=lambda: run_copy(source_entry.get(), from_entry.get(), to_entry.get(), dest_folder_display.cget("text")),
                               highlightthickness=0, borderwidth=0)
        run_button.pack(pady=20)


    elif action == "Delete Specific Files":

        unwanted_file_entry = tk.Entry(main_frame, width=50, bd=1, relief="solid", fg="black")
        unwanted_file_entry.pack(pady=(0, 10))

        # Frame for Browse Files and Browse Folders buttons
        browse_frame = tk.Frame(main_frame, bg="#ffffff")
        browse_frame.pack(pady=(0, 10))

        browse_file_button = tk.Button(browse_frame, text="Browse Files", command=lambda: browse_file(unwanted_file_entry), bg="#2c3e50", fg="white")
        browse_file_button.pack(side=tk.LEFT, padx=(0, 10))

        browse_folder_button = tk.Button(browse_frame, text="Browse Folders", command=lambda: browse_folder(unwanted_file_entry), bg="#2c3e50", fg="white")
        browse_folder_button.pack(side=tk.LEFT)

        # Destination Range
        dest_label = tk.Label(main_frame, text="Destination Range (From Number To Number):", font=("Helvetica", 12), bg="#ffffff", fg="black")
        dest_label.pack(pady=(10, 0))

        from_frame = tk.Frame(main_frame, bg="#ffffff")
        from_frame.pack(pady=(10, 0))

        tk.Label(from_frame, text="From:", font=("Helvetica", 12), bg="#ffffff", fg="black").pack(side=tk.LEFT, padx=(0, 5))
        from_entry = tk.Entry(from_frame, width=5, bd=1, relief="solid", fg="black")
        from_entry.pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(from_frame, text="To:", font=("Helvetica", 12), bg="#ffffff", fg="black").pack(side=tk.LEFT, padx=(0, 5))
        to_entry = tk.Entry(from_frame, width=5, bd=1, relief="solid", fg="black")
        to_entry.pack(side=tk.LEFT)

        # Run button
        run_button = tk.Button(main_frame, text="Run", font=("Helvetica", 12), bg="#2c3e50", fg="white",
                               command=lambda: delete_files(unwanted_file_entry.get(), from_entry.get(), to_entry.get()), highlightthickness=0, borderwidth=0)
        run_button.pack(pady=20)
    elif action == "Delete Files by Type":


        # Folder selection instructions
        folder_instruction_label = tk.Label(main_frame, text="Select the folder where the deletion should happen \n (leave it blank to select full d drive)", font=("Helvetica", 12), bg="#ffffff", fg="black")
        folder_instruction_label.pack(pady=(10, 0))

        # Create an entry field for the folder path
        folder_path_entry = tk.Entry(main_frame, width=50, bd=1, relief="solid", fg="black")
        folder_path_entry.pack(pady=(10, 0))

        # Function to browse and select a folder
        def browse_folder_for_deletion():
            selected_folder = filedialog.askdirectory(title="Select Folder")  # Open folder dialog
            if selected_folder:
                folder_path_entry.delete(0, tk.END)  # Clear any existing text
                folder_path_entry.insert(0, selected_folder)  # Insert the selected folder path

        # Browse button for selecting folder
        browse_folder_button = tk.Button(main_frame, text="Browse Folder", command=browse_folder_for_deletion, bg="#2c3e50", fg="white")
        browse_folder_button.pack(pady=(5, 10))

        # Instruction text above file type selection
        instruction_label = tk.Label(main_frame, text="Select the type of file you want to delete", font=("Helvetica", 12), bg="#ffffff", fg="black")
        instruction_label.pack(pady=(10, 0))

        # Create a dropdown for selecting file extensions
        file_type_var = tk.StringVar(main_frame)
        file_types = ["png", "jpg", "txt", "mp4", "pdf", "docx", "Other"]
        file_type_var.set(file_types[0])  # default to "png"

        file_extension_dropdown = tk.OptionMenu(main_frame, file_type_var, *file_types)
        file_extension_dropdown.pack(pady=(10, 0))

        # If "Other" is selected, show a text box to enter the extension
        other_entry = tk.Entry(main_frame, width=20,bd=1, relief="solid", fg="black")

        def show_other_entry(*args):
            if file_type_var.get() == "Other":
                other_entry.pack(after=file_extension_dropdown, pady=(10, 0))  # Pack directly after dropdown
            else:
                other_entry.pack_forget()

        # Bind the function to show/hide the entry box when "Other" is selected
        file_type_var.trace("w", show_other_entry)


        # From and To range inputs
        dest_label = tk.Label(main_frame, text="Destination Range (From Number To Number):", font=("Helvetica", 12), bg="#ffffff", fg="black")
        dest_label.pack(pady=(10, 0))

        from_frame = tk.Frame(main_frame, bg="#ffffff")
        from_frame.pack(pady=(10, 0))

        tk.Label(from_frame, text="From:", font=("Helvetica", 12), bg="#ffffff", fg="black").pack(side=tk.LEFT, padx=(0, 5))
        from_entry = tk.Entry(from_frame, width=5, bd=1, relief="solid", fg="black")
        from_entry.pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(from_frame, text="To:", font=("Helvetica", 12), bg="#ffffff", fg="black").pack(side=tk.LEFT, padx=(0, 5))
        to_entry = tk.Entry(from_frame, width=5, bd=1, relief="solid", fg="black")
        to_entry.pack(side=tk.LEFT)

        # Run button to trigger the delete_file_type function
        run_button = tk.Button(main_frame, text="Run", font=("Helvetica", 12), bg="#2c3e50", fg="white",
                               command=lambda: delete_file_type(folder_path_entry.get(),  # Folder path
                                                                other_entry.get() if file_type_var.get() == "Other" else file_type_var.get(),  # Get file extension
                                                                from_entry.get(), to_entry.get()),  # Get start and end range
                               highlightthickness=0, borderwidth=0)
        run_button.pack(pady=20)
    elif action == "Backup Files":
        # Folder selection instructions
        folder_instruction_label = tk.Label(main_frame, text="Select the parent folder to backup files from \n (leave it blank to select from d drive) ", font=("Helvetica", 12), bg="#ffffff", fg="black")
        folder_instruction_label.pack(pady=(10, 0))

        # Create an entry field for the parent folder path
        folder_path_entry = tk.Entry(main_frame, width=50,bd=1, relief="solid", fg="black")
        folder_path_entry.pack(pady=(10, 0))

        # Function to browse and select a parent folder
        def browse_folder_for_backup():
            selected_folder = filedialog.askdirectory(title="Select Folder")  # Open folder dialog
            if selected_folder:
                folder_path_entry.delete(0, tk.END)  # Clear any existing text
                folder_path_entry.insert(0, selected_folder)  # Insert the selected folder path

        # Browse button for selecting the folder
        browse_folder_button = tk.Button(main_frame, text="Browse Folder", command=browse_folder_for_backup, bg="#2c3e50", fg="white")
        browse_folder_button.pack(pady=(5, 10))

        # Instruction text above file type selection
        instruction_label = tk.Label(main_frame, text="Select the type of file you want to backup", font=("Helvetica", 12), bg="#ffffff", fg="black")
        instruction_label.pack(pady=(10, 0))

        # Create a dropdown for selecting file extensions
        file_type_var = tk.StringVar(main_frame)
        file_types = ["png", "jpg", "txt", "mp4", "pdf", "docx", "Other"]
        file_type_var.set(file_types[0])  # default to "png"

        file_extension_dropdown = tk.OptionMenu(main_frame, file_type_var, *file_types)
        file_extension_dropdown.pack(pady=(10, 0))

        # If "Other" is selected, show a text box to enter the extension
        other_entry = tk.Entry(main_frame, width=20, bd=1, relief="solid", fg="black")

        def show_other_entry(*args):
            if file_type_var.get() == "Other":
                other_entry.pack(after=file_extension_dropdown, pady=(10, 0))  # Pack directly after dropdown
            else:
                other_entry.pack_forget()

        # Bind the function to show/hide the entry box when "Other" is selected
        file_type_var.trace("w", show_other_entry)

        # Destination folder selection instructions
        dest_folder_label = tk.Label(main_frame, text="Select the destination folder to backup files", font=("Helvetica", 12), bg="#ffffff", fg="black")
        dest_folder_label.pack(pady=(10, 0))

        # Create an entry field for the destination folder path
        dest_folder_entry = tk.Entry(main_frame, width=50, bd=1, relief="solid", fg="black")
        dest_folder_entry.pack(pady=(10, 0))

        # Function to browse and select a destination folder
        def browse_destination_folder():
            selected_folder = filedialog.askdirectory(title="Select Destination Folder")  # Open folder dialog
            if selected_folder:
                dest_folder_entry.delete(0, tk.END)  # Clear any existing text
                dest_folder_entry.insert(0, selected_folder)  # Insert the selected folder path

        # Browse button for selecting destination folder
        browse_dest_folder_button = tk.Button(main_frame, text="Browse Destination Folder", command=browse_destination_folder, bg="#2c3e50", fg="white")
        browse_dest_folder_button.pack(pady=(5, 10))

        # Destination range input (From and To)
        dest_range_label = tk.Label(main_frame, text="Source Computer Range:", font=("Helvetica", 12), bg="#ffffff", fg="black")
        dest_range_label.pack(pady=(10, 0))

        from_frame = tk.Frame(main_frame, bg="#ffffff")
        from_frame.pack(pady=(10, 0))

        tk.Label(from_frame, text="From:", font=("Helvetica", 12), bg="#ffffff", fg="black").pack(side=tk.LEFT, padx=(0, 5))
        from_entry = tk.Entry(from_frame, width=5, bd=1, relief="solid", fg="black")
        from_entry.pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(from_frame, text="To:", font=("Helvetica", 12), bg="#ffffff", fg="black").pack(side=tk.LEFT, padx=(0, 5))
        to_entry = tk.Entry(from_frame, width=5, bd=1, relief="solid", fg="black")
        to_entry.pack(side=tk.LEFT)

        # Run button to trigger the backup_files function
        run_button = tk.Button(main_frame, text="Run", font=("Helvetica", 12), bg="#2c3e50", fg="white",
                               command=lambda: backup_files(  # Call the backup_files function
                                   folder_path_entry.get(),  # Folder path
                                   other_entry.get() if file_type_var.get() == "Other" else file_type_var.get(),  # File extension
                                   dest_folder_entry.get(),  # Destination path
                                   from_entry.get(),  # Start range
                                   to_entry.get()  # End range
                               ),
                               highlightthickness=0, borderwidth=0)
        run_button.pack(pady=20)



    # Go Back text
    go_back_text = tk.Label(main_frame, text="Go Back", fg="black", bg="#ffffff", cursor="hand2")
    go_back_text.bind("<Button-1>", lambda e: go_back())
    go_back_text.pack(pady=10)

# Initialize the main application window
root = tk.Tk()
root.title("NPS LabSync")
root.geometry("800x680")
root.configure(bg="#ffffff")

# Main frame
main_frame = tk.Frame(root, bg="#ffffff")
main_frame.pack(fill="both", expand=True)

# Actions for the main menu
actions = [
    ("Copy Files", "Copy Files"),
    ("Delete Specific Files", "Delete Specific Files"),
    ("Delete Files by Type", "Delete Files by Type"),
    ("Backup Files", "Backup Files")
]
image_paths = [
    fr"file_copy.png",            # Image for "Copy Files"
    fr"target.png",               # Image for "Delete Specific Files"
    fr"delete_files.png",         # Image for "Delete Files by Type"
    fr"backup.png"                # Image for "Backup Files"
]

# Create main menu with options
tk.Label(main_frame, text="Select Your Task", font=("Helvetica", 20,"bold"), bg="#ffffff", fg="black").pack(pady=20)
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
        icon = PhotoImage(master=root, file=icon_path) 
        
        # Store image reference to prevent garbage collection
        image_references.append(icon)
        #print("pil_image = ", pil_image)
    except Exception as e:
        print(f"Error loading image {icon_path}: {e}")
        continue
    
        
    # Create a button without the border around it
    button = tk.Button(
    buttons_frame,
    image=icon,
    text=text,
    font=("Helvetica", 12),
    bg="white",
    fg="black",
    compound="top",
    command=lambda a=text: show_screen(a),  # Explicitly bind `text` to `a`
    highlightthickness=0,
    borderwidth=0
    )

    # Place the button side by side in the same row using grid
    button.grid(row=0, column=idx, padx=10, pady=10)

    # Set button size to match the frame size
    button.config(width=frame_width, height=frame_height)

banner_frame = tk.Frame(root, bg="white", bd=2, relief="solid")
banner_frame.pack(fill="x", pady=20)  # `fill="x"` ensures it spans the width

# Load the image for the banner (ensure the file path is correct)
banner_image = PhotoImage(master=root, file="@npsboy_logo.png")  # Replace with your image path

# Create a label for the image inside the banner frame
image_label = tk.Label(banner_frame, image=banner_image, bg="white")
image_label.pack(side="left", padx=(200,10) )  # `side="left"` places it on the left

# Create a label for the text inside the banner frame
text_label = tk.Label(banner_frame, text="Made by @npsboy : Tushar V", font=("Helvetica", 14), fg="black", bg="white")
text_label.pack(side="left", padx=10)


root.iconbitmap(bitmap=rf"C:\Users\Tusha\OneDrive\Documents\LabSync\app_icon.ico")

# Start the application
root.mainloop()