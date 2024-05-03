import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
class LoginMenu:
    def __init__(self, root, on_successful_login, on_retry_login, login_callback, main_menu_callback):
        background = ctk.CTkFrame(root)
        self.root = root
        self.root.title("Login Menu")
        self.root = ctk.CTkFrame(self.root)
        root = ctk.CTkFrame(self.root)

        empty_label = ctk.CTkLabel(root, text="\nlog in:\n------------------------------------")
        empty_label.pack(padx = 25)

        self.on_successful_login = on_successful_login
        self.on_retry_login = on_retry_login
        self.login_callback = login_callback

        # Create username and password variables
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Create labels, entry fields, and login button
        username_label = ctk.CTkLabel(root, text="Username:")
        username_label.pack(pady=10)
        username_entry = ctk.CTkEntry(root, textvariable=self.username_var)
        username_entry.pack(pady=5)

        password_label = ctk.CTkLabel(root, text="Password:")
        password_label.pack(pady=10)
        password_entry = ctk.CTkEntry(root, textvariable=self.password_var, show="*")
        password_entry.pack(pady=5)

        login_button = ctk.CTkButton(root, text="Login", command=self.check_login)
        login_button.pack(pady=10)

        self.main_menu_callback = main_menu_callback
        return_button = ctk.CTkButton(root, text="back", command=self.main_menu_callback)
        return_button.pack()

        empty_label = ctk.CTkLabel(root, text="")
        empty_label.pack()

        root.pack(fill=ctk.BOTH, expand=True)
        self.root.pack(pady=25)

    def check_login(self):
        # Check login details (replace this with your actual authentication logic)
        username = self.username_var.get()
        password = self.password_var.get()

        # Replace the condition below with your authentication logic
        result = self.login_callback(username, password)
        print("result==================")
        print(result)
        if result != False:
            messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
            self.on_successful_login(username, result)
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password. Please try again.")
            self.on_retry_login()



def load_main_menu():
    # Replace this with the code to load your main menu
    print("Main menu loaded!")

if __name__ == "__main__":
    root = tk.Tk()

    def on_successful_login():
        load_main_menu()

    def on_retry_login():
        # You can add additional logic or UI updates here
        print("Retrying login...")

    login_menu = LoginMenu(root, on_successful_login, on_retry_login)

    root.mainloop()
