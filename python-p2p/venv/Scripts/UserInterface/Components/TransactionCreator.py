import random
import time
import threading
import customtkinter
class TransactionCreator:
    def __init__(self, master, people_callback, button_callback):
        self.master = customtkinter.CTkFrame(master)
        self.transactions = people_callback()
        self.filtered_transactions = self.transactions.copy()
        self.selected_transaction = customtkinter.StringVar()

        self.people_callback = people_callback
        self.button_callback = button_callback

        self.setup_ui()
        self.update_people_list()

    def setup_ui(self):
        # Create a search bar
        self.search_bar = customtkinter.CTkEntry(self.master, placeholder_text="Search...")
        self.search_bar.pack(pady=10, padx=10, fill=customtkinter.X)

        # Bind the search bar to the filter_transactions function
        self.search_bar.bind("<KeyRelease>", self.filter_transactions)

        # Create a scrollable frame to display transaction names
        self.transaction_frame = customtkinter.CTkScrollableFrame(self.master, width=300, height=200)
        self.transaction_frame.pack(pady=10, padx=10)

        # Call display_transactions to populate the scrollable frame initially
        self.display_transactions()

        # Create an amount entry
        self.amount_entry = customtkinter.CTkEntry(self.master, placeholder_text='Amount')
        self.amount_entry.pack()

        # Create a "Send" button
        self.send_button = customtkinter.CTkButton(self.master, text="Send ✈️", command=lambda : self.button_callback())
        self.send_button.pack(pady=10)

        self.error_label = customtkinter.CTkLabel(self.master, text="", text_color='red')
        self.error_label.pack()

    def filter_transactions(self, *args):
        search_term = self.search_bar.get().lower()
        self.filtered_transactions.clear()
        for transaction in self.transactions:
            if search_term in transaction.lower():
                self.filtered_transactions.append(transaction)
        self.display_transactions()

    def set_error_text(self, error):
        self.error_label.configure(text=error)

    def display_transactions(self):
        for widget in self.transaction_frame.winfo_children():
            widget.destroy()
        for transaction in self.filtered_transactions:
            radio_button = customtkinter.CTkRadioButton(master=self.transaction_frame, text=transaction, value=transaction, variable=self.selected_transaction, command=self.update_search_bar)
            radio_button.pack(padx=10, pady=5, anchor="w")

    def update_search_bar(self):
        print("wjaaaa")
        self.search_bar.delete(0, customtkinter.END)
        self.search_bar.insert(0, self.selected_transaction.get())

    def send_transaction(self):
        amount = self.amount_entry.get()
        selected_transaction = self.selected_transaction.get()

    def update_users(self, new_users):
        self.transactions = new_users
        self.filtered_transactions = self.transactions.copy()
        self.display_transactions()

    def update_people_list(self):
        new_people_list = self.get_people_list()
        if new_people_list != self.transactions:
            self.transactions = new_people_list
            self.filtered_transactions = self.transactions.copy()
            self.display_transactions()
        self.master.after(1000, self.update_people_list)

    def get_people_list(self):
        return self.people_callback()

    def get_transaction_details(self):
        amount = self.amount_entry.get()
        selected_transaction = self.selected_transaction.get()
        return selected_transaction, amount

def get_transactions():
    return random.choice([['noam', 'oren'], ['noam', 'oren', 'itamar']])

if __name__ == "__main__":
    # Create the CustomTkinter app
    app = customtkinter.CTk()

    # Set the appearance mode
    customtkinter.set_appearance_mode("System")  # Options: "System" (standard), "Dark", "Light"

    # List of transactions
    transactions_list = []

    # Initialize the TransactionCreator with the app as the master and the transactions list
    transaction_creator = TransactionCreator(app, get_transactions, lambda :print(":)"))

    transaction_creator.update_users(["Dot.dotams", "Dog Gale.doggale", "Down.downfr97", "lozardo.lozardo", "otrfrsnk.otrfrenk"])
    transaction_creator.master.pack()

    app.mainloop()
