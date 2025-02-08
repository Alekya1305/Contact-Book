import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create/Connect to SQLite database
conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()

# Create Contacts table
cursor.execute('''
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY,
    name TEXT,
    phone TEXT,
    email TEXT,
    address TEXT
)
''')

conn.commit()

# Function to Add Contact
def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()

    if name and phone:
        cursor.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                       (name, phone, email, address))
        conn.commit()
        messagebox.showinfo("Success", "Contact added successfully")
        clear_entries()
        display_contacts()
    else:
        messagebox.showwarning("Input Error", "Name and phone number are required!")

# Function to Update Contact
def update_contact():
    selected_id = contact_listbox.curselection()
    if selected_id:
        contact_id = contact_listbox.get(selected_id[0]).split()[0]
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get()

        cursor.execute("UPDATE contacts SET name = ?, phone = ?, email = ?, address = ? WHERE id = ?",
                       (name, phone, email, address, contact_id))
        conn.commit()
        messagebox.showinfo("Success", "Contact updated successfully")
        display_contacts()
        clear_entries()
    else:
        messagebox.showwarning("Selection Error", "Please select a contact to update.")

# Function to Delete Contact
def delete_contact():
    selected_id = contact_listbox.curselection()
    if selected_id:
        contact_id = contact_listbox.get(selected_id[0]).split()[0]
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        conn.commit()
        messagebox.showinfo("Success", "Contact deleted successfully")
        display_contacts()
    else:
        messagebox.showwarning("Selection Error", "Please select a contact to delete.")

# Function to Display Contacts
def display_contacts():
    contact_listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    for contact in contacts:
        contact_listbox.insert(tk.END, f"{contact[0]} {contact[1]} - {contact[2]}")

# Function to Search Contacts
def search_contact():
    search_term = search_entry.get().lower()
    contact_listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?",
                   ('%' + search_term + '%', '%' + search_term + '%'))
    contacts = cursor.fetchall()
    for contact in contacts:
        contact_listbox.insert(tk.END, f"{contact[0]} {contact[1]} - {contact[2]}")

# Function to Clear Entry Fields
def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

# Setup Tkinter GUI
root = tk.Tk()
root.title("Contact Book")

# Create GUI Widgets
frame = tk.Frame(root)
frame.pack(pady=10)

name_label = tk.Label(frame, text="Name:")
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

phone_label = tk.Label(frame, text="Phone:")
phone_label.grid(row=1, column=0, padx=5, pady=5)
phone_entry = tk.Entry(frame)
phone_entry.grid(row=1, column=1, padx=5, pady=5)

email_label = tk.Label(frame, text="Email:")
email_label.grid(row=2, column=0, padx=5, pady=5)
email_entry = tk.Entry(frame)
email_entry.grid(row=2, column=1, padx=5, pady=5)

address_label = tk.Label(frame, text="Address:")
address_label.grid(row=3, column=0, padx=5, pady=5)
address_entry = tk.Entry(frame)
address_entry.grid(row=3, column=1, padx=5, pady=5)

# Buttons
add_button = tk.Button(root, text="Add Contact", command=add_contact)
add_button.pack(pady=5)

update_button = tk.Button(root, text="Update Contact", command=update_contact)
update_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Contact", command=delete_contact)
delete_button.pack(pady=5)

# Search
search_label = tk.Label(root, text="Search:")
search_label.pack(pady=5)

search_entry = tk.Entry(root)
search_entry.pack(pady=5)

search_button = tk.Button(root, text="Search", command=search_contact)
search_button.pack(pady=5)

# Contact Listbox
contact_listbox = tk.Listbox(root, width=50, height=10)
contact_listbox.pack(pady=10)

# Display contacts when the application starts
display_contacts()

root.mainloop()

# Close the database connection when the application closes
conn.close()