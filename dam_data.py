import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import pytz

# Define the base URL for DAM data
dam_url_base = "https://www.ercot.com/content/cdr/html/{date}_dam_spp.html"

# Define the CST timezone
cst = pytz.timezone('US/Central')

# Function to scrape DAM ERCOT data
def scrape_dam_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table in the HTML
        table = soup.find('table')
        if table is None:
            print("Error: Could not find table in the HTML")
            return pd.DataFrame()  # Return an empty DataFrame if no table is found

        # Parse the table into a DataFrame
        df = pd.read_html(str(table))[0]
        return df
    except Exception as e:
        print(f"Error scraping DAM data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

# Function to refresh DAM data and update the GUI
def refresh_dam_data(tree, time_label, url):
    df = scrape_dam_data(url)

    if df.empty:
        print("No data available.")
        return

    # Clear the tree
    for row in tree.get_children():
        tree.delete(row)

    # Insert new data
    for index, row in df.iterrows():
        values = row.tolist()
        tree.insert('', tk.END, values=values)

    # Update the time label to CST
    now_cst = datetime.now(cst)
    time_label.set("Last Updated: " + now_cst.strftime("%H:%M:%S %Z"))

# Function to create the DAM Data tab and its elements
def create_dam_tab(frame):
    # Create a label for the drop-down menu
    tk.Label(frame, text="Operating Day:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

    # Create a Combobox for the Operating Day
    operating_days = get_next_and_last_four_days()  # Adjusted function to get the next day and last four days
    operating_day_combobox = ttk.Combobox(frame, values=operating_days, font=("Helvetica", 12))
    operating_day_combobox.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

    # Set the default value to today's date
    today = datetime.now(cst).strftime('%Y-%m-%d')
    if today in operating_days:
        operating_day_combobox.set(today)
    else:
        operating_day_combobox.current(0)

    # Treeview for displaying DAM data
    columns = [
        'Oper Day', 'Hour Ending', 'HB_BUSAVG', 'HB_HOUSTON', 'HB_HUBAVG', 'HB_NORTH', 'HB_PAN',
        'HB_SOUTH', 'HB_WEST', 'LZ_AEN', 'LZ_CPS', 'LZ_HOUSTON', 'LZ_LCRA', 'LZ_NORTH', 'LZ_RAYBN', 'LZ_SOUTH', 'LZ_WEST'
    ]
    tree = ttk.Treeview(frame, columns=columns, show='headings', height=24)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor=tk.CENTER)

    tree.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=1, column=3, sticky=(tk.N, tk.S))

    # Add a refresh button and time label
    time_label = tk.StringVar()
    tk.Label(frame, textvariable=time_label, font=("Helvetica", 12)).grid(row=2, column=0, sticky=tk.W)
    now_cst = datetime.now(cst)
    time_label.set("Last Updated: " + now_cst.strftime("%H:%M:%S %Z"))

    # Function to handle the refresh button click
    def refresh_dam_data_button():
        selected_day = operating_day_combobox.get()
        formatted_date = selected_day.replace("-", "")
        dam_url = dam_url_base.format(date=formatted_date)
        print(f"Fetching DAM data from URL: {dam_url}")
        refresh_dam_data(tree, time_label, dam_url)

    refresh_button = tk.Button(frame, text="Refresh Now", font=("Helvetica", 12), command=refresh_dam_data_button)
    refresh_button.grid(row=3, column=0, pady=10)

    # Make the frame and treeview expandable
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    tree.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Initial load of data
    refresh_dam_data_button()  # Use the selected operating day to load data

# Function to get the next day and the last four days
def get_next_and_last_four_days():
    today = datetime.now(cst)
    days = [(today + timedelta(days=1)).strftime('%Y-%m-%d')]  # Next day
    days += [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(4)]  # Previous 4 days
    return days
