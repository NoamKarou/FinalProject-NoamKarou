import tkinter as tk

class CreateAccount:
    def __init__(self, master):
        self.master = master
        self.create_account_frame = self.create_frame()
        self.account_creation_callback = None

    def create_account(self, username, password):
        self.account_creation_callback(username, password)

    def create_frame(self):
        frame = tk.Frame(self.master, padx=10, pady=10)

        # Username entry
        username_label = tk.Label(frame, text="New Username:")
        username_label.pack(pady=5)
        username_entry = tk.Entry(frame)
        username_entry.pack(pady=5)

        # Password entry
        password_label = tk.Label(frame, text="New Password:")
        password_label.pack(pady=5)
        password_entry = tk.Entry(frame, show="*")
        password_entry.pack(pady=5)

        # Submit button with dummy lambda function
        submit_button = tk.Button(frame, text="Create Account", command=lambda: self.create_account(username_entry, password_entry))
        submit_button.pack(pady=10)

        return frame

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Create Account")

    create_account_app = CreateAccount(root)
    create_account_frame = create_account_app.create_account_frame
    create_account_frame.pack(expand=True, fill='both')

    root.mainloop()
