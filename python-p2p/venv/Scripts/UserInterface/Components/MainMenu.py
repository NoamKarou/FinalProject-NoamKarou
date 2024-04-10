import tkinter as tk
from tkinter import ttk
from Scripts.UserInterface import Colors
import customtkinter as ctk
class MainMenu:
    header_color: str
    def __init__(self, root):
        self.header_color = "#d8d8d8"
        self.root = root
        # Calculate the screen height
        screen_height = self.root.winfo_screenheight()
        screen_width = self.root.winfo_screenheight()

        self.frame = ctk.CTkFrame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        # Create a frame for the header
        header_height = int(screen_height / 2)
        self.header_frame = ctk.CTkFrame(self.frame, height=header_height)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)

        self.sidebar = ctk.CTkFrame(self.frame, width=int(screen_width/5.5), fg_color='gray17')
        self.sidebar.pack(fill=tk.Y, side=tk.LEFT)

        # Create a notebook for the tabbed interface
        self.notebook = ctk.CTkTabview(self.frame, anchor='w')
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create a frame for the tab
        self.tab_frame = tk.Frame(self.notebook)
        self.notebook.add("create\n transfer ")
        self.notebook.add(" transaction \nhistory ")
        self.notebook.add(" network \n mapper ")
        self.notebook.add(" current \n connections ")

        # Add widgets to the tab frame
        tab_label = tk.Label(self.tab_frame, text="Tab Section")
        tab_label.pack(pady=10)
        tab_button = tk.Button(self.tab_frame, text="Click me too!")
        tab_button.pack(fill=tk.Y)

    def add_widget_to_header(self, widget, side=tk.LEFT):
        widget.pack(in_=self.header_frame, side=side, padx=10)

    def add_widget_to_body(self, widget):
        widget.pack(in_=self.tab_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)

    # Example of adding widgets to the header and body
    header_widget = tk.Label(root, text="Widget added to Header")
    body_widget = tk.Label(root, text="Widget added to Body")

    app.add_widget_to_header(header_widget)
    app.add_widget_to_body(body_widget)

    root.mainloop()
