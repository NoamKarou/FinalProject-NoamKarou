import tkinter as tk
from tkinter import ttk
from Scripts.UserInterface import Colors
import customtkinter as ctk
class MainMenu:
    header_color: str
    titles: dict[str,str]
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
        self.login_request = ctk.CTkFrame(self.frame, fg_color='gray15')
        self.requestion_entry = ctk.CTkLabel(self.login_request, text="log in to unlock the POWER of the network")
        self.requestion_entry.pack(pady=20)



        # Create a frame for the tab
        self.tab_frame = tk.Frame(self.notebook)

        self.titles = {
            'transfer': "create\n transfer ",
            'history': " transaction \nhistory ",
            'network': " network \n mapper ",
            'connections': " current \n connections ",
            'mining': " miner \n summary ",
            'inbox': "  notification  \n  inbox",
        }

        for option in self.titles.values():
            self.notebook.add(option)

        #self.notebook.add(self.titles['transfer'])
        #self.notebook.add(self.titles['history'])
        #self.notebook.add(self.titles['network'])
        #self.notebook.add(self.titles['connections'])

        # Add widgets to the tab frame
        tab_label = tk.Label(self.tab_frame, text="Tab Section")
        tab_label.pack(pady=10)
        tab_button = tk.Button(self.tab_frame, text="Click me too!")
        tab_button.pack(fill=tk.Y)

    def add_widget_to_header(self, widget, side=tk.LEFT):
        widget.pack(in_=self.header_frame, side=side, padx=10)

    def add_widget_to_body(self, widget):
        widget.pack(in_=self.tab_frame)

    def attach_widget_to_tab(self, widget, tab_name):
        # Get the index of the tab by its name
        tab_index = None
        for idx in range(notebook.index('end')):
            if self.notebook.tab(idx, "text") == tab_name:
                tab_index = idx
                break

        # If tab with specified name is found, attach the widget to that tab
        #if tab_index is not None:
        #    #notebook.forget(tab_index)  # Remove the existing tab temporarily
        #    notebook.insert(tab_index, widget, text=tab_name)  # Insert the widget in the tab
        #    notebook.select(tab_index)

    def set_login_status(self, status):
        if status is not False:
            self.notebook.pack(fill=tk.BOTH, expand=True)
            self.login_request.pack_forget()
        else:
            self.notebook.pack_forget()
            self.login_request.pack(fill=tk.BOTH, expand=True)
if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)

    # Example of adding widgets to the header and body
    header_widget = tk.Label(root, text="Widget added to Header")
    body_widget = tk.Label(root, text="Widget added to Body")

    app.add_widget_to_header(header_widget)
    app.add_widget_to_body(body_widget)

    root.mainloop()
