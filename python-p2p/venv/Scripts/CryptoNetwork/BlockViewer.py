import customtkinter as ctk

class ExpandableFrame(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.expanded = False
        self.default_height = 100
        self.expanded_height = 300

        # Set initial size
        self.configure(height=self.default_height, width=200)

        # Create a label to indicate click action
        self.label = ctk.CTkLabel(self, text="Click to expand")
        self.label.pack(pady=20)

        # Bind the click event
        self.bind("<Button-1>", self.toggle_expand)
        self.label.bind("<Button-1>", self.toggle_expand)

    def toggle_expand(self, event):
        if self.expanded:
            self.configure(height=self.default_height)
            self.label.configure(text="Click to expand")
        else:
            self.configure(height=self.expanded_height)
            self.label.configure(text="Click to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\nClick to collapse\n")
        self.expanded = not self.expanded

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("400x400")

    expandable_frame = ExpandableFrame(root, bg_color="lightblue")
    expandable_frame.pack(pady=50, padx=50)

    root.mainloop()
