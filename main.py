import PyPDF2
import os
import tkinter as tk
import subprocess
import pyperclip


class FileLabels:
    def __init__(self):
        self.all_widgets = []

    def create_name_button(self, filename):
        new_button = tk.Button(text=filename, command=lambda: openfile(filename))
        new_button.grid(row=6 + found_files.index(filename), column=1, columnspan=1)
        self.all_widgets.append(new_button)

    def create_copy_buttons(self, filename):
        copy_number_button = tk.Button(text="Copy #", command=lambda: copy_number(filename))
        copy_number_button.grid(row=6 + found_files.index(filename), column=2)
        copy_name_button = tk.Button(text="Copy Name", command=lambda: copy_name(filename))
        copy_name_button.grid(row=6 + found_files.index(filename), column=3)
        self.all_widgets.append(copy_number_button)
        self.all_widgets.append(copy_name_button)


def openfile(filename):
    path = f'{directory}\{filename}'
    subprocess.Popen([path], shell=True)


def get_folder():
    global folder_entry
    global start_window
    start_window = tk.Tk()
    start_window.title("BSP PDF Searcher")
    folder_label = tk.Label(text="1. Copy paste all PDF's into a folder on your computer.\n"
                                 "2. Copy paste the folder location here and click OK.\n"
                                 "Get some coffee. This may take a few minutes.")
    folder_label.grid(row=1, column=1)
    folder_entry = tk.Entry()
    folder_entry.grid(row=1, column=2)
    folder_button = tk.Button(text="OK", command=lambda: extract_pdf(widgets))
    folder_button.grid(row=2, column=2)
    widgets = []
    start_window.mainloop()


def extract_pdf(widgets):
    for i in widgets:
        i.destroy()
    global directory
    global search_entry
    global drawing_contents
    global files_in_folder
    global damaged
    try:
        directory = folder_entry.get()
    except _tkinter.TclError:
        pass

    # create dictionary of contents
    damaged = []
    files_in_folder = 0
    drawing_contents = {}

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        with open(f, "rb") as pdf_file:
            try:
                read_pdf = PyPDF2.PdfFileReader(pdf_file)
            except:
                pass
            else:
                files_in_folder += 1
            number_of_pages = read_pdf.getNumPages()
            page = read_pdf.pages[0]
            try:
                page_content = page.extractText().lower()
            except IndexError:
                damaged.append(filename)
            else:
                drawing_contents[filename] = page_content
    display_results()


def display_results():
    global search_entry
    global search_button
    try:
        start_window.destroy()
    except _tkinter.TclError:
        pass

    results_window = tk.Tk()
    results_window.title("BSP PDF Searcher")
    dir_label = tk.Label(text=f"Searching in {directory}\n{files_in_folder} files, {len(damaged)} damaged")
    dir_label.grid(row=1, column=1)
    search_label = tk.Label(text="Enter words to search: ")
    search_label.grid(row=3, column=1)
    search_entry = tk.Entry()
    search_entry.grid(row=3, column=2)
    search_button = tk.Button(text="Search", command=lambda: search(widgets))
    search_button.grid(row=3, column=3)
    try:
        x = found_files_label
    except NameError:
        found_files_label = tk.Label()
        found_count_label = tk.Label()
        widgets = []


def search(widgets):
    global found_files_label
    global found_count_label
    global found_files

    for i in file_labels.all_widgets:
        i.destroy()

    try:
        found_count_label.destroy()
    except NameError:
        pass

    key_words_list = list(search_entry.get().split(" "))
    key_words_list = [i.lower() for i in key_words_list]
    for i in widgets:
        i.destroy()
    found_count = 0
    found_files = []
    for filename, contents in drawing_contents.items():
        if all(i in contents for i in key_words_list):
            found_files.append(filename)
            found_count += 1

    for i in found_files:
        file_labels.create_name_button(i)
        file_labels.create_name_button(i)
        file_labels.create_copy_buttons(i)

    found_count_label = tk.Label(text=f"{found_count} results:")
    found_count_label.grid(row=4, column=1, columnspan=1)


def copy_number(filename):
    pyperclip.copy(filename[:24])


def copy_name(filename):
    pyperclip.copy(filename[25:len(filename) - 4])


file_labels = FileLabels()
get_folder()