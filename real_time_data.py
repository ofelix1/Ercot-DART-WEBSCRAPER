import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pytz

# Define the URL for real-time data
real_time_url = "https://www.ercot.com/content/cdr/html/hb_lz.html"

# Define the CST timezone
cst = pytz.timezone('US/Central')

# Function to scrape Real-Time ERCOT data
def scrape_real_time_data(url):
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
        print(f"Error scraping Real-Time data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

# Function to refresh Real-Time data and update the GUI
def refresh_real_time_data(tree, time_label, url):
    df = scrape_real_time_data(url)

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

# Function to create the Real-Time Data tab and its elements
def create_real_time_tab(frame):
    columns = ['Settlement Point', 'LMP', '5 Min Change to LMP']

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 12))
    style.configure("Treeview", font=("Helvetica", 12))

    tree = ttk.Treeview(frame, columns=columns, show='headings', height=24)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor=tk.CENTER)

    tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

    # Add a refresh button and time label
    time_label = tk.StringVar()
    tk.Label(frame, textvariable=time_label, font=("Helvetica", 12)).grid(row=1, column=0, sticky=tk.W)
    now_cst = datetime.now(cst)
    time_label.set("Last Updated: " + now_cst.strftime("%H:%M:%S %Z"))

    refresh_button = tk.Button(frame, text="Refresh Now", font=("Helvetica", 12), command=lambda: refresh_real_time_data(tree, time_label, real_time_url))
    refresh_button.grid(row=2, column=0, pady=10)

    # Make the frame and treeview expandable
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Initial load of data
    refresh_real_time_data(tree, time_label, real_time_url)
