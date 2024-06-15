import random
import time
import threading
import customtkinter
import customtkinter as ctk
from Scripts.CryptoNetwork.Transaction import Transaction
from Scripts.CryptoNetwork.UserGenerator import generate_key_pair

my_account = 'noam'
database_transaction_callback = None
class TransactionCreator:
    def __init__(self, master, people_callback, button_callback, my_username, database_transaction_callback_parm, username_callback):
        global database_transaction_callback, my_account
        '''
        :param master: tkinter master frame
        :param people_callback: a callback to a list of the people in the transaction creator
        :param button_callback:
        :param my_username:
        :param database_transaction_callback:
        '''
        self.master = customtkinter.CTkFrame(master)
        self.transactions = people_callback()

        self.filtered_transactions = self.transactions.copy()
        self.selected_transaction = customtkinter.StringVar()
        self.username_callback = my_username
        database_transaction_callback = database_transaction_callback_parm
        my_account = username_callback
        if my_account() in self.transactions:
            self.transactions.remove(my_account())

        self.people_callback = people_callback
        self.button_callback = button_callback

        self.setup_ui()
        self.update_people_list()

    def setup_ui(self):
        self.secondary_frame = ctk.CTkFrame(self.master)

        self.user_datails = ctk.CTkLabel(self.secondary_frame, text="wow im a username and more!\n\n\nMULTIPLE LINES!!!")
        self.user_datails.pack()

        self.transaction_history_display = Inbox(self.secondary_frame)
        self.transaction_history_display.pack()

        self.secondary_frame.pack(side=ctk.RIGHT, anchor='n')
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
        self.user_datails.configure(text=self.username_callback())
        self.transaction_history_display.transaction_display_manager()
        self.master.after(1000, self.update_people_list)

    def get_people_list(self):
        return self.people_callback()

    def get_transaction_details(self):
        amount = self.amount_entry.get()
        selected_transaction = self.selected_transaction.get()
        return selected_transaction, amount

'''
=============================start inbox section
'''
class Inboxtransaction(ctk.CTkFrame):
    def __init__(self, parent, transaction: Transaction, *args, **kwargs):
        global my_account
        super().__init__(parent, *args, **kwargs)

        self.configure(corner_radius=0)  # Add corner_radius=10 for rounded corners
        if transaction.sender == my_account():
            transaction_text = f'➖ {transaction.amount} | {transaction.receiver} | {transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S')}'
        else:
            transaction_text = f'➕ {transaction.amount} | {transaction.sender} | {transaction.timestamp}'
        #self.sender_label = ctk.CTkLabel(self, text=transaction_data["sender"], text_color="gray", anchor="w", bg_color='transparent', fg_color='transparent')
        self.content_label = ctk.CTkLabel(self, text=transaction_text, wraplength=400, justify="left", anchor="w")
        self.side_rectangle = ctk.CTkFrame(self, fg_color='#f4b034', corner_radius=0, width=3, height=1)
        self.additional_info_label = None
        self.info_window = None

        self.create_widgets(transaction)
        self.configure_widgets(transaction)
        self.pack_widgets()


    def create_widgets(self, transaction_data):
        self.transaction_data = transaction_data.sender

    def configure_widgets(self, transaction_data):
        if transaction_data.sender == my_account():
            self.configure(fg_color='#3f0a13')
        else:
            self.configure(fg_color='#14763b')

    def pack_widgets(self):
        #self.sender_label.pack(side="bottom", fill="x", padx=10, pady=1)

        self.content_label.pack(side="top", fill="both", expand=True, padx=10, pady=1)
        if self.additional_info_label:
            self.additional_info_label.pack(side="left", fill="x", padx=10, pady=1)

        # Update geometry after packing
        self.update_idletasks()

    def show_additional_info(self, additional_info):
        if self.info_window:
            self.info_window.destroy()

        self.info_window = ctk.CTkToplevel(self)
        self.info_window.title("Additional Information")
        self.info_window.attributes('-topmost', True)
        info_label = ctk.CTkLabel(self.info_window, text=additional_info, wraplength=400, justify="left")
        info_label.pack(padx=10, pady=10)

    def get_height(self):
        return self.winfo_reqheight() + 25

class Inbox(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure()
        #self.header = ctk.CTkFrame(self, fg_color='red', height=80)
        #self.header_text = ctk.CTkLabel(self.header, text='inbox')
        #self.header_text.pack()
        #self.header.pack(fill=ctk.X)

        self.canvas = ctk.CTkCanvas(self, highlightthickness=0)
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.create_widgets()
        self.configure_widgets()
        self.pack_widgets()

        self.transaction_frames = []
        self.current_y = 0



        self.transaction_jsons: list[str] = list()


    def transaction_display_manager(self):
        global database_transaction_callback, my_account
        temp_transactions = database_transaction_callback(my_account())
        for transaction in temp_transactions:
            if transaction not in self.transaction_jsons:
                self.transaction_jsons.append(transaction)
                self.add_transaction(Transaction.from_json(transaction))

    def update_transactions(self):
        database_transaction_callback

    def create_widgets(self):
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0, bg='gray15')
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)

    def configure_widgets(self):
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        #print(f'c_y: {self.current_y} - w_i: {self.winfo_height()}')
        if self.current_y >= self.winfo_height():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def pack_widgets(self):
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def add_transaction(self, transaction_data):
        transaction = Inboxtransaction(self.canvas, transaction_data)
        transaction_id = self.canvas.create_window(0, 0, anchor="nw", window=transaction, width=4000)
        self.transaction_frames.insert(0, (transaction_id, transaction))

        # Update positions of all transactions
        self.current_y = 0
        for transaction_id, frame in self.transaction_frames:
            self.canvas.moveto(transaction_id, 0, self.current_y)
            self.current_y += frame.get_height()

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
'''
=============================end inbox section
'''



def get_transactions():
    return random.choice([['noam', 'oren'], ['noam', 'oren', 'itamar']])

def transactions_manager(me):
    pub, priv = generate_key_pair()
    start_transaction_data = Transaction("noam", "itamar", 200, None)
    return [random.choice([start_transaction_data.to_json(), bot_transaction.to_json()])]

bot_transaction = Transaction("itamar", "noam", 200, None)

if __name__ == "__main__":
    # Create the CustomTkinter app
    app = customtkinter.CTk()

    # Set the appearance mode
    customtkinter.set_appearance_mode("System")  # Options: "System" (standard), "Dark", "Light"

    # List of transactions
    transactions_list = []

    # Initialize the TransactionCreator with the app as the master and the transactions list
    transaction_creator = TransactionCreator(app, get_transactions, lambda :print(":)"), lambda : 'noam', transactions_manager, lambda : 'noam')

    transaction_creator.update_users(["Dot.dotams", "Dog Gale.doggale", "Down.downfr97", "lozardo.lozardo", "otrfrsnk.otrfrenk"])
    transaction_creator.master.pack()

    app.mainloop()
