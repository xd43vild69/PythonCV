import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import customtkinter

# Function to apply dark theme
def apply_dark_theme():
    style = ttk.Style()

    # Configure the style for various elements
    style.theme_use('clam')  # Use 'clam' theme as a base
    style.configure('.', background='#1B1B1B', foreground='#353535', fieldbackground='#2E2E2E')
    style.map('.', background=[('disabled', '#2E2E2E'), ('selected', '#3E3E3E')])

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.title('Theme Demo')
root.geometry('400x300')
root.style = ttk.Style(root)

apply_dark_theme()

def change_tab(event):
    selected_tab = notebook.index(notebook.select())
    print(f"Selected Tab: {selected_tab}")


def cleanFiles():
    print("Ok1")
    return

# Create a notebook (tabs container)
notebook = ttk.Notebook(root)

# Create tabs
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
#tab4 = ttk.Frame(notebook)

# Add tabs to the notebook
notebook.add(tab1, text="Organization")
notebook.add(tab2, text="Captioning")
notebook.add(tab3, text="Lora setup")
#notebook.add(tab4, text="Lora setup")

# Add content to tabs
#label1 = tk.Label(tab1, text="Normalize")
#label1.pack(padx=10, pady=10)
5
buttonNormalize = tk.Button(tab1, text="Normalize", command=cleanFiles)
buttonNormalize.place(x=20, y=40)

buttonAugmentation = tk.Button(tab1, text="Augmentation", command=cleanFiles)
buttonAugmentation.place(x=20, y=80)

"""
label2 = tk.Label(tab1, text="Aumentation")
label2.pack(padx=10, pady=20)
"""

label3 = tk.Label(tab2, text="Pick the path to aumentation")
label3.pack(padx=10, pady=10)

"""

label3 = tk.Label(tab3, text="This is Step 3 content.")
label3.pack(padx=10, pady=10)
"""

# Pack the notebook (tabs container) into the main window
notebook.pack(expand=1, fill="both")

# Bind the event to the tab change
notebook.bind("<<NotebookTabChanged>>", change_tab)

# Start the application
root.mainloop()