import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import pytz

# Define the base URL for Real-Time Settlement Points data
real_time_spp_url_base = "https://www.ercot.com/content/cdr/html/{date}_real_time_spp.html"

# Define the CST timezone
cst = pytz.timezone('US/Central')

# Function to get the next day and the last four days
def get_next_and_last_four_days():
    today = datetime.now(cst)
    days = [(today + timedelta(days=1)).strftime('%Y-%m-%d')]  # Next day
    days += [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(4)]  # Previous 4 days
    return days

# Function to scrape Real-Time Settlement Points ERCOT data
def scrape_real_time_spp_data(url):
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

        # Ensure the Interval Ending column is correctly formatted
        if 'Interval Ending' in df.columns:
            df['Interval Ending'] = df['Interval Ending'].apply(lambda x: f"{int(x):04d}")

        return df
    except Exception as e:
        print(f"Error scraping Real-Time Settlement Points data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

# Function to refresh Real-Time Settlement Points data and update the GUI
def refresh_real_time_spp_data(tree, time_label, url, on_date_change_callback=None):
    df = scrape_real_time_spp_data(url)

    if df.empty:
        print("No data available.")
        return df  # Return the DataFrame, even if empty

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

    # If there is a callback for date change, execute it
    if on_date_change_callback:
        on_date_change_callback(df)

    return df  # Return the DataFrame with the updated data

# Function to create the Real-Time Settlement Points tab and its elements
def create_real_time_spp_tab(frame, on_date_change_callback=None):
    # Create a label for the drop-down menu
    tk.Label(frame, text="Operating Day:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

    # Create a Combobox for the Operating Day
    operating_days = get_next_and_last_four_days()
    operating_day_combobox = ttk.Combobox(frame, values=operating_days, font=("Helvetica", 12))
    operating_day_combobox.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

    # Set the default value to today's date
    today = datetime.now(cst).strftime('%Y-%m-%d')
    if today in operating_days:
        operating_day_combobox.set(today)
    else:
        operating_day_combobox.current(0)

    # Treeview for displaying Real-Time Settlement Points data
    columns = [
        'Oper Day', 'Interval Ending', 'HB_BUSAVG', 'HB_HOUSTON', 'HB_HUBAVG', 'HB_NORTH', 'HB_PAN',
        'HB_SOUTH', 'HB_WEST', 'LZ_AEN', 'LZ_CPS', 'LZ_HOUSTON', 'LZ_LCRA', 'LZ_NORTH', 'LZ_RAYBN', 'LZ_SOUTH', 'LZ_WEST'
    ]
    tree = ttk.Treeview(frame, columns=columns, show='headings', height=24)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor=tk.CENTER)  # Adjust the width as necessary

    tree.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Add a vertical scrollbar
    scrollbar_y = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar_y.set)
    scrollbar_y.grid(row=1, column=3, sticky=(tk.N, tk.S))

    # Add a horizontal scrollbar
    scrollbar_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
    tree.configure(xscroll=scrollbar_x.set)
    scrollbar_x.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E))

    # Add a refresh button and time label
    time_label = tk.StringVar()
    tk.Label(frame, textvariable=time_label, font=("Helvetica", 12)).grid(row=3, column=0, sticky=tk.W)
    now_cst = datetime.now(cst)
    time_label.set("Last Updated: " + now_cst.strftime("%H:%M:%S %Z"))

    # Function to handle the refresh button click
    def refresh_real_time_spp_data_button():
        selected_day = operating_day_combobox.get()
        formatted_date = selected_day.replace("-", "")
        real_time_spp_url = real_time_spp_url_base.format(date=formatted_date)
        print(f"Fetching Real-Time Settlement Points data from URL: {real_time_spp_url}")
        return refresh_real_time_spp_data(tree, time_label, real_time_spp_url, on_date_change_callback)

    refresh_button = tk.Button(frame, text="Refresh Now", font=("Helvetica", 12), command=refresh_real_time_spp_data_button)
    refresh_button.grid(row=4, column=0, pady=10)

    # Make the frame and treeview expandable
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    tree.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Initial load of data
    real_time_spp_data = refresh_real_time_spp_data_button()  # Use the selected operating day to load data

    return real_time_spp_data  # Return the DataFrame with the Real-Time Settlement Points data
