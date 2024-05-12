import threading
import time

import customtkinter as ctk

class InboxMessage(ctk.CTkFrame):
    def __init__(self, parent, message_data, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.configure(corner_radius=0)  # Add corner_radius=10 for rounded corners

        #self.sender_label = ctk.CTkLabel(self, text=message_data["sender"], text_color="gray", anchor="w", bg_color='transparent', fg_color='transparent')
        self.content_label = ctk.CTkLabel(self, text=message_data["content"], wraplength=400, justify="left", anchor="w")
        self.side_rectangle = ctk.CTkFrame(self, fg_color='#f4b034', corner_radius=0, width=3, height=1)
        self.additional_info_label = None
        self.info_window = None

        self.create_widgets(message_data)
        self.configure_widgets(message_data)
        self.pack_widgets()


    def create_widgets(self, message_data):
        self.message_data = message_data
        if message_data["additional_information"]:
            self.additional_info_label = ctk.CTkLabel(self, text="learn more", text_color="#2596be", cursor="hand2")
            self.additional_info_label.bind("<Button-1>", lambda e: self.show_additional_info(message_data["additional_information"]))

    def configure_widgets(self, message_data):
        if not message_data["was_read"]:
            self.side_rectangle.pack(side='left', fill=ctk.Y)
            self.configure(fg_color='#444037')
        else:
            self.configure()

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

        self.message_frames = []
        self.current_y = 0

        start_message_data = {
            'content': 'this is the inbox! whenever something important happens you will be notified here.',
            'was_read': True,
            'additional_information': None
        }

        self.add_message(start_message_data)

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

    def add_message(self, message_data):
        message = InboxMessage(self.canvas, message_data)
        message_id = self.canvas.create_window(0, 0, anchor="nw", window=message, width=4000)
        self.message_frames.insert(0, (message_id, message))

        # Update positions of all messages
        self.current_y = 0
        for message_id, frame in self.message_frames:
            self.canvas.moveto(message_id, 0, self.current_y)
            self.current_y += frame.get_height()

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))



import random

def generate_message_data():
  """Generates a dictionary with message data

  Returns:
      A dictionary with the following keys:
          sender (str): The sender of the message.
          content (str): The content of the message.
          was_read (bool): A flag indicating if the message was read.
          additional_information (str): Additional information about the message.
  """

  names = ["Alice Smith", "Bob Johnson", "Charlie Brown", "David Miller", "Emily Garcia"]
  contents = ["Hello, how are you?", "This is a test message.", "I am having lunch.", "Can you meet me later?", "Let's go to the movies!"]
  additional_info = ["Meeting reminder", "Important update", "Just FYI", "", ""]

  return {
      "content": random.choice(contents),
      "was_read": random.choice([True, False]),
      "additional_information": random.choice(additional_info)
  }


def idk(inbox):
    for i in range(15):
        time.sleep(1)
        inbox.add_message(generate_message_data())

if __name__ == "__main__":
    # Example usage
    message_data = generate_message_data()
    print(message_data)

    root = ctk.CTk()
    root.title("Inbox")

    inbox = Inbox(root)
    inbox.pack(side="top", fill="both", expand=True, padx=10, pady=10)


    threading.Thread(target= lambda : idk(inbox) ).start()
    root.mainloop()

