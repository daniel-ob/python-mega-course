"""
Can store following book information:
Title, Author, Year, ISBN

User can:
- View all records
- Search an entry
- Add an entry
- Update selected entry
- Delete selected entry
- Close
"""
from tkinter import *
from backend import Database

database = Database("books.db")


class LibraryGUI:
    def __init__(self, window):
        self.window = window

        self.window.wm_title("Book Store")

        # Labels
        l1 = Label(self.window, text="Title")
        l1.grid(row=0, column=0)

        l2 = Label(self.window, text="Author")
        l2.grid(row=0, column=2)

        l3 = Label(self.window, text="Year")
        l3.grid(row=1, column=0)

        l4 = Label(self.window, text="ISBN")
        l4.grid(row=1, column=2)

        # Text Entries
        self.title_text = StringVar()
        self.e1 = Entry(self.window, textvariable=self.title_text)
        self.e1.grid(row=0, column=1)

        self.author_text = StringVar()
        self.e2 = Entry(self.window, textvariable=self.author_text)
        self.e2.grid(row=0, column=3)

        self.year_text = StringVar()
        self.e3 = Entry(self.window, textvariable=self.year_text)
        self.e3.grid(row=1, column=1)

        self.isbn_text = StringVar()
        self.e4 = Entry(self.window, textvariable=self.isbn_text)
        self.e4.grid(row=1, column=3)

        # Listbox
        self.list1 = Listbox(self.window, width=30)
        self.list1.grid(row=2, column=0, rowspan=6, columnspan=2)
        self.list1.bind("<<ListboxSelect>>", self.select_command)
        self.list1_cur_sel = tuple()

        # Scrollbar
        sb1 = Scrollbar(self.window)
        sb1.grid(row=2, column=2, rowspan=6, ipady=70)

        # Attach scrollbar to listbox
        self.list1.configure(yscrollcommand=sb1.set)
        sb1.configure(command=self.list1.yview)

        # Buttons
        b1 = Button(self.window, text="View All", width=12, command=self.refresh_list)
        b1.grid(row=2, column=3)

        b2 = Button(self.window, text="Search Entry", width=12, command=self.search_command)
        b2.grid(row=3, column=3)

        b3 = Button(self.window, text="Add Entry", width=12, command=self.add_command)
        b3.grid(row=4, column=3)

        b4 = Button(self.window, text="Update Selected", width=12, command=self.update_command)
        b4.grid(row=5, column=3)

        b5 = Button(self.window, text="Delete Selected", width=12, command=self.delete_command)
        b5.grid(row=6, column=3)

        b6 = Button(self.window, text="Close", width=12, command=self.window.destroy)
        b6.grid(row=7, column=3)

    def clear_entries(self):
        self.e1.delete(0, END)
        self.e2.delete(0, END)
        self.e3.delete(0, END)
        self.e4.delete(0, END)

    def refresh_list(self):
        self.list1.delete(0, END)
        for book in database.view():
            self.list1.insert(END, book)

    def search_command(self):
        self.list1.delete(0, END)
        for book in database.search(self.title_text.get(), self.author_text.get(), self.year_text.get(),
                                    self.isbn_text.get()):
            self.list1.insert(END, book)

    def add_command(self):
        self.list1.delete(0, END)
        database.insert(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())
        self.refresh_list()
        self.clear_entries()

    def update_command(self):
        if self.list1_cur_sel:
            database.update(self.list1_cur_sel[0], self.title_text.get(), self.author_text.get(), self.year_text.get(),
                            self.isbn_text.get())
            self.refresh_list()

    def delete_command(self):
        if self.list1_cur_sel:
            database.delete(self.list1_cur_sel[0])
            self.refresh_list()
            self.clear_entries()

    def select_command(self, event):
        if self.list1.curselection():
            self.list1_cur_sel = self.list1.get(self.list1.curselection())
            self.clear_entries()
            self.e1.insert(END, self.list1_cur_sel[1])
            self.e2.insert(END, self.list1_cur_sel[2])
            self.e3.insert(END, self.list1_cur_sel[3])
            self.e4.insert(END, self.list1_cur_sel[4])


root_window = Tk()
library_gui = LibraryGUI(root_window)
root_window.mainloop()
