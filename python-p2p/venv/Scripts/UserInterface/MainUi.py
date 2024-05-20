import time
import ctypes
from PIL import Image

from Scripts.UserInterface.Components import (
    UserAuthenticationField, UserCreation, ConnectToServer,
    MainMenu, UserDisplayWidget, LoginMenu, AccountCreation,
    MinerCheckbox, IDLabel, Logo, TransactionCreator, Inbox,
    CallbackDisplay)

import tkinter as tk

import tkinter
from tkinter import ttk
from tkinter.constants import *
from Scripts.CryptoNetwork import crypto_network_interface
import threading

import customtkinter as ctk

class Ui:
    main_ui_thread: threading.Thread
    root: tk.Tk

    def __init__(self):
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
        self.main_ui_thread = threading.Thread(target=self.ui_loop)
        self.main_ui_thread.start()

        self.interface = crypto_network_interface.interface()
        #self.interface.connect(20000, None, None)

        #set up the UI for the username

        print("tried creating user")

    def hide_all_children(self):
        children = self.root.winfo_children()
        for child in children:
            child.pack_forget()

    def ui_loop(self):
        self.root = ctk.CTk()
        ctk.set_default_color_theme(r'CtkThemes/red.json')
        self.root.title("Noam")
        self.tk_username = tk.StringVar()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        target_width = int(1.5 / 7 * screen_width)
        target_height = int(3 / 7 * screen_height)

        self.root.geometry(f"{target_width}x{target_height}")

        b1 = ttk.Button(self.root, text="Button 1")
        self.root.configure(bg_color='gray1')

        connect_ui = self.connect_ui()
        connect_ui.connect_frame.pack(expand=True, fill='both')

        self.root.mainloop()
        '''  
        authentication = UserCreation.CreateAccount(root)
        authentication.create_account_frame.pack(side=LEFT, padx=5, pady=10)
        authentication.account_creation_callback = self.create_account'''



    def create_account(self, username: ttk.Entry, password):
        print(username.get())
        print(password.get())
        self.interface.create_account(username.get(), password.get())

    def account_creation_callback(self, username, password):
        if self.interface.create_account(username, password):
            encryption_key = self.interface.try_login(username, password)
            self.on_successful_login(username, encryption_key)
            return True
        return False

    def connect_ui(self):
        connect_frame = ConnectToServer.ConnectToServer(self.root, self.connect_callback)
        return connect_frame

    def connect_callback(self, ip, out_port, in_port):
        print(out_port)
        if out_port == 0:
            out_port = None
            ip = None
        self.interface.connect(in_port, ip, out_port)
        self.hide_all_children()
        self.build_main_manu()


    def build_main_manu(self):
        self.main_menu = MainMenu.MainMenu(self.root)
        self.user_display = UserDisplayWidget.UserDisplayWidget(self.main_menu.frame, on_login_callback=self.load_login_screen, on_signup_callback=self.account_creation_ui)
        self.main_menu.add_widget_to_header(self.user_display)

        #self.miner_checkbox = MinerCheckbox.MinerCheckbox(self.main_menu.frame, self.interface.is_logged_in, self.interface.update_miner_status)
        #self.main_menu.add_widget_to_header(self.miner_checkbox.frame, side=tk.RIGHT)

        self.id_label = IDLabel.IDLabel(self.main_menu.sidebar, self.get_id)
        self.id_label.frame.pack(side = tk.BOTTOM, padx=15, pady=10)

        self.logo = Logo.Logo(self.main_menu.sidebar)
        self.logo.frame.pack(side=ctk.TOP, pady=16)

        #notebook setup

        self.transaction_creator = TransactionCreator.TransactionCreator(
            self.main_menu.notebook.tab(self.main_menu.titles['transfer']
                                        ), self.interface.database.get_users, self.transaction_creation_callback)
        self.transaction_creator.master.pack(anchor="nw")



        self.inbox = Inbox.Inbox(self.main_menu.notebook.tab(self.main_menu.titles['inbox']))
        self.inbox.pack(anchor="nw", fill=tk.BOTH, expand=True)

        self.main_menu.set_login_status(self.interface.is_logged_in())


    def transaction_creation_callback(self):
        name, amount = self.transaction_creator.get_transaction_details()
        if name == self.interface.username:
            self.transaction_creator.set_error_text("you can't transfer funds\nto yourself!")
            return
        try:
            temp = int(amount)
        except:
            self.transaction_creator.set_error_text("amount must be a positive integer!")
            return

        if int(amount) < 1 or int(amount) != float(amount):
            self.transaction_creator.set_error_text("amount must be a positive integer!")
            return

        print(f'{name} {amount}')
        if name == '' or amount == '':
            print('canceled')
            return
        self.interface.create_transaction(name, amount)
        self.transaction_creator.set_error_text("")



    def account_creation_ui(self):
        self.hide_all_children()
        login_object = AccountCreation.AccountCreation(
            self.root, on_successful_account_creation=self.on_successful_account_creation,
            on_retry_creation=lambda: None,
            creation_callback=self.account_creation_callback,
            main_menu_callback=self.load_main_menu
            )


    def get_id(self):
        return self.interface.listener.my_id

    def on_successful_account_creation(self, username):
        self.load_main_menu()
        #self.user_display.set_username(username)
        #self.user_display.set_logged_in(True)

    def load_login_screen(self):
        self.hide_all_children()
        login_object = LoginMenu.LoginMenu(
            self.root, on_successful_login=self.on_successful_login,
            on_retry_login= lambda : None,
            login_callback=self.interface.try_login,
            main_menu_callback=self.load_main_menu
        )

    def on_successful_login(self, username, encryption_key):
        self.load_main_menu()
        self.user_display.set_username(username)
        self.user_display.set_logged_in(True)
        self.interface.my_user = username
        self.interface.username = username
        self.interface.encryption_key = encryption_key
        self.interface.update_miner_status(True)
        #self.miner_checkbox.update_state()

        self.miner_callback_display = CallbackDisplay.CallbackDisplay(self.main_menu.notebook.tab(self.main_menu.titles['history']),
                                                                      self.interface.mining.update_callback)
        self.miner_callback_display.pack(anchor="nw", fill=tk.BOTH, expand=True)


    def load_main_menu(self):
        self.hide_all_children()
        self.main_menu.frame.pack(fill=tk.BOTH, expand=True)
        self.main_menu.set_login_status(self.interface.is_logged_in())



def dummy_function():
    print("dummy function called!")

if __name__ == '__main__':
    ui = Ui()
    while True:
        if input():
            exit(0)