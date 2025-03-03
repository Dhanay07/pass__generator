import string
import random
import sqlite3
from tkinter import *
from tkinter import messagebox

# Create database table if not exists
with sqlite3.connect("users.db") as db:
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (Username TEXT NOT NULL, Password TEXT NOT NULL);")
    db.commit()

# Function to generate password
def generate_password():
    username = username_entry.get().strip()
    length = length_entry.get().strip()

    if not username:
        messagebox.showerror("Error", "Username cannot be empty!")
        return
    if not length.isdigit() or int(length) < 6:
        messagebox.showerror("Error", "Enter a valid password length (min 6)!")
        return

    length = int(length)
    chars = string.ascii_letters + string.digits + "@#%&()?!"
    password = "".join(random.sample(chars, length))
    
    password_var.set(password)

# Function to save password
def save_password():
    username = username_entry.get().strip()
    password = password_var.get()

    if not username or not password:
        messagebox.showerror("Error", "Generate a password first!")
        return

    with sqlite3.connect("users.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE Username = ?", (username,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Username already exists! Choose another.")
            return
        
        cursor.execute("INSERT INTO users (Username, Password) VALUES (?, ?)", (username, password))
        db.commit()
    
    messagebox.showinfo("Success", "Password saved successfully!")

# Function to reset fields
def reset_fields():
    username_entry.delete(0, END)
    length_entry.delete(0, END)
    password_var.set("")

# Create GUI
root = Tk()
root.title("Password Generator")
root.geometry("400x300")
root.resizable(False, False)

Label(root, text="Username:").pack(pady=5)
username_entry = Entry(root)
username_entry.pack()

Label(root, text="Password Length:").pack(pady=5)
length_entry = Entry(root)
length_entry.pack()

password_var = StringVar()
Label(root, text="Generated Password:").pack(pady=5)
password_entry = Entry(root, textvariable=password_var, state="readonly")
password_entry.pack()

Button(root, text="Generate Password", command=generate_password).pack(pady=10)
Button(root, text="Save Password", command=save_password).pack(pady=5)
Button(root, text="Reset", command=reset_fields).pack(pady=5)  # Reset Button

root.mainloop()
