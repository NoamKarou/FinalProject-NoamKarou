import tkinter as tk
import customtkinter as ctk
class IDLabel:
    def __init__(self, parent, id_callback):
        self.parent = parent
        self.id_callback = id_callback

        self.frame = ctk.CTkFrame(self.parent)


        self.label = ctk.CTkLabel(self.frame)
        self.label.pack()

        self.update_label()


    def update_label(self):
        id_text = self.id_callback()
        self.label.configure(text=f" {id_text} ", fg_color='gray25', corner_radius=8)

if __name__ == "__main__":
    def id_callback():
        return "123456"  # Replace with your actual ID retrieval logic

    root = tk.Tk()
    id_label = IDLabel(root, id_callback)

    root.mainloop()
