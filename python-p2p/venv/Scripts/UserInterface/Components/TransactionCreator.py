import tkinter as tk
from tkinter import ttk

# List of names
names = ["Dot.dotams", "Dog Gale.doggale", "Down.downfr97", "lozardo.lozardo", "otrfrsnk.otrfrenk"]

root = tk.Tk()
root.title("Select Friends")

# Create a search bar
search_bar = ttk.Entry(root)
search_bar.pack(pady=5)

# Create a list to store the filtered names
filtered_names = names.copy()

# Function to filter names based on search input
def filter_names(*args):
    search_term = search_bar.get().lower()
    filtered_names.clear()
    for name in names:
        if search_term in name.lower():
            filtered_names.append(name)
    listbox.delete(0, tk.END)
    for name in filtered_names:
        listbox.insert(tk.END, name)

# Bind the search bar to the filter_names function
search_bar.bind("<KeyRelease>", filter_names)

# Create a Listbox
listbox = tk.Listbox(root, height=5, width=30)
listbox.pack(pady=10)

# Insert names into the Listbox
for name in names:
    listbox.insert(tk.END, name)

# Create an "Add" button
add_button = ttk.Button(root, text="Add")
add_button.pack(pady=5)

# Create a "Create" button
create_button = ttk.Button(root, text="Create")
create_button.pack(pady=5)

root.mainloop()