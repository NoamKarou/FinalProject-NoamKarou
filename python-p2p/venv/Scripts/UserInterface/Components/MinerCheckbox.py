import tkinter as tk


class MinerCheckbox:
    def __init__(self, parent, is_logged_in, miner_update_callback):
        self.parent = parent
        self.is_logged_in = is_logged_in

        self.frame = tk.Frame(self.parent)
        self.frame.pack(side=tk.LEFT)

        self.checkbox_var = tk.BooleanVar()
        self.checkbox_var.set(False)  # Initial state unchecked

        self.label_text = "Become a miner"
        self.label = tk.Label(self.frame, text=self.label_text, padx=5)
        self.label.pack(side=tk.LEFT)

        self.checkbox_button = tk.Button(self.frame, text="☐", command=self.toggle_miner,
                                         borderwidth=0, width=2, font=('Arial', 12))
        self.checkbox_button.pack(side=tk.LEFT)

        self.miner_update_callback = miner_update_callback

        self.update_state()

    def toggle_miner(self):
        if self.checkbox_var.get():
            self.label_text = "You are now a miner"
            self.checkbox_button.config(text="☑")
            self.miner_update_callback(True)
        else:
            self.label_text = "Become a miner"
            self.checkbox_button.config(text="☐")
            self.miner_update_callback(False)
        self.label.config(text=self.label_text)
        self.checkbox_var.set(not self.checkbox_var.get())

    def update_state(self):
        if self.is_logged_in():
            self.checkbox_button.config(state=tk.NORMAL)
        else:
            self.checkbox_button.config(state=tk.DISABLED)


if __name__ == "__main__":
    def is_logged_in():
        return True  # Replace with your authentication logic


    root = tk.Tk()
    top_bar = tk.Frame(root)
    top_bar.pack(fill=tk.X)

    miner_checkbox = MinerCheckbox(top_bar, is_logged_in)

    root.mainloop()
