import tkinter as tk
import random
from tkinter import messagebox
import customtkinter as ctk
from Scripts.UserInterface.Components import Logo

class StartingScreen:
    def __init__(self, master, auto_callback, manual_callback):
        self.master = master
        self.auto_callback = auto_callback
        self.manual_callback = manual_callback
        self.connect_frame = self.create_frame()



    def create_frame(self):
        frame = ctk.CTkFrame(self.master)

        logo_component = Logo.Logo(frame)
        logo_component.frame.pack(pady=35)

        large_font = ("Helvetica", 20)

        auto_login_button = ctk.CTkButton(frame, text='      Auto Login      ', font=large_font, command=self.auto_callback)
        auto_login_button.pack()
        recomendation_text = ctk.CTkLabel(frame, text="↑ recomended for most users ↑")
        recomendation_text.pack(pady=5)

        manual_login_button = ctk.CTkButton(frame, text='    Manual Login    ', font=large_font, command=self.manual_callback)
        manual_login_button.pack()
        recomendation_text = ctk.CTkLabel(frame, text="↑ for experienced users ↑")
        recomendation_text.pack(pady=5)

        return frame

if __name__ == "__main__":
    def on_connect(ip, port, my_port):
        print(f"Connecting to server at {ip}:{port} with my port {my_port}")
        # Add your connection initiation logic here

    root = ctk.CTk()
    root.title("Connect to Server")

    connect_to_server_app = StartingScreen(root, manual_callback=None, auto_callback=None)
    connect_frame = connect_to_server_app.connect_frame
    connect_frame.pack(expand=True, fill='both')

    root.mainloop()
