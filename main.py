import logging
import tkinter as tk
from tkinter import ttk, messagebox

from config import APP_TITLE
from logger import setup_logging
from validators import validate_all
from db import (
    init_db,
    insert_student,
    fetch_all_students,
    search_students_by_name,
    delete_student_by_id,
)
from exporter import export_to_csv

setup_logging()
logger = logging.getLogger(__name__)


def register():
    name = name_var.get()
    contact = contact_var.get()
    email = email_var.get()
    rollno = rollno_var.get()
    branch = branch_var.get()

    ok, errors = validate_all(name, contact, email, rollno, branch)
    if not ok:
        messagebox.showwarning("Validation Error", "\n".join(errors))
        return

    success, msg = insert_student(name, contact, email, rollno, branch)
    if success:
        messagebox.showinfo("Success", msg)
        Reset()
    else:
        messagebox.showerror("Error", msg)


def Reset():
    tree.delete(*tree.get_children())
    DisplayData()
    search_var.set("")
    name_var.set("")
    contact_var.set("")
    email_var.set("")
    rollno_var.set("")
    branch_var.set("")


def Delete():
    if not tree.selection():
        messagebox.showwarning("Warning", "Select data to delete")
        return

    confirm = messagebox.askquestion(
        "Confirm", "Are you sure you want to delete this record?", icon="warning"
    )
    if confirm != "yes":
        return

    cur_item = tree.focus()
    values = tree.item(cur_item)["values"]
    stu_id = values[0]

    success, msg = delete_student_by_id(stu_id)
    if success:
        tree.delete(cur_item)
        logger.info(msg)
    else:
        messagebox.showerror("Error", msg)


def SearchRecord():
    if search_var.get().strip() == "":
        return
    tree.delete(*tree.get_children())
    for row in search_students_by_name(search_var.get().strip()):
        tree.insert("", "end", values=tuple(row))


def DisplayData():
    tree.delete(*tree.get_children())
    for row in fetch_all_students():
        tree.insert("", "end", values=tuple(row))


def Export():
    rows = fetch_all_students()
    path = export_to_csv(rows)
    if path:
        messagebox.showinfo("Exported", f"Saved to {path}")
    else:
        messagebox.showwarning("Empty", "No records to export")


def DisplayForm():
    global tree, name_var, contact_var, email_var, rollno_var, branch_var, search_var

    screen = tk.Tk()
    screen.geometry("950x450")
    screen.title(APP_TITLE)

    name_var = tk.StringVar()
    contact_var = tk.StringVar()
    email_var = tk.StringVar()
    rollno_var = tk.StringVar()
    branch_var = tk.StringVar()
    search_var = tk.StringVar()

    top = tk.Frame(screen, width=600, bd=1, relief=tk.SOLID)
    top.pack(side=tk.TOP, fill=tk.X)

    left_form = tk.Frame(screen, width=350)
    left_form.pack(side=tk.LEFT, fill=tk.Y)

    left_search = tk.Frame(screen, width=500, bg="gray")
    left_search.pack(side=tk.LEFT, fill=tk.Y)

    mid = tk.Frame(screen, width=600)
    mid.pack(side=tk.RIGHT)

    tk.Label(
        top,
        text=APP_TITLE,
        font=("Times New Roman", 18),
        width=600,
        bg="#1C2833",
        fg="white",
    ).pack(fill=tk.X)

    for label, var in [
        ("Name  ", name_var),
        ("Contact ", contact_var),
        ("Email ", email_var),
        ("Rollno ", rollno_var),
        ("Branch ", branch_var),
    ]:
        tk.Label(left_form, text=label, font=("Arial", 12)).pack(side=tk.TOP)
        tk.Entry(
            left_form, font=("Arial", 10, "bold"), textvariable=var
        ).pack(side=tk.TOP, padx=10, fill=tk.X)

    tk.Button(
        left_form,
        text="Submit",
        font=("Arial", 10, "bold"),
        command=register,
    ).pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)

    tk.Label(
        left_search, text="Enter name to Search", font=("verdana", 10), bg="gray"
    ).pack()
    tk.Entry(
        left_search, textvariable=search_var, font=("verdana", 15), width=10
    ).pack(side=tk.TOP, padx=10, fill=tk.X)

    for text, cmd in [
        ("Search", SearchRecord),
        ("View All", DisplayData),
        ("Reset", Reset),
        ("Delete", Delete),
        ("Export CSV", Export),
    ]:
        tk.Button(left_search, text=text, command=cmd).pack(
            side=tk.TOP, padx=10, pady=10, fill=tk.X
        )

    scrollbar_x = tk.Scrollbar(mid, orient=tk.HORIZONTAL)
    scrollbar_y = tk.Scrollbar(mid, orient=tk.VERTICAL)
    tree = ttk.Treeview(
        mid,
        columns=("Student Id", "Name", "Contact", "Email", "Rollno", "Branch"),
        selectmode="extended",
        height=20,
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set,
    )
    scrollbar_y.config(command=tree.yview)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar_x.config(command=tree.xview)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

    for col in ("Student Id", "Name", "Contact", "Email", "Rollno", "Branch"):
        tree.heading(col, text=col, anchor=tk.W)

    tree.column("#0", stretch=tk.NO, minwidth=0, width=0)
    tree.column("#1", stretch=tk.NO, minwidth=0, width=90)
    tree.column("#2", stretch=tk.NO, minwidth=0, width=150)
    tree.column("#3", stretch=tk.NO, minwidth=0, width=110)
    tree.column("#4", stretch=tk.NO, minwidth=0, width=180)
    tree.column("#5", stretch=tk.NO, minwidth=0, width=90)
    tree.column("#6", stretch=tk.NO, minwidth=0, width=90)
    tree.pack()

    DisplayData()
    return screen


def main():
    init_db()
    app = DisplayForm()
    app.mainloop()


if __name__ == "__main__":
    main()