from real_time_data import create_real_time_tab
from dam_data import create_dam_tab
from real_time_settlement_data import create_real_time_spp_tab
from hourly_settlement_data import create_hourly_settlement_tab
import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()
    root.title("ERCOT Data")

    # Set the window size
    root.geometry("1200x800")

    # Create a Notebook (tabbed interface)
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')

    # Create frames for each tab
    real_time_frame = ttk.Frame(notebook, padding="10")
    dam_frame = ttk.Frame(notebook, padding="10")
    real_time_spp_frame = ttk.Frame(notebook, padding="10")
    hourly_settlement_frame = ttk.Frame(notebook, padding="10")
    real_time_frame.pack(fill='both', expand=True)
    dam_frame.pack(fill='both', expand=True)
    real_time_spp_frame.pack(fill='both', expand=True)
    hourly_settlement_frame.pack(fill='both', expand=True)

    # Add frames to the notebook
    notebook.add(real_time_frame, text="Real-Time Data")
    notebook.add(dam_frame, text="Day-Ahead Market (DAM)")
    notebook.add(real_time_spp_frame, text="Real-Time Settlement Points")
    notebook.add(hourly_settlement_frame, text="Hourly Settlement Data")

    # Real-Time Data Tab
    create_real_time_tab(real_time_frame)

    # Day-Ahead Market (DAM) Tab
    create_dam_tab(dam_frame)

    # Hourly Settlement Data Tab (to be used as a callback)
    update_hourly_data = create_hourly_settlement_tab(hourly_settlement_frame)

    # Real-Time Settlement Points Tab (with callback for hourly data update)
    create_real_time_spp_tab(real_time_spp_frame, on_date_change_callback=update_hourly_data)

    root.mainloop()

# Run the main function
if __name__ == "__main__":
    main()
