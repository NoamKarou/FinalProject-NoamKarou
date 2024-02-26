import tkinter as tk


class UserAuthentication:
    def __init__(self, master):
        self.master = master
        self.auth_frame = self.create_auth_frame()

    def authenticate(self, username, password):
        # Dummy authentication function
        print(f"Username: {username.get()}")
        print(f"Password: {password.get()}")
        # Add your authentication logic here

    def create_auth_frame(self):
        auth_frame = tk.Frame(self.master, padx=10, pady=10)

        # Username entry
        username_label = tk.Label(auth_frame, text="Username:")
        username_label.pack(pady=5)
        username_entry = tk.Entry(auth_frame)
        username_entry.pack(pady=5)

        # Password entry
        password_label = tk.Label(auth_frame, text="Password:")
        password_label.pack(pady=5)
        password_entry = tk.Entry(auth_frame, show="*")
        password_entry.pack(pady=5)

        # Submit button with dummy lambda function
        submit_button = tk.Button(auth_frame, text="Submit", command=lambda: self.authenticate(username_entry, password_entry))
        submit_button.pack(pady=10)

        return auth_frame

if __name__ == "__main__":
    root = tk.Tk()
    root.title("User Authentication")

    auth_app = UserAuthentication(root)
    auth_frame = auth_app.auth_frame
    auth_frame.pack(expand=True, fill='both')

    root.mainloop()
