#Changes made

#Class Structure: Introduced a class (NotesApp) to encapsulate the functionality, promoting better organization and reusability.
#Functions: Separated various functionalities into functions to improve code modularity and readability.
#Global Variables: Reduced the use of global variables by utilizing class attributes.
#Consistent Naming: Ensured consistent naming conventions for variables and functions within the class.
#Button Commands: Used instance methods as command functions for buttons, improving clarity and maintaining encapsulation


import os
from tkinter import *
from tkinter.filedialog import asksaveasfilename
from tkinter import ttk
import tkinter.scrolledtext as tkscroll

class NotesApp:
    def __init__(self, root):
        self.root = root
        root.geometry("1000x600")
        root.title("Notes")
        self.action = None
        self.create_gui()

    def create_gui(self):
        # Frames
        self.main_frame = Frame(self.root, bg='#C2C0BE')  # Main frame for note creation
        self.show_frame = Frame(self.root, bg='#C2C0BE')  # Frame for displaying note titles
        self.display_frame = Frame(self.root, bg='#C2C0BE')  # Frame for showing note content

        # Widgets for note creation
        self.title_label = Label(self.main_frame, text="Title  :  ", font=('Calibri', 20), bg='#BEB4AA', relief=RAISED)
        self.title_var = StringVar()
        self.title_entry = Entry(self.main_frame, textvariable=self.title_var, font=('Calibri', 20), relief=RAISED)
        self.body = Text(self.main_frame, font=('Calibri', 16), relief=RAISED)

        # Buttons for note creation
        Button(self.main_frame, text='Save', font=('Calibri', 20), command=self.save).place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.1)
        Button(self.main_frame, text='Show All', font=('Calibri', 20), command=self.show_all).place(relx=0.7, rely=0.8, relwidth=0.2, relheight=0.1)

        # Styling for Treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("mystyle.Treeview", font=('Calibri', 14), rowheight=50)
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 18, 'bold'))

        # Treeview for displaying note titles
        self.tree = ttk.Treeview(self.show_frame, selectmode='browse', style="mystyle.Treeview", show=['headings'])
        self.tree['columns'] = ('0')
        self.tree.heading("0", text="Title")
        self.tree.column("0", minwidth=100, width=275)
        self.tree.bind("<Double-1>", self.on_double_click)

        # Buttons for note deletion
        Button(self.main_frame, text='Delete', font=('Calibri', 20), command=self.delete_note).place(relx=0.1, rely=0.8, relwidth=0.2, relheight=0.1)

        # ScrolledText for displaying note content
        self.dis_label = tkscroll.ScrolledText(self.display_frame, font=('Calibri', 20), bg='#ffffff', relief=GROOVE)

        # Buttons for navigating between frames
        Button(self.show_frame, text='Back', font=('Calibri', 20), command=lambda: self.back('show')).place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)
        Button(self.display_frame, text='Back', font=('Calibri', 20), command=lambda: self.back('display')).place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)

        # Placing widgets and frames
        self.place_widgets()
        
    def place_widgets(self):
        # Note Creation Widgets
        self.title_label.place(relx=0.1, rely=0.05, relwidth=0.1, relheight=0.08)
        self.title_entry.place(relx=0.2, rely=0.05, relwidth=0.6, relheight=0.08)
        self.body.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.5)

        # Note Display Widgets
        self.dis_label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.7)

        # Placing frames
        self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.main_frame.lift()
        self.show_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.show_frame.lower()
        self.display_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.display_frame.lower()

        # Treeview
        self.tree.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.7)

    def back(self, frame):
        if frame == 'show':
            self.show_frame.lower()
        if frame == 'display':
            self.display_frame.lower()
        self.title_var.set('')
        self.body.delete(1.0, END)

    def save(self):
        title_text = self.title_var.get()
        content = self.body.get(1.0, END)
        save_file = asksaveasfilename(initialfile=f'{title_text}.txt', defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        try:
            with open(save_file, "w+") as file:
                file.writelines(content)
        except Exception as e:
            print(f"Error saving file: {e}")

    def show_all(self):
        self.tree.delete(*self.tree.get_children())
        files = [file[:len(file) - 4] for file in os.listdir() if '.txt' in file]
        for file in files:
            self.tree.insert('', END, values=(file))
        self.show_frame.lift()

    def on_double_click(self, event):
        title = self.tree.set(self.tree.identify_row(event.y))['0']
        files = [file for file in os.listdir() if title in file]
        for file in files:
            self.display(file)

    def display(self, file):
        with open(file, 'r') as f:
            content = f.read()
        self.dis_label.insert(1.0, content)
        self.display_frame.lift()

    def delete_note(self):
        file = self.tree.set(self.tree.selection())['0']
        os.remove(f'{file}.txt')
        self.show_all()

if __name__ == "__main__":
    root = Tk()
    app = NotesApp(root)
    root.mainloop()
