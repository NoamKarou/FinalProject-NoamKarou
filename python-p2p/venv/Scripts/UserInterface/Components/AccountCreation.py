import tkinter as tk
from tkinter import messagebox

class AccountCreation:
    def __init__(self, root, on_successful_account_creation, on_retry_creation, creation_callback):
        self.root = root
        self.root.title("Creation Menu")

        self.on_successful_account_creation = on_successful_account_creation
        self.on_retry_creation = on_retry_creation
        self.creation_callback = creation_callback

        # Create username and password variables
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Create labels, entry fields, and login button
        username_label = tk.Label(root, text="Username:")
        username_label.pack(pady=10)
        username_entry = tk.Entry(root, textvariable=self.username_var)
        username_entry.pack(pady=5)

        password_label = tk.Label(root, text="Password:")
        password_label.pack(pady=10)
        password_entry = tk.Entry(root, textvariable=self.password_var, show="*")
        password_entry.pack(pady=5)

        login_button = tk.Button(root, text="Sign-Up", command=self.check_login)
        login_button.pack(pady=10)

    def check_login(self):
        # Check login details (replace this with your actual authentication logic)
        username = self.username_var.get()
        password = self.password_var.get()

        # Replace the condition below with your authentication logic
        if self.creation_callback(username, password):
            messagebox.showinfo("Account Creation Successful", "Welcome, " + username + "!")
            self.on_successful_account_creation(username)
        else:
            messagebox.showerror("Account Creation Failed", "Username Already Exists. Please try again.")
            self.on_retry_creation()

def load_main_menu():
    # Replace this with the code to load your main menu
    print("Main menu loaded!")

if __name__ == "__main__":
    root = tk.Tk()

    def on_successful_account_creation():
        load_main_menu()

    def on_retry_creation():
        # You can add additional logic or UI updates here
        print("Retrying login...")

    login_menu = LoginMenu(root, on_successful_account_creation, on_retry_creation)

    root.mainloop()
