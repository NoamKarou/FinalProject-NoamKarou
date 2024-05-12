import tkinter as tk
import customtkinter as ctk
import threading
import time

class CallbackDisplay(ctk.CTkFrame):
    def __init__(self, master, callback, **kwargs):
        super().__init__(master, **kwargs)
        self.callback = callback
        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack(pady=10)
        self.update_result()

    def update_result(self):
        result = self.callback()
        self.result_label.configure(text=str(result))
        self.after(500, self.update_result)  # Schedule the next update in 0.5 seconds


if __name__ == '__main__':
    # Example usage
    root = ctk.CTk()


    def get_time():
        return time.strftime("%H:%M:%S")


    callback_display = CallbackDisplay(root, get_time)
    callback_display.pack(padx=20, pady=20)

    root.mainloop()