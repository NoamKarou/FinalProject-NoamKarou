import tkinter as tk


class MyApp:
    def __init__(self, function):
        self.function = function

        # Create the main application window
        self.root = tk.Tk()
        self.root.title("Tkinter App")

        # Create a button widget
        self.button = tk.Button(self.root, text="Click me!", command=self.execute_function)
        self.button.pack(pady=20)

    def execute_function(self):
        self.function()

    def run(self):
        # Run the Tkinter event loop
        self.root.mainloop()








def my_function():
    print("Button clicked!")


# Create an instance of the MyApp class, passing the function to execute
app = MyApp(my_function)
app.run()
