import tkinter as tk
import random
from tkinter import messagebox
import customtkinter as ctk
from Scripts.UserInterface.Components import Logo

class ConnectToServer:
    def __init__(self, master, connect_callback=None, my_port=None):
        self.master = master
        self.connect_callback = connect_callback
        self.my_port = my_port
        self.connect_frame = self.create_frame()

    def connect_to_server(self, ip_entry, port_entry, my_port_entry):
        try:
            ip = ip_entry.get() if ip_entry.get() else "127.0.0.1"
            port = int(port_entry.get()) if port_entry.get() else random.randint(1024, 49151)
            my_port = int(my_port_entry.get()) if my_port_entry.get() else self.my_port or random.randint(1024, 49151)

            # Call the provided callback function
            if self.connect_callback:
                self.connect_callback(ip, port, my_port)

        except Exception as ex:
            raise (ex)
            messagebox.showerror("Error", "Invalid port. Please enter a valid integer.")
            return

    def create_frame(self):
        frame = ctk.CTkFrame(self.master)

        logo_component = Logo.Logo(frame)
        logo_component.frame.pack(pady=15)

        #empty_label = ctk.CTkLabel(frame, text="\nwelcome to the CBT network!")
        #empty_label.pack(pady=15)

        # IP entry with default text
        ip_label = ctk.CTkLabel(frame, text="Server IP:")
        ip_label.pack(pady=5)
        ip_entry = ctk.CTkEntry(frame)
        ip_entry.insert(0, "127.0.0.1")  # Default text
        ip_entry.pack(pady=5)

        # Port entry with default text
        port_label = ctk.CTkLabel(frame, text="Server Port:")
        port_label.pack(pady=5)
        port_entry = ctk.CTkEntry(frame)
        if self.my_port is not None:
            port_entry.insert(0, str(self.my_port))
        else:
            port_entry.insert(0, str(0))  # Default random port
        port_entry.pack(pady=5)

        # My Port entry with default text
        my_port_label = ctk.CTkLabel(frame, text="My Port:")
        my_port_label.pack(pady=5)
        my_port_entry = ctk.CTkEntry(frame)
        my_port_entry.insert(0, str(random.randint(1024, 49151)))  # Default random port
        my_port_entry.pack(pady=5)

        # Connect button with user-defined callback function
        connect_button = ctk.CTkButton(frame, text="Connect", command=lambda: self.connect_to_server(ip_entry, port_entry, my_port_entry))
        connect_button.pack(pady=10)

        return frame

if __name__ == "__main__":
    def on_connect(ip, port, my_port):
        print(f"Connecting to server at {ip}:{port} with my port {my_port}")
        # Add your connection initiation logic here

    root = tk.Tk()
    root.title("Connect to Server")

    connect_to_server_app = ConnectToServer(root, connect_callback=on_connect, my_port=5000)
    connect_frame = connect_to_server_app.connect_frame
    connect_frame.pack(expand=True, fill='both')

    root.mainloop()
