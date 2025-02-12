import random
import csv
import os
from tkinter import *
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox

# Character sets
upper_case_alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lower_case_alphabets = "abcdefghijklmnopqrstuvwxyz"
characters = "!@$*%.<>/"
numbers = "1234567890"

def generate():
    password_field.delete(0, END)
    try:
        length = int(entry_length.get())
        if length < 4:
            messagebox.showerror("Error", "Password length must be at least 4 characters")
            return
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number")
        return
    
    first_letter = "#"
    password = [first_letter]
    for _ in range(length - 1):
        password.append(random.choice(upper_case_alphabets + lower_case_alphabets + characters + numbers))
    result_string = "".join(password)
    password_field.insert(0, result_string)
    
    # Save to CSV in Documents folder
    documents_path = os.path.join(os.path.expanduser("~"), "Documents")
    file_path = os.path.join(documents_path, "Generated_Passwords.csv")
    try:
        with open(file_path, "a+", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([result_string, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving: {e}")
    

def show_previous_passwords():
    documents_path = os.path.join(os.path.expanduser("~"), "Documents")
    file_path = os.path.join(documents_path, "Generated_Passwords.csv")
    
    if not os.path.exists(file_path):
        messagebox.showinfo("Info", "No passwords have been generated yet.")
        return
    
    history_window = Toplevel(win)
    history_window.title("Previous Passwords")
    history_window.geometry("500x300")
    history_window.configure(bg="#121212")  # Dark theme background
    history_window.iconbitmap("icon.ico")
    
    frame = Frame(history_window, bg="#121212")
    frame.pack(fill=BOTH, expand=True)
    
    tree = ttk.Treeview(frame, columns=("Password", "Date & Time"), show="headings")
    tree.heading("Password", text="Password")
    tree.heading("Date & Time", text="Date & Time")
    tree.column("Password", width=200)
    tree.column("Date & Time", width=250)
    
    style = ttk.Style()
    style.configure("Treeview", background="#1E1E1E", foreground="white", fieldbackground="#1E1E1E")
    style.configure("Treeview.Heading", background="#333333", foreground="white")
    
    scrollbar = Scrollbar(frame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    tree.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    def copy_selected():
        selected_item = tree.selection()
        if selected_item:
            values = tree.item(selected_item[0], "values")
            history_window.clipboard_clear()
            history_window.clipboard_append(values[0])
            history_window.update()
    
    def cut_selected():
        selected_item = tree.selection()
        if selected_item:
            values = tree.item(selected_item[0], "values")
            history_window.clipboard_clear()
            history_window.clipboard_append(values[0])
            tree.delete(selected_item[0])
            history_window.update()
    
    context_menu = Menu(history_window, tearoff=0, bg="#333333", fg="white")
    context_menu.add_command(label="Copy", command=copy_selected)
    context_menu.add_command(label="Cut", command=cut_selected)
    
    def show_tree_context_menu(event):
        context_menu.post(event.x_root, event.y_root)
    
    tree.bind("<Button-3>", show_tree_context_menu)
    
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            tree.insert("", END, values=row)

def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)

def copy_password():
    win.clipboard_clear()
    win.clipboard_append(password_field.get())
    win.update()

def cut_password():
    win.clipboard_clear()
    win.clipboard_append(password_field.get())
    password_field.delete(0, END)
    win.update()

# UI Setup
win = Tk()
win.title("RyuX Passgen")
win.geometry("480x454")
win.iconbitmap("icon.ico")

# Set background image
bg_image = PhotoImage(file="background.png")
bg_label = Label(win, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Title background bar
title_frame = Frame(win, bg="#000000", height=60)
title_frame.pack(fill=X)
Label(title_frame, text="RyuX Passgen", fg="white", bg="#000000", font=("Arial", 16, "bold"), anchor="w").pack(pady=(10, 5), padx=20, fill=X)
Frame(title_frame, height=2, width=120, bg="white").pack(padx=20, pady=(0, 10), anchor="w")

# Content Labels
content_frame = Frame(win, bg="#000000")
content_frame.pack(fill=X, padx=20, pady=15)
Label(content_frame, text="Enter the no. of characters.", fg="white", bg="#000000", font=("Arial", 12), anchor="w").pack(fill=X)

# Input Fields
entry_length = Entry(win, font=("Arial", 14), width=35, justify=LEFT, bg="#F0F3FF", relief=FLAT)
entry_length.pack(pady=10, padx=20, anchor="w")
password_field = Entry(win, font=("Arial", 14), width=35, justify=LEFT, bg="#F0F3FF", relief=FLAT)
password_field.pack(pady=10, padx=20, anchor="w")
password_field.bind("<Button-3>", show_context_menu)

# Context Menu
context_menu = Menu(win, tearoff=0)
context_menu.add_command(label="Copy", command=copy_password)
context_menu.add_command(label="Cut", command=cut_password)

# Generate Button
button = Button(win, text="Generate", command=generate, bg="#007BFF", fg="white", font=("Arial", 14, "bold"), relief=FLAT, width=20, height=2, bd=0, highlightthickness=0)
button.pack(pady=10, padx=20, anchor="w")

# Show Previous Passwords Button
view_button = Button(win, text="Show Previous Passwords", command=show_previous_passwords, bg="#28A745", fg="white", font=("Arial", 14, "bold"), relief=FLAT, width=25, height=2, bd=0, highlightthickness=0)
view_button.pack(pady=10, padx=20, anchor="w")

win.mainloop()
