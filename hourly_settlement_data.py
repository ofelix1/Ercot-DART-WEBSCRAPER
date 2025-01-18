import tkinter as tk
from tkinter import ttk
import pandas as pd
from datetime import datetime, timedelta
import pytz

# Define the CST timezone
cst = pytz.timezone('US/Central')

# Function to calculate hourly settlement averages from 15-minute intervals
def calculate_hourly_averages(spp_data):
    spp_data['Interval Ending'] = spp_data['Interval Ending'].astype(int) // 100  # Convert to hour
    hourly_data = spp_data.groupby(['Oper Day', 'Interval Ending']).mean().reset_index()

    # Round the results to 2 decimal places
    hourly_data = hourly_data.round(2)

    return hourly_data

# Function to refresh and display hourly settlement data
def refresh_hourly_settlement_data(tree, time_label, spp_data):
    hourly_data = calculate_hourly_averages(spp_data)

    # Clear the tree
    for row in tree.get_children():
        tree.delete(row)

    # Insert new data
    for index, row in hourly_data.iterrows():
        values = row.tolist()
        tree.insert('', tk.END, values=values)

    # Update the time label to CST
    now_cst = datetime.now(cst)
    time_label.set("Last Updated: " + now_cst.strftime("%H:%M:%S %Z"))

# Function to create the Hourly Settlement Data tab and its elements
def create_hourly_settlement_tab(frame):
    # Define columns for the Treeview
    columns = ['Oper Day', 'Interval Ending', 'HB_BUSAVG', 'HB_HOUSTON', 'HB_HUBAVG', 'HB_NORTH', 'HB_PAN',
               'HB_SOUTH', 'HB_WEST', 'LZ_AEN', 'LZ_CPS', 'LZ_HOUSTON', 'LZ_LCRA', 'LZ_NORTH', 'LZ_RAYBN', 'LZ_SOUTH', 'LZ_WEST']

    tree = ttk.Treeview(frame, columns=columns, show='headings', height=24)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor=tk.CENTER)  # Adjust the width as necessary

    tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Add a vertical scrollbar
    scrollbar_y = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar_y.set)
    scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))

    # Add a horizontal scrollbar
    scrollbar_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
    tree.configure(xscroll=scrollbar_x.set)
    scrollbar_x.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E))

    # Add a time label
    time_label = tk.StringVar()
    tk.Label(frame, textvariable=time_label, font=("Helvetica", 12)).grid(row=2, column=0, sticky=tk.W)

    # Function to handle the refresh of hourly data when the date changes in the real-time tab
    def update_hourly_data(spp_data):
        refresh_hourly_settlement_data(tree, time_label, spp_data)

    # Return the update function to be used as a callback
    return update_hourly_data
