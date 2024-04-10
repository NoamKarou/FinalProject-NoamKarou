import tkinter as tk
import customtkinter as ctk
from PIL import Image
import os
class Logo:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(self.parent, fg_color='transparent')

        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the full path to the image file
        image_path = os.path.join(current_dir, 'image_assets', 'logo', 'logo.png')

        logo_image = ctk.CTkImage(light_image=Image.open(image_path),
                                  dark_image=Image.open(image_path), size=(128,128))
        self.image = ctk.CTkLabel(self.frame, text='', image=logo_image, fg_color='transparent', bg_color='transparent')
        self.image.pack(fill=ctk.BOTH)




if __name__ == "__main__":
    root = ctk.CTk()
    id_label = Logo(root)

    root.mainloop()
