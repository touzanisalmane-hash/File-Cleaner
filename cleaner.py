import os
from tkinter import Tk, Label, Button, Text, Scrollbar
from tkinter import filedialog
from tkinter import messagebox

empty_files_found = []


def scan_folder():
    folder_path = filedialog.askdirectory(title="Choose a folder to scan")

    if folder_path == "":
        return

    empty_files_found.clear()
    result_box.delete("1.0", "end")
    result_box.insert("end", "Scanning folder: " + folder_path + "\n\n")

    for current_folder, subfolders, files in os.walk(folder_path):
        for file_name in files:
            full_path = os.path.join(current_folder, file_name)

            try:
                file_size = os.path.getsize(full_path)

                if file_size == 0:
                    empty_files_found.append(full_path)
                    result_box.insert("end", full_path + "\n")

            except Exception as error:
                result_box.insert("end", "Could not check file: " + full_path + "\n")
                print("Error checking file:", error)

    total = len(empty_files_found)
    result_box.insert("end", "\nTotal empty files found: " + str(total) + "\n")


def delete_empty_files():
    if len(empty_files_found) == 0:
        messagebox.showinfo("Nothing to delete", "No empty files found. Please scan a folder first.")
        return

    question = "Are you sure you want to delete " + str(len(empty_files_found)) + " empty file(s)?"
    answer = messagebox.askyesno("Confirm delete", question)

    if answer == False:
        return

    deleted_count = 0

    for file_path in empty_files_found:
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                deleted_count = deleted_count + 1
        except Exception as error:
            result_box.insert("end", "Could not delete: " + file_path + "\n")
            print("Error deleting file:", error)

    result_box.insert("end", "\nDeleted " + str(deleted_count) + " empty file(s).\n")
    messagebox.showinfo("Done", "Deleted " + str(deleted_count) + " empty file(s).")

    empty_files_found.clear()


window = Tk()
window.title("Cleaner")
window.geometry("500x400")

title_label = Label(window, text="Cleaner", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

scan_button = Button(window, text="Scan", width=20, command=scan_folder)
scan_button.pack(pady=5)

delete_button = Button(window, text="Delete Empty Files", width=20, command=delete_empty_files)
delete_button.pack(pady=5)

scrollbar = Scrollbar(window)
scrollbar.pack(side="right", fill="y")

result_box = Text(window, height=15, width=60, yscrollcommand=scrollbar.set)
result_box.pack(pady=10)

scrollbar.config(command=result_box.yview)

window.mainloop()