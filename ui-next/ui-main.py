import tkinter as tk
from tkinter import ttk

def change_tab(event):
    selected_tab = notebook.index(notebook.select())
    print(f"Selected Tab: {selected_tab}")

# Create main window
root = tk.Tk()
root.title("Integrated UI with Tabs")

# Create a notebook (tabs container)
notebook = ttk.Notebook(root)

# Create tabs
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)

# Add tabs to the notebook
notebook.add(tab1, text="Step 1")
notebook.add(tab2, text="Step 2")
notebook.add(tab3, text="Step 3")
notebook.add(tab4, text="Step 4")

# Add content to tabs
label1 = tk.Label(tab1, text="This is Step 1 content.")
label1.pack(padx=10, pady=10)

label2 = tk.Label(tab2, text="This is Step 2 content.")
label2.pack(padx=10, pady=10)

label3 = tk.Label(tab3, text="This is Step 3 content.")
label3.pack(padx=10, pady=10)

# Pack the notebook (tabs container) into the main window
notebook.pack(expand=1, fill="both")

# Bind the event to the tab change
notebook.bind("<<NotebookTabChanged>>", change_tab)

# Start the application
root.mainloop()