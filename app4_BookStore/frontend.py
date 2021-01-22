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
import backend

global cur_sel
cur_sel = tuple()


# Clear Text Entries
def clear_entries():
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)


# wrapper functions
def refresh_list():
    list1.delete(0, END)
    for book in backend.view():
        list1.insert(END, book)


def search_command():
    list1.delete(0, END)
    for book in backend.search(title_text.get(), author_text.get(), year_text.get(), isbn_text.get()):
        list1.insert(END, book)


def add_command():
    list1.delete(0, END)
    backend.insert(title_text.get(), author_text.get(), year_text.get(), isbn_text.get())
    refresh_list()


def update_command():
    if cur_sel:
        backend.update(cur_sel[0], title_text.get(), author_text.get(), year_text.get(),
                       isbn_text.get())
        refresh_list()


def delete_command():
    if cur_sel:
        backend.delete(cur_sel[0])
        refresh_list()
        clear_entries()


def select_command(event):
    if list1.curselection():
        global cur_sel
        cur_sel = list1.get(list1.curselection())
        clear_entries()
        e1.insert(END, cur_sel[1])
        e2.insert(END, cur_sel[2])
        e3.insert(END, cur_sel[3])
        e4.insert(END, cur_sel[4])


window = Tk()
window.wm_title("Book Store")

# Labels
l1 = Label(window, text="Title")
l1.grid(row=0, column=0)

l2 = Label(window, text="Author")
l2.grid(row=0, column=2)

l3 = Label(window, text="Year")
l3.grid(row=1, column=0)

l4 = Label(window, text="ISBN")
l4.grid(row=1, column=2)

# Text Entries
title_text = StringVar()
e1 = Entry(window, textvariable=title_text)
e1.grid(row=0, column=1)

author_text = StringVar()
e2 = Entry(window, textvariable=author_text)
e2.grid(row=0, column=3)

year_text = StringVar()
e3 = Entry(window, textvariable=year_text)
e3.grid(row=1, column=1)

isbn_text = StringVar()
e4 = Entry(window, textvariable=isbn_text)
e4.grid(row=1, column=3)

# Listbox
list1 = Listbox(window, width=30)
list1.grid(row=2, column=0, rowspan=6, columnspan=2)
list1.bind("<<ListboxSelect>>", select_command)

# Scrollbar
sb1 = Scrollbar(window)
sb1.grid(row=2, column=2, rowspan=6, ipady=70)

# Attach scrollbar to listbox
list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

# Buttons
b1 = Button(window, text="View All", width=12, command=refresh_list)
b1.grid(row=2, column=3)

b2 = Button(window, text="Search Entry", width=12, command=search_command)
b2.grid(row=3, column=3)

b3 = Button(window, text="Add Entry", width=12, command=add_command)
b3.grid(row=4, column=3)

b4 = Button(window, text="Update Selected", width=12, command=update_command)
b4.grid(row=5, column=3)

b5 = Button(window, text="Delete Selected", width=12, command=delete_command)
b5.grid(row=6, column=3)

b6 = Button(window, text="Close", width=12, command=window.destroy)
b6.grid(row=7, column=3)

window.mainloop()
