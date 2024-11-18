# What is it?
LabSync is a program that helps you manage files on your school's / workplace's / organisation's computer network
# What can it do?
It can:
- copy files from 1 source to all computers
- Delete a specific file from all computers
- Delete a specific file type from all computers (eg: all PNG files)
- Backup specific file types (eg: all PNG files) from all computers (or from subfolders) into 1 computer
# How to use it?
1. Download the repo as a Zip file
2. Unzip the file
3. Double-click on the 'install_requirements.bat' This will run a batch script that will install all necessary Python libraries for the program mentioned in 'requirements.txt'
4. Open the 'LabSync.pyw' file in a text editor
5. Replace line 16
    `hardcode_path = lambda i: fr"your_computer_{i}\d"`
     with the actual path to **any one** computer's d-drive <br>
     For example, if the path to your 21st computer's d-drive is `\\your_company_21\d` <br>
     put this code in line 16: `hardcode_path = lambda i: fr"\\your_company_21\d"`
6. In line 16, replace the computer number with `{i}` <br>
      In this example replace `hardcode_path = lambda i: fr"\\your_company_21\d"` <br>
      with `hardcode_path = lambda i: fr"\\your_company_{i}\d"`
7. Save the file
8. To run the program just double-click on the 'LabSync.pyw' file. As it is a 'pyw' file, it will run automatically without a console or text editor.
# How does it work?
- The UI is made using Python's Tkinter library
- Users can browse files from their computer, and choose to copy, delete or backup that file from all computers
- The program recognises that the file browsed is that of the user's computer but uses that path to find the same file on all other computers.
- It then uses Python's OS or Shutil libraries to perform operations on that file
# Limitations:
- It can only operate on files in the d-drive of all computers
- All computers need to have a uniform naming system. eg: computer_1, computer_2 ... computer_21 .........
- The Tkinter UI is mainly designed for Windows. UI will face some glitches for Mac users
