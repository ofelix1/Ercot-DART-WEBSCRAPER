import tkinter as tk
from tkinter import ttk
import pandas as pd

# Function to calculate and display the basis (difference between DAM and RT)
def calculate_basis(rt_data, dam_data):
    # Ensure the columns match between the two datasets
    common_columns = ['Settlement Point'] + [col for col in rt_data.columns if col in dam_data.columns and col != 'Settlement Point']

    # Merge the two datasets on the 'Settlement Point' column
    merged_data = pd.merge(rt_data, dam_data, on='Settlement Point', suffixes=('_RT', '_DAM'))

    # Calculate the basis for each column in common_columns, except 'Settlement Point'
    for col in common_columns:
        if col != 'Settlement Point':
            merged_data[f'Basis_{col}'] = merged_data[f'{col}_RT'] - merged_data[f'{col}_DAM']

    # Return only the Settlement Point and the calculated basis columns
    basis_columns = ['Settlement Point'] + [f'Basis_{col}' for col in common_columns if col != 'Settlement Point']
    return merged_data[basis_columns]

# Function to create the Basis Data tab and its elements
def create_basis_tab(frame, rt_data, dam_data):
    # Calculate the basis
    basis_data = calculate_basis(rt_data, dam_data)

    # Create Treeview to display the basis data
    columns = basis_data.columns.tolist()

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 12))
    style.configure("Treeview", font=("Helvetica", 12))

    tree = ttk.Treeview(frame, columns=columns, show='headings', height=24)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor=tk.CENTER)

    tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

    # Insert basis data into the treeview
    for index, row in basis_data.iterrows():
        values = row.tolist()
        tree.insert('', tk.END, values=values)

    # Make the frame and treeview expandable
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
