import tkinter as tk
from Scripts.UserInterface import Colors
import customtkinter as ctk

class UserDisplayWidget(ctk.CTkFrame):
    def __init__(self, root, on_login_callback=None, on_signup_callback=None):
        super().__init__(root)
        self.root = root
        self.on_login_callback = on_login_callback
        self.on_signup_callback = on_signup_callback

        self.logged_in = False
        self.username = "Guest"

        self.create_widgets()
        self.configure(bg_color='transparent')

    def create_widgets(self):
        self.inner_frame = ctk.CTkFrame(self, fg_color='transparent')

        self.label = ctk.CTkLabel(self.inner_frame, text="Welcome, " + self.username)
        self.label.pack(pady=10, padx=10, side=tk.LEFT)

        if self.logged_in:
            # Display username if logged in
            self.label.configure(text="Welcome, " + self.username)
        else:
            # Display login and signup buttons if not logged in
            self.login_button = ctk.CTkButton(self.inner_frame, text="Log In", command=self.on_login_callback, corner_radius=10, width=90)
            self.login_button.pack(side=tk.LEFT, padx=5, pady=5)

            self.signup_button = ctk.CTkButton(self.inner_frame, text="Sign Up", command=self.on_signup_callback, corner_radius=10, width=90)
            self.signup_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.inner_frame.pack()

    def set_username(self, username):
        self.username = username
        if self.logged_in:
            self.label.config(text="Welcome, " + self.username)

    def set_logged_in(self, logged_in):
        self.logged_in = logged_in
        if self.logged_in:
            self.label.configure(text="Welcome, " + self.username)
            try:
                self.login_button.pack_forget()
                self.signup_button.pack_forget()
            except:
                None
        else:
            self.label.config(text="")

if __name__ == "__main__":
    def login_callback():
        print("Log in button pressed")

    def signup_callback():
        print("Sign up button pressed")

    root = tk.Tk()
    user_display_widget = UserDisplayWidget(root, on_login_callback=login_callback, on_signup_callback=signup_callback)
    user_display_widget.pack()

    # Example of setting the username and changing the login state
    user_display_widget.set_username("JohnDoe")
    user_display_widget.set_logged_in(True)

    root.mainloop()
