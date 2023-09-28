import sqlite3
import tkinter as tk
from tkinter import messagebox

# Initialize SQLite database
conn = sqlite3.connect('urls.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS urls
             (id INTEGER PRIMARY KEY,
              url TEXT,
              description TEXT)''')
conn.commit()

# Define functions for database operations
def add_url():
    url = url_entry.get()
    description = description_entry.get()
    c.execute("INSERT INTO urls (url, description) VALUES (?, ?)", (url, description))
    conn.commit()
    refresh_list()

def delete_url():
    selected_id = url_listbox.curselection()
    if selected_id:
        c.execute("DELETE FROM urls WHERE id=?", (selected_id[0]+1,))
        conn.commit()
        refresh_list()

def refresh_list():
    url_listbox.delete(0, tk.END)
    for row in c.execute("SELECT * FROM urls"):
        url_listbox.insert(tk.END, f"{row[2]} - {row[1]}")

# Create the main application window
app = tk.Tk()
app.title("URL Manager")

# Create and place widgets
url_label = tk.Label(app, text="URL:")
url_label.grid(row=0, column=0, sticky='e')
url_entry = tk.Entry(app)
url_entry.grid(row=0, column=1, padx=5, pady=5, sticky='we', columnspan=2)

description_label = tk.Label(app, text="Description:")
description_label.grid(row=1, column=0, sticky='e')
description_entry = tk.Entry(app)
description_entry.grid(row=1, column=1, padx=5, pady=5, sticky='we', columnspan=2)

add_button = tk.Button(app, text="Add URL", command=add_url)
add_button.grid(row=0, column=3, padx=5, pady=5, sticky='we')

delete_button = tk.Button(app, text="Delete Selected", command=delete_url)
delete_button.grid(row=1, column=3, padx=5, pady=5, sticky='we')

url_listbox = tk.Listbox(app, width=50, height=10)
url_listbox.grid(row=2, column=0, padx=5, pady=5, sticky='nswe', columnspan=4)
url_listbox.grid_rowconfigure(0, weight=1)
url_listbox.grid_columnconfigure(0, weight=1)

# Populate the listbox
refresh_list()

# Start the GUI application
app.mainloop()

# Close the database connection when the app exits
conn.close()
