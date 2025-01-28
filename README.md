
# **ERCOT Scraper - First Commit**

   **This is a tool I’ve built to scrape and display data from ERCOT. It’s a GUI-based application that handles real-time (RT) prices, day-ahead market (DAM) prices, and settlement data.**




 **1. Real-Time (RT) Data**

    -Displays live RT prices in real-time.

    -Prices turn red when they spike, making it easy to spot high pricing events.

**2. Day-Ahead Market (DAM) Data**

    -Shows pricing data for the day-ahead market.

    -Includes detailed 15-minute settlement data for RT prices.

**3. Hourly Settlement Data**

    -Aggregates 15-minute RT settlement data into hourly intervals.

    -Provides an easy way to view hourly data.

    -Lets you export this data to a CSV file with just one click.

**4. Export to CSV**

    -Both DAM and hourly settlement data can be exported to CSV files.

    -Filenames are generated automatically using the flow date (e.g., Hourly_Settlement_Data_YYYY-MM-DD.csv).

# **What’s Next**

**Basis Tab**

    -A new tab to calculate and display the difference (basis) between RT and DAM prices.
    
**Load Tab**
    -Include load data to make the analysis more robust.
