import tkinter as tk
import customtkinter

class SimpleUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple UI")

        self.label = tk.Label(root, text="Hello, UI!")
        self.label.pack()

        self.button = tk.Button(root, text="Click Me", command=self.change_label_text)
        self.button.pack()

        buttonClean = customtkinter.CTkButton(root, text="Clean", command=self.change_label_text)
        buttonClean.place(x=80, y=430)

    def change_label_text(self):
        self.label.config(text="Button clicked!")


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.geometry("600x500")

# Create the main window
#root = tk.Tk()

# Create an instance of the SimpleUI class
ui = SimpleUI(root)

# Start the main event loop
root.mainloop()