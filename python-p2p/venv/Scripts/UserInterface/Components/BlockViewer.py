import tkinter as tk
import customtkinter as ctk
from typing import List


class Transaction:
    def __init__(self, transaction_id, details):
        self.transaction_id = transaction_id
        self.details = details


class Block:
    def __init__(self, block_id, last_block_hash, miner, transactions, salt):
        self.block_id = block_id
        self.last_block_hash = last_block_hash
        self.miner = miner
        self.transactions = transactions
        self.salt = salt


class BlockFrame(ctk.CTkFrame):
    def __init__(self, master, block, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.block = block
        self.expanded = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.block_id_label = ctk.CTkLabel(self, text=f"ID: {block.block_id}")
        self.block_id_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.miner_label = ctk.CTkLabel(self, text=f"Miner: {block.miner}")
        self.miner_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.salt_label = ctk.CTkLabel(self, text=f"Salt: {block.salt[:10]}...")
        self.salt_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.toggle_button = ctk.CTkButton(self, text="Show More", command=self.toggle)
        self.toggle_button.grid(row=0, column=3, padx=5, pady=5, sticky="e")

        self.details_frame = None

    def toggle(self):
        if self.expanded:
            self.hide_details()
        else:
            self.show_details()

    def show_details(self):
        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.grid(row=1, column=0, columnspan=4, sticky="we")

        self.full_salt_label = ctk.CTkLabel(self.details_frame, text=f"Full Salt: {self.block.salt}")
        self.full_salt_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.hash_label = ctk.CTkLabel(self.details_frame, text=f"Hash: {self.block.last_block_hash}")
        self.hash_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.transactions_label = ctk.CTkLabel(self.details_frame, text="Transactions:")
        self.transactions_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        for i, transaction in enumerate(self.block.transactions):
            transaction_label = ctk.CTkLabel(self.details_frame,
                                             text=f"{transaction.signature_text()}")
            transaction_label.grid(row=3 + i, column=0, padx=5, pady=5, sticky="w")

        self.toggle_button.configure(text="Show Less")
        self.expanded = True

    def hide_details(self):
        if self.details_frame:
            self.details_frame.destroy()
        self.toggle_button.configure(text="Show More")
        self.expanded = False


class BlockApp:
    def __init__(self, master, get_blocks_callback):
        self.master = master
        self.get_blocks_callback = get_blocks_callback

        self.main_frame = ctk.CTkFrame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self.main_frame, bg='gray15', highlightthickness=0)
        self.scrollbar = ctk.CTkScrollbar(self.main_frame, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color='gray15', border_color='gray15')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.displayed_block_ids = set()
        self.update_blocks()
        self.poll_blocks()

    def update_blocks(self):
        blocks = self.get_blocks_callback()
        for block in blocks:
            if block.block_id not in self.displayed_block_ids:
                block_frame = BlockFrame(self.scrollable_frame, block)
                block_frame.pack(fill=tk.X, padx=10, pady=5)
                self.displayed_block_ids.add(block.block_id)

    def poll_blocks(self):
        self.update_blocks()
        self.master.after(1000, self.poll_blocks)


def get_blocks_callback() -> List[Block]:
    # Replace this with your actual function to fetch blocks
    return [
        Block(1, 12345, "miner1", [Transaction(1, "details1"), Transaction(2, "details2")], "abcdefghijklmnopqrst"),
        Block(2, 67890, "miner2", [Transaction(3, "details3")], "uvwxyzabcdefghijklmn"),
        # Add more blocks here as needed for testing
    ]


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Block Viewer")
    root.geometry("800x600")

    app = BlockApp(root, get_blocks_callback)
    root.mainloop()
