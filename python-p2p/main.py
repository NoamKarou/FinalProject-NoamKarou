import customtkinter

class TransactionCreator:
    def __init__(self, master, friends):
        self.master = master
        self.friends = friends
        self.filtered_friends = self.friends.copy()
        self.selected_friend = customtkinter.StringVar()

        self.setup_ui()

    def setup_ui(self):
        self.master.title("Select Friends")

        # Create a search bar
        self.search_bar = customtkinter.CTkEntry(self.master, placeholder_text="Search...")
        self.search_bar.pack(pady=10, padx=10)

        # Bind the search bar to the filter_friends function
        self.search_bar.bind("<KeyRelease>", self.filter_friends)

        # Create a scrollable frame to display friend names
        self.friend_frame = customtkinter.CTkScrollableFrame(self.master, width=300, height=200)
        self.friend_frame.pack(pady=10, padx=10)

        # Call display_friends to populate the scrollable frame initially
        self.display_friends()

        # Create an amount entry
        self.amount_entry = customtkinter.CTkEntry(self.master, placeholder_text='Amount')
        self.amount_entry.pack()

        # Create a "Send" button
        self.send_button = customtkinter.CTkButton(self.master, text="Send ✈️", command=self.send_transaction)
        self.send_button.pack(pady=10)

    def filter_friends(self, *args):
        search_term = self.search_bar.get().lower()
        self.filtered_friends.clear()
        for friend in self.friends:
            if search_term in friend.lower():
                self.filtered_friends.append(friend)
        self.display_friends()

    def display_friends(self):
        for widget in self.friend_frame.winfo_children():
            widget.destroy()
        for friend in self.filtered_friends:
            radio_button = customtkinter.CTkRadioButton(master=self.friend_frame, text=friend, value=friend, variable=self.selected_friend, command=self.update_search_bar)
            radio_button.pack(padx=10, pady=5, anchor="w")

    def update_search_bar(self):
        self.search_bar.delete(0, customtkinter.END)
        self.search_bar.insert(0, self.selected_friend.get())

    def send_transaction(self):
        amount = self.amount_entry.get()
        selected_friend = self.selected_friend.get()
        # Perform action with the selected friend and amount, e.g., sending transaction

if __name__ == "__main__":
    # Create the CustomTkinter app
    app = customtkinter.CTk()

    # Set the appearance mode
    customtkinter.set_appearance_mode("System")  # Options: "System" (standard), "Dark", "Light"

    # List of friends
    friends_list = ["Dot.dotams", "Dog Gale.doggale", "Down.downfr97", "lozardo.lozardo", "otrfrsnk.otrfrenk"]

    # Initialize the TransactionCreator with the app as the master and the friends list
    transaction_creator = TransactionCreator(app, friends_list)

    app.mainloop()
